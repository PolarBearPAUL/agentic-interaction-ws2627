import os
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

# API-Key aus der .en v-Datei laden
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# create is a method to create a new chat completion using the Groq client
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful travel planning assistant."
        },
        {
            "role": "user",
            "content": "Plan my trip to Stuttgart."
        }
    ],
    model="openai/gpt-oss-20b"
)

print(chat_completion.choices[0].message.content)


# Read command line arguments for the user input
# start the script with: python agent/__main__.py "Plan my trip to Stuttgart."
# start process 