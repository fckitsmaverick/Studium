from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.database import update_score_progress, get_experience
from database_tools.pokemon_database import get_pokedex, check_pokemon_rank, add_to_pokedex
from functions.quizz_functions import ec_quizz, ecpinyin_quizz, last_x_quizz, worst_x_quizz, random_x_quizz, hsk_quizz, ce_random_quizz, sentence_quizz
from functions.functions_kit import print_pokedex, new_vocab_auto, study_personal, update_word_personal_vocab, delete_specific_word_line


from datetime import datetime
from termcolor import cprint
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

import random
import time
import pandas as pd
import sys


score_player_1 = 0
limitation = 10001


bad_ans = {

}

progress = {

}

console = Console()
console.show_cursor()



def display_menu():
    """Display the main menu using rich formatting."""
    console.print(Panel("[bold magenta]Welcome to the Pokemon Quizz Menu![/bold magenta]", expand=False))

    table = Table(title="Main Menu", show_edge=False, header_style="bold blue")
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Description", style="green")

    table.add_row("1", "Enter Quizz Mode")
    table.add_row("2", "Enter Pokemon Mode")
    table.add_row("3", "Enter Study Mode")
    table.add_row("4", "Enter Dictionnary Mode")
    table.add_row("5", "Exit")

    console.print(table)


def display_quizz_submenu():
    """Display the quizz mode submenu."""
    console.print(Panel("[bold magenta]Quizz Mode[/bold magenta]", expand=False))

    table = Table(title="Quizz Mode Options", show_edge=False, header_style="bold blue")
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Description", style="green")

    table.add_row("1", "English to Chinese Pinyin Quizz")
    table.add_row("2", "Random X Words Quizz (taken from your personal dictionnary)")
    table.add_row("3", "Last X Words Quizz (taken from your personal dictionnary)")
    table.add_row("4", "Worst X Words Quizz (your words with the worst ratio!)")
    table.add_row("5", "HSK Quizz (you can choose your level!)")
    table.add_row("6", "Chinese character to Pinyin Quizz")
    table.add_row("7", "Chinese Sentences Quizz")
    table.add_row("8", "Back to Main Menu")

    console.print(table)


def display_pokemon_submenu():
    """Display the pokemon mode submenu."""
    console.print(Panel("[bold magenta]Pokemon Mode[/bold magenta]", expand=False))

    table = Table(title="Pokemon Mode Options", show_edge=False, header_style="bold blue")
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Description", style="green")

    table.add_row("1", "See your Pokedex")
    table.add_row("2", "Check Pokémon Rank")
    table.add_row("3", "See your current XP")
    table.add_row("4", "Add a pokemon to your pokedex")
    table.add_row("5", "Back to Main Menu")

    console.print(table)


def get_user_choice():
    """Prompt the user for input."""
    return Prompt.ask("[bold yellow]Please select an option[/bold yellow]", choices=["1", "2", "3", "4", "5"])

def get_submenu_choice(choices):
    """Prompt the user for input in the submenu."""
    return Prompt.ask("[bold yellow]Please select an option[/bold yellow]", choices=choices)

def quizz_mode():
    """Handle Quizz Mode submenu actions."""
    while True:
        display_quizz_submenu()
        quizz_choice = get_submenu_choice(["1", "2", "3", "4", "5", "6", "7", "8"])

        if quizz_choice == "1":
            console.print("[bold green]Starting a new English to Chinese Pinyin Quizz ![/bold green]")
            ecpinyin_quizz("1")
            return
        elif quizz_choice == "2":
            console.print("[bold green]Starting a new Random Test ![/bold green]")
            random_x_quizz("2")
            return
        elif quizz_choice == "3":
            console.print("[bold green]Starting a new Last X Test ![/bold green]")
            last_x_quizz("3")
            return
        elif quizz_choice == "4":
            console.print("[bold green]Starting a new Worst X Test ![/bold green]")
            worst_x_quizz("4")
            return
        elif quizz_choice == "5":
            console.print("[bold green]Starting a new HSK Test ![/bold green]")
            hsk_quizz("5")
            return
        elif quizz_choice == "6":
            console.print("[bold green]Starting a new Chinese Character to Pinyin Quizz ![/bold green]")
            ce_random_quizz("6")
            return
        elif quizz_choice == "7":
            console.print("[bold green]Starting a new Chinese Sentences Quizz ![/bold green]")
            sentence_quizz("7")
            return
        elif quizz_choice == "8":
            return  # Return to the main menu

def pokemon_mode():
    """Handle Pokemon Mode submenu actions."""
    while True:
        display_pokemon_submenu()
        pokemon_choice = get_submenu_choice(["1", "2", "3", "4"])

        if pokemon_choice == "1":
            console.print("[bold green]Catching a Pokémon![/bold green]")
            my_pokedex = get_pokedex()
            print_pokedex(my_pokedex)
            return
        elif pokemon_choice == "2":
            console.print("[bold green]Checking Pokémon rank![/bold green]")
            check_pokemon_rank()
            return
        elif pokemon_choice == "3":
            console.print("[bold green]Check your XP!")
            get_experience()
            return
        elif pokemon_choice == "4":
            console.print("[bold green]Adding a Pokémon to your Pokedex![/bold green]")
            add_to_pokedex()
            return
        elif pokemon_choice == "5":
            return  # Return to the main menu

def display_dictionnary_submenu():
    """Display the dictionnary mode submenu."""
    console.print(Panel("[bold magenta]Dictionnary Mode[/bold magenta]", expand=False))

    table = Table(title="Dictionnary Mode Options", show_edge=False, header_style="bold blue")
    table.add_column("Option", justify="center", style="bold yellow")
    table.add_column("Description", style="green")

    table.add_row("1", "Add New Vocabulary")
    table.add_row("2", "Deleting Vocabulary")
    table.add_row("3", "Update Vocabulary")
    table.add_row("4", "Back to Main Menu")

    console.print(table)

def dictionnary_mode():
    while True:
        display_dictionnary_submenu()
        dictionary_choice = get_submenu_choice(["1", "2", "3", "4"])

        if dictionary_choice == "1":
            console.print("[bold green]Adding new vocabulary ![/bold green]")
            new_vocab_auto()
            return
        elif dictionary_choice == "2":
            console.print("[bold green]Deleting a word in your personal vocabulary ![/bold green]")
            delete_specific_word_line()
            return
        elif dictionary_choice == "3":
            console.print("[bold green]Update a dictionnary entry[/bold green]")
            update_word_personal_vocab()
            return
        elif dictionary_choice == "4":
            return  # Return to the main menu



def main():
    while True:
        # Display the main menu
        display_menu()

        # Get user's choice
        choice = get_user_choice()

        if choice == "1":
            quizz_mode()  # Call the Quizz Mode submenu
        elif choice == "2":
            pokemon_mode()  # Call the Pokemon Mode submenu
        elif choice == "3":
            console.print("Study Mode selected!")
            study_personal()
        elif choice == "4":
            console.print("[bold green]Entering Dictionnary Mode ![/bold green]")
            dictionnary_mode()
        elif choice == "5":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)
        else:
            console.print("[bold red]Invalid option! Try again.[/bold red]")


if __name__ == "__main__":
    main()



final_timer = time.time() - start

print(f"Score: {score_player_1}, Total length: {len(dq_vocabulary)}, Final timer: {int(final_timer)}")