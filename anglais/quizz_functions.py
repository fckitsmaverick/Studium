from questions_vocabulaire import d_voc, d_voc_french
from database_english import update_score_progress, update_word_stats, get_word_stats, get_worst_word_ratios

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

#Englisht to Chinese quizz 2 inputs pinyin and chinese character
def def_to_word(inp, count, limitation):
    score_player_1 = 0
    count = 0
    limitation = 1001

    if inp == "dw":

        for i in d_voc:
                question_pick = random.choice(list(d_voc.values()))

                #Pick random new question 
                while question_pick.done == 1:
                    question_pick = random.choice(list(d_voc.values()))

                if question_pick.done == 0:
                    cprint(question_pick.english_def, "light_cyan")
                    ans = input() 

                    if (ans == question_pick.english_word):
                        cprint("Good Answer", "green")
                        score_player_1 += question_pick.difficulty
                        update_word_stats(question_pick.english_word, True)

                    else:
                        cprint("Bad Answer", "red")
                        print(question_pick.english_word)
                        bad_ans[i] = question_pick
                        update_word_stats(question_pick.english_word, False)

                    question_pick.done = 1
                    count+=1
                if count >= int(limitation):
                    break

        print(score_player_1)
        #Update Database
        update_score_progress(score_player_1, time.time() - start, inp)

#English to Chinese quizz only one input required to validate the answer (pinyin)
def french_to_english_word (inp, count, limitation):

    score_player_1 = 0

    for i in d_voc:
        question_pick = random.choice(list(d_voc.values()))
        
        while question_pick.done == 1:
            question_pick = random.choice(list(d_voc.values()))

        if question_pick.done == 0:
            cprint(f"{question_pick.french_equivalent}", "light_magenta")
            ans = input() 

            if (ans == question_pick.english_word):
                cprint("Good Answer", "green")
                score_player_1 += question_pick.difficulty
                update_word_stats(question_pick.english_word, True)

            else:
                cprint("Bad Answer")
                cprint(f"{question_pick.english_word}", "red")
                bad_ans[i] = question_pick
                update_word_stats(question_pick.english_word, False)

            question_pick.done = 1
            count += 1

        if count >= int(limitation):
            break
            
    score_player_1 = round(score_player_1)
    update_score_progress(score_player_1, time.time() - start, inp)

#Quizz about the last x entries in the dictionnary, user can choose x
def last_x_quizz(inp, count, limitation):
    x = input("Last x numbers(type x): ")
    x = int(x)
    count = 0
    score_player_1 = 0

    for key, value in dq_vocabulary.items():

        if len(dq_vocabulary) - count <= (x-1):
            question_pick = value
            cprint(f"{question_pick.english}", "light_blue", attrs=["bold"])
            ans = input() 

            if (ans == question_pick.chinese_pinyin):
                cprint("Good Answer", "green", attrs=["underline"])
                score_player_1 += question_pick.difficulty
                update_word_stats(key, True)

            else:
                cprint("Bad Answer")
                cprint(f"{question_pick.chinese_pinyin}, {question_pick.chinese_character}", "red", attrs =["underline"])
                update_word_stats(key, False)
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
