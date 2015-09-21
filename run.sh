#!bin/bash

if [ $# -ne 1 ]
    then
        echo "The first argument must be the directory containing the input files."
        exit
else
    python clean_text.py "$1"
    #python create_datasheet.py
    echo "Done"
fi