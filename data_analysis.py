from os import listdir
from os.path import isfile, join
import sys
import csv

input_directory = sys.argv[1]
mode = sys.argv[2]

wc = 0
sentcount = 0
hedgecount = 0
outlines = []
total_hedgecount = 0

prevsent = ""

if "amt" in mode:
    onlyfile = [f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".amt.csv" in f)]
    print onlyfile
    for amt_file in onlyfile:
        with open(join(input_directory, amt_file), 'rU') as amt_f:
            reader = csv.reader(amt_f)
            for l in reader:
                sent = l[0]
                judg = l[4]
                if sent != prevsent:
                    sentcount = sentcount + 1
                    sent_wds = sent.split(" ")
                    wc = wc + len(sent_wds)
                    sent = prevsent
                if "n" not in judg:
                        hedgecount = hedgecount + 1

total_hedgecount = hedgecount
onlyfiles = ["amt_file"]
totalwc = wc
totalsentcount = sentcount
totalhRelcount = "NA"
totalhPropcount = "NA"



                
            
if "gold" in mode:
#We are only interested in files from the input directory that contain .cmp.txt
    onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".anno.txt" in f) ]



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
    total_hedgecount = totalhRelcount + totalhPropcount

with open("data_analysis1.csv", 'w') as outfile:
    outfile.write("Document,WordCount,SentenceCount,Words/Sentence,hRelCount,hPropCount,TotalHedges,Hedges/Total Words,Hedges/Sentence")
    outfile.write("\n")
    for output_lines in outlines:
        outfile.write(output_lines)
        outfile.write("\n")
    outfile.write("\n")

    
    outfile.write(",".join([str(len(onlyfiles)), str(totalwc), str(totalsentcount), str(float(totalwc)/float(totalsentcount)), str(totalhRelcount), str(totalhPropcount), str(total_hedgecount), str(float(total_hedgecount)/float(totalwc)), str(float(total_hedgecount)/float(totalsentcount))]))
            