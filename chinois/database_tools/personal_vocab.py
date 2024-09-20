import sqlite3
import os
import sys

from contextlib import contextmanager

from cedict_database import get_def_pinyin_simplified
from hsk_database import get_hsk_level

# Context manager to temporarily modify sys.path
@contextmanager
def add_to_sys_path(path):
    original_sys_path = sys.path.copy()
    sys.path.append(path)
    try:
        yield
    finally:
        sys.path = original_sys_path

# Path to the 'chinois' directory
chinois_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Use the context manager to safely import from the parent directory
with add_to_sys_path(chinois_dir):
    from questions_vocabulaire import dq_vocabulary

db_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools')
db_filename = ('personal_vocabulary.db')

db_path = os.path.join(db_directory, db_filename)

def initiate_personal_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_vocab (
            hsk_level INTEGER DEFAULT 1,
            simplified VARCHAR(255) NOT NULL,
            pinyin VARCHAR(255) NOT NULL,
            english VARCHAR(255) NOT NULL,
            UNIQUE (simplified, pinyin, english)
        )
    ''')
    
    conn.close()

def add_personal_vocab():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    pinyin_input = input("Pinyin: ")
    simplified_input = input("Simplified: ")

    #Get the definition, hsk level and characters of a word
    dict_result = get_def_pinyin_simplified(pinyin_input, simplified_input)
    hsk_result = get_hsk_level(pinyin_input, simplified_input)
    if dict_result and hsk_result: 
        #Include it in database
        cursor.execute('''
            INSERT OR IGNORE INTO personal_vocab (hsk_level, simplified, pinyin, english)
            VALUES (?, ?, ?, ?)
        ''', (hsk_result["hsk_level"], dict_result["simplified"], dict_result["pinyin"], dict_result["english"]))

        cursor.execute('SELECT DISTINCT hsk_level, simplified, pinyin, english FROM personal_vocab WHERE simplified = ? AND pinyin = ?', (simplified_input, pinyin_input))

        result = cursor.fetchall()
        print(result)

        user_confirmation = input("Do you agree with these entries ?")
        if user_confirmation.lower() == "yes":
            print("New vocabulary added")
        else:
            print("Sad, new vocabulary added")

    else:
        print("No dictionary entry found for these inputs, can't add to database")

    conn.commit()
    conn.close()

def populate_personal_vocab():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for i in dq_vocabulary:
        hsk_result = get_hsk_level(dq_vocabulary[i].chinese_pinyin, dq_vocabulary[i].chinese_character)
        
        cursor.execute('''
            INSERT OR IGNORE INTO personal_vocab (hsk_level, simplified, pinyin, english)
            VALUES (?, ?, ?, ?)
        ''', (hsk_result["hsk_level"], dq_vocabulary[i].chinese_character, dq_vocabulary[i].chinese_pinyin, dq_vocabulary[i].english))
    
    cursor.execute('SELECT * FROM personal_vocab')

    result = cursor.fetchall()
    print(result)
    
    conn.commit()
    conn.close()
 

def main():
    initiate_personal_db()
    add_personal_vocab()
    populate_personal_vocab()


if __name__ == "__main__":
    main()
