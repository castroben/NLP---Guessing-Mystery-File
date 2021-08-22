import string
import nltk
import numpy as np
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
stopEn = stopwords.words('english')

#Arguments:
# filename: name of file to read in
#Returns: a list of strings
# each string is one line in the file, 
# and all of the characters should be lowercase, have no newlines, and have both a prefix and suffix of '__' (2 underscores)
def getFormattedText(filename) :
    #fill in

    with open(filename, "r") as file:
        corpus = file.read()
        lines = corpus.splitlines()

    for i in range(len(lines)):
        lines[i] = lines[i].lower()
        lines[i] = '__'+lines[i]+'__'
            
    return lines
        
        

#Arguments:
# line: a string of text
#Returns: a list of 3-character n-grams
def getNgrams(line) :
    #fill in
    nGrams = [line[i:i+3] for i in range(0, len(line)-4)]

    
    return nGrams

#Arguments:
#  filename: the filename to create an n-gram dictionary for
#Returns: a dictionary
#  where ngrams are the keys and the count of that ngram is the value.
def getDict(filename):
    #fill in
    lines = getFormattedText(filename)
    nGrams = []
    for i in range(len(lines)):
        tempList = getNgrams(lines[i])
        nGrams.extend(tempList)


    nGramDict = dict.fromkeys(nGrams,0)
    for i in range(len(nGrams)):
        nGramDict[nGrams[i]]+=1
   
    return nGramDict

#Arguments:
#   filename: the filename to generate a list of top N (most frequent n-gram, count) tuples for
#   N: the number of most frequent n-gram tuples to have in the output list.
#Returns: a list of N tuples 
#   which represent the (n-gram, count) pairs that are most common in the file.
def topNCommon(filename,N):

    origDict = getDict(filename)
    commonN = []
    #sortedDict = {k:v for k,v in sorted(origDict.items(),key = lambda item: item[1])}

    for i in range(N):
        key = max(origDict, key= lambda x: origDict[x])
        val = origDict.pop(key)
        commonN.append((key,val))
    return commonN

#Arguments:
#   fileNamesList: a list of filepath strings for the different language text files to process
#Returns: a list of dictionaries 
#   where each dictionary corresponds to one of the filepath strings.
def getAllDicts(fileNamesList):
    langDicts = [getDict(file) for file in fileNamesList]

    return langDicts

#Arguments:
#   listOfDicts: A list of dictionaries where the keys are n-grams and the values are the count of the n-gram
#Returns: an alphabetically sorted list containing all of the n-grams across all of the dictionaries in listOfDicts (note, do not have duplicates n-grams)
def dictUnion(listOfDicts):

    tempset = set()

    for i in range(len(listOfDicts)):
        tempset.update(listOfDicts[i].keys())
    s = list(tempset)
    
    return sorted(s)


#Arguments:
#   langFiles: list of filepaths of the languages to compare testFile to.
#Returns a sorted list of all the n-grams across the languages
def getAllNGrams(langFiles):

    dictList = getAllDicts(langFiles)
    return dictUnion(dictList)

#Arguments:
#   testFile: mystery file's filepath to determine language of
#   langFiles: list of filepaths of the languages to compare testFile to.
#   N: the number of top n-grams for comparison
#Returns the filepath of the language that has the highest number of top 10 matches that are similar to mystery file.
def compareLang(testFile,langFiles,N):
    mystTopNGrams = set([tup[0] for tup in topNCommon(testFile,N)])
    max = 0
    for path in langFiles:
        tempset = set(tup[0] for tup in topNCommon(path,N))
        if(len(mystTopNGrams.intersection(tempset))>max):
            max = len(mystTopNGrams.intersection(tempset))
            langMatch = path
    
    return langMatch




if __name__ == '__main__':
    from os import listdir
    from os.path import isfile, join, splitext
    #Test topNCommon()
    path = join('ngrams','english.txt')
    #print(topNCommon(path,10))
    
    #Compile ngrams across all 6 languages and determine a mystery language
    path='ngrams'
    fileList = [f for f in listdir(path) if isfile(join(path, f))]
    pathList = [join(path, f) for f in fileList if 'mystery' not in f]#conditional excludes mystery.txt
    #print(getAllNGrams(pathList)) #list of all n-grams spanning all languages
    testFile = join(path,'mystery.txt')
    print(compareLang(testFile, pathList, 20)) #determine language of mystery file