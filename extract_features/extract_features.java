import java.io.*;
import java.util.*;
import java.lang.*;


import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;

public class extract_features {
    public static void main(String[] args) throws FileNotFoundException {
        MaxentTagger tagger = new MaxentTagger("/Users/aproko/Downloads/stanford-postagger-2015-04-20/models/english-left3words-distsim.tagger");
        
        List<List<HasWord>> sentences = MaxentTagger.tokenizeText(new BufferedReader(new FileReader("/Users/aproko/Desktop/hedge_annotation/hedge-data-processing/extract_features/sentences.txt")));
        for (List<HasWord> sentence : sentences) {
            List<TaggedWord> tSentence = tagger.tagSentence(sentence);
            System.out.println(Sentence.listToString(tSentence, false));
        }
    }
    
}
/*
        List<List<HasWord>> tokenizedSentences = MaxentTagger.tokenizeText(new StringReader(processedSentence));
        //System.out.println(taggedSentence);
        List<TaggedWord> taggedSentence = new ArrayList<TaggedWord>();
        for(List<HasWord> tokenizedSentence : tokenizedSentences) {
            taggedSentence.addAll(TAGGER.tagSentence(tokenizedSentence));
        }
    }
}*/