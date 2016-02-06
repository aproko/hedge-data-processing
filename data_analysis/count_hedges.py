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
                    if dict_lemma not in dict:
                        dict[dict_lemma] = 0
                elif mode == "multi":
                    if line[0] not in dict:
                        dict[line[0]] = 0


def main():
    
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/dictionary.csv', "dict")
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/multiword_dict.csv', "multi")

    with open("/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/data_analysis/amt_processed_data.csv", 'rU') as infile:
        reader = csv.reader(infile)
        next(reader, None)
        for line in reader:
            dict[line[1]] = dict[line[1]] + 1

    for it, val in dict.items():
        print it+","+str(val)

main()