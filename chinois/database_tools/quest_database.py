import sqlite3
import time

db_directory = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools'
db_filename = 'quest.db'
db_path = os.path.join(db_directory, db_filename)

def initiate_quest_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_quest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL,
            reward INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 0,
            date completed TEXT DEFAULT (DATE('now'))
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS main_quest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT NOT NULL, 
            reward INTEGER NOT NULL,
            completed BOOLEAN DEFAULT 0,
        )
    ''')
    
