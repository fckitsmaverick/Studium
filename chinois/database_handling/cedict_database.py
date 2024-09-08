import sqlite3
import os
import time

from parser import create_dict

db_directory = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_handling'
db_filename = 'cedict.db'
db_path = os.path.join(db_directory, db_filename)

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

def initiate_cedict():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CeDict (
            Pinyin VARCHAR(255) NOT NULL,
            English VARCHAR(255) NOT NULL,
            Simplified VARCHAR(255) NOT NULL,
            Traditional VARCHAR(255),
            UNIQUE (Pinyin, Simplified, Traditional)
        )
    ''')

# Create the dictionnary database
def create_cedb(ce_d):

    conn = sqlite3.connect(db_path)

    cursor = conn.cursor()

    for curr in ce_d:
        
        cursor.execute('''
            INSERT OR IGNORE INTO CeDict (Pinyin, English, Simplified, Traditional)
            Values (?, ?, ?, ?)
        ''', (curr["pinyin"], curr["english"], curr["simplified"], curr["traditional"]))

    conn.commit()

# Sort the dictionnary by English definition
def sort_cedict():

    list_of_dicts = create_dict()

    sorted_list = sorted(list_of_dicts, key=lambda d: d["english"])
    #for i in sorted_list:
        #print(i["english"][0])
    return sorted_list


# Remove all the entries that are duplicates by english def (pretty sure it's a bad idea but)
def remove_duplicate():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM CeDict
        WHERE ROWID NOT IN (
            SELECT MIN(ROWID)
            FROM CeDict
            GROUP BY English
        )
    ''')

    conn.commit()
    print("Duplicate English definitions removed")


# Get a definition by asking the user Pinyin input (may result in more than 1 answer)
def get_def():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    word = input("Input Pinyin: ")
    start = time.time()
    cursor.execute('SELECT English, Simplified FROM CeDict WHERE Pinyin = ?', (word,))
    result = cursor.fetchall()
    end = time.time()
    if result:
        print(result)
    else:
        print("No matching result")
    print(f"Timer: {round(end-start, 3)}")


# Get a definiton by asking the user Pinyin and Simplified Chinese character input
def get_def_pinyin_simplified(pinyin_input, simplified_input, user_input=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    if user_input == True:
        pinyin_input = input("Input Pinyin: ")
        simplified_input = input("Input Simplified: ")

    start = time.time()
    cursor.execute('SELECT DISTINCT English, Pinyin, Simplified FROM CeDict WHERE Pinyin = ? AND Simplified = ?', (pinyin_input, simplified_input))
    result = cursor.fetchall()
    end = time.time()
    print(result)

    #return a dictionary with key1 being english def and key2 being pinyin
    if result:
        dict_result = {"english": result[0][0], "pinyin": result[0][1], "simplified": result[0][2]}
        return dict_result
    else:
        print("No matching result")
        return False

    print(f"Timer: {round(end-start, 3)}")
    

def main():

    sorted_list = sort_cedict()
    create_cedb(sorted_list)
    remove_duplicate()
    #get_def()
    get_def_pinyin_simplified()

if __name__ == "__main__":
    initiate_cedict()
    main()
