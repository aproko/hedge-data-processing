from os import listdir
from os.path import isfile, join
import sys
import nltk.data
import re

#The input directory is provided as an argument through the run.sh script.
input_directory = sys.argv[1]

#We are only interested in files from the input directory that contain .cmp.txt
onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".cmp.txt" in f) ]



for files in onlyfiles:
    cleanLines = []
    with open(join(input_directory,files), 'rU') as fileToClean:
        for line in fileToClean:
            #We take out all the html markup tags
            cleanLine = re.sub(r'<.*?>', '', line)
            
            #We put quotes around all sentences to avoid problems with commas
            cleanLine = cleanLine.replace("\"", "'")
            
            #We skip all empty lines, newline and carriage return characters
            if not cleanLine.strip() or line not in ('\n', '\r\n'):
                
                #We use nltk to parse the remaining lines into sentences
                sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
                listOfSentences = sent_detector.tokenize(cleanLine.strip())
                for sentences in listOfSentences:
                    cleanLines.append(sentences)

    #To avoid duplication due to 'quotes' of previous posts, we remove duplicate sentences
    cleanedUpLines = set(cleanLines)

    #The resulting sentences are written to a file with the same numeric identifier but ending with .toAnno.txt
    outfilename = join(input_directory, files.replace(".cmp.txt", ""))+ ".toAnno.txt"
    with open(outfilename, 'w') as cleanFile:
        for item in cleanedUpLines:
            cleanFile.write(item)
            cleanFile.write("\n")