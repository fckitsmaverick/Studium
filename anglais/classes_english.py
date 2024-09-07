class Vocabulary:
    def __init__(self, english_word, english_def, difficulty):
        self.english_word = english_word
        self.english_def = english_def
        self.french_def = french_def
        self.difficulty = difficulty
        self.done = 0
        self.right = 0
        self.wrong = 0
        self.success = 0

class VocabularyFrench:
    def __init__(self, english_word, french_equivalent, difficulty):
        self.english_word = english_word
        self.french_equivalent = french_equivalent
        self.difficulty = difficulty
        self.french_definition = ""
        self.done = 0
        self.right = 0
        self.wrong = 0
        self.success = 0
