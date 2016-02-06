import csv
wanted = []

with open("/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/belief_signals.txt", 'rU') as want:
    for word in want:
        word = word.strip()
        wanted.append(word)



with open("/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/out_vecs_50_10_probs.csv", 'rU') as infile:
    reader = csv.reader(infile)
    next(reader, None)
    for line in reader:
        hedge = line[252].strip()
        if hedge in wanted:
            print line