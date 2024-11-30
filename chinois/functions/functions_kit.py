import re
import os
import sys
import random

from rich_pixels import Pixels
from rich.console import Console
from PIL import Image
from rich.columns import Columns
from rich.table import Table
from rich.box import SIMPLE, ROUNDED, SQUARE, HEAVY, DOUBLE, HORIZONTALS, SIMPLE_HEAVY, MINIMAL_DOUBLE_HEAD
from rich.prompt import Prompt
from rich.text import Text
from rich.panel import Panel
from rich.align import Align

from database_tools.cedict_database import get_def_pinyin_simplified
from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.hsk_database import get_hsk_level, get_hsk_dict_def
from database_tools.database import update_word_stats, get_word_stats, get_best_word_ratios, get_worst_word_ratios



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
    console = Console()
    console.show_cursor()

    while True:
        pinyin_input = Prompt.ask("[bold yellow]Pinyin: [/bold yellow]")
        simplified_input = Prompt.ask("[bold yellow]Simplified: [/bold yellow]")
        category = Prompt.ask("[bold yellow]Vocabulary or Sentence ?:[/bold yellow]", default="Vocabulary", choices=["Vocabulary", "Sentence"])
        kind = Prompt.ask("[bold yellow]Type of word:[/bold yellow]", default="general", choices=["general", "verb", "grammar"])

        while pinyin_input == "" and simplified_input == "":
            console.print("[bold red]Both fields are empty, please enter a pinyin and a simplified character[/bold red]")

            finished = Prompt.ask("[bold yellow]Do you want to quit ?[/bold yellow]", default="yes", choices=["yes", "no"])
            if finished == "yes": return

            pinyin_input = Prompt.ask("[bold yellow]Pinyin: [/bold yellow]")
            simplified_input = Prompt.ask("[bold yellow]Simplified: [/bold yellow]")

        dict_result = get_def_pinyin_simplified(pinyin_input, simplified_input)
        hsk_dict_result = get_hsk_dict_def(pinyin_input, simplified_input)
        dict_hsk = get_hsk_level(pinyin_input, simplified_input)

        add_topic = Prompt.ask("[bold yellow]Do you want to add a topic ?[/bold yellow]", default="no", choices=["yes", "no"])

        duplicate = False
        #If cedict doesn't have the entries but hsk does use hsk
        if dict_result == False and hsk_dict_result != False:
             dict_result = hsk_dict_result
        

        if dict_result != False:
            for i in dq_vocabulary:
                if dq_vocabulary[i].chinese_character == dict_result["simplified"] and dq_vocabulary[i].chinese_pinyin == dict_result["pinyin"]:
                    console.print("[bold yellow]You already have this word in your personal vocab[/bold yellow]")
                    keep_going = Prompt.ask("[bold yellow]Do you still wish to add it to your dictionnary ?[/bold yellow]", default="no", choices=["yes", "no"])
                    if keep_going == "no": 
                        duplicate = True

        if dict_result != False and duplicate == False: 
            simplified = dict_result["simplified"]
            pinyin = dict_result["pinyin"]
            english = dict_result["english"]

            if dict_hsk != False: hsk_level = dict_hsk["hsk_level"] 
            elif dict_hsk == False: hsk_level = Prompt.ask("[bold yellow]Assign an hsk level (level of difficutly from 1 to 6) to your entry: [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])

            want_to_change = Prompt.ask(f"[bold yellow]Here is the English definition from the dictionnary [bold blue]{english}[/bold blue].\nDo you want to change it ?[/bold yellow]", default="no", choices=["yes", "no"])
            if want_to_change == "yes": 
                english = Prompt.ask("[bold yellow]Enter the new definition: [/bold yellow]")

            if add_topic == "yes":
                topic_pick = Prompt.ask("[bold yellow]Enter the topic (you can add more than one by using ', ' separator): [/bold yellow]")
                topic_pick = topic_pick.split(", ")
            
            
            confirm = Prompt.ask(f"[bold yellow]Do you want to add this \n[bold magenta]Chinese Pinyin: {pinyin_input}\nChinese characters: {simplified_input}\nEnglish definition: {english}[/bold magenta]\nto you personal dictionnary?[/bold yellow]", default="yes", choices=["yes", "no"])
            
            if confirm == "yes":
                with open("dict_tools/questions_vocabulaire.py", "a") as f:
                    print(f'\ndq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level}, category="{category}", kind="{kind}", topic={topic_pick if add_topic == "yes" else []})', file=f)
                    console.print("[bold green]New entry in your dictionnary[/bold green]")
                    f.close()
            else:
                break


        elif dict_result == False:
            console.print("[bold red]Could not find this word in the dictionnary.[/bold red]")
            manual_input = Prompt.ask("[bold yellow]Do you want to manually input the definition ?[/bold yellow]", default="yes", choices=["yes", "no"])

            if manual_input == "yes":

                english = Prompt.ask("[bold yellow]Enter the English definition: [/bold yellow]")
                if add_topic == "yes":
                    topic_pick = Prompt.ask("[bold yellow]Enter the topic (you can add more than one by using ', ' separator): [/bold yellow]")
                    topic_pick = topic_pick.split(", ")

                if dict_hsk != False:
                    hsk_level = dict_hsk["hsk_level"] 
                elif dict_hsk == False:
                    hsk_level = Prompt.ask("[bold yellow]Assign an hsk level (level of difficutly from 1 to 6) to your entry: [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])


                confirm = Prompt.ask(f"[bold yellow]Do you want to add this \n[bold magenta]Chinese Pinyin: {pinyin_input}\nChinese characters: {simplified_input}\nEnglish definition: {english}[/bold magenta]\nto you personal dictionnary?[/bold yellow]", default="yes", choices=["yes", "no"])
            
                if confirm == "yes":
                    with open("dict_tools/questions_vocabulaire.py", "a") as f:
                        print(f'\ndq_vocabulary["{simplified_input}"] = Vocabulary("{pinyin_input}", "{simplified_input}", "{english}", {hsk_level}, category="{category}", kind="{kind}", topic= {topic_pick if add_topic == "yes" else []})', file=f)
                        console.print("[bold green]New entry in your dictionnary[/bold green]")
                        f.close()
                else:
                    return


        keep_going = Prompt.ask("[bold red]Do you wish to add more vocabulary ?[/bold red]", default="yes", choices=["yes", "no"])

        if keep_going.lower() == "no":
            # Make it restart so that the words added to the dictionnary are taken into account
            console.print("[bold red]Now restarting ... [/bold red]")
            os.execl(sys.executable, sys.executable, *sys.argv)


            


def delete_specific_word_line():
    console = Console()
    console.show_cursor()
    file_path = 'dict_tools/questions_vocabulaire.py'  # Replace with the actual file path
    exact_key = Prompt.ask("[bold yellow]Enter the exact word you want to delete (in Chinese Character): [/bold yellow]") 
    # Define a regex pattern to match the exact dictionary key line
    pattern = rf'^dq_vocabulary\["{re.escape(exact_key)}"\]'  # Matches lines starting with dq_vocabulary["学"]

    # Read all lines from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Write back only the lines that do not match the specific pattern
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            # If the line does not match the exact pattern, write it back
            if not re.match(pattern, line.strip()):  # Match and strip leading/trailing spaces
                file.write(line)
    
    console.print("[bold green]Word successfully deleted from your personal vocabulary ![/bold green]")
    console.print("[bold red]Now restarting ... [/bold red]")
    os.execl(sys.executable, sys.executable, *sys.argv)




def update_word_personal_vocab():
    console = Console()
    console.show_cursor()

    file_path = 'dict_tools/questions_vocabulaire.py'
    exact_key = Prompt.ask("[bold yellow]Enter the exact word you want to modify (in Chinese Character): [/bold yellow]")
    
    if exact_key not in dq_vocabulary:
        console.print("[bold red]Error: Cannot find the word in your personal vocabulary[/bold red]")
        return
    
    try:
        # Pattern to match the exact dictionary line
        pattern = rf'^dq_vocabulary\["{re.escape(exact_key)}"\]'
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        modified_lines = []

        update_choice = Prompt.ask(
            "[bold yellow]Which argument would you like to update? Enter 1 for Chinese Character, 2 for Chinese Pinyin, 3 for English: [/bold yellow]",
            choices=["1", "2", "3"]
        )

        current_value_map = {
            "1": dq_vocabulary[exact_key].chinese_character,
            "2": dq_vocabulary[exact_key].chinese_pinyin,
            "3": dq_vocabulary[exact_key].english
        }
        console.print(f"[bold yellow]Current value: {current_value_map[update_choice]}[/bold yellow]")

        # Updated regex patterns with improved matching
        argument_map = {
            "1": (r'(dq_vocabulary\[".*?"\] = Vocabulary\()"(.*?)"(,)', r'\1"{new_value}"\3'),
            "2": (r'(dq_vocabulary\[".*?"\] = Vocabulary\(".*?", )"(.*?)"(,)', r'\1"{new_value}"\3'),
            "3": (r'(dq_vocabulary\[".*?"\] = Vocabulary\(".*?", ".*?", )"(.*?)"(,)', r'\1"{new_value}"\3')
        }

        # Get the regex pattern and replacement format
        regex_pattern, replacement_format = argument_map[update_choice]

        # Prompt the user for the new value of the selected argument
        new_value = Prompt.ask(f"[bold yellow]Enter the new value for the selected argument: [/bold yellow]")

        # Iterate through lines to find and modify the target line
        for line in lines:
            if re.match(pattern, line.strip()):
                # Replace the selected argument with the new value
                modified_line = re.sub(regex_pattern, replacement_format.format(new_value=new_value), line)
                if modified_line != line:  # Only print if the line has changed
                    console.print(f"[bold green]Updating line: {line.strip()} to {modified_line.strip()}[/bold green]")
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)

        # Write all lines back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(modified_lines)
            console.print("[bold green]Word successfully updated in your personal vocabulary![/bold green]")
            console.print("[bold red]Now restarting ... [/bold red]")
            os.execl(sys.executable, sys.executable, *sys.argv)

    except Exception as e:
        console.print(f"[bold red]Error: Cannot update, try again. Details: {str(e)}[/bold red]")


def update_vocab_dictionnary(d_voc, sentence_included=False, kind_of_word=False, difficulty_set=False, kind="general", difficulty_limit="1"):
    d_voc_copy = d_voc
    if sentence_included == False:
        d_voc_copy = {key: value for key, value in d_voc_copy.items() if value.category != "Sentence"}
    if kind_of_word != False:
        d_voc_copy = {key: value for key, value in d_voc_copy.items() if value.kind == kind}
    if difficulty_set != False:
        d_voc_copy = {key: value for key, value in d_voc_copy.items() if value.difficulty == int(difficulty_limit)}
    return(d_voc_copy)

def reset_vocab_dictionnary(d_voc):
    for key, value in d_voc.items():
        value.done = 0


def assign_true_false(curr, bool_value):
    if bool_value == "yes":
        curr = True
    elif bool_value == "no":
        curr = False
    return curr


def study_personal():
    console = Console()
    console.show_cursor()
    table = Table(title="[bold blue]Study Table", box=DOUBLE, show_lines=True, row_styles=["bright_blue", "yellow", "bright_green"])
    sentence_study = Prompt.ask("[bold yellow]Do you want to study sentences ?[/bold yellow]", default="no", choices=["yes", "no"])
    difficulty_set = Prompt.ask("[bold yellow]Do you want to set a difficulty limit ?[/bold yellow]", default="no", choices=["yes", "no"])
    difficulty_limit = Prompt.ask("[bold yellow]Enter the difficulty limit (1 to 6): [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])
    sentence_study = assign_true_false(sentence_study, sentence_study)
    difficulty_set = assign_true_false(difficulty_set, difficulty_set)

    table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
    table.add_column("Pinyin", justify="center", style="bright_blue")
    table.add_column("English", justify="center", style="bright_blue")

    if difficulty_set == True:
        for i in dq_vocabulary:
            if dq_vocabulary[i].difficulty == int(difficulty_limit):
                if sentence_study == False:
                    if dq_vocabulary[i].category != "Sentence":
                        table.add_row(dq_vocabulary[i].chinese_character, dq_vocabulary[i].chinese_pinyin, dq_vocabulary[i].english)
                elif sentence_study == True:
                    table.add_row(dq_vocabulary[i].chinese_character, dq_vocabulary[i].chinese_pinyin, dq_vocabulary[i].english)
        return

    else:
        for i in dq_vocabulary:
            table.add_row(dq_vocabulary[i].chinese_character, dq_vocabulary[i].chinese_pinyin, dq_vocabulary[i].english, end_section=True) 
        
    console.print(table)



def take_user_preferences():
    difficulty_limit = "1"
    kind="general"

    user_limit = Prompt.ask("[bold yellow]Number of words you want to study:[/bold yellow]", default="10")

    sentence_included = Prompt.ask("[bold yellow]Do you want to include sentences?[/bold yellow]", choices=["yes", "no"], default="no")
    sentence_included = assign_true_false(sentence_included, sentence_included)

    kind_of_word = Prompt.ask("[bold yellow]Do you want to study a specific kind of word?[/bold yellow]", choices=["yes", "no"], default="no")
    kind_of_word = assign_true_false(kind_of_word, kind_of_word)
    if kind_of_word == True:
        kind = Prompt.ask("[bold yellow]Enter the kind of word you want to study: [/bold yellow]", choices=["general", "verb", "grammar"], default="general")

    difficulty_set = Prompt.ask("[bold yellow]Do you want to set a difficulty limit?[/bold yellow]", choices=["yes", "no"], default="no")
    difficulty_set = assign_true_false(difficulty_set, difficulty_set)
    if difficulty_set == True:
         difficulty_limit = Prompt.ask("[bold yellow]Enter the difficulty limit (1 to 6): [/bold yellow]", choices=["1", "2", "3", "4", "5"], default="1")

    return int(user_limit), sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit

def display_bad_ans(curr_d):
        console = Console()
        console.show_cursor()

        table = Table(title="[bold red]Summary of Bad Answers[/bold red]")
        table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
        table.add_column("Pinyin", justify="center", style="bright_blue")
        table.add_column("English", justify="center", style="bright_blue")

        for key in curr_d:
            table.add_row(f"{curr_d[key].chinese_character}", f"{curr_d[key].chinese_pinyin}", f"{curr_d[key].english}")
        
        console.print(table)

def compare_ans(user_ans, correct_ans):
    console = Console()
    compared_str = Text()
    corrected_str = Text()

    # Compare each character of both strings
    for i, char in enumerate(user_ans):
        if i < len(correct_ans):
            if char == correct_ans[i]:
                compared_str.append(char, style="bold green")  # Correct character
                corrected_str.append(char, style="bold green")  # Correct character
            else:
                compared_str.append(char, style="bold underline red")    # Incorrect character
                corrected_str.append(correct_ans[i], style="bold underline green")
        else:
            compared_str.append(char, style="bold underline red")        # Extra character in user_ans

    # If correct_ans is longer than user_ans, highlight the extra characters in correct_ans
    if len(correct_ans) > len(user_ans):
        compared_str.append(f" (Missing: {correct_ans[len(user_ans):]})", style="bold underline yellow")
        corrected_str.append(f" Missing: {correct_ans[len(user_ans):]}", style="bold underline yellow")

    # Create panels for the user's answer and the correct answer
    user_ans_panel = Panel(
        Align.center(compared_str), 
        title="[bold red]Your Answer[/bold red]", 
        border_style="red", 
        expand=False
    )

    correct_ans_panel = Panel(
        Align.center(corrected_str), 
        title="[bold green]Correct Answer[/bold green]", 
        border_style="green", 
        expand=False
    )

    # Print the panels side by side
    console.print(user_ans_panel)
    console.print(correct_ans_panel)

    return compared_str, corrected_str

def redo_bad_ans(bad_ans_d):
    console = Console()
    console.show_cursor()
    redo = Prompt.ask("[bold magenta]Do you want redo the questions you got wrong?[/bold magenta]", choices=["yes", "no"], default="no")

    if redo == "yes":
        for key, value in bad_ans_d.items():
            console.print(Panel(f"[bold blue]{value.english}[/bold blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin or character): [/bold yellow]")

            if ans == value.chinese_character or ans == value.chinese_pinyin:
                console.print("[bold green]Correct![/bold green]")
            else:
                console.print("[bold red]Wrong Answer![/bold red]")
                #Check if user typed pinyin or chinese character
                #Then compare the answer and output the hightlighted error(s)
                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, value.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, value.chinese_character)

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {value.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("Your Answer", justify="center", style="bright_blue")

                table.add_row(f"{value.chinese_character}", f"{value.chinese_pinyin}", f"{value.english}")
                console.print(table)

                update_word_stats(key, False)
    else:
        return

def add_english_vocab():
    console = Console()
    console.show_cursor()

    while True:
        english_word = Prompt.ask("[bold yellow]Enter the English word: [/bold yellow]")
        english_def = Prompt.ask("[bold yellow]Enter the English definition: [/bold yellow]")
        french_equivalent = Prompt.ask("[bold yellow]Enter the French equivalent: [/bold yellow]")
        difficulty = Prompt.ask("[bold yellow]Enter the difficulty level (1 to 6): [/bold yellow]", default="1", choices=["1", "2", "3", "4", "5", "6"])
        category = Prompt.ask("[bold yellow]Enter the category: [/bold yellow]", default="Vocabulary")
        topic = Prompt.ask("[bold yellow]Enter the topic: [/bold yellow]", default="")

        with open("dict_tools/english_vocab.py", "a") as f:
            print(f'\nd_english["{english_word}"] = EnglishVocabulary("{english_word}", "{english_def}", {difficulty}, "{category}", "{topic}", french_equivalent="{french_equivalent}")', file=f)
            console.print("[bold green]New entry in your dictionnary[/bold green]")
            f.close()

        keep_going = Prompt.ask("[bold red]Do you wish to add more vocabulary ?[/bold red]", default="yes", choices=["yes", "no"])

        if keep_going.lower() == "no": return

def pick_questions(updated_d, user_limit=10):
    console = Console()
    if user_limit > (len(updated_d)):
        console.print("[bold red]Fail, your limit is longer than the size of your dictionnary [/bold red]")
        return None

    final_d = {}
    for i in range(0, user_limit):

        pick = random.choice(list(updated_d.values()))
        while pick.done == 1:
            pick = random.choice(list(updated_d.values()))

        if pick.done == 0:
            pick.done = 1
            final_d[i] = pick
    return final_d

    
def handle_tone_sandhi(answer):

    string_list = answer.split()

    for word in string_list:
        print(word)
        if word == "":
            return
    
