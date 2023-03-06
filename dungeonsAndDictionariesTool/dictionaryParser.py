# The dictionary is sorted into 26 dictionaries, one for each letter of the alphabet
# Each dictionary contains a list of words that start with that letter and their definitions.
# Each definition is broken up by a semicolon
# The dictionary is stored in a json file

import json
from utils import *
import spacy
from nltk.corpus import wordnet as wn

dictionary_file = "dictionary.json"
all_words_file = "words_dictionary.json"

dictionary = {}
allWords = {}
nlp = None

def isWordNoun(word):
    try:

        doc = nlp(word)
        if (doc[0].tag_ == 'NNP'):
            return True
        else:
            return False
    except:
        return False


def getDictionary():
    try:
        with open(dictionary_file, "r") as file:
            dictionary = json.load(file)
            return dictionary
    except:
        debug("Dictionary not found", DebugLevel.ERROR)
        exit()


def getWordList():
    # Get all the words out of the dictionary and put them in a array
    words = []
    for letter in dictionary:
        for word in letter:
            words.append(word)

    debug("Loaded " + str(len(words)) + " words")
    return words


def getDefinitation(word):
    try:
        # print(dictionary)
        firstLetterIndex = ord(word[0].lower()) - 97
        return dictionary[firstLetterIndex][word]
    except:
        return None

def getNounsFromWordlist():
    debug("Loading nouns from wordlist ... ")
    allNouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    debug("Loaded " + str(len(allNouns)) + " nouns")

    filteredNouns = []

    # Remove any words with '_' or " " in them
    for word in allNouns:
        if not ("_" in word or " " in word):
            filteredNouns.append(word)

    debug("Removed " + str(len(allNouns) - len(filteredNouns)) + " nouns. " + str(len(filteredNouns)) + " nouns left")
    return filteredNouns




def initilizeDictionary():
    global dictionary
    global allWords
    global nlp

    debug("Loading word processor ... ")
    dictionary = getDictionary()
    allWords = getWordList()
    nlp = spacy.load("en_core_web_sm")
    debug("Word processor loaded")


initilizeDictionary()
