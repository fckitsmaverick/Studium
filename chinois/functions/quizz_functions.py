from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.database import update_score_progress, update_word_stats, get_word_stats, get_worst_word_ratios, update_experience, return_all_SR, clean_db
from database_tools.cedict_database import get_def, get_def_pinyin_simplified
from database_tools.hsk_database import get_hsk_by_level
from functions.functions_kit import update_vocab_dictionnary, assign_true_false, take_user_preferences, display_bad_ans, compare_ans, redo_bad_ans, reset_vocab_dictionnary, pick_questions, tts_audio

from datetime import datetime
from termcolor import cprint
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import track
from playsound import playsound

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



#This quizz is the basis for the others
#English to Chinese quizz only one input required to validate the answer (pinyin)
#Yes my functions are too long
def ecpinyin_quizz(inp):
    # Start rich console
    console = Console()
    console.show_cursor()

    score_player_1 = 0
    count = 0
    bad_ans = {}

    user_limit, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit, audio, tts_model = take_user_preferences()
    updated_dq = update_vocab_dictionnary(dq_vocabulary, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit)

    for i in updated_dq:
        question_pick = random.choice(list(updated_dq.values()))

        # Skip already answered questions
        while question_pick.done == 1:
            question_pick = random.choice(list(updated_dq.values()))

        if question_pick.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold bright_blue]{question_pick.english}[/bold bright_blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

            if ans.lower() == "exit": return

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

                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, question_pick.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, question_pick.chinese_character)

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

                bad_ans[i] = question_pick
                update_word_stats(question_pick.chinese_character, False)

            question_pick.done = 1
            count += 1
            update_experience(question_pick.difficulty)
            console.print(f"[bold yellow]Questions Completed: {count}/{len(dq_vocabulary)}, {round((count/len(dq_vocabulary))*100)}%[/bold yellow]")
            console.rule("[bold red]\n")

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Display final score
    score_player_1 = round(score_player_1 * 0.75)
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))



def last_x_quizz(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    user_limit, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit, audio, tts_model = take_user_preferences()
    updated_dq = update_vocab_dictionnary(dq_vocabulary, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit)
    update_ratio = Prompt.ask("[bold yellow]Do you want to update the success ratio?[/bold yellow]", choices=["yes", "no"], default="no")

    counter = 0
    score_player_1 = 0
    total_questions = len(updated_dq) - (len(updated_dq) - user_limit)
    bad_ans = {}

    # Loop over the last x entries and ask questions
    for key, value in updated_dq.items():
        # Iterate until the entry we want
        if len(updated_dq) - count <= (user_limit):
            question_pick = value
            
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold cyan]{question_pick.english}[/bold cyan]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]") 
            result = False

            if ans.lower() == "exit": return

            if ans == question_pick.chinese_pinyin or ans == question_pick.chinese_character:
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

                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, question_pick.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, question_pick.chinese_character)

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

                bad_ans[key] = question_pick

            if audio == "yes":
                try:
                    tts_audio(tts_model, question_pick)
                except:
                    console.print("[bold red]An error occured.[/bold red]")

            update_experience(question_pick.difficulty)
            console.rule("[bold]\n")
            # Update the ratio if the user opted to
            if update_ratio.lower() == "yes": 
                update_word_stats(question_pick.chinese_character, result)

            counter += 1
            if counter >= user_limit:
                break
        else:
            count += 1
        # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Display final score in a panel
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))


def worst_x_quizz(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    clean = Prompt.ask("[bold yellow]Do you wish to clean the database before starting the quizz ?[/bold yellow]", choices=["yes", "no"], default="no")
    if clean == "yes":
        db = return_all_SR()
        for word in db:
            if word[0] not in dq_vocabulary.keys():
                clean_db(word[0])

    # Take user input for number of worst words to quiz on
    user_limit = Prompt.ask("[bold yellow]Worst x words (type x)[/bold yellow]", default="10")
    user_limit = int(user_limit)
    way_of_counting = Prompt.ask("[bold yellow]Which data do you wish to use to rank your worst words ?[/bold yellow]", default="ratio", choices=["ratio", "brutewrong", "bruteright"])
    score_player_1 = 0
    bad_ans = {}
    counter, counter_right, counter_wrong = 0, 0, 0
    worst10 = get_worst_word_ratios(user_limit, way_of_counting)

    # Loop through vocabulary to ask questions about the worst words
    for word in reversed(worst10):
        for key, value in dq_vocabulary.items():
            if word["word"] == value.chinese_character:
                # Ask the question (displaying the English meaning)
                console.print(Panel(f"[bold magenta]{value.english}[/bold magenta]", title="Question", expand=False))
                ans = console.input("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

                if ans.lower() == "exit": return

                if ans == value.chinese_pinyin:
                    console.print("[bold green]Correct![/bold green]")
                    score_player_1 += value.difficulty
                    #You can choose to update the ratio
                    #update_word_stats(key, True)
                else:
                    console.print("[bold bright_red]Incorrect![/bold bright_red]", style="bold red")
                    
                    bad_ans[key] = value

                    if len(ans) > 0:
                        if ans[0].isascii():
                            correct_ans = compare_ans(ans, value.chinese_pinyin)
                        else:
                            correct_ans = compare_ans(ans, value.chinese_character)
                        
                        # Display correct answer in a table
                        table = Table(title=f"[bold]Correct Answer[/bold] - {value.chinese_character}")
                        table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                        table.add_column("Pinyin", justify="center", style="bright_blue")
                        table.add_column("English", justify="center", style="bright_blue")

                        table.add_row(f"{value.chinese_character}", f"{value.chinese_pinyin}", f"{value.english}")
                        console.print(table)

                    #update_word_stats(key, False)

                get_word_stats(value.chinese_character, value.chinese_pinyin, True) 
                update_experience(value.difficulty)
                # Print separator after each question
                console.rule("[bold red]\n")
    

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Calculate final score and display it
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))



def random_x_quizz(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    score_player_1 = 0
    counter = 0
    counter_right, counter_wrong = 0, 0
    bad_ans = {}

    # Get user preferences for the quiz
    user_limit, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit, audio, tts_model = take_user_preferences()

    # Update the vocabulary dictionary based on preferences
    updated_dq = update_vocab_dictionnary(dq_vocabulary, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit)

    questions = pick_questions(updated_dq, user_limit)
    if questions == None:
        console.print("[bold red]Error, try to input a smaller limit.[/bold red]")
        return
    
    # Start timer
    start_time = time.time()

    for key, value in questions.items():

        # Ask the question (displaying the English meaning)
        console.print(Panel(f"[bold blue]{value.english}[/bold blue]", title="Question", expand=False))
        ans = Prompt.ask("[bold yellow]Enter your answer (pinyin or character): [/bold yellow]")

        # Allow user to exit quiz
        if ans.lower() == "exit":
            return

        # Check if the answer is correct
        if ans == value.chinese_pinyin or ans == value.chinese_character:
            console.print("[bold green]Good Answer![/bold green]")
            score_player_1 += value.difficulty
            update_word_stats(value.chinese_character, True)
            counter_right += 1

            # Update quest progress and add experience if quest is completed
            #update_quest_progress('daily', quest_id=1, increment=1)  # Assuming 'daily' quest with quest_id=1

        else:
            console.print("[bold red]Wrong Answer![/bold red]")
            counter_wrong += 1

            # Check if user typed pinyin or Chinese character and highlight errors
            if len(ans) > 0:
                if ans[0].isascii():
                    correct_ans = compare_ans(ans, value.chinese_pinyin)
                else:
                    correct_ans = compare_ans(ans, value.chinese_character)
        

            # Display the correct answer in a table
            table = Table(title=f"[bold]Correct Answer[/bold] - {value.chinese_character}")
            table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
            table.add_column("Pinyin", justify="center", style="bright_blue")
            table.add_column("Your Answer", justify="center", style="bright_blue")
            table.add_row(f"{value.chinese_character}", f"{value.chinese_pinyin}", f"{value.english}")
            console.print(table)

            # Store bad answers and update word stats
            bad_ans[key] = value
            update_word_stats(value.chinese_character, False)
        
        #get_word_stats(question_pick.chinese_character, question_pick.chinese_pinyin)
        if audio == "yes":
            try:
                tts_audio(tts_model, value)
            except:
                console.print("[bold red]An error occured.[/bold red]")


        # Mark the question as answered
        counter += 1

        # Update player's experience based on question difficulty
        update_experience(value.difficulty)

        # Display progress counter
        if user_limit <= len(updated_dq):
            console.print(f"[bold yellow]Questions Completed: {counter}/{user_limit}[/bold yellow]")
        else:
            console.print(f"[bold yellow]Questions Completed: {counter}/{len(updated_dq)}[/bold yellow]")
        console.rule("[bold red]\n")

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Reset the vocabulary dictionary
    reset_vocab_dictionnary(dq_vocabulary)

    # Display final score and summary
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))
    console.print(Panel(f"[bold magenta]Right Answer(s): {counter_right} \nWrong Answer(s): {counter_wrong} \nRatio: {round((counter_right/counter)*100, 2)}[/bold magenta]", expand=False))
    # Display elapsed time
    console.print(f"[bold green]Time Elapsed: {minutes}m {seconds}s[/bold green]")






def hsk_quizz(inp):
    # Start rich console
    console = Console()
    console.show_cursor()

    # Take user input for HSK level and question limit
    hsk_level = Prompt.ask("[bold yellow]Which HSK level do you want? (1 to 6)[/bold yellow]")
    limitation = Prompt.ask("[bold yellow]Do you wish to set a limit to the number of questions? (yes or no, blank is no)[/bold yellow]", choices=["yes", "no"], default="no")
    user_limit = 500
    if limitation.lower() == "yes":
        user_limit = Prompt.ask("[bold yellow]Enter the number of questions you want to answer[/bold yellow]", default="500")
    order = Prompt.ask("[bold yellow]Do you want it to appear ordered ?[/bold yellow]", choices=["yes", "no"], default="no")

    # Get HSK vocabulary by level
    hsk_dict = get_hsk_by_level(hsk_level)
    bad_ans = {}
    score_player_1 = 0
    count = 0

    for key, value in hsk_dict.items():
        if order == "no":
            word = random.choice(list(hsk_dict.values()))

            # Skip already answered questions
            while word.done == 1:
                word = random.choice(list(hsk_dict.values()))
        else:
            word = value
        
        
        if word.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold royal_blue1]{word.english}[/bold royal_blue1]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

            if ans.lower() == "exit": return

            if ans == word.chinese_pinyin:
                console.print("[bold green]Good Answer![/bold green]")
                score_player_1 += word.difficulty
            else:
                console.print("[bold red]Wrong Answer![/bold red]")
                bad_ans[key] = word
                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, word.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, word.chinese_character)

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {word.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{word.chinese_character}", f"{word.chinese_pinyin}", f"{word.english}")
                console.print(table)

            console.rule("[bold red]\n")
            count += 1
            console.print(f"[bold yellow]Questions Completed: {count}/{len(hsk_dict)}, {round((count/len(hsk_dict))*100)}%[/bold yellow]")
            word.done = 1
            
            # Break if limit is reached
            if limitation.lower() == "yes" and count >= int(user_limit):
                break

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Calculate final score and display it
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))
    update_score_progress(score_player_1, time.time() - start, "hsk")


def ce_random_quizz(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    # Take user input for number of random questions
    user_limit = Prompt.ask("[bold yellow]Random x number of words (type x)[/bold yellow]", default="10")
    user_limit = int(user_limit)
    score_player_1 = 0
    counter = 0
    bad_ans = {}

    # Start timer
    start_time = time.time()

    for key, value in dq_vocabulary.items():
        question_pick = random.choice(list(dq_vocabulary.values()))

        # Skip already answered questions
        while question_pick.done == 1:
            question_pick = random.choice(list(dq_vocabulary.values()))

        if question_pick.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold blue]{question_pick.chinese_character} / {question_pick.chinese_pinyin}[/bold blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin or character): [/bold yellow]")

            if ans.lower() == "exit": return

            if ans == question_pick.chinese_pinyin:
                console.print("[bold green]Good Answer![/bold green]")
                score_player_1 += question_pick.difficulty
            else:
                console.print("[bold red]Wrong Answer![/bold red]")
                bad_ans[key] = question_pick
                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, question_pick.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, question_pick.chinese_character)

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {question_pick.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

                bad_ans[key] = question_pick

            question_pick.done = 1
            counter += 1
            #update_experience(question_pick.difficulty)
            console.rule("[bold red]\n")

            # Display progress counter
            console.print(f"[bold yellow]Questions Completed: {counter}/{user_limit}[/bold yellow]")

            # Check if the user has reached the limit
            if counter >= user_limit:
                break

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))
    
    # Display elapsed time
    console.print(f"[bold green]Time Elapsed: {minutes}m {seconds}s[/bold green]")



def sentence_quizz(inp):
    # Start rich console
    console = Console()
    console.show_cursor()

    user_limit = Prompt.ask("[bold yellow]Number of sentences you want to study (type x)[/bold yellow]", default="10")
    user_limit = int(user_limit)

    score_player_1 = 0
    count = 0
    bad_ans = {}

    sentence_dict = {}

    for key, value in dq_vocabulary.items():
        if value.category == "Sentence":
            sentence_dict[key] = value

    for i in sentence_dict:
        question_pick = random.choice(list(sentence_dict.values()))

        # Skip already answered questions
        while question_pick.done == 1:
            question_pick = random.choice(list(sentence_dict.values()))

        if question_pick.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold bright_blue]{question_pick.english}[/bold bright_blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

            if ans.lower() == "exit": return

            if ans == question_pick.chinese_pinyin:
                console.print("[bold bright_green]Good Answer![/bold bright_green]\n")
                score_player_1 += question_pick.difficulty
                #update_word_stats(question_pick.chinese_character, True)
            else:
                console.print("[bold bright_red]Bad Answer![/bold bright_red]\n")
                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, question_pick.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, question_pick.chinese_character)

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {question_pick.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

                bad_ans[i] = question_pick
                #update_word_stats(question_pick.chinese_character, False)

            question_pick.done = 1
            count += 1
            update_experience((question_pick.difficulty)*len(question_pick.chinese_pinyin.split(" ")))
            console.rule("[bold red]")
            console.print(f"[bold yellow]Questions Completed: {count}/{user_limit}, {round((count/user_limit)*100)}%[/bold yellow]")

            if count >= user_limit:
                break

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Display final score
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))


def topic_quizz(inp):
    # Start rich console
    console = Console()
    console.show_cursor()

    topic_pick = Prompt.ask("[bold yellow]Which topic do you want to study ?[/bold yellow]")

    user_limit = Prompt.ask("[bold yellow]Number of sentences you want to study (type x)[/bold yellow]", default="10")
    user_limit = int(user_limit)

    score_player_1 = 0
    count = 0
    bad_ans = {}

    topic_dict = {}

    for key, value in dq_vocabulary.items():
        if value.topic == topic_pick:
            topic_dict[key] = value

    for i in topic_dict:
        question_pick = random.choice(list(topic_dict.values()))

        # Skip already answered questions
        while question_pick.done == 1:
            question_pick = random.choice(list(topic_dict.values()))

        if question_pick.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold bright_blue]{question_pick.english}[/bold bright_blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin): [/bold yellow]")

            if ans.lower() == "exit": return

            if ans == question_pick.chinese_pinyin:
                console.print("[bold bright_green]Good Answer![/bold bright_green]\n")
                score_player_1 += question_pick.difficulty
                #update_word_stats(question_pick.chinese_character, True)
            else:
                console.print("[bold bright_red]Bad Answer![/bold bright_red]\n")
                if len(ans) > 0:
                    if ans[0].isascii(): correct_ans = compare_ans(ans, question_pick.chinese_pinyin)
                    else: correct_ans = compare_ans(ans, question_pick.chinese_character)

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {question_pick.chinese_character}")
                table.add_column("Simplified", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("Pinyin", justify="center", style="bright_blue")
                table.add_column("English", justify="center", style="bright_blue")

                table.add_row(f"{question_pick.chinese_character}", f"{question_pick.chinese_pinyin}", f"{question_pick.english}")
                console.print(table)

                bad_ans[i] = question_pick
                #update_word_stats(question_pick.chinese_character, False)

            question_pick.done = 1
            count += 1
            update_experience(question_pick.difficulty)
            console.rule("[bold red]")
            console.print(f"[bold yellow]Questions Completed: {count}/{len(user_limit)}, {round((count/len(user_limit))*100)}%[/bold yellow]")

            if count >= user_limit:
                break

    # Display a summary of bad answers
    if bad_ans:
        display_bad_ans(bad_ans)
        redo_bad_ans(bad_ans)

    # Display final score
    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))




# Ask the def of a word and it will return the matching result (you can ask english, pinyin, simplified or traditional)
#def ask_def():
    # Parse U8 file and return a list of dict with this form {traditional:, simplified:, pinyin:, english:}
    #ce_dict = create_dict()

    #word_asked = input("Definition of:")

    # Implement some kind of search
    #for curr in ce_dict:
    #    if curr["pinyin"] == word_asked or curr["simplified"] == word_asked or curr["traditional"] == word_asked or curr["english"]:
    #    print(f"Definition of {word_asked} is Pinyin: {curr["pinyin"]}, Simplified: {curr["simplified"]}, English: {curr["english"]}")
    


