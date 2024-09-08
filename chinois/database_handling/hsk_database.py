import sqlite3
import os
import pandas as pd

db_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_handling')
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

    conn.close()


def create_hsk_db():
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #Turn CSV into pandas dataframe
    df_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_handling')
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

    
def get_hsk_level(pinyin_input, simplified_input, user_input=False):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    #If the user ask explicitely for it, otherwise the function is just meant to be called as part of the code
    if user_input = True:
        pinyin_input = input("Pinyin: ")
        simplified_input = input("Simplified: ")

    cursor.execute('SELECT hsk_level, simplified, pinyin, english FROM hsk_vocab WHERE pinyin = ? AND simplified = ?', (pinyin_input, simplified_input))

    result = cursor.fetchall()

    if result:
        #result[0][0] is hsk_level, [0][1] is simplified, [0][2] is pinyin and [0][3] is english
        print(result[0][1], result[0][2])
        #Since we just want the hsk_level we return it
        return result[0][0]
    else:
        print("No result found for this word")
        return False

    conn.close()



def main():
    initiate_hsk_db()
    create_hsk_db()
    get_hsk_level()

if __name__ == "__main__":
    main()