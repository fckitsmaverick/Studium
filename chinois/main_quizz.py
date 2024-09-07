from questions_vocabulaire import dq_vocabulary
from database import update_score_progress
from quizz_functions import ec_quizz, ecpinyin_quizz, last_x_quizz, worst_x_quizz, random_x_quizz, ce_quizz

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


inp = input("Choice of the quizz (ec, ce, ec pinyin, timed, last x, worst x, random x): " )


start = time.time()
count = 0


if inp == "ec":
    ec_quizz(inp, count, limitation)

elif inp == "ce":
    ce_quizz(count, limitation)


elif inp == "ec pinyin":
    ecpinyin_quizz(inp, count, limitation)

elif inp == "last x":
    last_x_quizz(inp, count, limitation)

elif inp == "worst x":
    worst_x_quizz(inp, count, limitation)

elif inp == "random x":
    random_x_quizz(inp, count, limitation)





elif inp == "timed":
    start_timer = time.time()
    end_timer = 0
    counter = 0
    for i in dq_vocabulary:
        question_pick = random.choice(list(dq_vocabulary.values()))
        while question_pick.done == 1:
            question_pick = random.choice(list(dq_vocabulary.values()))
        if question_pick.done == 0:
            cprint(f"{question_pick.english}", "light_magenta")
            ans = input() 
            if (ans == question_pick.chinese_pinyin):
                cprint("Good Answer", "green")
                score_player_1 += 1
            #if ans2 == question_pick.chinese_pinyin or ans2 == question_pick.chinese_character:
                #cprint("Good Answer", "green")
            else:
                cprint("Bad Answer")
                print(question_pick.chinese_pinyin  , question_pick.chinese_character, "red")
                bad_ans[i] = question_pick
            question_pick.done = 1
            end_timer = time.time()
            if end_timer - start_timer > 60:
                print(score_player_1)
                break 



final_timer = time.time() - start

print(f"Score: {score_player_1}, Total length: {len(dq_vocabulary)}, Final timer: {int(final_timer)}")