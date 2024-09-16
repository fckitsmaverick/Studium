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
from database_tools.database import update_word_stats


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

            finished = Prompt.ask("[bold yellow]Do you want to quit ?[/bold yellow]", default="no", choices=["yes", "no"])
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
                topic_pick = Prompt.ask("[bold yellow]Enter the topic: [/bold yellow]")

            with open("dict_tools/questions_vocabulaire.py", "a") as f:
                print(f'\ndq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level}, category="{category}", kind="{kind}", topic="{topic_pick if add_topic == "yes" else ""}")', file=f)
                console.print("[bold green]New entry in your dictionnary[/bold green]")
                f.close()


        elif dict_result == False:
            console.print("[bold red]Could not find this word in the dictionnary.[/bold red]")
            manual_input = Prompt.ask("[bold yellow]Do you want to manually input the definition ?[/bold yellow]", default="yes", choices=["yes", "no"])

            if manual_input == "yes":

                english = Prompt.ask("[bold yellow]Enter the English definition: [/bold yellow]")
                if add_topic == "yes":
                    topic_pick = Prompt.ask("[bold yellow]Enter the topic: [/bold yellow]")

                if dict_hsk != False:
                    hsk_level = dict_hsk["hsk_level"] 
                elif dict_hsk == False:
                    hsk_level = Prompt.ask("[bold yellow]Assign an hsk level (level of difficutly from 1 to 6) to your entry: [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])




                with open("dict_tools/questions_vocabulaire.py", "a") as f:
                    print(f'\ndq_vocabulary["{simplified_input}"] = Vocabulary("{pinyin_input}", "{simplified_input}", "{english}", {hsk_level}, category="{category}", kind="{kind}", topic="{topic_pick if add_topic == "yes" else ""}")', file=f)
                    console.print("[bold green]New entry in your dictionnary[/bold green]")
                    f.close()


        keep_going = Prompt.ask("[bold red]Do you wish to add more vocabulary ?[/bold red]", default="yes", choices=["yes", "no"])

        if keep_going.lower() == "no": return
            



def study_personal():
    console = Console()
    console.show_cursor()
    table = Table(title="[bold blue]Study Table", box=DOUBLE, show_lines=True, row_styles=["bright_blue", "yellow", "bright_green"])
    sentence_study = Prompt.ask("[bold yellow]Do you want to study sentences ?[/bold yellow]", default="no", choices=["yes", "no"])
    difficulty_set = Prompt.ask("[bold yellow]Do you want to set a difficulty limit ?[/bold yellow]", default="no", choices=["yes", "no"])
    difficulty_limit = Prompt.ask("[bold yellow]Enter the difficulty limit (1 to 6): [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])

    # Modify dq_vocabulary without reassigning
    if sentence_study == "yes":
        dq_vocabulary_copy = {key: value for key, value in dq_vocabulary.items() if value.category == "Sentence"}
        dq_vocabulary.clear()
        dq_vocabulary.update(dq_vocabulary_copy)

    if difficulty_set.lower() == "yes":
        dq_vocabulary_copy = {key: value for key, value in dq_vocabulary.items() if value.difficulty == int(difficulty_limit)}
        dq_vocabulary.clear()
        dq_vocabulary.update(dq_vocabulary_copy)

    table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
    table.add_column("Pinyin", justify="center", style="bright_blue")
    table.add_column("English", justify="center", style="bright_blue")

    for i in dq_vocabulary:
        table.add_row(dq_vocabulary[i].chinese_character, dq_vocabulary[i].chinese_pinyin, dq_vocabulary[i].english, end_section=True) 
    
    console.print(table)

def update_vocab_dictionnary(d_voc, sentence_included=False, kind_of_word=False, difficulty_set=False, kind="general", difficulty_limit="1"):
    d_voc_copy = d_voc
    if sentence_included == False:
        d_voc_copy = {key: value for key, value in d_voc_copy.items() if value.category != "Sentence"}
    if kind_of_word != False:
        d_voc_copy = {key: value for key, value in d_voc_copy.items() if value.kind == kind}
    if difficulty_set != False:
        d_voc_copy = {key: value for key, value in d_voc_copy.items() if value.difficulty == int(difficulty_limit)}
    return(d_voc_copy)


def assign_true_false(curr, bool_value):
    if bool_value == "yes":
        curr = True
    elif bool_value == "no":
        curr = False
    return curr


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


if __name__ == "__main__":
    update_vocab_dictionnary(dq_vocabulary, sentence_included=True, kind_of_word=True, difficulty_set=False, kind="general", difficulty_limit="1")