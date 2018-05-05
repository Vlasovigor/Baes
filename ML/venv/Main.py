from __future__ import division
from math import log
from _collections import defaultdict


def clean(word):
    if((word[-1] == '.') or (word[-1] == ',')):
        return word[:len(word)-1]
    return word


traningFile = open("/home/igor/Загрузки/news_data/news_train.txt")
allStrings = traningFile.readlines()
traningFile.close()

tags = ['science', 'style', 'culture', 'life', 'economics', 'business', 'travel', 'forces', 'media', 'sport']

classesStr = defaultdict(lambda: '')
countTag = defaultdict(lambda: 0)

for str in allStrings:
    a = str.split('\t')
    classesStr[a[0]] += a[2]
    countTag[a[0]] += 1

probabilityClass = defaultdict(lambda: 0)
countWord = defaultdict(lambda: 0)

for tag in tags:
    a = classesStr[tag].split()
    for word in a:
        word = clean(word)
        probabilityClass[tag, word] += 1
        countWord[tag] += 1

for tag, word in probabilityClass:
    probabilityClass[tag, word] = log(probabilityClass[tag, word]/ countWord[tag], 10 ** -7)

for tag in countTag:
    countTag[tag] = log(countTag[tag]/60000, 10 ** -7)

testFile = open("/home/igor/Загрузки/news_data/news_test.txt")
testAllStr = testFile.readlines()
testFile.close()

outputFile = open("/home/igor/Загрузки/news_data/output.txt", 'w')

for str in testAllStr:
    a = str.split('\t')
    b = a[1].split()

    probability = defaultdict(lambda: 1)

    for tag in tags:
        for word in b:
            word = clean(word)
            if (probabilityClass[tag, word] == 0):
                probability[tag] += log(1/(2*countWord[tag]), 10 ** -7)
            else:
                probability[tag] += probabilityClass[tag, word]

        probability[tag] += countTag[tag]

 #   for tag in tags:
  #      print(probability[tag])
   # print('\n')

    maxProb = probability[tags[0]]
    maxTag = tags[0]
    for tag in tags:
        if probability[tag] < maxProb:
            maxProb = probability[tag]
            maxTag = tag
    outputFile.write(maxTag + '\n')
outputFile.close()