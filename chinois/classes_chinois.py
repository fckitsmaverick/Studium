class Vocabulary:
    def __init__(self, chinese_pinyin, chinese_character, english, difficulty):
        self.chinese_pinyin = chinese_pinyin
        self.chinese_character = chinese_character
        self.english = english
        self.difficulty = difficulty
        self.done = 0
        self.right = 0
        self.wrong = 0
        self.success = 0
    

class Sentences:
    def __init__(self, chinese_pinyin, chinese_character, english):
        self.chinese_pinyin = chinese_pinyin
        self.chinese_character = chinese_character
        self.english = english
        self.done = 0