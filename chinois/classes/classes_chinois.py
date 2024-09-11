class Vocabulary:
    def __init__(self, chinese_pinyin, chinese_character, english, difficulty, category="Vocabulary", kind="general", topic=""):
        self.chinese_pinyin = chinese_pinyin
        self.chinese_character = chinese_character
        self.english = english
        self.difficulty = difficulty
        self.category = category
        self.kind = kind
        self.topic = topic
        self.done = 0
        self.right = 0
        self.wrong = 0
        self.success = 0
    
