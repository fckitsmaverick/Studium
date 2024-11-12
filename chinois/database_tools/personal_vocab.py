import sqlite3
import os
import sys

from contextlib import contextmanager

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
    from dict_tools.questions_vocabulaire import dq_vocabulary

db_directory = ('/Users/gabriel/Documents/VSCode/Python/Studium/chinois/database_tools')
db_filename = ('personal_vocabulary.db')

db_path = os.path.join(db_directory, db_filename)

def initiate_personal_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS personal_vocab (
            hsk_level INTEGER DEFAULT 1,
            simplified TEXT NOT NULL,
            pinyin TEXT NOT NULL,
            english TEXT NOT NULL,
            category TEXT NOT NULL,
            kind TEXT NOT NULL,
            topic TEXT NOT NULL,
            UNIQUE (simplified, pinyin, english)
        )
    ''')
    
    conn.close()

def add_personal_vocab():
    console = Console()
    console.show_cursor()

    while True:
        pinyin_input = Prompt.ask("[bold yellow]Pinyin: [/bold yellow]")
        simplified_input = Prompt.ask("[bold yellow]Simplified: [/bold yellow]")
        category = Prompt.ask("[bold yellow]Vocabulary or Sentence ?:[/bold yellow]", default="Vocabulary", choices=["Vocabulary", "Sentence"])
        kind = Prompt.ask("[bold yellow]Type of word:[/bold yellow]", default="general", choices=["general", "verb", "grammar"])

        while pinyin_input == "" and simplified_input == "":
            console.print("[bold red]Both fields are empty, please enter a pinyin and a simplified character[/bold red]")

            finished = Prompt.ask("[bold yellow]Do you want to quit ?[/bold yellow]", default="yes", choices=["yes", "no"])
            if finished == "yes": return

            pinyin_input = Prompt.ask("[bold yellow]Pinyin: [/bold yellow]")
            simplified_input = Prompt.ask("[bold yellow]Simplified: [/bold yellow]")

        dict_result = get_def_pinyin_simplified(pinyin_input, simplified_input)
        hsk_dict_result = get_hsk_dict_def(pinyin_input, simplified_input)
        dict_hsk = get_hsk_level(pinyin_input, simplified_input)

        add_topic = Prompt.ask("[bold yellow]Do you want to add a topic ?[/bold yellow]", default="no", choices=["yes", "no"])

        duplicate = False
        #If cedict doesn't have the entries but hsk does use hsk
        if dict_result == False and hsk_dict_result != False:
             dict_result = hsk_dict_result
        

        if dict_result != False:
            for i in dq_vocabulary:
                if dq_vocabulary[i].chinese_character == dict_result["simplified"] and dq_vocabulary[i].chinese_pinyin == dict_result["pinyin"]:
                    console.print("[bold yellow]You already have this word in your personal vocab[/bold yellow]")
                    keep_going = Prompt.ask("[bold yellow]Do you still wish to add it to your dictionnary ?[/bold yellow]", default="no", choices=["yes", "no"])
                    if keep_going == "no": 
                        duplicate = True

        if dict_result != False and duplicate == False: 
            simplified = dict_result["simplified"]
            pinyin = dict_result["pinyin"]
            english = dict_result["english"]

            if dict_hsk != False: hsk_level = dict_hsk["hsk_level"] 
            elif dict_hsk == False: hsk_level = Prompt.ask("[bold yellow]Assign an hsk level (level of difficutly from 1 to 6) to your entry: [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])

            want_to_change = Prompt.ask(f"[bold yellow]Here is the English definition from the dictionnary [bold blue]{english}[/bold blue].\nDo you want to change it ?[/bold yellow]", default="no", choices=["yes", "no"])
            if want_to_change == "yes": 
                english = Prompt.ask("[bold yellow]Enter the new definition: [/bold yellow]")

            if add_topic == "yes":
                topic_pick = Prompt.ask("[bold yellow]Enter the topic (you can add more than one by using ', ' separator): [/bold yellow]")
                topic_pick = topic_pick.split(", ")

            with open("dict_tools/questions_vocabulaire.py", "a") as f:
                print(f'\ndq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level}, category="{category}", kind="{kind}", topic={topic_pick if add_topic == "yes" else []})', file=f)
                console.print("[bold green]New entry in your dictionnary[/bold green]")
                f.close()


        elif dict_result == False:
            console.print("[bold red]Could not find this word in the dictionnary.[/bold red]")
            manual_input = Prompt.ask("[bold yellow]Do you want to manually input the definition ?[/bold yellow]", default="yes", choices=["yes", "no"])

            if manual_input == "yes":

                english = Prompt.ask("[bold yellow]Enter the English definition: [/bold yellow]")
                if add_topic == "yes":
                    topic_pick = Prompt.ask("[bold yellow]Enter the topic (you can add more than one by using ', ' separator): [/bold yellow]")
                    topic_pick = topic_pick.split(", ")

                if dict_hsk != False:
                    hsk_level = dict_hsk["hsk_level"] 
                elif dict_hsk == False:
                    hsk_level = Prompt.ask("[bold yellow]Assign an hsk level (level of difficutly from 1 to 6) to your entry: [/bold yellow]", default=1, choices=["1", "2", "3", "4", "5", "6"])




                with open("dict_tools/questions_vocabulaire.py", "a") as f:
                    print(f'\ndq_vocabulary["{simplified_input}"] = Vocabulary("{pinyin_input}", "{simplified_input}", "{english}", {hsk_level}, category="{category}", kind="{kind}", topic= {topic_pick if add_topic == "yes" else []})', file=f)
                    console.print("[bold green]New entry in your dictionnary[/bold green]")
                    f.close()


        keep_going = Prompt.ask("[bold red]Do you wish to add more vocabulary ?[/bold red]", default="yes", choices=["yes", "no"])

        if keep_going.lower() == "no":
            # Make it restart so that the words added to the dictionnary are taken into account
            console.print("[bold red]Now restarting ... [/bold red]")
            os.execl(sys.executable, sys.executable, *sys.argv)

        #Include it in database
        cursor.execute('''
            INSERT OR IGNORE INTO personal_vocab (hsk_level, simplified, pinyin, english, category, king, topic)
            VALUES (?, ?, ?, ?)
        ''', (hsk_result["hsk_level"], dict_result["simplified"], dict_result["pinyin"], dict_result["english"]))

        cursor.execute('SELECT DISTINCT hsk_level, simplified, pinyin, english FROM personal_vocab WHERE simplified = ? AND pinyin = ?', (simplified_input, pinyin_input))

    conn.commit()
    conn.close()

def populate_personal_vocab():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for key, value in dq_vocabulary.items():
        topic = ""
        for top in value.topic:
            topic += top
            topic += ","

        cursor.execute('''
            INSERT OR IGNORE INTO personal_vocab (hsk_level, simplified, pinyin, english, category, kind, topic)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (value.difficulty, value.chinese_character, value.chinese_pinyin, value.english, value.category, value.kind, topic))
    
    cursor.execute('SELECT * FROM personal_vocab')

    results = cursor.fetchall()
    print(results)
    
    conn.commit()
    conn.close()
 

def main():
    initiate_personal_db()
    populate_personal_vocab()


if __name__ == "__main__":
    main()
