import csv

hedges = {}

with open('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/dictionary.csv', 'rU') as indict:
    reader = csv.reader(indict)
    next(reader, None)
    for line in reader:
        hedges[line[0]] = [0, 0]
        
with open('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/multiword_dict.csv', 'rU') as indict:
    reader = csv.reader(indict)
    next(reader, None)
    for line in reader:
        hedges[line[0]] = [0, 0]

with open('amt_process_with_counts.csv', 'rU') as infile:
    reader = csv.reader(infile)
    next(reader, None)
    for line in reader:
        hedge = line[1]
        count = line[3]
        if hedge in hedges:
            oldcounts = hedges[hedge]
            newcount= [int(oldcounts[0]) + int(count),int(oldcounts[1]) + 1]
            hedges[hedge] = newcount
        else:
            hedges[hedge] = [int(count), 1]


with open('hedge_distrib.csv', 'w') as outfile:
    for key, value in hedges.items():
        outfile.write(key + "," + ",".join([str(value[0]), str(value[1])]))
        outfile.write("\n")

