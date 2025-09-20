''' 
Add modules you want to import first

'''
import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter, defaultdict
class CorpusReader_SLM:
    def __init__(self, corpus, stopWord='none', toStem=False, smooth=False, trigram=False):
        self.smooth = smooth
        self.use_trigram = trigram

        # grab all the sentences from the corpus
        sents = corpus.sents()

        # make everything lowercase so it's consistent
        sents = [[w.lower() for w in sent] for sent in sents]

        # set up stopwords if we’re using them
        stoplist = set()
        if stopWord == "standard":
            stoplist = set(stopwords.words("english"))
        elif stopWord != "none":
        # if a file is given, load those words as stopwords
            with open(stopWord, "r") as f:
                stoplist = set(line.strip().lower() for line in f)

         # actually remove the stopwords from each sentence
        if stoplist:
            sents = [[w for w in sent if w not in stoplist] for sent in sents]

        # stem words if user asked for it
        if toStem:
            stemmer = SnowballStemmer("english")
            sents = [[stemmer.stem(w) for w in sent] for sent in sents]

        # flatten everything into one big token list
        self.tokens = [w for sent in sents for w in sent]
        self.vocab = set(self.tokens)
        self.V = len(self.vocab)
        self.N = len(self.tokens)

        # count how often each unigram/bigram/trigram shows up
        self.unigram_counts = Counter(self.tokens)
        self.bigram_counts = Counter((sent[i], sent[i+1]) for sent in sents for i in range(len(sent)-1))
        self.trigram_counts = Counter()
        if trigram:
            self.trigram_counts = Counter((sent[i], sent[i+1], sent[i+2]) for sent in sents for i in range(len(sent)-2))

        # Unigrams
        if smooth:
            self.unigram_probs = {w: (c+1)/(self.N+self.V) for w, c in self.unigram_counts.items()}
        else:
            self.unigram_probs = {w: c/self.N for w, c in self.unigram_counts.items()}

        # Bigrams
        if smooth:
            self.bigram_probs = {(w1, w2): (c+1)/(self.unigram_counts[w1]+self.V) 
                                 for (w1, w2), c in self.bigram_counts.items()}
        else:
            self.bigram_probs = {(w1, w2): c/self.unigram_counts[w1] 
                                 for (w1, w2), c in self.bigram_counts.items()}

        # Trigrams
        self.trigram_probs = {}
        if trigram:
            if smooth:
                self.trigram_probs = {(w1, w2, w3): (c+1)/(self.bigram_counts.get((w1, w2), 0)+self.V) 
                                      for (w1, w2, w3), c in self.trigram_counts.items()}
            else:
                self.trigram_probs = {(w1, w2, w3): c/self.bigram_counts[(w1, w2)] 
                                      for (w1, w2, w3), c in self.trigram_counts.items() 
                                      if self.bigram_counts.get((w1, w2), 0) > 0}
                
    def unigram(self, count = 0):
        return []

    def bigram(self, count = 0):
        return []

    def trigram(self, count = 0):
        return []

    def unigramGenerate(self, code=0, head=[]):
        return ""

    def bigramGenerate(self, code=0, head=[]):
        return ""

    def trigramGenerate(self, code=0, head=[]):
        return ""

