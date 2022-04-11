###############################################################################
# Lolan
###############################################################################
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

import Logic as logic
import datetime
import numpy as np
import matplotlib.pyplot as mp
# from tkcalendar import DateEntry

class ChartsPanel(tk.Frame):
    def __init__(self, logic, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        self.logic = logic
        self.logic.windows['CHARTSPANEL'] = self
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        parent.title('Charts')
        parent.iconphoto(False, tk.PhotoImage(file='Vocabulary\\img\\icon_report.png'))
        self.makeWidgets()

    def makeWidgets(self):
        ft = tkFont.Font(size=14, weight=tkFont.BOLD)
        self.btns = []

        yearNow = datetime.datetime.now().year
        monthNow = datetime.datetime.now().month
        years = [yearNow-i for i in range(3)]
        months = [i+1 for i in range(12)]

        frmTopBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=5, pady=5)
        frmTopBar.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        tk.Label(frmTopBar, font=ft, text='开始日期').pack(side=tk.LEFT)
        self.fYearChosen = ttk.Combobox(frmTopBar, font=('', 14), width=4)
        self.fYearChosen['values'] = years
        self.fYearChosen.pack(side=tk.LEFT)
        self.fYearChosen.current(years.index(yearNow-1))
        tk.Label(frmTopBar, font=ft, text='年').pack(side=tk.LEFT)

        self.fMonthChosen = ttk.Combobox(frmTopBar, font=('', 14), width=2)
        self.fMonthChosen['values'] = months
        self.fMonthChosen.pack(side=tk.LEFT)
        self.fMonthChosen.current(months.index(monthNow))
        tk.Label(frmTopBar, font=ft, text='月').pack(side=tk.LEFT)
        
        tk.Label(frmTopBar, font=ft, text='    ').pack(side=tk.LEFT)

        tk.Label(frmTopBar, font=ft, text='结束日期').pack(side=tk.LEFT)
        self.tYearChosen = ttk.Combobox(frmTopBar, font=('', 14), width=4)
        self.tYearChosen['values'] = years
        self.tYearChosen.pack(side=tk.LEFT)
        self.tYearChosen.current(years.index(yearNow))
        tk.Label(frmTopBar, font=ft, text='年').pack(side=tk.LEFT)

        self.tMonthChosen = ttk.Combobox(frmTopBar, font=('', 14), width=2)
        self.tMonthChosen['values'] = months
        self.tMonthChosen.pack(side=tk.LEFT)
        self.tMonthChosen.current(months.index(monthNow))
        tk.Label(frmTopBar, font=ft, text='月').pack(side=tk.LEFT)

        frmBtns = tk.Frame(self, highlightbackground='Gray',
                                highlightthickness=1, padx=10, pady=5)
        frmBtns.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)


        self.btnMP = tk.Button(frmBtns, text ='月表现', font=ft, width=7, 
                    fg='black', relief=tk.RAISED, command=self.onShowMPChart)
        self.btnMP.pack(side=tk.LEFT, padx=70)
        # self.btnMP.grid(row=0, column=0, sticky=tk.EW, padx=3, pady=3)


        self.btnV = tk.Button(frmBtns, text ='趋势', font=ft, width=7, 
                    fg='black', relief=tk.RAISED, command=self.onShowVDChart)
        self.btnV.pack(side=tk.RIGHT, padx=70)

        frmFootBar = tk.Frame(self, highlightbackground='Gray', 
                                highlightthickness=1, padx=5, pady=5)
        frmFootBar.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.btnS = tk.Button(frmFootBar, text ='总体情况', font=ft, width=7, 
                    fg='black', relief=tk.RAISED, command=self.onShowSMChart)
        self.btnS.pack()
        # self.btnV.grid(row=0, column=1, sticky=tk.EW, padx=3, pady=3)
        # side=tk.LEFT
   
    def onShowMPChart(self):
        yf = int(self.fYearChosen.get())
        mf = int(self.fMonthChosen.get())
        yt = int(self.tYearChosen.get())
        mt = int(self.tMonthChosen.get())
        # rng = [[yf, mf], [yt, mt]]
        self.logic.getPerformance()
        mPData = self.logic.getMonthlyPerformance(yf, mf, yt, mt)

        ym = np.array([mp[0] for mp in mPData[1:]])
        newW = np.array([int(mp[1]) for mp in mPData[1:]])
        revW = np.array([int(mp[2]) for mp in mPData[1:]])
        wday = np.array([int(mp[3]) for mp in mPData[1:]])

        barwide = 0.2
        index = np.arange(len(newW))
        mp.figure('Monthly Performance', facecolor='white', figsize=(18,6))
        mp.title('Monthly Performance', fontsize=18)
        mp.grid(linestyle=':')
        mp.bar(index-barwide, newW, barwide, color='darkorange', label='New words',tick_label=ym)
        mp.bar(index, revW, barwide, color='steelblue', label='Review words',tick_label=ym)
        mp.bar(index+barwide, wday, barwide, color='mediumseagreen', label='Work days',tick_label=ym)

        for a,b in zip(index-barwide, newW):   
            mp.text(a, b, b, ha='center', va='bottom', fontsize=9);
        for a,b in zip(index, revW):   
            mp.text(a, b, b, ha='center', va='bottom', fontsize=9);
        for a,b in zip(index+barwide, wday):   
            mp.text(a, b, b, ha='center', va='bottom', fontsize=9);
        
        mp.ylim(0, revW.max() * 1.2)
        
        mp.legend()
        mp.show()

    def onShowVDChart(self):
        yf = int(self.fYearChosen.get())
        mf = int(self.fMonthChosen.get())
        yt = int(self.tYearChosen.get())
        mt = int(self.tMonthChosen.get())

        self.logic.getPerformance()
        vData = self.logic.getVocabularyData(yf, mf, yt, mt)
        ym = np.array([mp[0] for mp in vData[1:]])
        vList = np.array([int(mp[1]) for mp in vData[1:]])
        
        mPData = self.logic.getMonthlyPerformance(yf, mf, yt, mt)
        newW = np.array([int(mp[1]) for mp in mPData[1:]])
        revW = np.array([int(mp[2]) for mp in mPData[1:]])
        # wday = np.array([int(mp[3]) for mp in mPData[1:]])

        fig = mp.figure('Trend', facecolor='white', figsize=(14,10))
        
        ax1 = fig.add_subplot(211)
        ax1.grid(linestyle=':')

        ax1.plot(ym, vList, 'o-', label='Vocabulary')
        ax1.set_ylim(0, vList.max() * 1.2)
        ax1.fill_between(ym, vList, alpha=0.2)

        for a, b in zip(ym, vList):
            ax1.text(a, b, b, ha='center', va='bottom', fontsize=10)

        ax1.legend()
        ax1.set_title('Vocabulary', fontsize=18)

        ax2 = fig.add_subplot(212)
        
        ax2.plot(ym, newW, 'o-', label='New words', color='darkorange')
        ax2.hlines(np.mean(newW), ym[0], ym[-1], label='New words average',
                            linestyle=':', color='darkorange')
        
        ax2.plot(ym, revW, 'o-', label='Review words', color='steelblue')
        ax2.grid(linestyle=':')
        ax2.hlines(np.mean(revW), ym[0], ym[-1], label='Review words average',
                            linestyle=':', color='steelblue')
        
        ax2.yaxis.set_minor_locator(mp.MultipleLocator(10))
        ax2.set_ylim(0, revW.max() * 1.2)
        
        for a, b in zip(ym, newW):
            ax2.text(a, b, b, ha='center', va='bottom', fontsize=10)
        for a, b in zip(ym, revW):
            ax2.text(a, b, b, ha='center', va='bottom', fontsize=10)
        
        ax2.legend()
        ax2.set_title('Performance', fontsize=18)

        mp.tight_layout()
        mp.show()

    def onShowSMChart(self):
        mp.rcParams["font.sans-serif"]=["SimHei"] #设置字体
        mp.rcParams["axes.unicode_minus"]=False #正常显示负号

        self.logic.getPerformance()
        sData = self.logic.getSummary()
        labels = np.array(sData[0][1:])
        colors = np.array(['lightslategrey', 'dodgerblue', 'limegreen', 'gold'])
        spaces = np.array([0.03] * 4)

        all_Title = sData[1][0]
        all_Values = sData[1][1:]
        
        mainfig = mp.figure('Summary', facecolor='white', figsize=(8,6))
        mp.title(all_Title, fontsize=18)
        mp.pie(
            all_Values,
            spaces,
            labels,
            colors,
            # autopct='%.1f%%',
            autopct=lambda x: self.my_label(x, all_Values),
            radius=1.2,
            wedgeprops=dict(width=0.4, edgecolor='w'),
            pctdistance=0.8
        )
        mp.legend(loc='upper right', bbox_to_anchor=(1.3, 1))
        
        viewnum = len(sData)
        subcount = 1
        for i in range(2, len(sData), 6):
            subfig = mp.figure('Subproject ' + str(subcount), facecolor='white', figsize=(16,8))
            subcount += 1
            # mp.title(i, fontsize=18)
            
            for j in range(6):
                if j+i < viewnum:
                    sub_Title = sData[j+i][0]
                    sub_Values = np.array(sData[j+i][1:])
                    sub_mask = np.array([True if k>0 else False for k in sub_Values])

                    ax = subfig.add_subplot(231+j)
                    ax.pie(
                        sub_Values[sub_mask],
                        spaces[sub_mask],
                        labels[sub_mask],
                        colors[sub_mask],
                        autopct='%.1f%%',
                        radius=1.1,
                        wedgeprops=dict(width=0.4, edgecolor='w'),
                        pctdistance=0.8
                    )
                    ax.set_title(sub_Title)
            l, b = mainfig.axes[-1].get_legend_handles_labels()
            subfig.legend(l, b, loc='upper right')

        mp.tight_layout()
        mp.show()

    def my_label(self, pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return '{:.1f}%\n({:d})'.format(pct, absolute)
    
    def onQuit(self):
        # if 'WORDSCALENDER' in self.logic.windows.keys():
        self.logic.windows.pop('CHARTSPANEL')

class ChartsPanelPop(ChartsPanel):
    def __init__(self, logic, ismodal=True, parent=None):
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        # self.popup.title(date.strftime("%Y/%m/%d"))
        ChartsPanel.__init__(self, logic, parent=self.popup)
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

def tester():
    # ChartsPanelPop(None, ismodal=False)
    pass

if __name__ == "__main__":
    root = tk.Tk()
    tk.Button(root, text='tester', command=lambda : tester()).pack(side=tk.LEFT)
    root.mainloop()
