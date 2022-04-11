import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import datetime

import Logic as logic
import DailyWordsTable as dailyWordsTable
from Vocabulary import WordType
from tkinter.messagebox import showwarning
from tkcalendar import DateEntry
# import Outputer as outputer

class WordsTableMaker(tk.Frame):
    
    def __init__(self, logic, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.logic = logic
        self.logic.windows['WORDSTABLEMAKER'] = self
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        parent.title('New Words')
        parent.iconphoto(False, tk.PhotoImage(file='.\\img\\icon_report.png'))
        self.makeWidgets()

    def makeWidgets(self):
        ft = tkFont.Font(size=14, weight=tkFont.BOLD)

        frmTopBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=10, pady=5)
        frmTopBar.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        tk.Label(frmTopBar, font=ft, text='新词数量').pack(side=tk.LEFT)
        self.newChosen = ttk.Combobox(frmTopBar, font=('', 14), width=3)
        self.newChosen['values'] = list(range(0, 21))
        self.newChosen.pack(side=tk.LEFT)
        self.newChosen.current(3)

        tk.Label(frmTopBar, font=ft, text='    ').pack(side=tk.LEFT)

        tk.Label(frmTopBar, font=ft, text='复习数量').pack(side=tk.LEFT)
        self.reviewChosen = ttk.Combobox(frmTopBar, font=('', 14), width=3)
        self.reviewChosen['values'] = list(range(0, 21))
        self.reviewChosen.pack(side=tk.LEFT)
        self.reviewChosen.current(17)

        tk.Label(frmTopBar, font=ft, text='    ').pack(side=tk.LEFT)

        tk.Label(frmTopBar, font=ft, text='日期').pack(side=tk.LEFT)
        self.entDate = DateEntry(frmTopBar, width=10, background='DarkOrange',
                foreground='white', font=ft, date_pattern='yyyy/mm/dd', 
                borderwidth=1)
        self.entDate.pack(side=tk.LEFT)

        # frmTopBar_Scale = tk.Frame(frmTopBar, highlightbackground='Gray', 
                                    # highlightthickness=1, padx=10, pady=5)
        # frmTopBar_Scale.pack(side=tk.RIGHT)
        self.isRandom = False
        # tk.Label(frmTopBar_Scale, font=ft, text='按顺序学习').pack(side=tk.LEFT)
        self.btnMode = tk.Button(frmTopBar, text ='乱序', font=ft, width=7, 
                    fg='black', bg='GhostWhite', relief=tk.RAISED, 
                                                    command=self.onModeChanged)
        self.btnMode.pack(side=tk.RIGHT)
        

        frmNew = tk.Frame(self)
        frmNew.pack(side=tk.TOP, expand=tk.YES)
        self.newS = tk.StringVar()

        frmNew_E = tk.Frame(frmNew, width=20)
        frmNew_E.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=10)
        tk.Label(frmNew_E, font=ft, text='自选新词').pack(side=tk.LEFT)
        self.entNew = tk.Entry(frmNew_E, textvariable=self.newS, font=ft)
        self.entNew.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entNew.bind('<KeyRelease>', 
                          (lambda event: self.onSearchEnter(isNew=True)))

        frmNew_S = tk.Frame(frmNew)
        frmNew_S.grid(row=1, column=0, sticky=tk.EW, padx=10)
        self.lstNew_S = tk.Listbox(frmNew_S, font=ft, selectmode='single', 
                                        height=7, width=35, fg="blue")
        scrNew_S = tk.Scrollbar(frmNew_S)
        scrNew_S.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstNew_S.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lstNew_S.bind('<Double-Button-1>', 
                            (lambda event: self.onWordAdd(isNew=True)))
        scrNew_S.config(command=self.lstNew_S.yview)
        self.lstNew_S.config(yscrollcommand=scrNew_S.set)

        frmNew_B = tk.Frame(frmNew)
        frmNew_B.grid(row=1, column=2, sticky=tk.EW, padx=15)
        tk.Button(frmNew_B, font=ft, text='>>', 
            command=(lambda : self.onWordAdd(isNew=True))).pack(side=tk.TOP)
        # btnNew_Add.pack(side=tk.TOP)
        tk.Button(frmNew_B, font=ft, text='<<', 
            command=(lambda : self.onWordSub(isNew=True))).pack(side=tk.BOTTOM)
        # btnNew_Sub.pack(side=tk.BOTTOM)

        frmNew_C = tk.Frame(frmNew)
        frmNew_C.grid(row=1, column=3, sticky=tk.EW, padx=10)
        self.lstNew_C = tk.Listbox(frmNew_C, font=ft, selectmode='single',
                                        height=7, width=35, fg="blue")
        scrNew_C = tk.Scrollbar(frmNew_C)
        scrNew_C.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstNew_C.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lstNew_C.bind('<Double-Button-1>', 
                            (lambda event: self.onWordSub(isNew=True)))
        scrNew_C.config(command=self.lstNew_C.yview)
        self.lstNew_C.config(yscrollcommand=scrNew_C.set)

        frmReview = tk.Frame(self, pady=10)
        frmReview.pack(side=tk.TOP, expand=tk.YES)
        self.reviewS = tk.StringVar()

        frmReview_E = tk.Frame(frmReview, width=20)
        frmReview_E.grid(row=2, column=0, sticky=tk.EW, padx=10, pady=10)
        tk.Label(frmReview_E, font=ft, text='自选复习').pack(side=tk.LEFT)
        self.entReview = tk.Entry(frmReview_E, textvariable=self.reviewS, font=ft)
        self.entReview.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entReview.bind('<KeyRelease>', 
                                (lambda event: self.onSearchEnter(isNew=False)))

        frmReview_S = tk.Frame(frmReview)
        frmReview_S.grid(row=3, column=0, sticky=tk.EW, padx=10)
        self.lstReview_S = tk.Listbox(frmReview_S, font=ft, selectmode='single', 
                                            height=12, width=35, fg="blue")
        scrReview_S = tk.Scrollbar(frmReview_S)
        scrReview_S.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstReview_S.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lstReview_S.bind('<Double-Button-1>', 
                            (lambda event: self.onWordAdd(isNew=False)))
        scrReview_S.config(command=self.lstReview_S.yview)
        self.lstReview_S.config(yscrollcommand=scrReview_S.set)

        frmReview_B = tk.Frame(frmReview)
        frmReview_B.grid(row=3, column=2, sticky=tk.EW, padx=15)
        tk.Button(frmReview_B, font=ft, text='>>', 
            command=(lambda : self.onWordAdd(isNew=False))).pack(side=tk.TOP)
        # btnReview_Add.pack(side=tk.TOP)
        tk.Button(frmReview_B, font=ft, text='<<', 
            command=(lambda : self.onWordSub(isNew=False))).pack(side=tk.BOTTOM)
        # btneview_Sub.pack(side=tk.BOTTOM)

        frmReview_C = tk.Frame(frmReview)
        frmReview_C.grid(row=3, column=3, sticky=tk.EW, padx=10)
        self.lstReview_C = tk.Listbox(frmReview_C, font=ft, selectmode='single', 
                                        height=12, width=35, fg="blue")
        scrReview_C = tk.Scrollbar(frmReview_C)
        scrReview_C.pack(side=tk.RIGHT, fill=tk.Y)
        self.lstReview_C.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lstReview_C.bind('<Double-Button-1>', 
                            (lambda event: self.onWordSub(isNew=False)))
        scrReview_C.config(command=self.lstReview_C.yview)
        self.lstReview_C.config(yscrollcommand=scrReview_C.set)

        frmBottomBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=10, pady=5)
        frmBottomBar.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)
        tk.Button(frmBottomBar, font=ft, text='生成单词表', bg='DarkOrange', 
            fg='white', command=self.onMakeTable) \
                    .pack(side=tk.TOP, fill=tk.X, expand=True)
    
    def onSearchEnter(self, isNew):
        ent = self.newS if isNew else self.reviewS
        lst = self.lstNew_S if isNew else self.lstReview_S
        sWord = ent.get().strip()
        newList = self.logic.fuzzySearch(sWord)
        lst.delete(0, tk.END)
        for w in newList:
            word = '%s: %s' % (w.word, w.explanation)
            lst.insert(tk.END, word)
    
    def onWordAdd(self, isNew):
        lst_f = self.lstNew_S if isNew else self.lstReview_S
        lst_t = self.lstNew_C if isNew else self.lstReview_C
        seled = lst_f.curselection()
        if len(seled) > 0:
            word = lst_f.get(seled)
            if word not in lst_t.get(0, tk.END):
                lst_t.insert(tk.END, word)

    def onWordSub(self, isNew):
        lst = self.lstNew_C if isNew else self.lstReview_C
        seled = lst.curselection()
        if len(seled) > 0:
            lst.delete(seled)

    def onModeChanged(self):
        if self.btnMode['relief'] == tk.SUNKEN:
            self.btnMode.config(relief=tk.RAISED, fg='black', bg='GhostWhite')
            self.isRandom = False
        else:
            self.btnMode.config(relief=tk.SUNKEN, fg='white', bg='DarkOrange')
            self.isRandom = True
    
    def onMakeTable(self):
        wordsNew = self.getWords(isNew=True)
        wordsReview = self.getWords(isNew=False)
        newNum = int(self.newChosen.get()) - len(wordsNew)
        reviewNum = int(self.reviewChosen.get()) - len(wordsReview)
        date = self.entDate.get_date().strftime("%Y/%m/%d")
        if (len(self.logic.currNewVocabs) > 0 or len(self.logic.currRevVocabs) > 0 ) \
                                    or len(wordsNew) > 0 or len(wordsReview) > 0:
            wordsTable = self.logic.makeWordsTable(wordsNew, wordsReview, 
                                        newNum, reviewNum, self.isRandom, date)
            for w in wordsNew + wordsReview:
                wordsTable[w.word] = w
            # date = datetime.date.today().strftime("%Y/%m/%d")
            # dailyWordsTable.DailyWordsTable_Create(self.logic, self.logic.today, wordsTable)
            dailyWordsTable.DailyWordsTable_Create(self.logic, date, wordsTable)
        else:
            showwarning('注意', '无法生成空白单词表')
    
    def getWords(self, isNew):
        lst = self.lstNew_C if isNew else self.lstReview_C
        res = [self.logic.preciseSearch(w.split(':')[0].strip()) 
                                for w in lst.get(0, tk.END)]
        for w in res:
            w.type = WordType.NEW if isNew else WordType.REVIEW
        return res
    
    def onQuit(self):
        # if 'WORDSTABLEMAKER' in self.logic.windowList:
        self.logic.windows.pop('WORDSTABLEMAKER')

class WordsTableMakerPop(WordsTableMaker):
    def __init__(self, logic, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        WordsTableMaker.__init__(self, logic, parent=self.popup)
        x = self.logic.windows['Root'].winfo_x()
        y = self.logic.windows['Root'].winfo_y()
        self.popup.geometry('+%d+%d' % (x+100, y+100))
        self.popup.deiconify()

    def onQuit(self):
        super().onQuit()
        self.popup.destroy()

def tester():
    # WordsTableMakerPop()
    pass

if __name__ == "__main__":
    root = tk.Tk()
    tk.Button(root, text='tester', command=lambda : tester()).pack(side=tk.LEFT)
    root.mainloop()



