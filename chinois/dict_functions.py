from cedict_database import get_def_pinyin_simplified()



def add_vocabulary(pinyin, simplified, english, hsk_level = 1):
    # word def is either False if there is no corresponding entry in the cedict or a dict{english: , pinyin: }
    word_def = get_def_pinyin_simplified()
    hsk_level = get_hsk_level()

    
    if word_def != False: 
        count = 0
        with open("questions_vocabulaire.py", "a") as f:
            print(f'dq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level})', file=f)
            print("done")