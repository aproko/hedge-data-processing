import os
from os import listdir
from os.path import isfile, join
import datetime
import csv
import sys
import itertools
import numpy


#number_of_turkers = int(sys.argv[1])

map_month={"Jan":1, "Feb":2, "Mar":3, "Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}

#update addFields and updateJudgments so it calcualtes in batches
def addFields(csv_string_list):
    HIT_judgments = {}
    for csv_string in csv_string_list:
        #if csv_string[27] in HIT_judgments:
        #   entry = HIT_judgments[csv_string[27]]
        #else:
        #    entry = [csv_string[28], csv_string[29], 0,0]
   
        #if csv_string[118] == "n":
        #    entry[3] = entry[3] + 1
        #else:
        #    entry[2] = entry[2] + 1
        
        #HIT_judgments[csv_string[27]] = list(entry)

        for i in range(0,9):
            ent_key = ",".join([csv_string[37+i*9],csv_string[39+i*9]])
            if ent_key in HIT_judgments:
                entry = HIT_judgments[ent_key]
            else:
                entry = [csv_string[38 + i*9], csv_string[39 + i*9], 0,0]


            if csv_string[119+i] == "n":
                entry[3] = entry[3] + 1
            else:
                entry[2] = entry[2] + 1
 

            HIT_judgments[ent_key] = list(entry)

    for ent, jud in HIT_judgments.items():
        agreement = float(jud[2])/float(jud[3]+jud[2])
        if agreement > 0.5:
            final = 1.0
        else:
            final = 0.0
            agreement = 1 - agreement

        HIT_judgments[ent] = [jud[0], jud[1], [final], [agreement]]
    return  HIT_judgments

def addAgreement(all_hits, new_hits):
    for hit_key, hit_value in new_hits.items():
        #print hit_key
        #print hit_value
        if hit_key in all_hits:
            ent = all_hits[hit_key]
            ent[2] = ent[2] + hit_value[2]
            ent[3] = ent[3] + hit_value[3]
            all_hits[hit_key] = ent
          
        else:
            all_hits[hit_key] = hit_value
    return all_hits

def process(hit_list, turkers):
    #smaller_list = []
    #cur_first_date = datetime.datetime(2016,12,31,23,59,59,10)
    #time_list = []
    #top_list = []
        #for a in range(0,len(hit_list)):

    #cur_line = hit_list[a]
        #date = cur_line[18].split()
        #time = date[3].split(":")

        #date_object = datetime.datetime(int(date[5]),map_month[date[1]],int(date[2]),int(time[0]),int(time[1]),int(time[2]), a)
        #time_list.append(date_object)
    #time_list.sort()
        #for b in range(0, min(turkers, len(hit_list))):
    #top_list.append(hit_list[time_list[b].microsecond])
    return itertools.combinations(hit_list, turkers)

    #def average(hits_list, total_combos):
        #for h, v in hits_list.items():
        #print v[3]
        #print float(v[3])/float(total_combos)
        #new_v = [v[0], v[1], float(v[2])/float(total_combos), float(v[3])/float(total_combos)]
    #hits_list[h]= new_v
#return hits_list

def main():

    onlyfiles = [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) and "amt_added_data1" in f]
    
    for files in onlyfiles:
        print files
        fileLines = {}
        with open(files, 'rU') as input_file:
            reader = csv.reader(input_file)
            next(reader, None)
            first_line = reader.next()
            current_HIT_id = first_line[0]
     
            hits = {}
            one_hit_lines = []
            hit_agr = {}
            one_hit_lines.append(first_line)
            
            for line in reader:
                if line[0] == current_HIT_id:
                 
                    if line[36] == line[118]:
                        one_hit_lines.append(line)
                else:
                    hitLines = process(one_hit_lines, len(one_hit_lines))
                    #hitLines = process(one_hit_lines, number_of_turkers) #creates a set of lists of #ofturker judgments
                    count = 0
             
                    for it in hitLines:
                        count += 1
                        hits = addFields(it) #returns dictionary of (SentenceID --> [Sentence, Hedge, 1/0 majority vote]
                        hit_agr = addAgreement(hit_agr, hits) # 1/0 majority vote to existing other judgments:  (SentenceID --> [Sentence, Hedge, mj_vote1, mj_vote2, ..., mj_voten]
                    #hits = {}
                    for kkk, vvv in hit_agr.items():
                     
                        hit_agr[kkk] = [vvv[0], vvv[1], numpy.mean(vvv[2]), numpy.mean(vvv[3])]
                            #hits = average(hits, count)
                    fileLines.update(hit_agr)
                    current_HIT_id = line[0]
                    one_hit_lines = []
                    if line[36] == line[118]:
                        one_hit_lines.append(line)
                        #hits = {}
            hitLines = process(one_hit_lines, len(one_hit_lines))
            #hitLines = process(one_hit_lines, number_of_turkers) #creates a sorted list of HIT responses (= number of turkers)
            count = 0
            for it in hitLines:
                #print it
                count += 1
                hits = addFields(it)
                hit_agr = addAgreement(hit_agr, hits)
                        #hits = {}
            for kk, vv in hit_agr.items():
          
                hit_agr[kk] = [vv[0], vv[1], numpy.mean(vv[2]), numpy.mean(vv[3])]
                    #hits = average(hits, count)
            fileLines.update(hit_agr)



        with open(files.replace("amt_added", "amt_final"), 'w') as outFile:
            outFile.write("SentenceID,HedgeWord,Sentence,Final,Agreement\n")
            for item, value in fileLines.items():
                fi = value[2]
                if value[2] > 1.0:
                    fi = value[2] / 2
                agr = value[3]
                if value[3] > 1.0:
                    agr = value[3] / 2
                outFile.write(item + "," + ",".join(["\""+value[0]+"\"", str(fi), str(agr)]))
                outFile.write("\n")

main()
