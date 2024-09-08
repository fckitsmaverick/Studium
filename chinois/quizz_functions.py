from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.database import update_score_progress, update_word_stats, get_word_stats, get_worst_word_ratios
from database_tools.cedict_database import get_def, get_def_pinyin_simplified

from datetime import datetime
from termcolor import cprint

import random
import time
import pandas as pd


score_player_1 = 0
limitation = 10001

bad_ans = {

}

progress = {

}

start = time.time()
count = 0

#ce_dict = create_dict()
#print(ce_dict[0])

#Englisht to Chinese quizz 2 inputs pinyin and chinese character
def ec_quizz(inp, count, limitation):
    score_player_1 = 0

    if inp == "ec":

        for i in dq_vocabulary:
                question_pick = random.choice(list(dq_vocabulary.values()))

                #Pick random new question 
                while question_pick.done == 1:
                    question_pick = random.choice(list(dq_vocabulary.values()))

                if question_pick.done == 0:
                    cprint(question_pick.english, "light_cyan")
                    ans = input() 
                    ans2 = input()

                    if (ans == question_pick.chinese_character and ans2 == question_pick.chinese_pinyin) \
                    or (ans == question_pick.chinese_pinyin and ans2 == question_pick.chinese_character):
                        cprint("Good Answer", "green")
                        score_player_1 += question_pick.difficulty
                        update_word_stats(question_pick.chinese_character, True)

                    else:
                        cprint("Bad Answer", "red")
                        print(question_pick.chinese_character, " ", question_pick.chinese_pinyin)
                        bad_ans[i] = question_pick
                        update_word_stats(question_pick.chinese_character, False)

                    question_pick.done = 1
                    count+=1
                if count >= int(limitation):
                    break

        print(score_player_1)
        #Update Database
        update_score_progress(score_player_1, time.time() - start, inp)

#English to Chinese quizz only one input required to validate the answer (pinyin)
def ecpinyin_quizz(inp, count, limitation):
    score_player_1 = 0
    for i in dq_vocabulary:
        question_pick = random.choice(list(dq_vocabulary.values()))
        
        while question_pick.done == 1:
            question_pick = random.choice(list(dq_vocabulary.values()))

        if question_pick.done == 0:
            cprint(f"{question_pick.english}", "light_magenta")
            ans = input() 

            if (ans == question_pick.chinese_pinyin):
                cprint("Good Answer", "green")
                score_player_1 += question_pick.difficulty
                update_word_stats(question_pick.chinese_character, True)

            else:
                cprint("Bad Answer")
                print(f"{question_pick.chinese_pinyin}, {question_pick.chinese_character}", "red")
                bad_ans[i] = question_pick
                update_word_stats(question_pick.chinese_character, False)

            question_pick.done = 1
            count += 1

        if count >= int(limitation):
            break
            
    score_player_1 = round(score_player_1*0.75)
    update_score_progress(score_player_1, time.time() - start, inp)

#Quizz about the last x entries in the dictionnary, user can choose x
def last_x_quizz(inp, count, limitation):
    x = input("Last x numbers(type x): ")
    update_ratio = input("Do you want to update ratio ?: ")
    x = int(x)
    count = 0
    score_player_1 = 0

    for key, value in dq_vocabulary.items():

        if len(dq_vocabulary) - count <= (x-1):
            question_pick = value
            cprint(f"{question_pick.english}", "light_blue", attrs=["bold"])
            ans = input() 
            result = False

            if (ans == question_pick.chinese_pinyin):
                cprint("Good Answer", "green", attrs=["underline"])
                score_player_1 += question_pick.difficulty
                result = True

            else:
                cprint("Bad Answer")
                cprint(f"{question_pick.chinese_pinyin}, {question_pick.chinese_character}", "red", attrs =["underline"])
                result = False

            if update_ratio.lower() == "yes": update_word_stats(key, result)
            get_word_stats(key, question_pick.chinese_pinyin)
            count += 1
        else:
            count += 1

    score_player_1 = round(score_player_1*0.75)
    update_score_progress(score_player_1, time.time() - start, inp)

#Quizz about the words with the worst ratio of right/wrong answers, user can choose x
def worst_x_quizz(inp, count, limitation):
    user_limit = input("Worst x words (type x): ")
    if user_limit == "": user_limit = 10

    user_limit = int(user_limit)
    score_player_1 = 0
    worst10 = get_worst_word_ratios(user_limit)

    for key, value in dq_vocabulary.items():
        for word in worst10:

            if word["word"] == value.chinese_character:
                cprint(f"{value.english}", "magenta", attrs=["underline"])
                ans = input()

                if ans == value.chinese_pinyin:
                    cprint("Good Answer", "green", attrs=["bold"])
                    score_player_1 += value.difficulty
                    update_word_stats(key, True)

                else:
                    cprint(f"Wrong Answer, {value.chinese_pinyin}, {value.chinese_character}", "red", attrs=["bold"])
                    update_word_stats(key, False)

    score_player_1 = round(score_player_1*0.75)
    update_score_progress(score_player_1, time.time() - start, inp)


#Like ec pinyin but user choose the number of question (x)
def random_x_quizz(inp, count, limitation):
    user_limit = input("Random x numbers of words (type x): ")
    if user_limit == "": user_limit = 10
    user_limit = int(user_limit)
    score_player_1 = 0
    counter = 0

    for key, value in dq_vocabulary.items():
        question_pick = random.choice(list(dq_vocabulary.values()))

        while question_pick.done == 1:
            question_pick = random.choice(list(dq_vocabulary.values()))

        if question_pick.done == 0:
            cprint(question_pick.english, "blue", attrs=["bold"]) 
            ans = input()

            if ans == question_pick.chinese_pinyin or ans == question_pick.chinese_character:
                cprint("Good Answer", "green", attrs=["underline"])
                update_word_stats(key, True)
                score_player_1 += question_pick.difficulty

            else:
                cprint("Wrong Anser", "red", attrs=["underline"])
                cprint(f"{question_pick.chinese_pinyin}, {question_pick.chinese_character}", attrs=["bold"])
                update_word_stats(key, False)

            question_pick.done = 1
        counter += 1 
        if counter >= user_limit: break

    score_player_1 = round(score_player_1*0.75)
    update_score_progress(score_player_1, time.time() - start, inp)



#Chinese to english quizz, doesn't update the stats because checking right answer is too tedious
def ce_quizz(count, limitation):
        for i in dq_vocabulary:

            question_pick = random.choice(list(dq_vocabulary.values()))

            while question_pick.done == 1:
                question_pick = random.choice(list(dq_vocabulary.values()))

            if question_pick.done == 0:
                cprint(f"{question_pick.chinese_character}, {question_pick.chinese_pinyin}", "blue", attrs=["bold"])
                ans = input() 
                cprint(f"{question_pick.english}", "light_green", attrs=["bold"])
                question_pick.done = 1 
                count +=1 
                if count == limitation:
                    break
        return


def use_cedict(user_input):
    # Parse U8 file and return a list of dict with this form {traditional:, simplified:, pinyin:, english:}
    ce_dict = create_dict()

        

def add_vocabulary(pinyin, simplified, english, hsk_level = 1):
    word_def = get_def_pinyin_simplified()

    if word_def != False: 
        count = 0
        with open("questions_vocabulaire.py", "a") as f:
            print(f'dq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level})', file=f)
            print("done")

if __name__ == "__main__":
    add_vocabulary("ran2 hou4", "然后", "and then")

# Ask the def of a word and it will return the matching result (you can ask english, pinyin, simplified or traditional)
#def ask_def():
    # Parse U8 file and return a list of dict with this form {traditional:, simplified:, pinyin:, english:}
    #ce_dict = create_dict()

    #word_asked = input("Definition of:")

    # Implement some kind of search
    #for curr in ce_dict:
    #    if curr["pinyin"] == word_asked or curr["simplified"] == word_asked or curr["traditional"] == word_asked or curr["english"]:
    #    print(f"Definition of {word_asked} is Pinyin: {curr["pinyin"]}, Simplified: {curr["simplified"]}, English: {curr["english"]}")
    


