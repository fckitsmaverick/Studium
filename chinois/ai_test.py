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

def generate_new_sentence():
    chinese_sentence = '我到哪儿去买飞机票'

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Beijing native, you lived for 28 years in Beijing and got a good education."},
            {
                "role": "user",
                "content": f"I'll provide you a sentence in Chinese you will see that the input i give you is oral sentences mostly using Beijing style of speaking, i want your answer to be a variation of that sentence basically using the same grammar pattern AND THE SAME STYLE but using different vocabulary. Here is the sentence in Chinese: {chinese_sentence}. I want your answer to be only the sentence in Chinese and the translation in English separated by a coma like this 'Sentence 1, Sentence2'. Also when you give me the English translation i don't necessarily want it to be grammatically correct i want that if you give someone the English translation he can guess what word you used in the Chinese sentence, so the words order MUST FOLLOW THE ORDER OF THE CHINESE SENTENCE you can add parenthesis, give hints whatever you want."
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