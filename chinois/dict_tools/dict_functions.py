from cedict_database import get_def_pinyin_simplified
from questions_vocabulaire import dq_vocabulary



def new_vocab():
    while True:
        pinyin_input = input("Pinyin: ")
        simplified_input = input("Pinyin: ")

        dict_result = get_def_pinyin_simplified(pinyin_input, simplified_input)

        if dict_result: 
            ans = input()
            with open("questions_vocabulaire.py", "a") as f:
                print(f'dq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level})', file=f)
                print("New entry in your dictionnary")

            keep_going = input("Do you wish to add more vocabulary ?")

            if keep_going.lower() == "no": break


