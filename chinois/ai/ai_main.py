import os
import string

from dotenv import load_dotenv
import openai
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from pydantic import BaseModel
from playsound import playsound

from ai.ai_functions import take_input
from ai.ai_audio_functions import record_audio_manual
from ai.ai_elevenlabs import tts_chinese 
from dict_tools.questions_vocabulaire import dq_vocabulary

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set the API key for OpenAI
openai.api_key = openai_api_key

db_directory = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/ai/'
db_filename = 'speech.mp3'
db_path = os.path.join(db_directory, db_filename)

from openai import OpenAI
client = OpenAI()

console = Console()

class ChineseSentence(BaseModel):
    characters: str
    pinyin: str
    english: str

class ChineseVocabulary(BaseModel):
    characters: str
    pinyin: str
    english: str

class ChineseDictionary(BaseModel):
    dictionary: list[ChineseVocabulary]

class ChineseConversation(BaseModel):
    conversation: list[ChineseSentence]

def how_to_say():
    english_sentence = Prompt.ask("[bold magenta]Enter the sentence you want to say in Chinese: ")
    console.print("[bold magenta]Generating an explanation ...")

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are a Beijing native, you lived for 28 years in Beijing and you had a good education.
            You are dedicated to teach Chinese to Chinese students and you emphasize teaching the local, oral way of talking.
        """},
        {
            "role": "user", 
            "content": f"How would you say: {english_sentence}, in Chinese (using an oral/casual tone) ? And Translate it to chinese pinyin (your chinese pinyin must match the chinese characters). Then break it down and explain the grammatical structure."
        }
        ]
    )

    console.print(f"[bold green]{response.choices[0].message.content}")



def explain_a_sentence():

    chinese_sentence = Prompt.ask("[bold magenta]Enter the Chinese sentence you wish to be explained: ")
    console.print("[bold magenta]Generating an explanation ...")
   
    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are a Beijing native, you lived for 28 years in Beijing and you had a good education.
            You are dedicated to teach Chinese to Chinese students and you emphasize teaching the local, oral way of talking.
        """},
        {
            "role": "user", 
            "content": f"I'll provide you a Chinese sentence and I want you to explain the meaning of the sentence in English, you shall explain the grammatical structure of the sentence but also the vocabulary and the specifity of certain words (if needed to). Here is the sentence in Chinese: {chinese_sentence}."
        }
        ]
    )

    console.print(f"[bold green]{response.choices[0].message.content}")

def chinese_conversation():

    topic = Prompt.ask("[bold magenta]Which topic do you wish to study ?[/bold magenta]")

    console.print(f"[bold green]Generating a conversation about {topic}[/bold green]")

    completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are a Beijing native, you lived for 28 years in Beijing and you had a good education.
            You are dedicated to teach Chinese to Chinese students and you emphasize teaching the local, oral way of talking.
        """},
        {
            "role": "user",
            "content": f"Generate a conversation in Chinese (using an oral/casual tone, and using erhua like if you were from Beijing) on the theme '{topic}'. And Translate it to chinese pinyin (your chinese pinyin must match the chinese characters)."
        }
    ],
    response_format = ChineseConversation
    )

    for i in completion.choices[0].message.parsed.conversation:
        console.print(Panel(f"[bold blue]{i.characters}\n{i.pinyin}\n{i.english}[/bold blue]"))

    #chinese_conversation_listening_quizz(completion.choices[0].message.parsed.conversation)
    
    return completion.choices[0].message.parsed.conversation

def sentence_correction(ans, original_sentence):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
            {"role": "system", "content": "You are a Beijing native, you lived for 28 years in Beijing and got a good academic education. Now you are a Chinese teacher, and your job is to teach foreigners Chinese."},
            {
                "role": "user",
                "content": f"""A student was asked to translate this sentence: {original_sentence.english} into Chinese, here is its answer: {ans}.
                Here is the 10/10 academic answer in Pinyin: {original_sentence.pinyin} and in Chinese characters: {original_sentence.characters}.
                Even if the answer doesn't perfectly match the 10/10 answer you may rate the answer 10, you are a teacher act like one. 
                The student writes pinyin under this form: [word:accent] so for example ni3 is 你, it is the correct and only accepted form.
                Give a grade from 0 to 10. 0 being completely wrong and 10 being the academic answer, then correct its major mistakes. 
                """
            }
        ]
    )

    console.print(Panel(f"[bold blue]{completion.choices[0].message.content}[/bold blue]")) 
    return


def make_chinese_vocab(conversation):
    completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": """You are a Beijing native, you lived for 28 years in Beijing and you had a good education.
            You are dedicated to teach Chinese to Chinese students and you emphasize teaching the local, oral way of talking.
        """},
        {
            "role": "user",
            "content": f"Here is a Chinese Conversation: {conversation}. I want you to make a list of all essential Chinese Vocabulary you need to underestand this conversation"
        }
    ],
    response_format = ChineseDictionary
    ) 
    print(completion.choices[0].message.parsed)

def chinese_personal_audio():
    for key, value in dq_vocabulary.items():
        console.print(Panel(f"[bold blue]{value.english}[bold blue]"))
        record_audio_manual("manual_recording.wav")
        ans = audio_to_text_check()
        print(ans, value.chinese_character)
        if ans.lower() == "exit":
            return
        if ans == value.chinese_character:
            console.print("[bold green]Good Answer ![/bold green]")
        else:
            console.print("[bold red]Wrong Answer ![/bold red]")
    


def chinese_conversation_quizz():
    conversation = chinese_conversation()
    audio, correction = take_input()
    for i in conversation:
        console.print(Panel(f"[bold blue]{i.english}[/bold blue]"))
        if audio == "yes":
            record_audio_manual("manual_recording.wav")
            ans = audio_to_text_check()
            if ans.lower() == "exit": return
            if correction == "yes": sentence_correction(ans, i)
        else:
            ans = Prompt.ask("How would you translate this sentence in Chinese ?")
            console.print(f"[bold green]Here is the original 10/10 answer: {i.pinyin}\n{i.characters}[/bold green]")
            if ans.lower() == "exit": return
            if correction == "yes": sentence_correction(ans, i)
        #sentence_correction(ans, i)
    return

def chinese_conversation_listening_quizz():
    conversation = chinese_conversation()

    for i in conversation:
        characters_to_read = i.characters
        multiple_pass = False 

        to_remove_char = " 。？！：；-， ?!:;-,"
        for char in to_remove_char:
                i.characters = i.characters.replace(char, "")
                
        while True:
            ready = Prompt.ask("[bold magenta]Press enter when you are ready")
            if multiple_pass == False:
                tts_chinese(characters_to_read)
                multiple_pass == True
            ans = Prompt.ask("[bold magenta]Type what you heard (to listen one more time type 'again', to exit type 'exit'): ", default="again")
            
            if ans == "again":
                playsound(db_path)
                continue
            if ans == "exit": return

            if ans == i.characters or ans == i.pinyin:
                console.print("[bold green]Good Answer !")
                break
            elif ans != i.characters and ans != i.pinyin:
                console.print("[bold red]Wrong Answer !")
                console.print(f"[bold red]Correct answer was: {i.pinyin} / {i.characters}")
                break
            else:
                continue

    console.print("[bold magenta]Quizz Finished !")
        


def audio_generation(speech):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1-hd",
        voice="alloy",
        input=f"""{speech}""",
    ) as response:
        response.stream_to_file(db_path)
    playsound(db_path)


def audio_to_text_check():
    audio_file= open("manual_recording.wav", "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    console.print(f"Here is your answer: {transcription.text}")
    return transcription.text

    
if __name__ == "__main__":
    print("What are you trying to do ?")