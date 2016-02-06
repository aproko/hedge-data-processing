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
na = []
cb = []
ncb = []
rob = []

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
                        dict[dict_lemma] = [line[1], 0,0,0,0]
                elif mode == "multi":
                    if line[0] not in dict:
                        multi_dict[line[0]] = [line[1],0,0,0,0]

def main():
    
    readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/dictionary.csv', "dict")
    #readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/multiword_dict.csv', "multi")
    
    onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".toAnno.txt" in f) ] 
    for file in onlyfiles:

        soup = BeautifulSoup(open(join(input_directory, file)), "lxml")
        paragraph = unicode(soup.get_text())
        nas = soup.find_all('na')
        for it in nas:
            item = it.string
            lemma_item = lemmatizer.lemmatize(item)
            if lemma_item in dict:
                ll = dict[lemma_item]
                dict[lemma_item] = [ll[0],ll[1]+1, ll[2], ll[3], ll[4]]
        cbs = soup.find_all('cb')
        for it in cbs:
            item = it.string
            lemma_item = lemmatizer.lemmatize(item)
            if lemma_item in dict:
                ll = dict[lemma_item]
                dict[lemma_item] = [ll[0],ll[1], ll[2]+1, ll[3], ll[4]]

        ncbs = soup.find_all('ncb')
        for it in ncbs:
            item = it.string
            lemma_item = lemmatizer.lemmatize(item)
            if lemma_item in dict:
                ll = dict[lemma_item]
                dict[lemma_item] = [ll[0],ll[1], ll[2], ll[3] + 1, ll[4]]

        robs = soup.find_all('rob')
        for it in robs:
            item = it.string
            lemma_item = lemmatizer.lemmatize(item)
            if lemma_item in dict:
                ll = dict[lemma_item]
                dict[lemma_item] = [ll[0],ll[1], ll[2], ll[3], ll[4] + 1]

            
    for its, val in dict.items():
        print its, ",", val

main()
