from os import listdir
from os.path import isfile, join

onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

for files in onlyfiles:
    cleanLines = []
    with open(file, 'rb') as fileToClean:
        for line in fileToClean:
            line = line.replace("\n", "")
            cleanLine = re.sub(r'<(.*?)>', '', line)
            if not cleanLine:
                cleanLines.append(cleanLine)

    outfilename = file + ".anno"
    with open(outfilename, 'w') as cleanFile:
        for item in cleanLines:
            cleanFile.write(item)