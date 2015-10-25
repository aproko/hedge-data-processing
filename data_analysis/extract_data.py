import os
from os import listdir
from os.path import isfile, join
from datetime import datetime
import csv
import sys

number_of_turkers = sys.argv[1]

map_month={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

#update addFields and updateJudgments so it calcualtes in batches
def addFields(csv_string_list):
    HIT_judgments = {}
    for csv_string in csv_string_list:

        entry = [csv_string[28], csv_string[29], 0,0]
        if csv_string[118] == "n":
            entry[3] = 1
        else:
            entry[2] = 1
        HIT_judgments[csv_string[27]] = list(entry)

        for i in range(0,9):
            new_entry = [csv_string[38 + i*9], csv_string[39 + i*9], 0,0]
            if csv_string[119+i] == "n":
                new_entry[3] = 1
            else:
                new_entry[2] = 1
            HIT_judgments[csv_string[37 + i*9]] = list(new_entry)

    return  HIT_judgments


def updateJudgments(judg_Dict, csv_line):
    past_entry = judg_Dict[csv_line[27]]
    if csv_line[118] == "n":
        past_entry[3] += 1
    else:
        past_entry[2] += 1
    judg_Dict[csv_line[27]] = list(past_entry)

    for i in range(0,9):
        past_entry = judg_Dict[csv_line[37+i*9]]
        if csv_line[119+i] == "n":
            past_entry[3] += 1
        else:
            past_entry[2] += 1
        judg_Dict[csv_line[37 + i*9]] = list(past_entry)

    return  judg_Dict
    


def process(hit_list, turkers):
    smaller_list = []
    cur_first_date = datetime.datetime(2016,12,31,23,59,59,10)
    time_list = []
    top_list = []
    for a in range(0,len(hit_list)):
        cur_line = hit_list[a]
        date = cur_line[18].split()
        time = date[3].split(":")
        date_object = datetime.datetime(date[5],map_month(date[1]),date[2],time[0],time[1],time[2], a)
        time_list.append(date_object)
        time_list.sort()
    for b in range(0, turkers)
        top_list.append(hit_list[time_list[b].microsecond])
    return top_list
        

def main():

    onlyfiles = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) and "amt" in f]
    
    for files in onlyfiles:
        fileLines = {}
        with open(files, 'rU') as input_file:
            reader = csv.reader(input_file)
            next(reader, None)
            first_line = reader.next()
            current_HIT_id = first_line[0]
            #hitLines = addFields(first_line)
            for line in reader:
                if line[0] == current_HIT_id:
                    one_hit_lines.append(line[0])
                    #hitLines = updateJudgments(hitLines, line)
                    #print hitLines
                else:
                    hitLines = process(one_hit_lines, number_of_turkers)
                    hitLines = updateJudgments(hitLines, number_of_turkers)
                    fileLines.update(hitLines)
                    current_HIT_id = line[0]
                    hitLines = addFields(line)
            fileLines.update(hitLines)

        with open(files.replace("amt", "data"), 'w') as outFile:
            outFile.write("SentenceID,Sentence,HedgeWord,Hedge,NotHedge,Final,Agreement\n")
            for item, value in fileLines.items():
                agreement = 0.0
                if value[2] > value[3]:
                    agreement = float(value[2])/float(value[2] + value[3])
                else:
                    agreement = float(value[3])/float(value[2]+value[3])
                outFile.write(item + "," + ",".join([value[0], value[1], str(value[2]),str(value[3]), str(float(value[2])/float(value[3] + value[2])), str(agreement)]))
                outFile.write("\n")

main()
