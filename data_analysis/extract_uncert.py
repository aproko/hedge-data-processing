import os
from os import listdir
from os.path import isfile, join
import datetime
import csv
import sys

number_of_turkers = int(sys.argv[1])

map_month={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

#update addFields and updateJudgments so it calcualtes in batches
def addFields(csv_string_list):
    HIT_judgments = {}
    for csv_string in csv_string_list:
        
        for i in range(0,10):
            print csv_string
            
            
            
            if "y" in csv_string[52 + i]:
                val = 1
            elif "n" in csv_string[52+i]:
                val = 0
            else:
                val = int(csv_string[52+i])
            
            if csv_string[30+i*2] in HIT_judgments:
                entry = HIT_judgments[csv_string[30+i*2]]
                entry[1] = entry[1] + val
                entry[2] = entry[2] + 1
            else:
                entry = [csv_string[31 + i*2], val, 1]
            
            HIT_judgments[csv_string[30 + i*2]] = list(entry)
    for ent, jud in HIT_judgments.items():
        agreement = 0.0
        if float(jud[2])/float(jud[3] + jud[2]) > 0.5:
            final = 1.0
        else:
            final = 0.0
    
        HIT_judgments[ent] = [jud[0], jud[1], final]

    return  HIT_judgments

def process(hit_list, turkers):
    smaller_list = []
    cur_first_date = datetime.datetime(2016,12,31,23,59,59,10)
    time_list = []
    top_list = []
    for a in range(0,len(hit_list)):
        cur_line = hit_list[a]
        date = cur_line[18].split()
        time = date[3].split(":")
        
        date_object = datetime.datetime(int(date[5]),map_month[date[1]],int(date[2]),int(time[0]),int(time[1]),int(time[2]), a)
        time_list.append(date_object)
        time_list.sort()
    for b in range(0, min(turkers, len(hit_list))):
        top_list.append(hit_list[time_list[b].microsecond])
    return top_list


def main():
    
    onlyfiles = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) and "uncert_" in f]
    
    for files in onlyfiles:
        fileLines = {}
        with open(files, 'rU') as input_file:
            reader = csv.reader(input_file)
            next(reader, None)
            first_line = reader.next()
            current_HIT_id = first_line[30]
            hits = []
            one_hit_lines = []
            #hitLines = addFields(first_line)
            for line in reader:
                if line[30] == current_HIT_id:
                    one_hit_lines.append(line)
                #hitLines = updateJudgments(hitLines, line)
                #print hitLines
                else:
                    hitLines = process(one_hit_lines, number_of_turkers) #creates a sorted list of HIT responses (= number of turkers)
                    hits = addFields(hitLines)
                    fileLines.update(hits)
                    current_HIT_id = line[30]
                    one_hit_lines = []
                    one_hit_lines.append(line)
            hitLines = process(one_hit_lines, number_of_turkers) #creates a sorted list of HIT responses (= number of turkers)
            hits = addFields(hitLines)
            fileLines.update(hits)
        
        with open(files.replace("uncert", "un_ana"), 'w') as outFile:
            outFile.write("SentenceID,Sentence,UncertTotal,NumTurkers,Final\n")
            for item, value in fileLines.items():
                average = 0.0
                average = float(value[1])/float(value[2])
                outFile.write(item + "," + ",".join([value[0], str(value[1]), str(value[2]),str(average)]))
                outFile.write("\n")

main()
