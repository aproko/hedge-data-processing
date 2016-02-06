import codecs
import csv
from nltk.stem import WordNetLemmatizer
from os import listdir
from os.path import isfile, join
import sys
import string
from bs4 import BeautifulSoup

dict = {}
multi_dict = {}
lemmatizer = WordNetLemmatizer()
input_directory = sys.argv[1]

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
                        dict[dict_lemma] = [line[1], 0]
                elif mode == "multi":
                    if line[0] not in dict:
                        multi_dict[line[0]] = [line[1], 0]


def main():
    
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/dictionary.csv', "dict")
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/multiword_dict.csv', "multi")

    onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and  ".toAnno.txt" in f) ]
    for file in onlyfiles:

        #with codecs.open(join(input_directory,file), 'rU', encoding='utf-8') as infile:
        
        #for line in infile:
                #s = line
        soup = BeautifulSoup(open(join(input_directory, file)), "lxml")
        line = unicode(soup.get_text())
        lines = line.split("\n")
        for l in lines:
            if len(l) > 2:
                id_and_s = l.split("::")
                s = id_and_s[1]
                for mult in multi_dict:
                    if mult in s:
                        s = s.replace(mult, "")
                        mu_li = multi_dict[mult]
                        multi_dict[mult] = [mu_li[0], mu_li[1] + 1]
                words = s.split()
                for word in words:
                    for ch in word:
                        if ch in string.punctuation:
                            word = word.replace(ch, "")
                    lemma_word = lemmatizer.lemmatize(word)
                    if lemma_word in dict:
                        li = dict[lemma_word]
                        dict[lemma_word] = [li[0], li[1] + 1]


    for it, val in dict.items():
        print it, ",", val
    for itm, valm in multi_dict.items():
        print itm, ",", valm

main()
