import os
import openai
from utils import *

engine = "text-davinci-003"
temperature = 0.9
max_tokens = 1000
top_p = 1
frequency_penalty = 0
presence_penalty = 0


# get api key from file "api_key.apikey"
def getAPIKey():
    try:
        with open("api_key.apikey", "r") as file:
            apiKey = file.read()
            return apiKey
    except:
        debug("API key not found", DebugLevel.ERROR)
        exit()


# Initialize the OpenAI API
def initializeAPI():
    openai.api_key = getAPIKey()


def sendPrompt(prompt):


    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )

    return response



def getPromptText(prompt):
    response = sendPrompt(prompt)

    if response is None:
        return None
    else:
        return response.choices[0].text


initializeAPI()
