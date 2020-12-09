import pandas as pd
import math
import numpy as np

###Available columns
#'TaxonOID', 'Domain', 'Sequencing Status', 'Study Name',
#       'Genome Name / Sample Name', 'Sequencing Center', 'IMG Genome ID',
#       'GOLD Analysis Project ID', 'GOLD Analysis Project Type',
#       'GOLD Sequencing Project ID', 'GOLD Study ID', 'Geographic Location',
#       'GOLD Ecosystem', 'GOLD Ecosystem Category', 'GOLD Ecosystem Subtype',
#       'GOLD Ecosystem Type', 'GOLD Sequencing Depth',
#       'GOLD Sequencing Quality', 'GOLD Sequencing Status',
#       'GOLD Sequencing Strategy', 'GOLD Specific Ecosystem', 'Habitat',
#       'Latitude', 'Longitude', 'Genome Size   * assembled',
#       'Gene Count   * assembled'


subject_field = "GOLD Analysis Project ID"
subject_field_prefix = "Analysis_project_ID"

object_fields = [
"TaxonOID",
#"IMG Genome ID",
"GOLD Sequencing Project ID",
#"GOLD Analysis Project ID",
"GOLD Analysis Project Type",
"GOLD Study ID",
"Geographic Location",
"GOLD Ecosystem",
"GOLD Ecosystem Category",
"GOLD Ecosystem Subtype",
"GOLD Ecosystem Type",
"GOLD Sequencing Depth",
"GOLD Sequencing Strategy",
"GOLD Specific Ecosystem",
"Latitude",
"Longitude",
"Habitat",
"Genome Size   * assembled",
"Gene Count   * assembled"
]

object_field_prefixes = [
"NCBItaxon",
#"IMG_genome_ID",
"Sequencing_project_ID",
#"Analysis Project ID",
"Analysis_project_type",
"Study_ID",
"Geographic_location",
"GOLD",
"GOLD",
"GOLD",
"GOLD",
"Depth",
"Sequencing_strategy",
"GOLD",
"Latitude",
"Longitude",
"Habitat",
"Assembly_size",
"Gene_count"
]

#TaxonOID
#IMG Genome ID
#GOLD Analysis Project ID
#GOLD Analysis Project Type
#GOLD Sequencing Project ID
#GOLD Study ID
#Geographic Location
#GOLD Ecosystem
#GOLD Ecosystem Category
#GOLD Ecosystem Subtype
#GOLD Ecosystem Type
#GOLD Sequencing Depth
#GOLD Sequencing Strategy
#GOLD Specific Ecosystem Habitat
#Genome Size   * assembled
#Gene Count   * assembled


kgx_header = "Subject\tEdge_label\tObject\tSource\n"



def load(source_path):
    df = pd.read_csv(source_path, sep='\t')

    columns = df.columns.str
    print(type(columns))
    print(columns)

    dims = df.shape

    print("dims "+str(dims))
    subject_index = df.columns.get_loc(subject_field)#columns.str.find(primary_field)
    print("subject_index "+str(subject_index))

    return (subject_index, df)


def parse(subject_index, df):
    output = []
    dims = df.shape
    for i in range(0, dims[0]) :
        for j in range(0, len(object_fields)):
            #secondary_index = columns.str.find(object_fields[j])
            secondary_index = df.columns.get_loc(object_fields[j])
            print("secondary_index " + str(secondary_index))
            addval = df.iloc[i, secondary_index]
            print("addval "+str(addval))

            if "Genome Size   * assembled" == object_fields[j] or "Gene Count   * assembled" == object_fields[j]:
                addval_orig = addval

                if (addval == 0):
                    addval = np.NAN
                else:
                    addval = math.log10(addval)
                    addval = round(addval, 0)

                print("addval "+str(addval_orig)+"\t"+str(addval))
            elif "GOLD Ecosystem Subtype" == object_fields[j] and addval in ["Unclassified"]:
                addval = np.NAN
            elif "Latitude" == object_fields[j] or "Longitude" == object_fields[j]:
                ###load pairwise distance file and ingest as sample-sample in separate code block
                addval = np.NAN

            ###write the edge
            if not pd.isnull(addval):
                #convert chars to underscore
                addval = str(addval).replace(" ","_")
                addval = str(addval).replace(",", "_")
                #lower case for case variation
                addval = addval.lower()
                newstr = subject_field_prefix+":"+str(df.iloc[i, subject_index]) +"\thas_quality\t"+object_field_prefixes[j]+":"+str(addval)+"\tGOLD"
                if newstr not in output:
                    output.append(newstr)
    return output

def write(output, outfile):
    with open(outfile, "w") as outfile:
        outfile.write(kgx_header)
        outfile.write("\n".join(output))



###
source_path = '/Users/marcin/Documents/KBase/KE/IMGVR/IMGVR_samples_table.tsv'

tuple = load(source_path)
subject_index = tuple[0]
df = tuple[1]

output = parse(subject_index, df)

outfile = "IMGVR_sample_KGX.tsv"
write(output, outfile)