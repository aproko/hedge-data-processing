#!/usr/bin/bash
filename="/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/sentences.txt"
while read -r line
do
    name=$line
    ./stanford-postagger.sh models/english-bidirectional-distsim.tagger $name >> labeled_s.txt

done < "$filename"

