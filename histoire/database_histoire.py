import sqlite3

dic_titre = {
    500: "Mangeur de feutres",
    800: "Coureuse de rempart",
    1200: "Aliboron",
    2000: "Nodocéphale",
    2800: "Joueur de flûte",
    3800: "Tête de pipe",
    5000: "Bêcheur d'eau",
    6500: "Prototype",
    8200: "Pompe à vélo",
    10000: "Pingouin",
    12000: "Mi-Cuit",
    15000: "Champion du Monde",
    19000: "Grand Vizir",
    24000: "Castafiore",
    30000: "Tournesol",
    40000: "Haddock",
    53000: "Tintin",
    68000: "Pithivier",
    80000: "Chaudard",
    100000: "Matteo Ricci"
}

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('histoire_progress.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table to track quiz scores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS QuizzScores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Score INTEGER NOT NULL,
        Time INTEGER NOT NULL,
        Type VARCHAR(255) NOT NULL
    )
''')

# Create a table to track overall progress
cursor.execute('''
    CREATE TABLE IF NOT EXISTS OverallProgress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Experience INTEGER NOT NULL,
        Titre VARCHAR(255) NOT NULL, 
        Prestige INTEGER NOT NULL
    )
''')

# Create a tble to track right and wrong answer
cursor.execute('''CREATE TABLE IF NOT EXISTS SuccessRate (
                    question TEXT PRIMARY KEY,
                    right_count INTEGER DEFAULT 0,
                    wrong_count INTEGER DEFAULT 0,
                    ratio REAL DEFAULT 0.0
                    )''')

# Step 1: Check if the OverallProgress table is empty
cursor.execute('SELECT COUNT(*) FROM OverallProgress')
count = cursor.fetchone()[0]

# Step 2: Insert a new record only if the table is empty
if count == 0:
    # Define the initial values you want to insert
    experience = 0
    prestige = 0
    titre = "Mangeur de feutres"
    
    cursor.execute('''
        INSERT INTO OverallProgress (Experience, Titre, Prestige)
        VALUES (?, ?, ?)
    ''', (experience, titre, prestige))

# Commit the changes
conn.commit()


# Connect to SQLite database (or create it if it doesn't exist)
def update_score_progress(score, time, mode):
    conn = sqlite3.connect('histoire_progress.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()


    # Example: Inserting sample data into QuizScores table
    cursor.execute('''
        INSERT INTO QuizzScores (Score, Time, Type)
        VALUES (?, ?, ?)
    ''', (score, time, mode))

    # Execute the SELECT statement to retrieve values where id = 1
    cursor.execute('''
        SELECT Experience, Titre, Prestige FROM OverallProgress WHERE id = 1
    ''')

    # Fetch the result
    result = cursor.fetchone()

    curr_experience = 0
    titre = ""

    # Check if the result is found and store the values in variables
    if result:
        print(result[0], result[1], result[2])
        curr_experience = result[0]
        titre = result[1]
        prestige = result[2]
        new_experience = (curr_experience + score)
        new_titre = titre
        for key, value in dic_titre.items():
            if new_experience >= key:
                new_titre = value
        # Step 4: Update the Experience and Titre in the database
        if new_experience != curr_experience:
            cursor.execute('''
            UPDATE OverallProgress
            Set Experience = ?
            WHERE id = ?
            ''', (new_experience, 1))

        if new_experience != curr_experience and new_titre != titre:
            cursor.execute('''
                UPDATE OverallProgress
                SET Experience = ?, Titre = ?
                WHERE id = ?
            ''', (new_experience, new_titre, 1))
            print(f"New title ! {new_titre}, experience: {curr_experience}")
            titre = new_titre
        

        # Commit the changes
        conn.commit()

        print(f"Current Stats - Experience: {new_experience}, Progress: {new_experience-curr_experience} Titre: {new_titre}, Prestige: {prestige}")
    else:
        print("No record found with ID 1.")


def update_question_stats(question, is_correct):
    conn = sqlite3.connect('histoire_progress.db')
    cursor = conn.cursor()

    # Check if the question exists in the table
    cursor.execute('SELECT right_count, wrong_count FROM SuccessRate WHERE question = ?', (question,))
    result = cursor.fetchone()

    if result:
        right_count, wrong_count = result
        if is_correct:
            right_count += 1
        else:
            wrong_count += 1
    else:
        # Initialize counts based on whether the answer is correct or not
        right_count = 1 if is_correct else 0
        wrong_count = 1 if not is_correct else 0

    # Calculate the ratio
    if wrong_count == 0:  # Handle the case with only correct answers
        ratio = 100.0
    else:
        ratio = (right_count / (right_count + wrong_count)) * 100

    # Update or insert the question statistics in the SuccessRate table
    if result:
        cursor.execute('''UPDATE SuccessRate 
                          SET right_count = ?, wrong_count = ?, ratio = ?
                          WHERE question = ?''', (right_count, wrong_count, ratio, question))
    else:
        cursor.execute('''INSERT INTO SuccessRate (question, right_count, wrong_count, ratio)
                          VALUES (?, ?, ?, ?)''', (question, right_count, wrong_count, ratio))

    conn.commit()
    conn.close()


def get_question_stats(question):
    conn = sqlite3.connect('histoire_progress.db')
    cursor = conn.cursor()

    cursor.execute('SELECT right_count, wrong_count, ratio FROM SuccessRate WHERE question = ?', (question,))
    result = cursor.fetchone()

    conn.close()
    if result:
        right_count, wrong_count, ratio = result
        print(f"Word: '{question}' - Right: {right_count}, Wrong: {wrong_count}, Ratio: {ratio}")
    else:
        print(f"Word: '{question}' not found in the database.")

def get_worst_question_ratios(limit=10):
    # Connect to the SQLite database
    conn = sqlite3.connect('histoire_progress.db')
    cursor = conn.cursor()

    # Retrieve the questions with the worst ratios
    cursor.execute('''
        SELECT question, right_count, wrong_count, ratio
        FROM SuccessRate
        ORDER BY ratio ASC
        LIMIT ?
    ''', (limit,))

    results = cursor.fetchall()

    conn.close()

    # Store the results in variables
    worst_questions = [{"question": question, "right_count": right_count, "wrong_count": wrong_count, "ratio": ratio}
                   for question, right_count, wrong_count, ratio in results]

    return worst_questions


cursor.execute('SELECT * FROM OverallProgress')
overall_progress = cursor.fetchall()

# Display the results

# Close the connection
conn.close()
