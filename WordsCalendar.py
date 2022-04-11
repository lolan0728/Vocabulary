###############################################################################
# Lolan
###############################################################################
import datetime
import tkinter as tk
import tkinter.font as tkFont

import Logic as logic
import DailyWordsTable as dailyWordsTable

class WordsCalendar(tk.Frame):
    def __init__(self, initYear, initMonth, logic, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.logic = logic
        self.logic.windows['WORDSCALENDER'] = self
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        parent.title('Calendar')
        parent.iconphoto(False, tk.PhotoImage(file='Vocabulary\\img\\icon_report.png'))
        self.makeWidgets()
        self.setCalendar(initYear, initMonth)

    def makeWidgets(self):
        ft_title = tkFont.Font(size=12, weight=tkFont.BOLD)
        ft_cal = tkFont.Font(size=16, weight=tkFont.BOLD)
        week = ('Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun')
        # week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

        self.btns = []

        frmTopBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=5, pady=5)
        frmTopBar.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        tk.Button(frmTopBar, text='<<', font=ft_title, command=self.onLastMonth) \
            .pack(side=tk.LEFT)
        tk.Button(frmTopBar, text='>>', font=ft_title, command=self.onNextMonth) \
            .pack(side=tk.RIGHT)

        frmDate = tk.Frame(frmTopBar)
        frmDate.pack(expand=tk.YES)
        self.lblYear = tk.Label(frmDate, font=ft_title)
        self.lblYear.pack(side=tk.LEFT)
        tk.Label(frmDate, text='年', font=ft_title).pack(side=tk.LEFT)
        self.lblMonth = tk.Label(frmDate, font=ft_title)
        self.lblMonth.pack(side=tk.LEFT)
        tk.Label(frmDate, text='月', font=ft_title).pack(side=tk.LEFT)

        frmCal = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=5, pady=5)
        frmCal.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)

        column = 0
        for d in week:
            tk.Label(frmCal, text=d, font=ft_title) \
                            .grid(row=0, column=column, sticky=tk.EW)
            column += 1
        
        row = 1
        for w in range(6):
            btnl = []
            for d in range(7):
                btn = tk.Button(frmCal, text='', font=ft_cal, bg='Gainsboro',
                            fg='Black', height=3, width=6, state=tk.DISABLED)
                btn.bind("<Button-1>", self.onShowWordsTable)
                btn.grid(row=row, column=d, sticky=tk.EW)
                btnl.append(btn)
            self.btns.append(btnl)
            row +=1
    
    def setCalendar(self, year, month):
        self.lblYear['text'] = year
        self.lblMonth['text'] = str(month).rjust(2,'0')
        cal = self.logic.makeCalendar(year, month)
        self.resetCalendar()
        for w in range(len(cal)):
            for d in range(len(cal[w])):
                self.btns[w][d]['text'] = \
                            str(cal[w][d]).rjust(2,'0') if cal[w][d] > 0 else ''
                if cal[w][d] > 0:
                    date = '/'.join([str(year), 
                        str(month).rjust(2,'0'), str(cal[w][d]).rjust(2,'0')])
                    if date in self.logic.dailyWordsTable.keys():
                        self.btns[w][d]['state'] = tk.NORMAL
                        self.btns[w][d]['bg'] = 'Yellow'
                        # self.btns[w][d]['fg'] = 'White'
    
    def resetCalendar(self):
        for w in self.btns:
            for d in w:
                d['text'] = ''
                d['bg'] = 'Gainsboro'
                d['fg'] = 'Black'
                d['state'] = tk.DISABLED
    
    def onShowWordsTable(self, event):
        if event.widget['text'] != '':
            year = int(self.lblYear['text'])
            month = int(self.lblMonth['text'])
            day = int(event.widget['text'])
            strDate = '/'.join([str(year), 
                            str(month).rjust(2,'0'), str(day).rjust(2,'0')])
            # date = datetime.date(year, month, day)
            if strDate in self.logic.dailyWordsTable.keys():
                wordsTable = self.logic.dailyWordsTable[strDate]
                dailyWordsTable.DailyWordsTable_Confirm(self.logic, strDate, 
                                                    wordsTable, ismodal=False)
    
    def onLastMonth(self):
        year = int(self.lblYear['text'])
        month = int(self.lblMonth['text'])
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        self.setCalendar(year, month)

    def onNextMonth(self):
        year = int(self.lblYear['text'])
        month = int(self.lblMonth['text'])
        if month == 12:
            year += 1
            month = 1
        else:
            month += 1
        self.setCalendar(year, month)
    
    def onQuit(self):
        # if 'WORDSCALENDER' in self.logic.windows.keys():
        self.logic.windows.pop('WORDSCALENDER')

class WordsCalendarPop(WordsCalendar):
    def __init__(self, initYear, initMonth, logic, ismodal=True, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        # self.popup.title(date.strftime("%Y/%m/%d"))
        WordsCalendar.__init__(self, initYear, initMonth, logic, parent=self.popup)
        x = self.logic.windows['Root'].winfo_x()
        y = self.logic.windows['Root'].winfo_y()
        self.popup.geometry('+%d+%d' % (x+100, y+100))
        if ismodal:
            self.popup.grab_set()                  
            self.popup.focus_set()
            self.popup.wait_window()
        self.popup.deiconify()

    def onQuit(self):
        super().onQuit()
        self.popup.destroy()

def tester(initYear, initMonth):
    # WordsCalendarPop(initYear, initMonth, ismodal=False)
    pass

if __name__ == "__main__":
    root = tk.Tk()
    tk.Button(root, text='tester', command=lambda : tester(2020, 7)).pack(side=tk.LEFT)
    root.mainloop()
