import os
from os import listdir
from os.path import isfile, join
import datetime
import csv
import sys

answer_dict = {}

with open('answer_dict.csv', 'rU') as input:
    reader = csv.reader(input)
    next(reader, None)
    for line in reader:
        answer_dict[line[0]] = [line[1], line[2], line[3], line[4]]


onlyfiles = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) and "amt_word" in f]

for file in onlyfiles:
    list_of_workers = {}
    if "def" in file:
        mode = 1
    elif "ex" in file:
        mode = 2
    else:
        mode = 3

    with open(file, 'rU') as input_file:
        freader = csv.reader(input_file)
        next(freader, None)
        for input_line in freader:
            workerid = input_line[15]
            if workerid in list_of_workers:
                entry = list_of_workers[workerid]
            else:
                entry = [0,0,0]
            sid = input_line[27]
            answer = input_line[118]
            amt_answers = answer_dict[sid]
         
            if answer in amt_answers[0]:
                entry[0] += 1
            entry[2] += 1
            if answer in amt_answers[mode]:
                 entry[1] += 1
                
            
            for i in range(0,9):
                sid = input_line[37+i*9]
                
                answer = input_line[119 + i]
          
                amt_answers = answer_dict[sid]
                if answer in amt_answers[0]:
                    entry[0] += 1
                entry[2] += 1
                if answer in amt_answers[mode]:
                    entry[1] += 1
                        
            list_of_workers[workerid] = entry

    with open(file.replace("amt", "byworker"), 'w') as outfile:
        outfile.write("WorkerID,Correct,Agreed,Total\n")
        for item, value in list_of_workers.items():
            outfile.write(item + "," + ",".join([str(value[0]), str(value[1]), str(value[2])]))
            outfile.write("\n")
