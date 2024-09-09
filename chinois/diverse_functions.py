from rich_pixels import Pixels
from rich.console import Console
from PIL import Image
from rich.columns import Columns
from rich.table import Table

from database_tools.cedict_database import get_def_pinyin_simplified
from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.hsk_database import get_hsk_level


def print_pokedex(pokedex):

    console = Console()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Name", style="dim", width=12)
    table.add_column("Characteristic")
    table.add_column("Image", justify="center")

    for pokemon in pokedex: 

        with Image.open(pokemon["file_path"]) as image:
            #new_image = image.crop((10, 10, 10, 10))
            resizing = (21, 27, 64, 55)
            new_image = image.crop(resizing)
            pixels = Pixels.from_image(new_image)

            table.add_row(
                pokemon["name"], pokemon["characteristic"], pixels
        )

    console.print(table
    )

def new_vocab_auto():
    while True:
        pinyin_input = input("Pinyin: ")
        simplified_input = input("Simplified: ")

        dict_result = get_def_pinyin_simplified(pinyin_input, simplified_input)
        dict_hsk = get_hsk_level(pinyin_input, simplified_input)
        print(dict_result)
        duplicate = False

        for i in dq_vocabulary:
            if dq_vocabulary[i].chinese_character == dict_result["simplified"] and dq_vocabulary[i].chinese_pinyin == dict_result["pinyin"]:
                print("You already have this word in your personal vocab, quitting...")
                duplicate = True

        if dict_result != False and duplicate == False: 
            simplified = dict_result["simplified"]
            pinyin = dict_result["pinyin"]
            english = dict_result["english"]
            if dict_hsk != False: hsk_level = dict_hsk["hsk_level"] 
            if dict_hsk == False: hsk_level = input("Assign an hsk level (level of difficutly from 1 to 6) to your entry: ")
            with open("dict_tools/questions_vocabulaire.py", "a") as f:
                print(f'dq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level})', file=f)
                print("New entry in your dictionnary")

            keep_going = input("Do you wish to add more vocabulary ?")

            if keep_going.lower() == "no": break
            
        else:
            if duplicate == False: print("No entries found for your input")

def study_personal():
    table = Table(title="[bold blue]Study Table")
    for i in dq_vocabulary:

    