from questionsHistoire.questionsListe import dq_list_rdf

from termcolor import cprint

game_choice = input("Choix du sujet (Rois de France): ").lower()
if game_choice == 1:
    print("Antiquité, Moyen-Âge Central, Moyen-Âge Tardif, Renaissance, Revolution, WW1, WW2, Général")
    game_choice = input("Choix de la période historique (pour voir l'ensemble des périodes disponibles, tapez 1): ")

if game_choice == "rois de france":
    i = 1
    for key, value in dq_list_rdf["roiDeFrance"].answer.items():
        name = input(f"Nom du Roi {i}: ").lower()
        if name == key:
            print("Nom correct")
        else:
            print(f"Mauvaise réponse, la réponse était {key}")
        date = input(f"Dates: ").lower()
        if date == value:
            cprint("Bonne réponse", "green")
        else:
            cprint(f"Mauvaise réponse, la réponse était {value}", "red")
        if key == "charles iv":
            print("Fin des Capétiens directs")
        if key == "philippe vi":
            print("Début de la branche des Capétiens de Valois")
        i+=1
