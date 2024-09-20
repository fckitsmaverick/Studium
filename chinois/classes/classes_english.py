class EnglishVocabulary:
    def __init__(self, english_word, english_def, difficulty, category, topic, french_equivalent=""):
        self.english_word = english_word
        self.english_def = english_def
        self.difficulty = difficulty
        self.category = category
        self.topic = topic
        self.french_equivalent = french_equivalent
        self.done = 0
        self.right = 0
        self.wrong = 0
        self.success = 0

