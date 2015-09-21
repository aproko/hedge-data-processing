#!bin/bash

if [ $# -ne 2 ]
    then
        echo "The first argument must be the directory containing the input files; the second argument must be the number of sentences per HIT in our AMT datasheet"
        exit
else
    python clean_text.py "$1"
    python create_datasheet.py "$1" "$2"
    echo "Done"
fi