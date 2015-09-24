from os import listdir
from os.path import isfile, join
import sys


input_directory = sys.argv[1]

#We are only interested in files from the input directory that contain .cmp.txt
onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".anno.txt" in f) ]


outlines = []
totalwc = 0
totalsentcount = 0
totalhRelcount = 0
totalhPropcount = 0

for files in onlyfiles:
    with open(join(input_directory, files), 'rU') as file:
        file_wordcount = 0
        file_sentcount = 0
        file_hRelcount = 0
        file_hPropcount = 0
        
        for line in file:
            if line.strip() not in ('\n', '\r\n'):
                split_line = line.split(" ")
                file_wordcount = file_wordcount + len(split_line)
                file_sentcount = file_sentcount + 1
                file_hRelcount = file_hRelcount + line.count("<hRel>")
                file_hPropcount = file_hPropcount + line.count("<hProp>")
    
        file_hedgecount = file_hRelcount + file_hPropcount
    
        totalwc = totalwc + file_wordcount
        totalsentcount = totalsentcount + file_sentcount
        totalhRelcount = totalhRelcount + file_hRelcount
        totalhPropcount = totalhPropcount + file_hPropcount

        outlines.append(",".join([files, str(file_wordcount), str(file_sentcount), str(float(file_wordcount)/float(file_sentcount)), str(file_hRelcount), str(file_hPropcount), str(file_hRelcount+file_hPropcount), str(float(file_hedgecount)/float(file_wordcount)), str(float(file_hedgecount)/float(file_sentcount))]))

with open("data_analysis.csv", 'w') as outfile:
    outfile.write("Document,WordCount,SentenceCount,Words/Sentence,hRelCount,hPropCount,TotalHedges,Hedges/Total Words,Hedges/Sentence")
    outfile.write("\n")
    for output_lines in outlines:
        outfile.write(output_lines)
        outfile.write("\n")
    outfile.write("\n")

    total_hedgecount = totalhRelcount + totalhPropcount
    outfile.write(",".join([str(len(onlyfiles)), str(totalwc), str(totalsentcount), str(float(totalwc)/float(totalsentcount)), str(totalhRelcount), str(totalhPropcount), str(total_hedgecount), str(float(total_hedgecount)/float(totalwc)), str(float(total_hedgecount)/float(totalsentcount))]))
            