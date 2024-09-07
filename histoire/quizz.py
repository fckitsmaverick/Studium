from questionsHistoire.questionsAntiquite import questionsAntiquite
from questionsHistoire.questionsRevolution import questionsRevolution
from questionsHistoire.questionsMoyenAgeCentral import questionsMoyenAgeCentral
from questionsHistoire.questionsMoyenAgeTardif import questionsMoyenAgeTardif
from questionsHistoire.questionsEpoqueModerne import questionsEpoqueModerne
from questionsHistoire.questionsWW1 import questionsWW1
from questionsHistoire.questionsWW2 import questionsWW2

from questionsHistoire.questionsListe import dq_list_rdf
from database_histoire import update_score_progress, update_question_stats, get_question_stats


from termcolor import cprint

import random
import string
import time

from unidecode import unidecode

scorePlayer1 = 0
scorePlayer2 = 0

general_questions = {

}

general_questions.update(questionsAntiquite)
general_questions.update(questionsRevolution)
general_questions.update(questionsMoyenAgeCentral)
general_questions.update(questionsMoyenAgeTardif)
general_questions.update(questionsEpoqueModerne)
general_questions.update(questionsWW1)
general_questions.update(questionsWW2)

scorePlayer1 = 0

game_choice = input("Choix de la période historique (pour voir l'ensemble des périodes disponibles, tapez 1): ")
if game_choice == 1:
    print("Antiquité, Moyen-Âge Central, Moyen-Âge Tardif, Renaissance, Revolution, WW1, WW2, Général")
    game_choice = input("Choix de la période historique (pour voir l'ensemble des périodes disponibles, tapez 1): ")

game_choice = game_choice.lower()
game_choice = game_choice.translate(str.maketrans('', '', string.punctuation))
game_choice = unidecode(game_choice)

def normalize_ans (ans):
    ans = ans.lower()
    return ans

if game_choice == "general":
    start = time.time()
    bad_ans = {} 
    for i in general_questions:
        question_pick = random.choice(list(general_questions.values()))
        while question_pick.done == 1:
            question_pick = random.choice(list(general_questions.values()))
        if question_pick.done == 0:
            cprint(question_pick.question, "cyan")
            ans = input() 
            ans = normalize_ans(ans)
            if ans == question_pick.answer:
                cprint("Good Answer", "green")
                scorePlayer1 += 1
                update_question_stats(question_pick.question, True)
            else:
                cprint("Bad Answer", "red")
                print(question_pick.answer)
                bad_ans[i] = question_pick
                update_question_stats(question_pick.question, False)
            question_pick.done = 1
            get_question_stats(question_pick.question)
    end = time.time()
    if bad_ans:
        for i in bad_ans:
            cprint(bad_ans[i].question)
            ans = normalize_ans(input())
            if ans == bad_ans[i].answer:
                cprint("Bonne Réponse", "green")
            else:
                cprint("Mauvaise Réponse", "red")
                cprint(bad_ans[i].answer)
    update_score_progress(scorePlayer1, end-start, game_choice)    

if game_choice == "rois de france":
    i = 1
    for key, value in dq_list_rdf["roiDeFrance"].answer.items():
        name = input(f"Nom du Roi {i}: ").lower()
        date = input(f"Dates: ").lower()
        if name == key:
            print("Correct name")
        if date == value:
            print("Correct dates")



print(scorePlayer1, "/", len(general_questions))

#question = random.choice(list(general_questions.values()))
#cprint(question.question, "cyan")

