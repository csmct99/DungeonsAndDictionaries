from AIWrapper import *
from dictionaryParser import *
from utils import *

RPGElements = [
    "Death", "Life", "Fire", "Water", "Earth", "Air",
    "Nature",
    "Electric", "Toxic",
    "Evil", "Good",
    "Blunt", "Cutting", "Piercing",
    "None"]

# Convert the rpg elements into a string like "Faith, Death, Fire, Water, Earth, Air, Blunt, Cutting"
RPGElementsInString = ",".join(RPGElements)

aiPrompt = "The following is a list of words that need to be tagged with the most accurate RPG element that the word can be categorized into."
aiPrompt += "\nPossible RPG elements are: " + RPGElementsInString
aiPrompt += "\nOnly one RPG element can be assigned to each word. Do not assign multiple RPG elements to a single word."
aiPrompt += "\nif a word cannot be categorized into any of the RPG elements, assign it the RPG element 'None'"
aiPrompt += "\n ==  Words == "
aiPrompt += "\nsword"
aiPrompt += "\nfire"
aiPrompt += "\nbaseball"
aiPrompt += "\nbomb"
aiPrompt += "\nskeleton"
aiPrompt += "\naaa"
aiPrompt += "\n == Tagging =="
aiPrompt += "\n"
aiPrompt += "\nsword : Cutting"
aiPrompt += "\ncryo : Water"
aiPrompt += "\nbaseball : Blunt"
aiPrompt += "\nbomb : Fire"
aiPrompt += "\nskeleton : Death"
aiPrompt += "\naaa : None"
aiPrompt += "\n ==  Words == "

# Constants

wordsCollected = []
wordsTagged = 0
amountOfWordsPerPrompt = 20
amountOfWordsToTag = 4
nameOfFileToSave = "taggedWords.txt"


## MAIN ##

taggedOutput = ""

# go through each word in the words dictionary
for word in allWords:
    # If we have tagged enough words, stop
    if wordsTagged >= amountOfWordsToTag:
        break

    # Check if the word is a noun
    if not isWordNoun(word):
        continue

    # Check if the word is in the dictionary
    if getDefinitation(word) is None:
        continue

    # Add the word to the list of words collected
    wordsCollected.append(word)

    aiResponse = ""

    # If we have collected 20 words, ask the AI to tag them
    if len(wordsCollected) >= amountOfWordsPerPrompt:
        # Ask the AI to tag the words
        aiResponse = getPromptText(aiPrompt + "\n\n" + "\n".join(wordsCollected) + "\n== Tagging ==\n")

        if aiResponse is None:
            debug("AI did not respond", DebugLevel.ERROR)
            wordsCollected = []
            continue

        # Print the response
        print(aiResponse)

        # Clear the words collected
        wordsCollected = []
        filteredResponse = ""

        # Remove any lines that end in ': None'
        for line in aiResponse.split("\n"):
            for element in RPGElements:
                if element == "None":
                    continue

                if element in line:
                    filteredResponse += line + "\n"
                    wordsTagged += 1
                    break

        taggedOutput += filteredResponse + "\n"
        debug("Tagged " + str(wordsTagged) + " words")

        # Save the tagged words to a file
        with open(nameOfFileToSave, "w") as file:
            # Remove empty lines
            for line in taggedOutput.split("\n"):
                if line != "":
                    file.write(line + "\n")

debug("Finished tagging words")
debug("Saved tagged words to " + nameOfFileToSave)





