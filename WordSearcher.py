import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import datetime

import Logic as logic
import WordsProfile as wp

class WordSearcher(tk.Frame):

    def __init__(self, logic, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.logic = logic
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        self.logic.windows['WORDSEARCHER'] = self
        parent.title('Word Searcher')
        parent.iconphoto(False, tk.PhotoImage(file='Vocabulary\\img\\icon_report.png'))
        self.makeWidgets()

    def makeWidgets(self):
        ft = tkFont.Font(size=14, weight=tkFont.BOLD)

        frm = tk.Frame(self)
        frm.pack(side=tk.TOP, expand=tk.YES, pady=10)

        self.newS = tk.StringVar()

        # frmNew_E = tk.Frame(frmNew, width=20)
        # frmNew_E.grid(row=0, column=0, sticky=tk.EW, padx=10, pady=5)
        tk.Label(frm, font=ft, text='搜索') \
                        .grid(row=0, column=0, sticky=tk.EW, padx=5)
        self.ent = tk.Entry(frm, textvariable=self.newS, font=ft)
        # self.ent.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.ent.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)
        self.ent.bind('<KeyRelease>', 
                          (lambda event: self.onSearchEnter()))

        frmLst = tk.Frame(frm)
        frmLst.grid(row=1, column=1, sticky=tk.EW, padx=5)
        self.lst = tk.Listbox(frmLst, font=ft, selectmode='single', 
                                        height=15, width=35, fg="blue")
        scr = tk.Scrollbar(frmLst)
        scr.pack(side=tk.RIGHT, fill=tk.Y)
        self.lst.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.lst.bind('<Double-Button-1>', 
                            (lambda event: self.onWordSelected()))
        scr.config(command=self.lst.yview)
        self.lst.config(yscrollcommand=scr.set)

    def onSearchEnter(self):
        sWord = self.ent.get().strip()
        newList = self.logic.fuzzySearch(sWord)
        self.lst.delete(0, tk.END)
        for w in newList:
            word = '%s: %s' % (w.word, w.explanation)
            self.lst.insert(tk.END, word)

    def onWordSelected(self):
        seled = self.lst.curselection()
        if len(seled) > 0:
            word = self.lst.get(seled).split(':')[0]
            wp.WordsProfilePop(self.logic, word, parent=self)

    def onQuit(self):
        self.logic.windows.pop('WORDSEARCHER')


class WordSearcherPop(WordSearcher):
    def __init__(self, logic, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        WordSearcher.__init__(self, logic, parent=self.popup)
        x = self.logic.windows['Root'].winfo_x()
        y = self.logic.windows['Root'].winfo_y()
        self.popup.geometry('+%d+%d' % (x+100, y+100))
        self.popup.deiconify()

    def onQuit(self):
        super().onQuit()
        self.popup.destroy()