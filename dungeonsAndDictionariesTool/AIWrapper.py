import os
import openai
from utils import *

engine = "gpt-3.5-turbo"
temperature = 0.3
max_tokens = 1000
top_p = 1
frequency_penalty = 0
presence_penalty = 0

totalTokensUsed = 0
costPer1kTokens = 0.002


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

def getCompletionText(sysPrompt, usrPrompt):
    debug("Sending completion request ...", DebugLevel.INFO)
    try:
        completion = openai.ChatCompletion.create(
            model=engine,
            messages=[
                {"role": "user", "content": sysPrompt},
                {"role": "user", "content": usrPrompt}
            ],
            api_key=getAPIKey(),
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        global totalTokensUsed
        tokensUsed = completion.usage.total_tokens
        totalTokensUsed += tokensUsed
        totalCost = (totalTokensUsed/1000) * costPer1kTokens
        debug("Tokens to complete: " + str(tokensUsed) + " [" + str(totalTokensUsed) + " total tokens] [$" + str(totalCost) + "]", DebugLevel.INFO)

        return completion.choices[0].message.content
    except:
        debug("Error getting completion text", DebugLevel.ERROR)
        return ""

initializeAPI()
