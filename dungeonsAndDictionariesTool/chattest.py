import openai
from AIWrapper import *

completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": """
        You are a categorization ai. you will be given a list of words and you will need to categorize 
        them into RPG video game elemental attack types. The words should thematically relate to the RPG element assigned.
        The purpose is to determine what type of damage a word does in the video game, keep that in mind when tagging.
        
        For example: 
        knife : Cutting                | because knives are used to cut.
        mining : Earth, Tech           | because we mine from the earth and use tech to do it
        bomb : Fire                    | because bombs are used to explode and cause fire
        skeleton : Death, Dark         | because skeletons are dead and evil (dark)
        jewel : Earth, Nature          | because jewels are made from the earth and are natural
        
        The ONLY Possible RPG elements are: Death, Life, Fire, Water, Earth, Air, Nature, Healing, Animal, Magic, Light, Dark,
        Electric, Toxic, Tech, Blunt, Cutting, Piercing
        
        A word can be assigned between 1 and 3 elements. Do not add more than 3 RPG elements to a single word. 
        Only use the RPG elements listed above, do not add new ones under any circumstances.
        Respond in the format: `` word : element1, element2, element3 (explanation)``
        """}, # Any word that does not have a relation to an RPG element can be given the tag "None", however this should be used rarely

        {"role": "user", "content": "Apple, Bear, Charlie, Dog, Elephant, Fish, Goat, Horse, Ice, Jelly, Kite, Lion, Monkey, Nuts, Orange, Pig, Queen, Rabbit, Snake, Tiger, Umbrella, Vase, Whale, Xylophone, Yarn, Zebra, aaron, billy, charlie, daniel, edward, frank, george, harry, ian, jacob, kyle, luke, mason, nathan, oliver, peter, quinn, ryan, sam, tom, ursula, victor, william, xavier, yvonne, zachary"},
    ],
    api_key=getAPIKey(),
    temperature=0.3,
)

print(completion.choices[0].message.content)