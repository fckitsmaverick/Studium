import sqlite3
import time

from parser import create_dict

conn = sqlite3.connect("cedict.db")

cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS CeDict (
        Pinyin VARCHAR(255) NOT NULL,
        English VARCHAR(255) NOT NULL,
        Simplified VARCHAR(255) NOT NULL,
        Traditional VARCHAR(255)
    )
''')

# Create the dictionnary database
def create_cedb(ce_d):

    conn = sqlite3.connect("cedict.db")

    cursor = conn.cursor()

    for curr in ce_d:
        
        cursor.execute('''
            INSERT INTO CeDict (Pinyin, English, Simplified, Traditional)
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
    conn = sqlite3.connect("cedict.db")
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
    conn = sqlite3.connect("cedict.db")
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
def get_def_pinyin_simplified():
    conn = sqlite3.connect("cedict.db")
    cursor = conn.cursor()

    pinyin = input("Input Pinyin: ")
    simplified = input("Input Simplified: ")
    start = time.time()

    cursor.execute('SELECT DISTINCT English, Pinyin FROM CeDict WHERE Pinyin = ? AND Simplified = ?', (pinyin, simplified))
    result = cursor.fetchall()
    end = time.time()

    if result:
        dict_result = {"english": result[0][0], "pinyin": result[0][1]}
        print(dict_result)
        #dict_result = {key:value for(key, value) in result.items()}
        #print(dict_result)
        return result
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
    main()
