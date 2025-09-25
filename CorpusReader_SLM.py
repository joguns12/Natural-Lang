import random
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from collections import Counter, defaultdict

class CorpusReader_SLM:
    def __init__(self, corpus, stopWord='none', toStem=False, smooth=False, trigram=True):
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
        words = list(self.unigram_probs.keys())
        prob = list(self.unigram_probs.values())

        ugrams = list(zip(words, prob))

        # must account for ties
        if count > 0:
            ugrams.sort(key=lambda x:x[1], reverse=True) # sort on probability count
            if count <= len(ugrams):
                cutoff = ugrams[count - 1][1]
                ugrams[:] = list(filter(lambda x:x[1] >= cutoff, ugrams))

        # sorted() creates a copy of original list while sort() does not
        ugrams.sort()
        return ugrams

    def bigram(self, count = 0):
        words = list(self.bigram_probs.keys())
        prob = list(self.bigram_probs.values())

        bigrams = list(zip(words, prob))

        if count > 0:
            bigrams.sort(key=lambda x:x[1], reverse=True)
            if count <= len(bigrams):
                cutoff = bigrams[count - 1][1]
                bigrams[:] = list(filter(lambda x:x[1] >= cutoff, bigrams))

        bigrams.sort()
        return bigrams

    def trigram(self, count = 0):
        # return an empty list if trigram set to false
        if self.trigram == False:
            return []

        words = list(self.trigram_probs.keys())
        prob = list(self.trigram_probs.values())

        trigrams = list(zip(words, prob))

        if count > 0:
            trigrams.sort(key=lambda x:x[1], reverse=True)
            if count <= len(trigrams):
                cutoff = trigrams[count - 1][1]
                trigrams[:] = list(filter(lambda x:x[1] >= cutoff, trigrams))

        trigrams.sort()
        return trigrams

    def unigramGenerate(self, code=0, head=[]):
        if code not in [0, 1, 2]:
            return ""

        sentence = list(head)

        # generate 10 words by default (fixed length)
        for _ in range(10):
            if code == 0: 
            # grab every word tied for max_prob, then randomly pick one
                max_prob = max(self.unigram_probs.values())
                best_words = [w for w, p in self.unigram_probs.items() if p == max_prob]
                word = random.choice(best_words)

            elif code == 1:  # weighted random
            # random.choices(..., k=1) picks *1 word* using probs as weights
            # if k was 2, it would pick 2 words, etc.
                words, probs = zip(*self.unigram_probs.items())
                word = random.choices(words, weights=probs, k=1)[0]

            elif code == 2:  # top-10 weighted random
                items = sorted(self.unigram_probs.items(), key=lambda x: -x[1])[:10]
                words, probs = zip(*items)
                word = random.choices(words, weights=probs, k=1)[0]

            sentence.append(word)

        return self._format_sentence(sentence)


    def bigramGenerate(self, code=0, head=[]):
        if code not in [0, 1, 2]:
            return ""

        sentence = list(head)

        for _ in range(10):
            if code == 0: 
                max_prob = max(self.bigram_probs.values())
                best_words = [w for w, p in self.bigram_probs.items() if p == max_prob]
                word = random.choice(best_words)

            elif code == 1:  # weighted random
                words, probs = zip(*self.bigram_probs.items())
                word = random.choices(words, weights=probs, k=1)[0]

            elif code == 2:  # top-10 weighted random
                items = sorted(self.bigram_probs.items(), key=lambda x: -x[1])[:10]
                words, probs = zip(*items)
                word = random.choices(words, weights=probs, k=1)[0]

            sentence.append(word[1])

        return self._format_sentence(sentence)

    def trigramGenerate(self, code=0, head=[], length=10):
        if code not in [0, 1, 2] or self.trigram == False:
            return ""

        sentence = list(head)
        
        for _ in range(length):
            context = tuple(sentence[-2:])
            candidates = {k: v for k, v in self.trigram_probs.items() if k[:2] == context} 
            if not candidates: 
                break

            if code == 0: 
                max_prob = max(self.trigram_probs.values())
                best_words = [w for w, p in self.trigram_probs.items() if p == max_prob]
                word = random.choice(best_words)[2]

            elif code == 1:  # weighted random
                words, probs = zip(*self.trigram_probs.items())
                word = random.choices(words, weights=probs, k=1)[0][2]

            elif code == 2:  # top-10 weighted random
                items = sorted(self.trigram_probs.items(), key=lambda x: -x[1])[:10]
                words, probs = zip(*items)
                word = random.choices(words, weights=probs, k=1)[0][2]

            sentence.append(word)

        return self._format_sentence(sentence)
    
        # helper to format sentences properly
    def _format_sentence(self, tokens):
        result = ""
        for i, w in enumerate(tokens):
            if i > 0 and w not in [".", ",", "!", "?", ";", ":"]:
                result += " "
            result += w
        return result