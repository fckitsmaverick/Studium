#1346, pandémie de peste noire
#1492, découverte de l'Amérique

from questionsHistoire.classes import Question

questionsMoyenAgeTardif = {

}

MoyenAgeTardif = "MoyenAgeTardif"

questionsMoyenAgeTardif["batailleAzincourt"] = Question("Date de la bataille d'Azincourt JJ/Mois/AAAA", "25 octobre 1415", "Moyen-Age Tardif", 1)

questionsMoyenAgeTardif["batailleVarna"] = Question("""Quelle est le nom de la bataille qui eut lieu en 1444 et qui permit aux Ottomans 
d'asseoir leur domination sur les Balkans ?""", "bataille de varna", "Moyen-Age Tardif", 1)

questionsMoyenAgeTardif["dateBatailleVarna"] = Question("Date de la bataille de Varna JJ/Mois/AAAA", "10 novembre 1444", "Moyen-Age Tardif", 1)

questionsMoyenAgeTardif["tamerlan"] = Question("Quel est le nom du fondateur de la dynastie des Timourides ?", "tamerlan", "Moyen-Age Tardif", 1) 
questionsMoyenAgeTardif["tamerlan"].add_second_answer("timour")

questionsMoyenAgeTardif["fletrissure"] = Question("Comment était nommé la peine infamante consistant à marquer au fer rouge un condamné sous l'Ancien Régime ?", "flétrissure", "Moyen-Age Tardif", 1)

questionsMoyenAgeTardif["leFou"] = Question("Quel Roi de France est surnommé 'le Fou' ?", "charles vi", MoyenAgeTardif, 1)

questionsMoyenAgeTardif["armagnacs"] = Question("Pendant la guerre civile qui ravage la France au début du 15ème siècle qui s'oppose aux Bourguignons ?", "armagnacs", MoyenAgeTardif, 1)

questionsMoyenAgeTardif["louisIerOrleans"] = Question("Quel prince fut assassiné sur les ordres de Jean sans Peur en 1407 ?", "louis ier d'orléans", MoyenAgeTardif, 1)

questionsMoyenAgeTardif["cabochiens"] = Question("Nom de la révolte parisienne instigué par Jean Sans Peur et impliquant la corporation des bouchers :", "révolte des cabochiens", MoyenAgeTardif, 1)

questionsMoyenAgeTardif["praguerie"] = Question("Quel est le nom de la révolte mené par Louis XI contre son père Charles VII ?", "praguerie", MoyenAgeTardif, 1)



