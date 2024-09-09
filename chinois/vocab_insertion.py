from database_tools.cedict_database import get_def_pinyin_simplified
from dict_tools.questions_vocabulaire import dq_vocabulary
from database_tools.hsk_database import get_hsk_level



def new_vocab_auto():
    while True:
        pinyin_input = input("Pinyin: ")
        simplified_input = input("Simplified: ")

        dict_result = get_def_pinyin_simplified(pinyin_input, simplified_input)
        dict_hsk = get_hsk_level(pinyin_input, simplified_input)
        print(dict_result)
        duplicate = False

        for i in dq_vocabulary:
            if dq_vocabulary[i].chinese_character == dict_result["simplified"] and dq_vocabulary[i].chinese_pinyin == dict_result["pinyin"]:
                print("You already have this word in your personal vocab, quitting...")
                duplicate = True

        if dict_result != False and duplicate == False: 
            simplified = dict_result["simplified"]
            pinyin = dict_result["pinyin"]
            english = dict_result["english"]
            if dict_hsk != False: hsk_level = dict_hsk["hsk_level"] 
            if dict_hsk == False: hsk_level = input("Assign an hsk level (level of difficutly from 1 to 6) to your entry: ")
            with open("dict_tools/questions_vocabulaire.py", "a") as f:
                print(f'dq_vocabulary["{simplified}"] = Vocabulary("{pinyin}", "{simplified}", "{english}", {hsk_level})', file=f)
                print("New entry in your dictionnary")

            keep_going = input("Do you wish to add more vocabulary ?")

            if keep_going.lower() == "no": break
            
        else:
            if duplicate == False: print("No entries found for your input")


if __name__ == "__main__":
    new_vocab_auto()