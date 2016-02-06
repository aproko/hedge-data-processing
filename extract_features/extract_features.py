import edu.stanford.nlp.tagger.maxent.Maxent

newlines = []
with open('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/sentences.txt', 'rU') as infile:
    for line in infile:
        ne = line.strip() + "!\n"
        newlines.append(ne)

with open('/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/out_sentences.txt', 'w') as outfile:
    for item in newlines:
        outfile.write(item)
        outfile.write("\n")


TAGGER = new MaxentTagger("/Users/aproko/Downloads/stanford-postagger-2015-04-20/models/english-left3words-distsim.tagger");

List<List<HasWord>> tokenizedSentences = MaxentTagger.tokenizeText(new StringReader(processedSentence));
//System.out.println(taggedSentence);
List<TaggedWord> taggedSentence = new ArrayList<TaggedWord>();
for(List<HasWord> tokenizedSentence : tokenizedSentences) {
    taggedSentence.addAll(TAGGER.tagSentence(tokenizedSentence));
}