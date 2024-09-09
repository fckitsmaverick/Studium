from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.database import update_score_progress, update_word_stats, get_word_stats, get_worst_word_ratios
from database_tools.cedict_database import get_def, get_def_pinyin_simplified
from database_tools.hsk_database import get_hsk_by_level

from datetime import datetime
from termcolor import cprint
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import track

import random
import time
import pandas as pd


score_player_1 = 0
limitation = 10001


progress = {

}

start = time.time()
count = 0

#ce_dict = create_dict()
#print(ce_dict[0])

#Englisht to Chinese quizz 2 inputs pinyin and chinese character
def ec_quizz(inp, count, limitation):
    score_player_1 = 0

    if inp == "ec":

        for i in dq_vocabulary:
                question_pick = random.choice(list(dq_vocabulary.values()))

                #Pick random new question 
                while question_pick.done == 1:
                    question_pick = random.choice(list(dq_vocabulary.values()))

                if question_pick.done == 0:
                    cprint(question_pick.english, "light_cyan")
                    ans = input() 
                    ans2 = input()

                    if (ans == question_pick.chinese_character and ans2 == question_pick.chinese_pinyin) \
                    or (ans == question_pick.chinese_pinyin and ans2 == question_pick.chinese_character):
                        cprint("Good Answer", "green")
                        score_player_1 += question_pick.difficulty
                        update_word_stats(question_pick.chinese_character, True)

                    else:
                        cprint("Bad Answer", "red")
                        print(question_pick.chinese_character, " ", question_pick.chinese_pinyin)
                        update_word_stats(question_pick.chinese_character, False)

                    question_pick.done = 1
                    count+=1
                    progress.update(task_ecpinyin, advance=1)

                if count >= int(limitation):
                    break

        print(score_player_1)
        #Update Database
        update_score_progress(score_player_1, time.time() - start, inp)



#This quizz is the basis for the others
#English to Chinese quizz only one input required to validate the answer (pinyin)
def ecpinyin_quizz(inp):
    # Start rich console
    console = Console()
    console.show_cursor()

    score_player_1 = 0
    count = 0
    bad_ans = {}

    for i in dq_vocabulary:
        question_pick = random.choice(list(dq_vocabulary.values()))

        # Skip already answered questions
        while question_pick.done == 1:
            question_pick = random.choice(list(dq_vocabulary.values()))

        if question_pick.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold bright_blue]{question_pick.english}[/bold bright_blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

            if ans == question_pick.chinese_pinyin:
                console.print("[bold bright_green]Good Answer![/bold bright_green]")
                score_player_1 += question_pick.difficulty
                update_word_stats(question_pick.chinese_character, True)
            else:
                console.print("[bold bright_red]Bad Answer![/bold bright_red]")

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {question_pick.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

                bad_ans[i] = question_pick
                update_word_stats(question_pick.chinese_character, False)

            question_pick.done = 1
            count += 1
            console.rule("[bold red]")

    # Display a summary of bad answers
    if bad_ans:
        table = Table(title="[bold red]Summary of Bad Answers[/bold red]")
        table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
        table.add_column("Pinyin", justify="center", style="bright_blue")
        table.add_column("English", justify="center", style="bright_blue")

        for i in bad_ans:
            table.add_row(f"{bad_ans[i].chinese_character}", f"{bad_ans[i].chinese_pinyin}", f"{bad_ans[i].english}")
        
        console.print(table)

    # Display final score
    score_player_1 = round(score_player_1 * 0.75)
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))

    update_score_progress(score_player_1, time.time() - start, inp)


def last_x_quizz(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    # Take user input for number of entries and whether to update ratio
    x = Prompt.ask("[bold yellow]Enter how many last entries you want to quiz on (type x)[/bold yellow]", default="5")
    update_ratio = Prompt.ask("[bold yellow]Do you want to update the success ratio?[/bold yellow]", choices=["yes", "no"], default="no")
    x = int(x)
    score_player_1 = 0
    total_questions = len(dq_vocabulary) - (len(dq_vocabulary) - x)

    # Loop over the last x entries and ask questions
    for key, value in dq_vocabulary.items():
        # Iterate until the entry we want
        if len(dq_vocabulary) - count <= (x - 1):
            question_pick = value
            
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold cyan]{question_pick.english}[/bold cyan]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]") 
            result = False

            if ans == question_pick.chinese_pinyin:
                console.print("[bold green]Correct![/bold green]", style="bold green")
                score_player_1 += question_pick.difficulty
                result = True
            else:
                console.print("[bold bright_red]Incorrect![/bold bright_red]", style="bold red")
                
                # Display correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {question_pick.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

            # Update the ratio if the user opted to
            if update_ratio.lower() == "yes": 
                update_word_stats(key, result)

            count += 1
        else:
            count += 1

    # Calculate final score
    score_player_1 = round(score_player_1 * 0.75)

    # Display final score in a panel
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))

    update_score_progress(score_player_1, time.time() - start, inp)




def worst_x_quizz(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    # Take user input for number of worst words to quiz on
    user_limit = Prompt.ask("[bold yellow]Worst x words (type x)[/bold yellow]", default="10")
    user_limit = int(user_limit)
    score_player_1 = 0
    worst10 = get_worst_word_ratios(user_limit)

    # Loop through vocabulary to ask questions about the worst words
    for key, value in dq_vocabulary.items():
        for word in worst10:
            if word["word"] == value.chinese_character:
                # Ask the question (displaying the English meaning)
                console.print(Panel(f"[bold magenta]{value.english}[/bold magenta]", title="Question", expand=False))
                ans = console.input("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

                if ans == value.chinese_pinyin:
                    console.print("[bold green]Correct![/bold green]")
                    score_player_1 += value.difficulty
                    update_word_stats(key, True)
                else:
                    console.print("[bold bright_red]Incorrect![/bold bright_red]", style="bold red")
                    
                    # Display correct answer in a table
                    table = Table(title=f"[bold]Correct Answer[/bold] - {value.chinese_character}")
                    table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                    table.add_column("Pinyin", justify="center", style="bright_blue")
                    table.add_column("English", justify="center", style="bright_blue")

                    table.add_row(f"{value.chinese_character}", f"{value.chinese_pinyin}", f"{value.english}")
                    console.print(table)

                    update_word_stats(key, False)

                # Print separator after each question
                console.rule("[bold red]")

    # Calculate final score and display it
    score_player_1 = round(score_player_1 * 0.75)
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))

    update_score_progress(score_player_1, time.time() - start, inp)


#Like ec pinyin but user choose the number of question (x)
def random_x_quizz(inp, count=0, limitation=10001):
    user_limit = input("Random x numbers of words (type x): ")
    if user_limit == "": user_limit = 10
    user_limit = int(user_limit)
    score_player_1 = 0
    counter = 0

    for key, value in dq_vocabulary.items():
        question_pick = random.choice(list(dq_vocabulary.values()))

        while question_pick.done == 1:
            question_pick = random.choice(list(dq_vocabulary.values()))

        if question_pick.done == 0:
            cprint(question_pick.english, "blue", attrs=["bold"]) 
            ans = input()

            if ans == question_pick.chinese_pinyin or ans == question_pick.chinese_character:
                cprint("Good Answer", "green", attrs=["underline"])
                update_word_stats(key, True)
                score_player_1 += question_pick.difficulty

            else:
                cprint("Wrong Anser", "red", attrs=["underline"])
                cprint(f"{question_pick.chinese_pinyin}, {question_pick.chinese_character}", attrs=["bold"])
                update_word_stats(key, False)

            question_pick.done = 1
        counter += 1 
        if counter >= user_limit: break

    score_player_1 = round(score_player_1*0.75)
    update_score_progress(score_player_1, time.time() - start, inp)



def hsk_quizz(inp):
    console = Console()
    console.show_cursor()

    hsk_level = input("Which hsk level do you want ?(1 to 6): ")
    limitation = input("Do you wish to set a limit to the number of questions ?(yes or no, blank is no): ")

    hsk_dict = get_hsk_by_level(hsk_level)
    for i in hsk_dict:
        print(hsk_dict[i].english, hsk_dict[i].chinese_pinyin)
    bad_ans = {}
    score_player_1 = 0

    for key, value in hsk_dict.items():
        word = random.choice(list(hsk_dict.values()))

        while word.done == 1:
            word = random.choice(list(hsk_dict.values()))

        if word.done == 0:
            console.print(f"[bold royal_blue1]{word.english}")
            ans = input()
            if ans == word.chinese_pinyin:
                console.print("[bold green]Good Answer")
                score_player_1 += word.difficulty
                update_word_stats(key, True)

            else:
                console.print("[bold red]Wrong Answer")
                bad_ans[key] = word
                update_word_stats(key, False)

                table = Table(title=(f"{word.chinese_character}"))

                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{word.chinese_character}", f"{word.chinese_pinyin}", f"{word.english}")

                console.print(table)

            console.rule("[bold red]")
            word.done = 1
        
    update_score_progress(score_player_1, time.time() - start, inp)

    table = Table(title=("[bold red]Bad Answers"))            
    table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
    table.add_column("Pinyin", justify="center", style="bright_blue")
    table.add_column("English", justify="center", style="bright_blue") 
    for i in bad_ans:
        table.add_row(f"{bad_ans[i].chinese_character}", f"{bad_ans[i].chinese_pinyin}, f{bad_ans[i].english}")
    console.print(table)

    score_player_1 = round(score_player_1)
    update_score_progress(score_player_1, time.time() - start, "hsk")









#Chinese to english quizz, doesn't update the stats because checking right answer is too tedious
def ce_quizz(count, limitation):
        for i in dq_vocabulary:

            question_pick = random.choice(list(dq_vocabulary.values()))

            while question_pick.done == 1:
                question_pick = random.choice(list(dq_vocabulary.values()))

            if question_pick.done == 0:
                cprint(f"{question_pick.chinese_character}, {question_pick.chinese_pinyin}", "blue", attrs=["bold"])
                ans = input() 
                cprint(f"{question_pick.english}", "light_green", attrs=["bold"])
                question_pick.done = 1 
                count +=1 
                if count == limitation:
                    break
        return


        

def add_vocabulary(pinyin, simplified, english, hsk_level = 1):
    word_def = get_def_pinyin_simplified()

    if word_def != False: 
        count = 0
        with open("questions_vocabulaire.py", "a") as f:
            print(f'dq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level})', file=f)
            print("done")

if __name__ == "__main__":
    add_vocabulary("ran2 hou4", "然后", "and then")

# Ask the def of a word and it will return the matching result (you can ask english, pinyin, simplified or traditional)
#def ask_def():
    # Parse U8 file and return a list of dict with this form {traditional:, simplified:, pinyin:, english:}
    #ce_dict = create_dict()

    #word_asked = input("Definition of:")

    # Implement some kind of search
    #for curr in ce_dict:
    #    if curr["pinyin"] == word_asked or curr["simplified"] == word_asked or curr["traditional"] == word_asked or curr["english"]:
    #    print(f"Definition of {word_asked} is Pinyin: {curr["pinyin"]}, Simplified: {curr["simplified"]}, English: {curr["english"]}")
    


