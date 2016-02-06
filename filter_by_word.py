import csv
import random
from sets import Set

gold_qs = []
wanted_words = []
filtered_hits = []
header = []

with open('wanted_words.txt', 'rU') as wwfile:
    for line in wwfile:
        wanted_words.append(line.strip())

with open('amt_all_data.csv', 'rU') as infile:
    reader = csv.reader(infile)
    header = next(reader)
    for line in reader:
        gold_qs.append(line[0:10])
        for i in range(0,9):
            hit = line[(10 + 9*i):(10 + 9*i + 9)]
            if hit[2] in wanted_words:
                filtered_hits.append(hit)
#gold_qs = Set(gold)

count = 0
with open('new_amt_data.csv', 'w') as outfile:
    outfile.write(",".join(header))
    outfile.write("\n")
    temp_def = []
    for item in filtered_hits:
        if count == 0:
            temp_def = random.choice(gold_qs)
            count += 1
        if count < 10 and count > 0:
            temp_def = temp_def + item
            count += 1
        if count == 10:
            outfile.write(",".join(temp_def))
            outfile.write("\n")
            count = 0
    if count != 0:
        outfile.write(",".join(temp_def))
        outfile.write("\n")