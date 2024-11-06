import os
from dotenv import load_dotenv
import openai
from rich.console import Console
from rich.panel import Panel

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI
openai.api_key = openai_api_key

from openai import OpenAI
client = OpenAI()

console = Console()

def how_to_say(english_sentence):
    chinese_sentence = '我到哪儿去买飞机票'

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a Beijing native, you lived for 28 years in Beijing and you had a good education.
                You are dedicated to teach Chinese to Chinese students however you emphasize teaching the local, oral way of talking.
                For example when a student ask you 'how to say this sentence in Chinese', you will give him the local, oral Beijing way to say it, not the litterary/school way.
            """},
            {
                "role": "user",
                "contenta z": f"How would you say:{english_sentence} in Chinese ? I want your output to be Sentence in Chinese Pinyin, Sentence in Chinese Characters, Sentence in English"
            }
        ]
    )

    console.print(Panel(f"[bold blue]{completion.choices[0].message}[/bold blue]"))

def explain_a_sentence():
   
    chinese_sentence = '我到哪儿去买飞机票'

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Beijing native, you lived for 28 years in Beijing and got a good academic education."},
            {
                "role": "user",
                "content": f"I'll provide you a Chinese sentence and I want you to explain the meaning of the sentence in English, you shall explain the grammatical structure of the sentence but also the vocabulary and the specifity of certain words (if needed to). Here is the sentence in Chinese: {chinese_sentence}. Format your answer as a list of bullet points."
            }
        ]
    )

    console.print(Panel(f"[bold blue]{completion.choices[0].message}[/bold blue]")) 

if __name__ == "__main__":
    explain_a_sentence()