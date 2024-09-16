import os
from dotenv import load_dotenv
import openai

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI
openai.api_key = openai_api_key

from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)