from AIWrapper import *
from dictionaryParser import *
from utils import *

# New chatgpt api
# https://medium.com/geekculture/a-simple-guide-to-chatgpt-api-with-python-c147985ae28

RPGElements = [
    "Death", "Life", "Fire", "Water", "Earth", "Air",
    "Nature", "Health", "Magic", "Light", "Dark",
    "Electric", "Toxic", "Tech",
    "Physical"]

# Convert the rpg elements into a string like "Faith, Death, Fire, Water, Earth, Air, Blunt, Cutting"
RPGElementsInString = ", ".join(RPGElements)

# PROMPT

systemPrompt = """
You are a categorization ai. you will be given a list of words and you will need to categorize 
them into RPG video game elemental attack types. The words should thematically relate to the RPG element assigned.
The purpose is to determine what type of damage a word does in the video game, keep that in mind when tagging.

For example: 
knife : Physical               | because knives are used to cut which is physical damage
mining : Earth, Tech           | because we mine from the earth and use tech to do it
bomb : Fire                    | because bombs are used to explode and cause fire
skeleton : Death, Dark         | because skeletons are dead and evil (dark)
jewel : Earth, Nature          | because jewels are made from the earth and are natural
bear : Nature                  | because bears are animals which are natural.

The ONLY Possible RPG elements are:
""" + RPGElementsInString + """

Every word must be assigned between 1 and 3 elements. Do not add more than 3 RPG elements to a single word. 
Only use the RPG elements listed above, do not add new ones under any circumstances and do not add any other text.
You should only respond with the RPG elements and the original word. Do not add any other text.
Respond in the format: `` word : element1, element2, element3``
"""

# Constants

wordsCollected = []
wordsTagged = 0
amountOfWordsPerPrompt = 30
amountOfWordsToTag = 9999999 # Can lower this for testing
nameOfFileToSave = "taggedWords.txt"
totalSuccessRate = 0
amountOfWordsRequested = 0

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

    # If we have collected X words, ask the AI to tag them
    if len(wordsCollected) >= amountOfWordsPerPrompt:
        # Ask the AI to tag the words
        aiResponse = getCompletionText(systemPrompt, "\n".join(wordsCollected))
        if aiResponse is None or aiResponse == "":
            debug("AI did not respond", DebugLevel.ERROR)
            wordsCollected = []
            continue

        # Print the response
        print(aiResponse)

        # Clear the words collected
        wordsCollected = []
        wordsReturned = 0
        filteredResponse = ""
        amountOfWordsRequested += amountOfWordsPerPrompt

        # Remove any lines that end in ': None'
        for line in aiResponse.split("\n"):
            for element in RPGElements:
                if element == "None":
                    continue

                if element.endswith("None"):
                    continue

                if element == "":
                    continue

                if element in line:
                    filteredResponse += line + "\n"
                    wordsTagged += 1
                    wordsReturned += 1
                    break

        taggedOutput += filteredResponse + "\n"
        debug("Tagged " + str(wordsTagged) + " words", DebugLevel.INFO)

        successRate = wordsReturned / amountOfWordsPerPrompt * 100
        totalSuccessRate = wordsTagged / amountOfWordsRequested * 100
        debug("Success rate: " + str(successRate) + "%", DebugLevel.INFO)
        debug("Total success rate: " + str(totalSuccessRate) + "%", DebugLevel.INFO)

        # If the rate is below 95, debug and error
        if successRate < 95:
            debug("Success rate is below 95% (" + str(wordsReturned) + ")", DebugLevel.ERROR)

        # Save the tagged words to a file
        with open(nameOfFileToSave, "w") as file:
            # Remove empty lines
            for line in taggedOutput.split("\n"):
                if line != "":
                    file.write(line + "\n")

debug("Finished tagging words")
debug("Saved tagged words to " + nameOfFileToSave)


