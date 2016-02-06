import csv
hedges = {}
with open('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/vecs_tf_only_data.csv', 'rU') as infile:
    reader = csv.reader(infile)
    for line in reader:
        hedge = line[250]
        if hedge in hedges:
            hedges[hedge] += 1
        else:
            hedges[hedge] = 1


for hed in hedges:
    print hed, ",", hedges[hed]