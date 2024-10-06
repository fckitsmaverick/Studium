import sqlite3
import os
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

console = Console()

db_directory = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools'
db_filename = 'quest.db'
db_path = os.path.join(db_directory, db_filename)

# Initialize database and create quest tables if they don't exist
def initialize_quests_db():
    conn = sqlite3.connect(db_path)  # Path to your quest database
    cursor = conn.cursor()
    
    # Create the permanent_quests table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS permanent_quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        goal INTEGER NOT NULL,
        progress INTEGER NOT NULL DEFAULT 0,
        reward INTEGER NOT NULL,
        completed INTEGER NOT NULL DEFAULT 0
    )
    ''')

    # Create the daily_quests table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_quests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT NOT NULL,
        goal INTEGER NOT NULL,
        progress INTEGER NOT NULL DEFAULT 0,
        reward INTEGER NOT NULL,
        completed INTEGER NOT NULL DEFAULT 0,
        date_assigned DATE NOT NULL
    )
    ''')

    conn.commit()
    conn.close()



# Function to add a quest
def add_quest(quest_type, description, goal, reward):
    conn = sqlite3.connect(db_path)  # Consistent DB path
    cursor = conn.cursor()

    if quest_type == 'permanent':
        cursor.execute('''
        INSERT INTO permanent_quests (description, goal, reward, completed)
        VALUES (?, ?, ?, 0)
        ''', (description, goal, reward))
    
    elif quest_type == 'daily':
        cursor.execute('''
        INSERT INTO daily_quests (description, goal, reward, date_assigned, completed)
        VALUES (?, ?, ?, date('now'), 0)
        ''', (description, goal, reward))
    
    conn.commit()
    conn.close()
    console.print(f'Quest "{description}" added successfully!', style="bold green")

# Function to update quest progress
def update_quest_progress(quest_type, quest_id, increment):
    reset_daily_quests()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update progress for the quest
    if quest_type == 'permanent':
        cursor.execute('''
        UPDATE permanent_quests 
        SET progress = progress + ?
        WHERE id = ? AND completed = 0
        ''', (increment, quest_id))
    
    elif quest_type == 'daily':
        cursor.execute('''
        UPDATE daily_quests 
        SET progress = progress + ?
        WHERE id = ? AND completed = 0 AND date_assigned = date('now')
        ''', (increment, quest_id))

    # Fetch quest details to check if the quest is now complete
    cursor.execute(f'''
    SELECT progress, goal, reward FROM {quest_type}_quests WHERE id = ?
    ''', (quest_id,))
    quest = cursor.fetchone()
    
    if quest[0] >= quest[1]:  # If progress >= goal
        reward = quest[2]  # Fetch the reward
        
        # Mark the quest as completed
        cursor.execute(f'''
        UPDATE {quest_type}_quests 
        SET completed = 1 
        WHERE id = ?
        ''', (quest_id,))
        
        # Add the reward to the user's Experience in quizz_progress.db
        add_reward_to_experience(reward)

        console.print(f'Quest {quest_id} completed! You earned {reward} Experience points!', style="bold green")
    
    conn.commit()
    conn.close()



# Function to display all active quests
def display_active_quests():
    conn = sqlite3.connect(db_path)  # Consistent DB path
    cursor = conn.cursor()

    # Fetch active permanent quests
    cursor.execute('''
    SELECT id, description, goal, progress, reward, completed FROM permanent_quests WHERE completed = 0
    ''')
    permanent_quests = cursor.fetchall()

    # Fetch active daily quests for today
    cursor.execute('''
    SELECT id, description, goal, progress, reward, completed FROM daily_quests 
    WHERE completed = 0 AND date_assigned = date('now')
    ''')
    daily_quests = cursor.fetchall()

    conn.close()

    # Creating a rich table to display the quests
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Type")
    table.add_column("Description")
    table.add_column("Goal")
    table.add_column("Progress")
    table.add_column("Reward")

    # Add permanent quests to the table
    for quest in permanent_quests:
        table.add_row(str(quest[0]), "Permanent", quest[1], str(quest[2]), str(quest[3]), str(quest[4]))

    # Add daily quests to the table
    for quest in daily_quests:
        table.add_row(str(quest[0]), "Daily", quest[1], str(quest[2]), str(quest[3]), str(quest[4]))

    # Display the table
    console.print(table)


# Function to add a quest with user input using rich prompts
def add_quest_with_input():
    # Ask for quest type (either permanent or daily)
    quest_type = Prompt.ask("What type of quest would you like to add?", choices=["permanent", "daily"])
    
    # Ask for the quest description
    description = Prompt.ask("Please enter a description for the quest")
    
    # Ask for the goal (as an integer)
    while True:
        try:
            goal = int(Prompt.ask("What is the goal of the quest (numeric)?"))
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number for the goal.[/bold red]")

    # Ask for the reward (as an integer)
    while True:
        try:
            reward = int(Prompt.ask("What is the reward for completing the quest (numeric)?"))
            break
        except ValueError:
            console.print("[bold red]Please enter a valid number for the reward.[/bold red]")

    # Call the add_quest function to insert the quest into the database
    add_quest(quest_type, description, goal, reward)

    console.print(f'[bold green]Quest "{description}" has been successfully added![/bold green]')

def reset_daily_quests():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Update all daily quests by resetting progress and setting date_assigned to today
    cursor.execute('''
    UPDATE daily_quests 
    SET progress = 0, date_assigned = date('now')
    WHERE date_assigned != date('now')
    ''')
    
    conn.commit()
    conn.close()
    console.print("[bold yellow]Daily quests have been reset for today.[/bold yellow]")

def add_reward_to_experience(reward):
    db_path_quizz_progress = '/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools/quizz_progress.db'  # Path to your quizz progress database
    conn = sqlite3.connect(db_path_quizz_progress)
    cursor = conn.cursor()

    # Ensure the experience table exists (assuming 'Experience' is part of a progress table)
    cursor.execute('SELECT Experience FROM OverallProgress')
    result = cursor.fetchone()

    if result is None:
        console.print("No Experience field found.", style="bold red")
    else:
        current_experience = result[0]
        new_experience = current_experience + reward
        cursor.execute('UPDATE OverallProgress SET Experience = ? WHERE id = 1', (new_experience,))  # Assuming there's only one user
        console.print(f"[bold green]You just finished a quest ! You earned experience: Previous Experience: {current_experience}, New Experience: {new_experience}[/bold green]")

    conn.commit()
    conn.close()


# Example of calling the function to add a quest and initialize the database
if __name__ == "__main__":
    initialize_quests_db()
    display_active_quests()
    add_quest_with_input()
