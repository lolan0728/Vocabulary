import tkinter as tk
from tkinter.constants import TRUE
import tkinter.font as tkFont
from tkinter import ttk
from tkcalendar import DateEntry
import datetime

import Logic as logic
import DailyWordsTable as dailyWordsTable
from tkinter.messagebox import askyesno
from Vocabulary import WordType
from tkinter.messagebox import showwarning
from tkinter.simpledialog import askstring
# import Outputer as outputer

class WordsProfile(tk.Frame):
    
    def __init__(self, logic, w, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.logic = logic
        self.word = self.logic.getWordInfo(w, isCloneReview=True)
        self.reviewsEntry = []
        self.ft = tkFont.Font(size=14)
        parent.title('Words Profile')
        parent.iconphoto(False, tk.PhotoImage(file='Vocabulary\\img\\icon_report.png'))
        self.makeWidgets()

    def makeWidgets(self):

        frmTop = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=2, pady=2)
        frmTop.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        tk.Label(frmTop, font=self.ft, text='单词', anchor=tk.NW) \
                                .grid(row=0, column=0, sticky=tk.EW, pady=2)
        tk.Label(frmTop, font=('', 16, tkFont.BOLD), 
                        text=self.word.word, anchor=tk.NW, fg="blue") \
                                .grid(row=0, column=1, sticky=tk.EW, pady=2) 
        
        tk.Label(frmTop, font=self.ft, text='中文解释', anchor=tk.NW) \
                                .grid(row=1, column=0, sticky=tk.EW, pady=2)
        self.explanation = tk.StringVar()
        self.explanation.set(self.word.explanation)
        self.entExp = tk.Entry(frmTop, textvariable=self.explanation, 
                                                    font=self.ft, width=25)
        self.entExp.grid(row=1, column=1, sticky=tk.EW, pady=2)

       
        self.newDate = tk.StringVar()
        self.newDate.set(self.word.newDate if self.word.newDate is not None else '')
        tk.Label(frmTop, font=self.ft, text='学习日期', anchor=tk.NW) \
                                .grid(row=2, column=0, sticky=tk.EW, pady=2)
        self.entNewDate = tk.Entry(frmTop, textvariable=self.newDate, 
                                                    font=self.ft, width=25)
        # self.entNewDate = DateEntry(frmTop, width=12, 
        #         background='DarkOrange', foreground='white', 
        #         font=self.ft, date_pattern='yyyy/mm/dd', borderwidth=2)
        # self.entNewDate.set_date(self.word.newDate)
        self.entNewDate.grid(row=2, column=1, sticky=tk.EW, pady=2)
        
        
        frmReview = tk.Frame(frmTop, highlightbackground='Gray', 
                                                        highlightthickness=1)
        frmReview.grid(row=4, column=0, columnspan=2, pady=2) 
        
        self.canvas = tk.Canvas(frmReview, borderwidth=0, width=310, height=200)
        vbar = tk.Scrollbar(frmReview)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.canvas.config(yscrollcommand=vbar.set)
        vbar.config(command=self.canvas.yview)

        self.drawCanvas()
        
        frmBottomBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1)
        frmBottomBar.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        tk.Button(frmBottomBar, font=tkFont.Font(weight=tkFont.BOLD), fg='white', 
            text='添加复习日期', bg='Blue', command=self.onInsReviewDate) \
                    .pack(side=tk.TOP, fill=tk.X, expand=True)
        tk.Button(frmBottomBar, font=tkFont.Font(weight=tkFont.BOLD), text='保存', 
            bg='DarkOrange', fg='white', command=self.onSave) \
                    .pack(side=tk.TOP, fill=tk.X, expand=True, pady=3)
        tk.Button(frmBottomBar, font=tkFont.Font(weight=tkFont.BOLD), text='删除', 
            bg='Red', fg='white', command=self.onDelete) \
                    .pack(side=tk.TOP, fill=tk.X, expand=True, pady=10)

    def onDelReviewDate(self, date):
        self.word.removeReviewDate(date)
        self.drawCanvas()

    def onInsReviewDate(self):
        date = askstring('Words Profile', '复习日期(yyyy/MM/dd)')
        if date is not None:
            if self.logic.isVaildDate(date):
                self.word.addReviewDate(date)
                self.drawCanvas()
            else:
                showwarning('注意', '请输入正确的日期', parent=self)
    
    def drawCanvas(self):

        self.canvas.delete("all")
        self.word.reviewDate.sort()

        rowpos = 1
        lbl =  tk.Label(self.canvas, font=self.ft, text='复习日期', anchor=tk.NW)
        self.canvas.create_window(1, rowpos, anchor=tk.NW, window=lbl)
        rowpos += 31

        for r in self.word.reviewDate:
            lbl =  tk.Label(self.canvas, font=self.ft, text=r, anchor=tk.NW)
            self.canvas.create_window(1, rowpos, anchor=tk.NW, window=lbl)

            btn = tk.Button(self.canvas, font=tkFont.Font(size=12), text='删除',
                            command=(lambda date=r: self.onDelReviewDate(date)))
            
            self.canvas.create_window(110, rowpos, anchor=tk.NW, window=btn)
            rowpos += 31
        
        fullsize = (0, 0, 310, rowpos)
        self.canvas.config(scrollregion=fullsize)

    def onSave(self):
        newdate = self.newDate.get()
        # newdate = self.entNewDate.get_date().strftime("%Y/%m/%d")
        explanation = self.explanation.get()
        if len(newdate.strip()) > 0:
            if not self.logic.isVaildDate(newdate):
                showwarning('注意', '请输入正确的日期', parent=self)
                return False
        else:
            newdate = None
        self.logic.uniVocabulary[self.word.word].update(explanation,
                                                newdate, self.word.reviewDate)
        self.logic.saveAll()
        self.logic.windows['WORDSEARCHER'].onSearchEnter()
        self.logic.windows['MAIN'].setVocabList()
        return True

    def onDelete(self):
        if askyesno('注意', '确认删除？'):
            self.logic.delWordFromAll(self.word.word)
            self.logic.windows['WORDSEARCHER'].onSearchEnter()
            self.logic.windows['MAIN'].setVocabList()
            return True

class WordsProfilePop(WordsProfile):
    def __init__(self, logic, w, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        WordsProfile.__init__(self, logic, w, parent=self.popup)
        x = self.logic.windows['Root'].winfo_x()
        y = self.logic.windows['Root'].winfo_y()
        self.popup.geometry('+%d+%d' % (x+100, y+100))
        self.popup.deiconify()

    def onSave(self):
        if WordsProfile.onSave(self):
          self.popup.destroy()

    def onDelete(self):
        if WordsProfile.onDelete(self):
          self.popup.destroy()




