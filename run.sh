#!bin/bash

    while getopts 'cdna*' flag; do
        case "${flag}" in
            c) python clean_text.py "$2"; echo "Cleaning Input Text" ;;
            d) python create_datasheet.py "$2" "$3"; echo "Creating Datasheet" ;;
            n) python data_analysis.py "$2" "$3"; echo "Analyzing $3 data" ;;
            a) python clean_text.py "$2"; python create_datasheet.py "$2" "$3"; echo "Running the entire pipeline" ;;
        esac
    done

