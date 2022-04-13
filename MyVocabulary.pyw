import math
import datetime
import tkinter as tk
import tkinter.font as tkFont
from tkinter.messagebox import askyesno, showwarning, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename

import Logic as logic
import WordsTableMaker as wtm
import WordsCalendar as wc
# import WordsProfile as wp
import WordSearcher as ws
import ChartsPanel as cp

# new git 1
class Processbar(tk.Frame):
    def __init__(self, maxnum, parent=None, process=0, maxBlock=10, width=30):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.X)
        self.maxnum = maxnum
        self.maxBlock = maxBlock
        self.width = width
        self.makeWidgets()
        self.onProgress(process)

    def makeWidgets(self):
        ft = tkFont.Font(size=14)
        self.blocks = []
        prewidth = self.width // self.maxBlock
        for i in range(self.maxBlock):
            block = tk.Label(self, width=prewidth)
            block.grid(row=0, column=i, sticky=tk.EW)
            self.blocks.append(block)
        self.lblProc = tk.Label(self, font=ft, bg='white', width=9)
        self.lblProc.grid(row=0, column=self.maxBlock, sticky=tk.EW)
        self.lblPerc = tk.Label(self, font=ft, bg='white', width=6, anchor=tk.E)
        self.lblPerc.grid(row=0, column=self.maxBlock+1, sticky=tk.EW)

    def onProgress(self, process):
        blockNum = math.ceil(self.maxBlock * process/self.maxnum)
        percent = round(process/self.maxnum * 100, 1) if process>0 else 0
        if percent < 100 and blockNum == self.maxBlock:
            blockNum -= 1
        for b in self.blocks:
            b['bg'] = 'GhostWhite'
        for i in range(blockNum):
            self.blocks[i]['bg'] = 'DarkOrange'
        self.lblProc['text'] = '%s/%s' % (process, self.maxnum)
        self.lblPerc['text'] = str(percent) + '%'

class MainFrame(tk.Frame):
    def __init__(self, parent=None):
        tk.Frame.__init__(self, parent)
        self.pack(expand=tk.YES, fill=tk.BOTH)
        parent.protocol('WM_DELETE_WINDOW', self.onQuit)
        parent.title('My Vocabulary')
        parent.iconphoto(False, tk.PhotoImage(file='.\\img\\icon_report.png'))
        self.logic = logic.Logic()
        self.logic.windows['MAIN'] = self
        self.logic.windows['Root'] = parent
        self.logic.loadAll()
        self.makeWidgets()

    def makeWidgets(self):
        self.makeToolBar()
        self.makeVocabList()
        self.setVocabList()

    def makeVocabList(self):
        self.winWidth = 850
        cavhigh = 100 + (len(self.logic.vocabList) + 1) * 35
        self.canvas = tk.Canvas(self, borderwidth=0, bg='white', 
                                                width=self.winWidth, height=cavhigh)
        vbar = tk.Scrollbar(self)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        self.canvas.config(yscrollcommand=vbar.set)
        vbar.config(command=self.canvas.yview) 

    def setVocabList(self):
        self.chkNewVocabs = {}
        self.chkRevVocabs = {}
        ft = tkFont.Font(size=14, weight=tkFont.BOLD)
        self.canvas.delete("all")
        rowpos = 1
        lbl = tk.Label(self.canvas, text='词汇表一览', bg='LightSteelBlue', 
                    font=ft, width=80, anchor='w')
        self.canvas.create_window(0, rowpos, anchor=tk.NW, window=lbl) 
        rowpos += 30

        lblNew = tk.Label(self.canvas, text='新', bg='white', font=('', 12), width=80, anchor='w')
        self.canvas.create_window(0, rowpos, anchor=tk.NW, window=lblNew) 

        lblRev = tk.Label(self.canvas, text='复', bg='white', font=('', 12), width=80, anchor='w')
        self.canvas.create_window(35, rowpos, anchor=tk.NW, window=lblRev) 
        rowpos += 25

        for v in self.logic.vocabList.values():
            colpos = 0

            chkNewVar = tk.IntVar()
            chkNew = tk.Checkbutton(self.canvas, bg='white',
                font=('', 14), anchor='w', variable=chkNewVar, 
                                                        command=self.onChkNewVocab)
            self.canvas.create_window(colpos, rowpos, anchor=tk.NW, window=chkNew)
            colpos += 35

            chkRevVar = tk.IntVar()
            chkRev = tk.Checkbutton(self.canvas, text=v.description, bg='white',
                font=('', 14), anchor='w', variable=chkRevVar, 
                                                        command=self.onChkRevVocab)
            self.canvas.create_window(colpos, rowpos, anchor=tk.NW, window=chkRev)
            colpos += 300

            cap = v.getCapacity()
            # pro = v.getProgress()
            pro = self.logic.getProgress(v.name)
            proc = Processbar(cap, self.canvas, process=pro)
            self.canvas.create_window(colpos, rowpos, anchor=tk.NW, window=proc)
            colpos += 450

            self.chkNewVocabs[v.name] = chkNewVar
            self.chkRevVocabs[v.name] = chkRevVar
            
            if v.name in self.logic.currNewVocabs.keys():
                chkNew.select()
            if v.name in self.logic.currRevVocabs.keys():
                chkRev.select()
            
            btn = tk.Button(self.canvas, font=tkFont.Font(size=13), text='删除',
                            command=(lambda vname=v.name: self.onDeleteVocabulary(vname)))
            self.canvas.create_window(colpos, rowpos, anchor=tk.NW, window=btn)
            rowpos += 35

        if len(self.logic.vocabList) > 0:
            lblsep = tk.Label(self.canvas, text='-'*80, bg='white', 
                font=('', 14), anchor='w')
            self.canvas.create_window(0, rowpos, anchor=tk.NW, window=lblsep)
            rowpos += 25
            lbltotal = tk.Label(self.canvas, text='总进度', bg='white',
                font=('', 14), anchor='w')
            self.canvas.create_window(0, rowpos, anchor=tk.NW, window=lbltotal)
            totalCap = len(self.logic.uniVocabulary)
            totalPro = len([w for w in self.logic.uniVocabulary.values() if w.newDate])
            totalProc = Processbar(totalCap, self.canvas, process=totalPro)
            self.canvas.create_window(335, rowpos, anchor=tk.NW, window=totalProc)
            rowpos += 35
        
        fullsize = (0, 0, self.winWidth, rowpos)
        self.canvas.config(scrollregion=fullsize)
        cavhigh = 100 + (len(self.logic.vocabList) + 1) * 35
        self.canvas.config(height=cavhigh)

    def makeToolBar(self):
        ft = tkFont.Font(size=12)
        self.setToolbar()
        if self.toolBar:
            toolbar = tk.Frame(self, relief=tk.SUNKEN, bd=2)
            toolbar.pack(side=tk.BOTTOM, fill=tk.X)
            for (name, action, where) in self.toolBar:
                tk.Button(toolbar, text=name, command=action, font=ft).pack(where)

    def setToolbar(self):
        self.toolBar = [
                ('新单词表',  self.onMakeWordsTable,   {'side': tk.LEFT}),
                ('词汇日历',  self.onShowCalendar,   {'side': tk.LEFT}),
                ('导入词汇表',  self.onImportVocabulary,   {'side': tk.LEFT}),
                ('单词信息',  self.onWordsProfile,   {'side': tk.LEFT}),
                # ('删除',  self.onDeleteVocabulary,   {'side': tk.LEFT}),
                ('总览',  self.onExportAnalysis,   {'side': tk.RIGHT}),
                ('分析图表',  self.onExportChart,   {'side': tk.RIGHT}),
                # ('退出',  self.onQuit,   {'side': tk.RIGHT}),
                # ('设置',  self.onSetting,   {'side': tk.RIGHT}),
                ]

    def onChkNewVocab(self):
        selVocabs = [n for (n,v) in self.chkNewVocabs.items() if v.get() == 1]
        self.logic.setCurrNewVocabs(selVocabs)
    
    def onChkRevVocab(self):
        selVocabs = [n for (n,v) in self.chkRevVocabs.items() if v.get() == 1]
        self.logic.setCurrRevVocabs(selVocabs)

    def onDeleteVocabulary(self, vocab):
        if askyesno('注意', '确认删除？'):
            self.logic.delVocabulary(vocab)
            self.setVocabList()
            # self.makeWidgets()

    def onShowCalendar(self):
        if 'WORDSCALENDER' not in self.logic.windows.keys():
            # self.logic.windowList.append('WORDSCALENDER')
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            wc.WordsCalendarPop(year, month, self.logic, ismodal=False, parent=self)
        else:
            self.logic.windows['WORDSCALENDER'].focus_force()

    def onSelfClean(self):
        self.logic.selfClean()
        self.setVocabList()

    def onExportChart(self):
        # title = '保存文件'
        # ftypes = [('Excel 文件', '.xlsx')]
        # initialfile = 'Charts_' + self.logic.today.replace('/', '')
        # savepath = asksaveasfilename(filetypes=ftypes, title=title,
        #                         initialfile=initialfile, defaultextension='.xlsx')
        # if savepath:
        #     self.logic.exportCharts(savepath)
        #     showinfo('通知', '输出完毕')
        if 'CHARTSPANEL' not in self.logic.windows.keys():
            cp.ChartsPanelPop(self.logic, ismodal=False, parent=self)
        else:
            self.logic.windows['CHARTSPANEL'].focus_force()


    def onExportAnalysis(self):
        title = '保存文件'
        ftypes = [('Excel 文件', '.xlsx')]
        initialfile = 'Analysis_' + self.logic.today.replace('/', '')
        # selVocabs = [n for (n,v) in self.chkVocabs.items() if v.get() == 1]
        selVocabs = [n for (n,v) in self.logic.vocabList.items()]
        if len(selVocabs) > 0:
            savepath = asksaveasfilename(filetypes=ftypes, title=title,
                                initialfile=initialfile, defaultextension='.xlsx')
            if savepath:
                self.logic.exportAnalysis(selVocabs, savepath)
                showinfo('通知', '输出完毕')
        else:
            showwarning('注意', '没有任何词汇表')

    def onImportVocabulary(self):
        title = '读取词汇表'
        ftypes = [('Excel 文件', '.xlsx')]
        openpath = askopenfilename(title=title, filetypes=ftypes)
        if openpath:
            self.logic.loadExcel(openpath)
            self.setVocabList()
            # self.makeWidgets()
            showinfo('通知', '读取完毕')

    def onWordsProfile(self):
        if 'WORDSEARCHER' not in self.logic.windows.keys():
            ws.WordSearcherPop(self.logic, parent=self)
        else:
            self.logic.windows['WORDSEARCHER'].focus_force()
    
    def onMakeWordsTable(self):
        if 'WORDSTABLEMAKER' not in self.logic.windows.keys():
            selNewVocabs = [n for (n,v) in self.chkNewVocabs.items() if v.get() == 1]
            self.logic.setCurrNewVocabs(selNewVocabs)

            selRevVocabs = [n for (n,v) in self.chkRevVocabs.items() if v.get() == 1]
            self.logic.setCurrRevVocabs(selRevVocabs)

            if len(selNewVocabs) == 0 and len(selRevVocabs) == 0:
                if not askyesno('注意', '没有选择任何词汇表，是否继续？'):
                    return
            # self.logic.windowList.append('WORDSTABLEMAKER')
            wtm.WordsTableMakerPop(self.logic, parent=self)
        else:
            self.logic.windows['WORDSTABLEMAKER'].focus_force()

    def onQuit(self):
        self.logic.saveAll()
        self.quit()

if __name__ == "__main__":
    root = tk.Tk()
    scrnW=root.winfo_screenwidth()
    scrnH=root.winfo_screenheight()
    root.withdraw()
    MainFrame(root)
    lPoint = (scrnW - 850) // 2
    tPoint = (scrnH - 500) // 2 - 50
    root.geometry('+%d+%d' % (lPoint, tPoint))
    root.deiconify()
    root.mainloop()

