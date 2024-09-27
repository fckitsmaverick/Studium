from dict_tools.english_vocab import d_english
from functions.functions_kit import update_vocab_dictionnary, assign_true_false, take_user_preferences, display_bad_ans, compare_ans, redo_bad_ans

from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import track

import random
import time

def random_x_english(inp, count=0, limitation=10001):
    # Start rich console
    console = Console()
    console.show_cursor()

    score_player_1 = 0
    counter = 0
    bad_ans = {}

    user_limit, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit = take_user_preferences()

    updated_dq = update_vocab_dictionnary(d_english, sentence_included, kind_of_word, difficulty_set, kind, difficulty_limit)
    
    # Start timer
    start_time = time.time()

    for key, value in updated_dq.items():
        question_pick = random.choice(list(updated_dq.values()))

        # Skip already answered questions
        while question_pick.done == 1:
            question_pick = random.choice(list(updated_dq.values()))

        if question_pick.done == 0:
            # Ask the question (displaying the English meaning)
            console.print(Panel(f"[bold blue]{question_pick.english_def}[/bold blue]", title="Question", expand=False))
            ans = Prompt.ask("[bold yellow]Enter your answer (pinyin or character): [/bold yellow]")

            if ans.lower() == "exit": return

            if ans == question_pick.english_word:
                console.print("[bold green]Good Answer![/bold green]")
                score_player_1 += question_pick.difficulty
            else:
                console.print("[bold red]Wrong Answer![/bold red]")
                #Check if user typed pinyin or chinese character
                #Then compare the answer and output the hightlighted error(s)
                if len(ans) > 0:
                    correct_ans = compare_ans(ans, question_pick.english_word)

                # Display the correct answer in a table
                table = Table(title=f"[bold]Correct Answer[/bold] - {question_pick.english_word}")
                table.add_column("English Word", justify="center", style="bright_blue", no_wrap=True)
                table.add_column("English Definition", justify="center", style="bright_blue")
                table.add_column("Your Answer", justify="center", style="bright_blue")

                table.add_row(f"{question_pick.english_word}", f"{question_pick.english_def}", f"{ans}")
                console.print(table)

                bad_ans[key] = question_pick
                #update_word_stats(question_pick.chinese_character, False)

            question_pick.done = 1
            counter += 1
            #update_experience(question_pick.difficulty)

            # Display progress counter
            if user_limit <= len(updated_dq): console.print(f"[bold yellow]Questions Completed: {counter}/{user_limit}[/bold yellow]")
            else: console.print(f"[bold yellow]Questions Completed: {counter}/{len(updated_dq)}[/bold yellow]")
            console.rule("[bold red]\n")

            # Check if the user has reached the limit
            if counter >= user_limit:
                break

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)


    console.print(Panel(f"[bold magenta]Quiz Complete![/bold magenta]\nYour final score: [bold yellow]{score_player_1}[/bold yellow]", expand=False))
    
    # Display elapsed time
    console.print(f"[bold green]Time Elapsed: {minutes}m {seconds}s[/bold green]")


if __name__ == "__main__":
    random_x_english("english")