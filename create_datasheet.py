from os import listdir
from os.path import isfile, join

listoflines = []
dict = {}

with open('dict.csv', 'rb') as d:
    reader = csv.reader(d)
    for line in reader:
        dict[line[0]] = line[2] + "," + line[3]

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for files in onlyfiles:
    with open(file, 'rb') as inputFile:
        for line in inputFile:
            line = line.replace("\n", "")
            words = line.split(" ")
            for word in words:
                if word in dict:
                    str = line + "," + word + "," + dict[word] + "\n"
                    listoflines.append(str)

with open('amt_input.csv', 'w') as out:
    for item in listoflines:
        out.write(item)
            