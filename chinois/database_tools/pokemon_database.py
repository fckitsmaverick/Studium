import sqlite3
import os
import sys
import random

db_directory = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools'
db_filename = 'pokemon.db'
db_path = os.path.join(db_directory, db_filename)

def initiate_pokemon_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokemon_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            rank INTERGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badges_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path VARCHAR(255) NOT NULL,
            quest VARCHAR(255)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pokedex (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            path VARCHAR(255) NOT NULL,
            charac VARCHAR(255)
        )
    ''')

    conn.commit()
    conn.close()

def populate_pokemon():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the directory name
    pokemon_directory = os.path.join(current_directory, 'pokemon')

    # Iterate through the files in the pokemon directory
    for filename in os.listdir(pokemon_directory):
        # Get the full path of the file
        file_path = os.path.join(pokemon_directory, filename)

        # Get the filename without the extension
        name = os.path.splitext(filename)[0]

        cursor.execute('''
            INSERT INTO pokemon_images (path, name, rank)
            VALUES (?, ?, ?) 
        ''', (file_path, name, random.randint(50, 10000)))

    
    conn.commit()
    conn.close()

def add_to_pokedex():
    conn_pokemon = sqlite3.connect(db_path)
    cursor_pokemon = conn_pokemon.cursor()

    # Connect to the quizz_progress.db to check user's points
    quizz_db_path = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools/quizz_progress.db'
    conn_quizz = sqlite3.connect(quizz_db_path)
    cursor_quizz = conn_quizz.cursor()

    # Get the user's current experience points from the OverallProgress table
    cursor_quizz.execute('SELECT Experience FROM OverallProgress')
    user_points = cursor_quizz.fetchone()[0]

    # Ask the user for the Pokémon they want
    user_wish = input("Which Pokémon do you wish to get? ")

    # Check if the Pokémon exists and get its rank and path from pokemon_images table
    cursor_pokemon.execute('SELECT rank, path FROM pokemon_images WHERE name = ?', (user_wish,))
    pokemon_data = cursor_pokemon.fetchone()

    if pokemon_data is None:
        print(f"Pokémon {user_wish} does not exist in the database.")
    else:
        pokemon_rank, pokemon_path = pokemon_data

        # Check if the user has enough points
        if user_points >= pokemon_rank:
            # Deduct points and update experience in quizz_progress.db
            new_points = user_points - pokemon_rank
            cursor_quizz.execute('UPDATE OverallProgress SET Experience = ? WHERE Experience = ?', (new_points, user_points))
            
            # Assign a random characteristic to the Pokémon
            characteristics = ['smart', 'strong', 'loving', 'cute', 'funny', 'ingenious']
            charac = random.choice(characteristics)

            # Add Pokémon to pokedex with its file path and characteristic
            cursor_pokemon.execute('''
                INSERT INTO pokedex (name, path, charac)
                VALUES (?, ?, ?)
            ''', (user_wish, pokemon_path, charac))

            print(f"Congratulations! You have added {user_wish} to your Pokedex. It is {charac}.")

            conn_pokemon.commit()
            conn_quizz.commit()
        else:
            print(f"Sorry, you need {pokemon_rank} points, but you only have {user_points} points.")

    # Close connections
    conn_pokemon.close()
    conn_quizz.close()

def get_pokedex():

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve all Pokémon from the pokedex table
    cursor.execute('SELECT name, path, charac FROM pokedex')
    pokedex_entries = cursor.fetchall()

    # Create a list to store the Pokémon data
    pokemon_list = []
    
    for entry in pokedex_entries:
        name, path, charac = entry
        pokemon_list.append({
            'name': name,
            'file_path': path,
            'characteristic': charac
        })

    conn.close()

    return pokemon_list

def check_pokemon_rank():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ask the user for the Pokémon they want to check
    user_wish = input("Enter the name of the Pokémon to check its rank: ")

    # Check if the Pokémon exists and get its rank from pokemon_images table
    cursor.execute('SELECT rank FROM pokemon_images WHERE name = ?', (user_wish,))
    pokemon_rank = cursor.fetchone()

    if pokemon_rank is None:
        print(f"Pokémon {user_wish} does not exist in the database.")
    else:
        print(f"The rank of {user_wish} is {pokemon_rank[0]} points.")

    conn.close()


if __name__ == "__main__":
    add_to_pokedex()
