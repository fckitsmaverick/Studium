from termcolor import cprint

class Question:
    def __init__(self, question, answer, period, score):
        self.question = question
        self.answer = answer
        self.period = period
        self.score = score
        self.done = 0

    def addHint(self, hint):
        self.hint = hint
    
    def add_second_answer(self, answer2):
        self.answer2 = answer2

    def showQuestion(self):
        print(self.question)

class Period:
    def __init__(self, period):
        self.period = period

class QuestionDate:
    def __init__(self, question, first_date, second_date):
        self.question = question
        self.first_date = first_date
        self.second_date = second_date

    def showQuestion(self):
        print(self.question)

class QuestionList:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def append_to_list(self, curr_list, curr_element):
        curr_list = curr_list.append(curr_element)
        return curr_list
    
    def check(self, curr_rank, curr_list, curr_ans, score):
        if curr_list[curr_rank] == curr_ans:
            score += 1
            return 1
        else:
            return 0


        
        


