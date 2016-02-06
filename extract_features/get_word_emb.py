import gensim
import csv
import numpy
import sys
from os import listdir
from os.path import isfile, join
from nltk.stem import WordNetLemmatizer

words = []
lemmatizer = WordNetLemmatizer()

def getSentences(filename):
    sents = []
    with open(filename, 'rU') as infile:
        #reader = csv.reader(infile)
        #next(reader, None)
        #for line in reader:
        for line in infile:
            newl = line.split("::")
            sents.append(newl[1].split())
    return sents


def getWords(filename):
    with open(filename, 'rU') as infile:
        reader = csv.reader(infile)
        count = 0
        for line in reader:
            count +=1
            #sents.append(line[1].decode('windows-1252').strip().split())
            words.append([line[0].replace("'", ""), line[8], line[9], line[10], line[11]])
    return words

def main():
    input_directory = "/Users/aproko/Desktop/all_data"
    sentences = []
    onlyfiles = [ f for f in listdir(input_directory) if (isfile(join(input_directory,f)) and ".toAnno.txt" in f) ]
    for file in onlyfiles:
     
        sentences = sentences + (getSentences(join(input_directory,file)))
    # print "Read in sentences"
    model = gensim.models.Word2Vec(sentences, size=50, window=10)
            # print "Generated model"
    #model = gensim.models.Word2Vec.load_word2vec_format('/Users/aproko/Downloads/google_vectors.bin', binary=True)
    
#bigram_transformer = gensim.models.Phrases(sentences)
#model2 = gensim.models.Word2Vec(bigram_transformer[sentences], size=100)
    
    #model = gensim.models.Word2Vec.load_word2vec_format('/Users/aproko/Downloads/google_vectors.bin', binary=True)
    #model = gensim.models.Word2Vec.load_word2vec_format('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/trunk/text8', binary=True)
    #model2 = gensim.models.Phrases.load_word2vec_format('/Users/aproko/Downloads/google_vectors.bin', binary=True)

    words = getWords("/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/added_data.csv")

            
    for word in words:
        if word[0] in model:
            numpy.set_printoptions(suppress=True, precision=5)
            print numpy.array_str(model[word[0]], max_line_width=4000), ",",
        elif " " in word[0]:
            wds = word[0].split()
            numpy.set_printoptions(suppress=True, precision=5)
            lis = [0]*50
            for x in range(0,len(wds)):
                if wds[x] in model:
                    lis = numpy.add(lis, model[wds[x]])
            print numpy.array_str(numpy.array(lis), max_line_width=4000), ",",
            
        else:
            if lemmatizer.lemmatize(word[0]) in model:
                numpy.set_printoptions(suppress=True, precision=5)
                print numpy.array_str(model[word[0]], max_line_width=4000), ",",
            else:
                ll = [0]*50
                print numpy.array_str(numpy.array(ll), max_line_width=4000), ",",

        for ind in range(1,len(word)):
            w = word[ind]
            if w in model:
                numpy.set_printoptions(suppress=True, precision=5)
                print numpy.array_str(model[w], max_line_width=4000), ",",

            else:
                
                if lemmatizer.lemmatize(w) in model:
                    numpy.set_printoptions(suppress=True, precision=5)
                    print numpy.array_str(model[lemmatizer.lemmatize(w)], max_line_width=4000), ",",
                else:
                    lls = [0]*50
                    numpy.set_printoptions(suppress=True, precision=5)
                    print numpy.array_str(numpy.array(lls), max_line_width=4000), ",",
        print ""
            #else:
#print ""
                #   elif word in model2:
#print model2[word]


main()