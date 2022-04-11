import datetime
from enum import Enum
from re import split

class WordType(Enum):
    NEW = 0
    REVIEW = 1
    OTHERS = 9

class Word:
    def __init__(self, word, explanation, newDate=None, reviewDate=None, 
                                            priority=4, wtype=WordType.OTHERS):
        self.word = word
        self.explanation = explanation
        self.newDate = newDate
        self.reviewDate = [] if reviewDate is None else reviewDate
        self.priority = priority
        self.type = wtype

    def clone(self, isCloneReview=False):
        w = Word(self.word, self.explanation, 
                            self.newDate, None, self.priority, self.type)
        if isCloneReview:
            w.reviewDate = self.reviewDate.copy()
        return w

    def setNewDate(self, date=None):
        date = datetime.date.today().strftime("%Y/%m/%d") \
             if date is None else date
        if self.newDate:
            if date < self.newDate:
                self.newDate = date
        else:
           self.newDate = date 

    def removeNewDate(self):
        self.newDate = None 

    def addReviewDate(self, date=None):
        date = datetime.date.today().strftime("%Y/%m/%d") \
             if date is None else date
        if date not in self.reviewDate:
            self.reviewDate.append(date)

    def removeReviewDate(self, date):
        if date in self.reviewDate:
            self.reviewDate.remove(date)

    def getLastReviewDate(self):
        if len(self.reviewDate) > 0:
            self.reviewDate.sort(reverse=True)
            return  self.reviewDate[0]
        else:
            return None

    def getReviewTimes(self):
        return len(self.reviewDate)

    def update(self, explanation, newDate, reviewDate):
        self.explanation = explanation
        if newDate is None:
            self.newDate = None
        else:
            self.newDate = newDate
        self.reviewDate = []
        for r in reviewDate:
            self.addReviewDate(r)

class Vocabulary:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.words = []

    def getCapacity(self):
        return len(self.words)
    
    def deleteWord(self, word):
        if word in self.words:
            self.words.remove(word)

class Vocabulary_Output(Vocabulary):
    def __init__(self, name, description):
        Vocabulary.__init__(self, name, description)
        self.words = {}
        self.alldates = []

class DailyPerformance:
    def __init__(self, date, newWords, reviews):
        self.date = date
        self.newWords = newWords
        self.reviews = reviews
        self.year = date.split('/')[0]
        self.month = date.split('/')[1]
        

    


    # def getProgress(self):
    #     return len([w for w in self.words.values() if w.newDate is not None])

    # def AddWord(self, word):
    #     self.words[word.word] = word

    # def delWord(self, word):
    #     if word.word in self.words.keys():
    #         self.words.pop(word.word)