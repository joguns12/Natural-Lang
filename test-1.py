from nltk.corpus import PlaintextCorpusReader, treebank
from CorpusReader_SLM import *




'''
print(len(inaugural.words()))
print(inaugural.sents())
print(len(inaugural.sents()))
print(inaugural.fileids())
print(inaugural.sents(['1789-washington.txt']))

print(len(brown.words()))
print(brown.sents())
'''
print(len(treebank.words()))
print(treebank.sents())

'''
myCorpus = CorpusReader_SLM(inaugural)

print(myCorpus.unigram())
print(myCorpus.bigram())
print(myCorpus.unigramGenerate())
print(myCorpus.unigramGenerate(10, [This]))
'''


#  This is for testing your own corpus
#
#  create a set of text files, store them in a directory specified from 'rootDir' variable
#
#  

rootDir = '_temp1'   # change that to the directory where the files are

newCorpus = PlaintextCorpusReader(rootDir, '.*txt')
x = newCorpus.sents()
for y in x:
    print(y)

'''
myC2 = CorpusReader_TFIDF(newCorpus)


print("-----\n")

'''
