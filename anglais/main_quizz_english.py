from quizz_functions import def_to_word, french_to_english_word

choice = input("Choose your quizz (dw, fw): ")

if choice == "dw":
    def_to_word(choice, 0, 1001)

if choice == "fw":
    french_to_english_word(choice, 0, 1001)
    