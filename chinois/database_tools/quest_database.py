import sqlite3
from datetime import date

# Global variable to track the player's total points
total_points = 0

# Function to create and close a database connection
def open_connection():
    return sqlite3.connect('quests.db')

# Create tables if they don't exist
def create_tables():
    conn = open_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            goal INTEGER,        -- Number of questions to complete
            reward INTEGER,      -- Points rewarded upon completion
            completed BOOLEAN    -- Indicates if the quest is completed
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quest_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quest_id INTEGER,     -- ID of the quest
            progress INTEGER,     -- Number of questions completed so far
            FOREIGN KEY (quest_id) REFERENCES quests(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quest_reset_date (
            id INTEGER PRIMARY KEY,
            last_reset DATE       -- Stores the date when quests were last reset
        )
    ''')

    conn.commit()
    conn.close()

# Function to reset quests and progress
def reset_quests():
    conn = open_connection()
    cursor = conn.cursor()

    # Reset all quests to not completed
    cursor.execute('UPDATE quests SET completed = 0')

    # Reset all quest progress
    cursor.execute('DELETE FROM quest_progress')

    # Add new quests if none exist
    cursor.execute('SELECT COUNT(*) FROM quests')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO quests (description, goal, reward, completed)
            VALUES ("Complete 10 questions", 10, 50, 0),
                   ("Complete 20 questions", 20, 100, 0),
                   ("Complete 50 questions", 50, 200, 0)
        ''')

    conn.commit()
    conn.close()

# Function to initialize quests and reset if it's a new day
def initialize_quests():
    conn = open_connection()
    cursor = conn.cursor()

    # Get the current date
    today = date.today().isoformat()

    # Check the last reset date
    cursor.execute('SELECT last_reset FROM quest_reset_date WHERE id = 1')
    result = cursor.fetchone()

    if result is None:  # If no reset date exists, set it to today and reset quests
        cursor.execute('INSERT INTO quest_reset_date (id, last_reset) VALUES (1, ?)', (today,))
        reset_quests()
    else:
        last_reset = result[0]
        if last_reset != today:
            reset_quests()
            cursor.execute('UPDATE quest_reset_date SET last_reset = ? WHERE id = 1', (today,))

    conn.commit()
    conn.close()

# Function to update quest progress after completing a set of quiz questions
def update_quest_progress(questions_answered):
    conn = open_connection()
    cursor = conn.cursor()

    # Get all active (not completed) quests
    cursor.execute('SELECT id, goal, reward FROM quests WHERE completed = 0')
    quests = cursor.fetchall()

    for quest_id, goal, reward in quests:
        # Get current progress for the quest
        cursor.execute('SELECT progress FROM quest_progress WHERE quest_id = ?', (quest_id,))
        progress_result = cursor.fetchone()

        if progress_result:
            current_progress = progress_result[0]
        else:
            current_progress = 0

        # Update the progress
        new_progress = current_progress + questions_answered
        cursor.execute('''
            INSERT OR REPLACE INTO quest_progress (quest_id, progress)
            VALUES (?, ?)
        ''', (quest_id, new_progress))

        # Check if the quest is completed
        if new_progress >= goal:
            reward_points = complete_quest(quest_id, reward)
            # Update the player's total points
            global total_points
            total_points += reward_points
            print(f"Total points: {total_points}")

    conn.commit()
    conn.close()

# Function to complete a quest and return reward points
def complete_quest(quest_id, reward):
    conn = open_connection()
    cursor = conn.cursor()

    cursor.execute('UPDATE quests SET completed = 1 WHERE id = ?', (quest_id,))
    print(f"Quest {quest_id} completed! You've earned {reward} points.")
    
    conn.commit()
    conn.close()

    # Return the reward points to update total score
    return reward

# Function to check if a specific quest is completed (optional)
def is_quest_completed(quest_id):
    conn = open_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT completed FROM quests WHERE id = ?', (quest_id,))
    result = cursor.fetchone()

    if result:
        completed = result[0]
        status = "completed" if completed else "not completed"
        print(f"Quest {quest_id} is {status}.")
    else:
        print(f"Quest {quest_id} does not exist.")

    conn.close()

# Example usage: Simulate running a quiz and answering a set of questions
def run_quiz():
    # Simulate completing 10 questions in a quiz
    questions_answered = 10

    # Update quest progress based on the number of questions completed
    update_quest_progress(questions_answered)

if __name__ == "__main__":
    # Initialize tables and quests on program startup
    create_tables()
    initialize_quests()

    # Check all quests' status after the quiz
    is_quest_completed(1)
    is_quest_completed(2)
