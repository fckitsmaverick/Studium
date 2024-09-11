import sqlite3
import pandas as pd

import sys
import os
from contextlib import contextmanager

from rich.console import Console

@contextmanager
def temporarily_add_path(path):
    sys.path.insert(0, path)
    try:
        yield  # This allows the code inside the "with" block to execute
    finally:
        sys.path.pop(0)  # Ensure that the path is removed after use

# Usage:
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

with temporarily_add_path(parent_dir):
    from classes_chinois import Vocabulary  # The path is temporarily modified here

# After the with block, sys.path is restored to its original state

db_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools')
db_filename = ('hsk_vocabulary.db')
db_path = os.path.join(db_directory, db_filename)


def initiate_hsk_db():

    #Create hsk database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #UNIQUE is to avoid duplicate entries
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hsk_vocab (
            hsk_level INTEGER DEFAULT 1,
            simplified VARCHAR(255) NOT NULL,
            pinyin VARCHAR(255) NOT NULL,
            english VARCHAR(255) NOT NULL,
            UNIQUE (simplified, pinyin, english)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hsk_grammar (
            hsk_level INTEGER DEFAULT 1,
            simplified TEXT NOT NULL,
            pinyin TEXT NOT NULL,
            english TEXT NOT NULL,
            UNIQUE (simplified, pinyin, english)
        )
    ''')

    conn.close()


def create_hsk_db():
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Turn CSV into pandas dataframe
    df_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools')
    df_filename = ('hsk-level-all.csv')
    df_path = os.path.join(df_directory, df_filename)

    df = pd.read_csv(df_path, names=(["hsk_level", "simplified", "pinyin", "english"]), usecols=["hsk_level", "simplified", "pinyin", "english"])

    #Then turn it into python dictionary
    hsk_dict = df.to_dict("index")

    for word in hsk_dict: 
        #Populate the database and ignoring duplicates
        cursor.execute('''
            INSERT OR IGNORE INTO hsk_vocab (hsk_level, simplified, pinyin, english)
            VALUES (?, ?, ?, ?)
        ''', (hsk_dict[word]["hsk_level"], hsk_dict[word]["simplified"], hsk_dict[word]["pinyin"], hsk_dict[word]["english"]))
    
    conn.commit()
    conn.close()

def create_hsk_grammar_db():
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Turn CSV into pandas dataframe
    df_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools')
    df_filename = ('hsk-1-grammar.csv')
    df_path = os.path.join(df_directory, df_filename)

    df = pd.read_csv(df_path, names=(["hsk_level", "simplified", "pinyin", "english"]), usecols=["hsk_level", "simplified", "pinyin", "english"])
    hsk_sentences_dict = df.to_dict("index")
    print(hsk_sentences_dict)

    for i in hsk_sentences_dict:
        cursor.execute('''
            INSERT OR IGNORE INTO hsk_grammar (hsk_level, simplified, pinyin, english)
            VALUES (?, ?, ?, ?)
        ''', (1, hsk_sentences_dict[i]["simplified"], hsk_sentences_dict[i]["pinyin"], hsk_sentences_dict[i]["english"]))
    
    

    
def get_hsk_level(pinyin_input, simplified_input, user_input=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    console = Console()
    console.show_cursor()

    #If the user ask explicitely for it, otherwise the function is just meant to be called as part of the code
    if user_input == True:
        pinyin_input = input("Pinyin: ")
        simplified_input = input("Simplified: ")

    cursor.execute('SELECT hsk_level, simplified, pinyin, english FROM hsk_vocab WHERE pinyin = ? AND simplified = ?', (pinyin_input, simplified_input))

    result = cursor.fetchall()

    if result:
        #result[0][0] is hsk_level, [0][1] is simplified, [0][2] is pinyin and [0][3] is english
        dict_result = {"hsk_level": result[0][0]}
        return dict_result
    else:
        console.print("[bold red]No result found for this word, hsk default value assigned: 1[/bold red]")
        dict_result = {"hsk_level": 1}
        return False

    conn.close()

def get_hsk_by_level(level):
    hsk_dict = {}

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''SELECT simplified, pinyin, english, hsk_level
                      FROM hsk_vocab
                      WHERE hsk_level = ?''', (level,))

    result = cursor.fetchall()

    for row in result:
        simplified = row[0]
        pinyin = row[1]
        english = row[2]
        hsk_level = row[3]
        hsk_dict[simplified] = Vocabulary(pinyin, simplified, english, hsk_level, category="Vocabulary")

    conn.close()

    return hsk_dict

def get_hsk_dict_def(pinyin_input, simplified_input, user_input=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    console = Console()
    console.show_cursor()

    #If the user ask explicitely for it, otherwise the function is just meant to be called as part of the code
    if user_input == True:
        pinyin_input = input("Pinyin: ")
        simplified_input = input("Simplified: ")

    cursor.execute('SELECT hsk_level, simplified, pinyin, english FROM hsk_vocab WHERE pinyin = ? AND simplified = ?', (pinyin_input, simplified_input))

    result = cursor.fetchall()

    if result:
        #result[0][0] is hsk_level, [0][1] is simplified, [0][2] is pinyin and [0][3] is english
        dict_result = {"simplified": result[0][1], "pinyin": result[0][2], "english": result[0][3]}
        return dict_result
    else:
        console.print("[bold red]No result found for this word in HSK dictionnary[/bold red]")
        return False

    conn.close() 


def main():
    initiate_hsk_db()
    create_hsk_db()

if __name__ == "__main__":
    main()