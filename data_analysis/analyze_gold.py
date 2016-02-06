import codecs
import csv
from nltk.stem import WordNetLemmatizer
from os import listdir
from os.path import isfile, join

dict = {}
lemmatizer = WordNetLemmatizer()

def readIn(filename, mode):
    with codecs.open(filename, 'rU', encoding='utf-8') as inputFile:
        reader = csv.reader(inputFile)
        next(reader, None)
        for line in reader:
            if mode == "gold":
                gold_qs.append(line)
            else:
                entry = [line[1], line[2], line[3], line[4], line[5], line[6]]
                if mode == "dict":
                    dict_lemma = lemmatizer.lemmatize(line[0])
                    if dict_lemma in dict:
                        dict[dict_lemma] = dict[dict_lemma] + 1
                    else:
                        dict[dict_lemma] = 1
                elif mode == "multi":
                    if line[0] in dict:
                        dict[line[0]] = dict[line[0]] + 1
                    else:
                        dict[line[0]] = 1


def main():
    
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/dictionary.csv', "dict")
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/multiword_dict.csv', "multi")
    input_directory="/Users/aproko/Desktop/hedging_gold"
    
    onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f))) ]
    
    #This lets us keep track of the number of instances of each word in our datasheet

    tp = 0
    fp = 0
    fn = 0
    for files in onlyfiles:
        with open(join(input_directory, files)) as infile:
            for line in infile:
                
                for keyword in dict:
                    if keyword in line:
                        hedge_key = ">" + keyword + "<"
                        if hedge_key in line:
                            tp += 1
                            line = line.replace("<hRel" + hedge_key + "/hRel", "")
                            line = line.replace("<hProp" + hedge_key + "/hProp", "")
                        else:
                            fp += 1
                fn = fn + line.count("<")

    print tp
    print fp
    print fn


main()

