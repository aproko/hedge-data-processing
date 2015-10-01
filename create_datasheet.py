from os import listdir
from os.path import isfile, join
#from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
import csv
import sys
import codecs

listoflines = []
uncert = []
dict = {}
multi_dict = {}
hedge_counts = {}

hRelDef = "create uncertainty in the commitment of the speaker to what they are saying (eg. 'I [think] (some fact)' as opposed to 'I [know] (some fact)')"
hPropDef = "introduce uncertainty or ambiguity into the content of the utterance itself (i.e. the speaker/author is fully committed to what they are saying but there is something imprecise in the content itself)"
hRelAttrDef = "imply that the speaker attributes information to some other source in order to downplay it OR to garner power for their statement instead of just committing to the statement themselves"

input_directory = sys.argv[1]
numSentPerHIT = int(sys.argv[2])

#lemmatizer = WordNetLemmatizer()
stemmer = EnglishStemmer()

#Dictionary is in the format: hedge, type of hedge, definition of that type of hedge, the hedging definition of that word, the hedging example of that word, the non-hedging definition of that word, the non-hedging example of that word
with codecs.open('dictionary.csv', 'rU', encoding='utf-8') as d:
    reader = csv.reader(d)
    next(reader, None)
    for line in reader:
        dict_stem = stemmer.stem(line[0])
        dict[dict_stem] = [line[1], line[2], line[3], line[4], line[5], line[6]]

with codecs.open('multiword_dict.csv', 'rU', encoding='utf-8') as md:
    md_reader = csv.reader(md)
    next(md_reader, None)
    for md_line in md_reader:
        multi_dict[md_line[0]] = [md_line[1], md_line[2], md_line[3], md_line[4], md_line[5], md_line[6]]

onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".toAnno.txt" in f and ".DS_Store" not in f) ]


for files in onlyfiles:
    with codecs.open(join(input_directory,files), 'rU', encoding='utf-8') as inputFile:
        for lines in inputFile:
            lines = lines.replace("\n", "")
            lines = lines.replace("\r", "")
            id_and_line = lines.split(",")
            line = id_and_line[1]
            id = id_and_line[0]
            if len(line.split(" ")) > 3:
                
                #For the uncertainty determination and confidence level datasheet, we just need the sentence to be annotated and the 3 different definitions of hedging
                uncert.append(id + ",\""+line + "\"")
                
                multi_line = line
                
                for multi_words in multi_dict:
                    multi_words_in_line = []
                    index = 0
                    if multi_words in line:
                        multi_line = line.replace(multi_words, str(index))

                        listoflines.append(id + ",\"" + line + "\"," + multi_words + "," + comma.join(multi_dict[multi_words]))
                        
                        multi_words_in_line.append(multi_words)
                        index = index + 1
                        if multi_words in hedge_counts:
                            hedge_counts[multi_words] = hedge_counts[multi_words] + 1
                        else:
                            hedge_counts[multi_words] = 1
            
                words = multi_line.split(" ")
            
                for word in words:
                    word_stem = stemmer.stem(word)
                    if word_stem in dict:
                        comma = ","
                        
                        #For the task identifying hedge senses based on word definitions and examples, we need the sentence, the potential hedge word and all the available information from the dictionary
                        def_str = id + ",\"" + line + "\"," + word + "," + comma.join(dict[word_stem])
                        listoflines.append(def_str)
                        if word_stem in hedge_counts:
                            hedge_counts[word_stem] = hedge_counts[word_stem] + 1
                        else:
                            hedge_counts[word_stem] = 1

#To be used for task asking about uncertainty present in the sentence and for confidence level determination
#Header is: hRelDef, hPropDef, hRelAttrDef, sentence0, sentence1, ...., sentence(#numSentPerHIT)
with codecs.open('amt_input_uncert.csv', 'w', encoding='utf-8') as out:
    a = 0
    header = "hRelDef,hPropDef,hRelAttrDef,"
    for x in range(0,numSentPerHIT):
        header = header + "sentenceID" + str(x) + ",sentence"+str(x)+","
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
with codecs.open('amt_input_defs_examples.csv', 'w', encoding='utf-8') as out_defs:
    header_defs="sentenceID0,sentence0,hedge0,hedgeType0,defHedgeType0,hedgingDef0,hedgingEx0,nonHedgeDef0,nonHedgeEx0"
    for i in range(1,numSentPerHIT):
        header_defs = header_defs + ",sentenceID" +str(i) + ",sentence"+ str(i)+",hedge"+str(i)+",hedgeType"+str(i)+",defHedgeType"+str(i)+",hedgingDef"+str(i)+",hedgingEx"+str(i)+",nonHedgeDef"+str(i)+",nonHedgeEx"+str(i)
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

with codecs.open('amt_hedge_counts.csv', 'w', encoding='utf-8') as data_out:
    for hedge, counts in hedge_counts.items():
        data_out.write(",".join([hedge, str(counts)]))
        data_out.write("\n")
