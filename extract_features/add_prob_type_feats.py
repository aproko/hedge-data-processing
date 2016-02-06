import csv

hedges = {}

def readIn(filename):

    with open(filename, 'rU') as indict:
        reader = csv.reader(indict)
        next(reader, None)
        for line in reader:
            hedges[line[0]] = [line[1], line[8]]


readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/dictionary.csv')
readIn('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/multiword_dict.csv')


with open('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/out_vecs_ngrams_50_10.csv', 'rU') as infile:
    reader = csv.reader(infile)
    next(reader, None)
    for line in reader:
        hed = line[250]
        hed = hed.replace("'", "")
        line = hedges[hed] + line
        print line






