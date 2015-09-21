from os import listdir
from os.path import isfile, join
import csv
import sys

listoflines = []
uncert = []
dict = {}

hRelDef = "create uncertainty in the commitment of the speaker to what they are saying (eg. 'I [think] (some fact)' as opposed to 'I [know] (some fact)')"
hPropDef = "introduce uncertainty or ambiguity into the content of the utterance itself (i.e. the speaker/author is fully committed to what they are saying but there is something imprecise in the content itself)"
hRelAttrDef = "imply that the speaker attributes information to some other source in order to downplay it OR to garner power for their statement instead of just committing to the statement themselves"

input_directory = sys.argv[1]
numSentPerHIT = int(sys.argv[2])

#Dictionary is in the format: hedge, type of hedge, definition of that type of hedge, the hedging definition of that word, the hedging example of that word, the non-hedging definition of that word, the non-hedging example of that word
with open('dict_test.csv', 'rU') as d:
    reader = csv.reader(d)
    next(reader, None)
    for line in reader:
        dict[line[0]] = [line[1], line[2], line[3], line[4], line[5], line[6]]

onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".toAnno.txt" in f and ".DS_Store" not in f) ]

for files in onlyfiles:
    with open(join(input_directory,files), 'rU') as inputFile:
        for line in inputFile:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            if len(line) > 0:
                
                #For the uncertainty determination and confidence level datasheet, we just need the sentence to be annotated and the 3 different definitions of hedging
                uncert.append("\""+line + "\"")
                words = line.split(" ")
                for word in words:
                    if word in dict:
                        comma = ","
                        
                        #For the task identifying hedge senses based on word definitions and examples, we need the sentence, the potential hedge word and all the available information from the dictionary
                        def_str = "\"" + line + "\"," + word + "," + comma.join(dict[word])
                        listoflines.append(def_str)

#To be used for task asking about uncertainty present in the sentence and for confidence level determination
#Header is: hRelDef, hPropDef, hRelAttrDef, sentence0, sentence1, ...., sentence(#numSentPerHIT)
with open('amt_input_uncert.csv', 'w') as out:
    a = 0
    header = "hRelDef,hPropDef,hRelAttrDef,"
    for x in range(0,numSentPerHIT):
        header = header + "sentence"+str(x)+","
    out.write(header)
    out.write("\n")
    for item_u in uncert:
        if a == 0:
            temp = hRelDef + "," + hPropDef + "," + hRelAttrDef +"," + item_u
            a = a+1
        elif a < numSentPerHIT and a > 0:
            temp = temp + "," + item_u
            a = a+1
        else:
            out.write(temp)
            out.write("\n")
            a = 0
    out.write(temp)

#To be used to task asking turkers to identify hedge senses of words based on definitions alone, examples alone, or a combination of the two
with open('amt_input_defs_examples.csv', 'w') as out_defs:
    header_defs="sentence0,hedge0,hedgeType0,defHedgeType0,hedgingDef0,hedgingEx0,nonHedgeDef0,nonHedgeEx0"
    for i in range(1,numSentPerHIT):
        header_defs = header_defs + "," + "sentence"+ str(i)+",hedge"+str(i)+",hedgeType"+str(i)+",defHedgeType"+str(i)+",hedgingDef"+str(i)+",hedgingEx"+str(i)+",nonHedgeDef"+str(i)+",nonHedgeEx"+str(i)
    out_defs.write(header_defs)
    out_defs.write("\n")
    b = 0
    for item in listoflines:
        if b == 0:
            temp_defs = item
            b = b + 1
        elif b < numSentPerHIT and b > 0:
            temp_defs = temp_defs + "," + item
            b = b + 1
        else:
            out_defs.write(temp_defs)
            out_defs.write("\n")
            b = 0
    out_defs.write(temp_defs)
