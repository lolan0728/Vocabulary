###############################################################################
# Lolan
###############################################################################

import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import showinfo
from tkinter.filedialog import asksaveasfilename

import Logic as Logic
import Outputer as outputer

class DailyWordsTable(tk.Frame):
    
    def __init__(self, logic, date, wordsTable, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        parent.iconphoto(False, tk.PhotoImage(file='.\\img\\icon_report.png'))
        self.logic = logic
        self.date = date
        self.wordsTable = wordsTable
        self.makeWidgets()

    def makeWidgets(self):

        winWidth = 500
        self.frmBottomBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=10, pady=5)
        self.frmBottomBar.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.X)
        self.canvas = tk.Canvas(self, borderwidth=0, bg='white', 
                                                    width=winWidth, height=620)
        vbar = tk.Scrollbar(self)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.canvas.config(yscrollcommand=vbar.set)
        vbar.config(command=self.canvas.yview)

        self.makeWordsTable()

    def makeWordsTable(self):

        self.canvas.delete("all")
        new_words, review_Words = outputer.Outputer() \
                        .formatWordsTable(self.wordsTable)
        
        ft = tkFont.Font(size=16, weight=tkFont.BOLD)
        txtNew    = 'New Words (' + str(len(new_words)) +')'
        txtReview = 'Review    (' + str(len(review_Words)) +')'

        rowpos = 1
        lbl = tk.Label(self.canvas, text=txtNew, bg='LightSteelBlue', 
                    font=ft, width=50, anchor='w')
        self.canvas.create_window(0, rowpos, anchor=tk.NW, window=lbl)
        rowpos += 28

        for w in new_words:
            chk = tk.Checkbutton(self.canvas, text=w, bg='white', font=('', 14),
                indicatoron=False, anchor='w', selectcolor="yellow", width=60)
            self.canvas.create_window(0, rowpos, anchor=tk.NW, window=chk)
            rowpos += 28

        lbl = tk.Label(self.canvas, text=txtReview, bg='LightSteelBlue', 
                    font=ft, width=50, anchor='w')
        self.canvas.create_window(0, rowpos, anchor=tk.NW, window=lbl)
        rowpos += 28

        for w in review_Words:
            chk = tk.Checkbutton(self.canvas, text=w, bg='white', font=('', 14), 
                indicatoron=False, anchor='w', selectcolor="yellow", width=60)
            self.canvas.create_window(0, rowpos, anchor=tk.NW, window=chk)
            rowpos += 28

        fullsize = (0, 0, (500), (rowpos))
        self.canvas.config(scrollregion=fullsize)
    
    def onOutput(self):
        title = '保存文件'
        ftypes = [('word 文件', '.docx')]
        initialfile = 'word' + str(self.date.replace('/', ''))
        self.savepath = asksaveasfilename(filetypes=ftypes, title=title,
                            initialfile=initialfile, defaultextension='.docx')
        if self.savepath:
            
            outputer.Outputer().outputDocx(self.logic.name + "'s Daily Words", 
                        self.logic.name, 
                        self.savepath, 
                        self.wordsTable,
                        self.date)

class DailyWordsTable_Create(DailyWordsTable):
    def __init__(self, logic, date, wordsTable, ismodal=True, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        self.popup.title(date)
        DailyWordsTable.__init__(self, logic, date, wordsTable, self.popup)
        x = self.logic.windows['Root'].winfo_x()
        y = self.logic.windows['Root'].winfo_y()
        self.popup.geometry('+%d+%d' % (x+200, y+200))
        self.popup.deiconify()
        if ismodal:
            self.popup.grab_set()                  
            self.popup.focus_set()
            self.popup.wait_window()
    
    def makeWidgets(self):
        DailyWordsTable.makeWidgets(self)    
        ft = tkFont.Font(size=16, weight=tkFont.BOLD)    
        tk.Button(self.frmBottomBar, text='确定并输出', font=ft, bg='DarkOrange', 
            fg='white',command=self.onOutput) \
                .pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
    
    def onOutput(self):
        DailyWordsTable.onOutput(self)
        if self.savepath:
            self.logic.saveWordsTable(self.date, self.wordsTable)
            self.logic.windows['MAIN'].setVocabList()
            self.popup.destroy()
            showinfo('通知', '输出完毕')

class DailyWordsTable_Confirm(DailyWordsTable):
    def __init__(self, logic, date, wordsTable, ismodal=True, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        self.popup.title(date)
        DailyWordsTable.__init__(self, logic, date, wordsTable, self.popup)
        x = self.logic.windows['Root'].winfo_x()
        y = self.logic.windows['Root'].winfo_y()
        self.popup.geometry('+%d+%d' % (x+200, y+200))
        self.popup.deiconify()
        if ismodal:
            self.popup.grab_set()                  
            self.popup.focus_set()
            self.popup.wait_window()
    
    def makeWidgets(self):
        DailyWordsTable.makeWidgets(self)
        ft = tkFont.Font(size=16, weight=tkFont.BOLD)        
        tk.Button(self.frmBottomBar, text='输出', font=ft, bg='DarkOrange', 
            fg='white',command=self.onOutput) \
                .pack(side=tk.TOP, fill=tk.X, expand=tk.YES)

    def onOutput(self):
        DailyWordsTable.onOutput(self)
        showinfo('通知', '输出完毕')

def tester(logic, date, table):
        # t = Toplevel()
        # DailyWordsTable(date, table, tk.Toplevel())
        # DailyWordsTablePop(logic, date, table)
        pass

if __name__ == "__main__":
    pass
    # import Logic as Logic
    # # tester('Harvey', 'C:\\Users\\eos\\Desktop\\')
    # logic = Logic.Logic()
    # # logic.loadDailyWordsTable()
    # date = sorted(logic.dailyWordsTable)[-1]
    # table = logic.dailyWordsTable[date]
    # root = tk.Tk()
    # tk.Button(root, text='tester', command=lambda : tester(logic, date, table)).pack(side=tk.LEFT)
    # root.mainloop()


        