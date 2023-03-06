from AIWrapper import *
from dictionaryParser import *
from utils import *

RPGElements = [
    "Death", "Life", "Fire", "Water", "Earth", "Air",
    "Nature", "Healing", "Animal", "Magic", "Light", "Dark",
    "Electric", "Toxic", "Tech",
    "Blunt", "Cutting", "Piercing"]

# Convert the rpg elements into a string like "Faith, Death, Fire, Water, Earth, Air, Blunt, Cutting"
RPGElementsInString = ",".join(RPGElements)

# PROMPT
aiPrompt = "The following is a list of words that need to be tagged with the most accurate RPG element that the word can be categorized into."
aiPrompt += "\nPossible RPG elements are: " + RPGElementsInString
aiPrompt += "\nmultiple RPG elements can be assigned to a single word. With a maximum of 3 elements per word."
aiPrompt += "\nevery word must be given an element even if the relation to the word is loose."
aiPrompt += "\n ==  Words == "
aiPrompt += "\nsword"
aiPrompt += "\nmining"
aiPrompt += "\nbaseball"
aiPrompt += "\nbomb"
aiPrompt += "\nskeleton"
aiPrompt += "\njewel"
aiPrompt += "\ndemon"
aiPrompt += "\n == Tagging =="
aiPrompt += "\nsword : Cutting, Piercing"
aiPrompt += "\nmining : Earth, Tech"
aiPrompt += "\nbaseball : Blunt"
aiPrompt += "\nbomb : Fire"
aiPrompt += "\nskeleton : Death, Dark"
aiPrompt += "\njewel : Earth, Nature"
aiPrompt += "\ndemon : Dark, Fire"
aiPrompt += "\n ==  Words == "

# Constants

wordsCollected = []
wordsTagged = 0
amountOfWordsPerPrompt = 25
amountOfWordsToTag = 9999999 # Can lower this for testing
nameOfFileToSave = "taggedWords.txt"


## MAIN ##


# Clear the old file
with open(nameOfFileToSave, "w") as file:
    file.write("")

taggedOutput = ""
allNouns = getNounsFromWordlist()

# go through each word in the words dictionary
for word in allNouns:
    # If we have tagged enough words, stop
    if wordsTagged >= amountOfWordsToTag:
        break

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


