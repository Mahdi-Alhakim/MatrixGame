from tkinter import *; import tkinter.messagebox as MB
import numpy as np
from random import choice
import time, sys, os; from math import *

from src.db import DB
from src.replay_manager import ReplayManager

WIDTH = 100

class Game:
  def __init__(self, parent):
    self.root = parent
    self.cntrW(self.root, 405, 440)
    self.root.resizable(0, 0)
    self.root.title("Matrix Game")
    self.table = [0] * 16
    self.cont = False
    self.able = True
    self.Time = StringVar()
    self.Time.set("0.0")
    self.btntxt = StringVar()
    self.btntxt.set("Start")
    self.startTime = time.time()
    self.main_canvas = Canvas(self.root, width=WIDTH * 4, height=WIDTH *4, bg="lightblue")
    self.main_canvas.grid(row=0, column=0)

    self.DB = DB()
    self.replay_manager = ReplayManager(self)

    self.back()
    self.sframe = Frame(self.root)
    self.sframe.grid(row=1, column=0)
    self.FS2()
    self.root.mainloop()
    
  def RTimes(self):
    self.times += str(int(floor((time.time() - self.Tme)*1000)))+"-"
    self.Tme = time.time()
  
  def timer(self, dpnd=2):
    if dpnd == 0:
      self.startTime = time.time()
      self.cont = True
    elif dpnd == 1:
      self.cont = False
    if self.cont == True:
      self.timeT = time.time()-self.startTime
      if (self.timeT-round(self.timeT)) >= 0.5:
        self.timeT = self.timeT-0.5
      self.Time.set(str(round(self.timeT)))
    self.root.after(1000, self.timer)
  
  
  
  def cntrW(self, root, w, h, bol=0):
    root.withdraw()
    root.update_idletasks()
    x = (root.winfo_screenwidth() - w)/2
    y = (root.winfo_screenheight() - h)/2
    if bol == 0:
      root.geometry("{}x{}".format(w, h))
    else: root.geometry("+{}+{}".format(x, y))
    root.deiconify()
  
  def FS2(self):
    self.Fs2 = Frame(self.sframe)
    self.Fs2.pack(side = LEFT)
    Label(self.Fs2, text = "Time: ").pack(side = LEFT)
    self.timeCount = Label(self.Fs2, textvariable = self.Time, foreground = "red").pack(side=LEFT)
    Label(self.sframe, text = "                           ").pack(side = LEFT)
    self.FS3 = Frame(self.sframe)
    self.FS3.pack(side = RIGHT)
    self.Bck = Button(self.FS3, text="<-- Back", command=self.back)
    self.Bck.pack(side = LEFT)
    self.Btn = Button(self.FS3, textvariable = self.btntxt, command=self.btn)
    self.Btn.pack(side = RIGHT)
  
  def back(self):
    if self.able == False:
      return
    self.timer(1)
    self.Time.set("0.0")
    self.main_canvas.destroy()
    self.main_canvas = Canvas(self.root, width=WIDTH * 4, height=WIDTH *4, bg="lightblue")
    self.main_canvas.grid(row=0, column=0)
    self.main_canvas.create_text(200, 50, text = "Matrix Game", fill = "Gold3", font = "Times 40")
    recordBtn = Button(self.root, text = "Records", background = "lightblue", command = self.replay_manager.records)
    GameBtn = Button(self.root, text = "Play", background = "lightblue", command = self.btn)
    HowToPlay = Button(self.root, text= "How To Play", background = "lightblue", command = self.howtoplay)
    self.main_canvas.create_window(200, 160, window = recordBtn)
    self.main_canvas.create_window(200, 110, window = GameBtn)
    self.main_canvas.create_window(200, 210, window = HowToPlay)
    self.btntxt.set("Start")
  
  
  
  def win3close(self):
    if self.Ron == False:
      self.win3.destroy()
      self.able = True
  
  
  def prgrs(self):
    self.PrBrC.create_rectangle(0, 0, 200, 15, fill="LightGray")
    
  def howtoplay(self):

      self.tutorial_win = Toplevel(self.root)
      self.tutorial_win.title("How To Play")
      self.cntrW(self.tutorial_win, 500, 500)
      self.tutorial_win.resizable(0, 0)
      self.tutorial_win.wm_attributes("-topmost", 1)
      Label(self.tutorial_win, text="""
      #### How to Play ####\n\n
      # Detect ABBA-patterns #\n\n
      An ABBA pattern is a group of four cells in the matrix that form a rectangle\n such that the diagonally opposite cells display the same shape.\n\n
      # 3-to-1 rule #\n\n
      ABBA patterns must be colored such that exactly three of the cells share the\n same color (red/blue) while the fourth has the opposite color.\n\n
      # Objective #\n\n
      When the matrix has been fully colored, click the `check` button.\n\n
      There is only one solution!\n\n
      ***Watch your replays, and strive for faster plays!***
      """).pack()
      
  
  def btn(self):
    if self.Btn["text"] == "Start" and self.able == True:
      self.btntxt.set("Check")
      self.start()
      self.timer(0)
    elif self.able == True:
      self.btntxt.set("Start")
      self.timer(1)
      self.end()

  def start(self):
    self.moves = ""
    self.times = ""
    self.Tme = time.time()
    self.stop = False
    self.edit = True
    self.main_canvas.destroy()
    self.main_canvas = Canvas(self.root, width=WIDTH * 4, height=WIDTH *4, bg="lightblue")
    self.main_canvas.grid(row=0, column=0)
    self.Imtx = self.MxM(self.MxM(self.RperM(4), self.gameMtx(1)), self.RperM(4))
    self.mtxString = ""
    for s in self.Imtx:
      for n in s:
        self.mtxString += str(n)+"_"
    self.mtxString = self.mtxString[:len(self.mtxString)-1]
    self.solution = self.solve(self.Imtx)
    self.FC = self.fixedCells(self.Imtx)
    self.mtx = self.Imtx
    self.draw()
    self.main_canvas.bind('<Button-1>', self.clickCell)
  
  def draw(self):
    for x in range(0, 4):
      for y in range(0, 4):
        fnt, bxfill, clr, diff = "Helvetica 40", "LightGrey", 'black', 8
        cell = self.mtx[y][x]
        if str(self.mtx[y][x])[0] == '+':
          cell = self.mtx[y][x][1]
          clr = 'VioletRed'
        elif int(self.mtx[y][x]) < 0:
          cell = str(self.mtx[y][x])[1]
          clr = 'Blue'
        if self.FC[y][x] == 1:
          fnt, bxfill, diff = "Helvetica 70", "DarkGrey", 0
        self.main_canvas.create_rectangle(x*100+1, y*100+1, x*100+102, y*100+102)
        self.main_canvas.create_rectangle(x*100+6, y*100+6, x*100+97, y*100+97, fill = bxfill)
        if int(cell) == 1:
          self.main_canvas.create_rectangle(x*100+30+diff, y*100+30+diff, x*100+73-diff, y*100+73-diff, fill = clr)
        elif int(cell) == 2:
          self.main_canvas.create_oval(x*100+30+diff, y*100+30+diff, x*100+73-diff, y*100+73-diff, fill = clr)
        elif int(cell) == 3:
          self.main_canvas.create_polygon(x*100+51, y*100+30+diff, x*100+30+diff, y*100+73-diff, x*100+73-diff, y*100+73-diff, outline = "black", fill = clr)
        else:
          self.main_canvas.create_line(x*100+29+diff, y*100+29+diff, x*100+72-diff, y*100+72-diff, width = 5, fill = clr)
          self.main_canvas.create_line(x*100+72-diff, y*100+29+diff, x*100+29+diff, y*100+72-diff, width = 5, fill = clr)
  
  def clickCell(self, event):
    x, y = event.x, event.y
    clmn, rw = int(floor(x/100)), int(floor(y/100))
    if self.FC[rw][clmn] == 1 or self.edit != True:
      return
    if str(self.mtx[rw][clmn])[0] != '+':
      self.mtx[rw][clmn] = '+'+str(abs(int(self.mtx[rw][clmn])))
    else:
      self.mtx[rw][clmn] = str(-int(self.mtx[rw][clmn]))
    self.moves = self.moves + str(rw) + str(clmn)
    self.RTimes()
    self.main_canvas.delete("all")
    self.draw()
  
  def end(self):
    if self.able == False:
      return
    self.times = self.times[:len(self.times)-1]
    self.able = False
    TimeTxt = "                      Time:   "+str(round(self.timeT))+"                      "
    self.edit = False
    if self.mtx == self.solution:
      bgc = "DarkBlue"
      txt = "                      Correct!!!!!                      "
      Tclr = "red"
      self.DB.db.commit()
      self.DB.cr.execute("Select date, id FROM Games"); rslt = self.DB.cr.fetchall()
      self.DB.cr.execute("SELECT MIN(score) FROM Games"); minval = self.DB.cr.fetchall()
      if len(rslt) > 20:
        DltID = list(reversed(rslt))[20][1]
        self.DB.cr.execute("DELETE FROM Games WHERE id < {} AND score != {}".format(int(DltID), int(minval[0][0]))); self.DB.db.commit()
      self.DB.cr.execute("Select score FROM Games"); rslt = self.DB.cr.fetchall()
      HIGHSCORE = False
      if len(rslt) == 0:
        HIGHSCORE = True
      else:
        HIGHSCORE = True
        for i in rslt:
          if int(i[0]) < int(round(self.timeT)):
            HIGHSCORE = False
      if HIGHSCORE == True:
        MB.showinfo("Congrats.", "NEW HIGHSCORE !!!")
      command = "INSERT INTO Games (id, date, matrix, score, moves, times) VALUES(NULL, NOW(), \"{}\", {}, \"{}\", \"{}\")".format(self.mtxString, str(round(self.timeT)), self.moves, self.times)
      self.DB.cr.execute(command)
      self.DB.db.commit()
    else:
      bgc = "Red"
      txt = "                       Incorrect!!                       "
      Tclr = "white"
    self.win2 = Toplevel(self.root, background=bgc)
    self.cntrW(self.win2, 220, 285)
    self.win2.title("Result")
    self.win2.resizable(0, 0)
    self.win2.wm_attributes("-topmost", 1)
    self.win2.protocol("WM_DELETE_WINDOW", self.enable)
    frm1 = Frame(self.win2)
    frm1.pack()
    Label(frm1, text=txt, fg=Tclr, bg=bgc, font="Times 17 bold").pack()
    Label(frm1, text=TimeTxt, fg = "green", bg = bgc, font = "Times 16").pack()
    Label(frm1, text = "                         Solution:                         ", fg = Tclr, bg = bgc, font = "Helvetica 15 bold").pack()
    sol = Canvas(self.win2, width=200, height=200, bg="LightGrey")
    sol.pack()
    for x in range(0, 4):
      for y in range(0, 4):
        cell = self.solution[y][x]
        if str(self.solution[y][x])[0] == '+':
          cell = self.solution[y][x][1]
          clr = 'VioletRed'
        elif int(self.solution[y][x]) < 0:
          cell = str(self.solution[y][x])[1]
          clr = 'Blue'
        sol.create_rectangle(x*50+1, y*50+1, x*50+52, y*50+52)
        if int(cell) == 1:
          sol.create_rectangle(x*50+15, y*50+15, x*50+36, y*50+36, fill = clr)
        elif int(cell) == 2:
          sol.create_oval(x*50+15, y*50+15, x*50+36, y*50+36, fill = clr)
        elif int(cell) == 3:
          sol.create_polygon(x*50+25, y*50+15, x*50+15, y*50+36, x*50+36, y*50+36, outline = "black", fill = clr)
        else:
          sol.create_line(x*50+14, y*50+14, x*50+36, y*50+36, width = 3, fill = clr)
          sol.create_line(x*50+36, y*50+14, x*50+14, y*50+36, width = 3, fill = clr)
    
    
  def enable(self):
    self.able = True
    self.win2.destroy()
  
  def RperM(self, N, nump=0):
    PerM = []
    seq = []
    choices = [i for i in range(N)]
    for i in range(0, N):
      v = choice(choices)
      seq.append(v)
      choices.remove(v)
    PerM = np.zeros((N, N), dtype=int)
    for i in range(0, N):
      PerM[i][seq[i]] = 1
    PerM = np.matrix(PerM)
    if type(PerM) is not list and nump == 0:
      PerM.tolist()
    return PerM
  
  def MxM(self, m1, m2, nump=0):
    if isinstance(m1, np.matrixlib.defmatrix.matrix) or (type(m1) is np.ndarray):
      m1 = m1.tolist()
    if isinstance(m2, np.matrixlib.defmatrix.matrix) or (type(m2) is np.ndarray):
      m2 = m2.tolist()
    if (not(isinstance(m1, list))) or (not(isinstance(m2, list))):
      raise Exception("parameters must be matricies.")
      return
    if len(m1[0]) != len(m2):
      raise Exception("Operation couldn't be done.")
      return
    Pmtx = []
    for i in range(len(m1)):
      row = []
      for s in range(len(m2[0])):
        v=0
        b = False
        for x in range(0, len(m1[i])):
          if ((type(m1[i][x]) is str) and (m2[x][s] == 1)):
            if m1[i][x][0] == '+':
              b = True
          elif ((type(m2[x][s]) is str) and (m1[i][x] == 1)):
            if m2[x][s][0] == '+':
              b = True
          v += int(m1[i][x]) * int(m2[x][s])
        if (v > 0) and (b == True):
          row.append('+'+str(v))
        else:
          row.append(v)
      Pmtx.append(row)
    Pmtx = np.matrix(Pmtx)
    if type(Pmtx) is not list and nump == 0:
      Pmtx = Pmtx.tolist()
    return Pmtx
  
  def gameMtx(self, l=1, nump=0):
    mtx = [[1, 2, 3, 4], [2, 1, 4, 3], [3, 4, 1, 2], [4, 3, 2, 1]]
    for i in range(len(mtx[0])):
      if l == 0:
        if choice([0, 1]) == 0:
          mtx[0][i] = -mtx[0][i]
        else:
          mtx[0][i] = '+'+str(mtx[0][i])
      elif l == 1:
        if choice([0, 1]) == 0:
          mtx[i][i] = -mtx[i][i]
        else:
          mtx[i][i] = '+'+str(mtx[i][i])
    for i in range(1, len(mtx)):
      if l == 0:
        if choice([0, 1]) == 0:
          mtx[i][0] = -mtx[i][0]
        else:
          mtx[i][0] = '+'+str(mtx[i][0])
      elif l == 1:
        g = choice(list(range(i)))
        if choice([0, 1]) == 0:
          mtx[i][g] = -mtx[i][g]
        else:
          mtx[i][g] = '+'+str(mtx[i][g])
    r = 0
    c = 0
    restart = False
    while True:
      flse = False
      if l == 0:
        if r == 0:
          r = choice(list(range(len(mtx))))
          flse = True
        if c == 0 or r == c:
          c = choice(list(range(len(mtx[0]))))
          flse = True
        if flse == False:
          break
      elif l == 1:
        if c == 0 or r == c or restart == True:
          c = choice(list(range(1, len(mtx[0]))))
          flse = True
        if not(r < c) or restart == True:
          r = choice(list(range(c)))
          flse = True
        restart = False
        if int(mtx[c][r])<0 or str(mtx[c][r])[0] == '+':
          restart = True
          flse = True
        elif type(mtx[c][r]) is str:
          if mtx[c][r][0] == '+':
            restart = True
            flse = True
        if flse == False:
          break
  
    if choice([0, 1]) == 0:
      mtx[r][c] = -mtx[r][c]
    else:
      mtx[r][c] = '+'+str(mtx[r][c])
    for i in range(1, 5):
      passit = False
      for rw in range(4):
        for clm in range(4):
          if (len(str(mtx[rw][clm])) == 2) and (abs(int(mtx[rw][clm])) == i):
            passit = True
      if passit == False:
        return self.gameMtx(l, nump)
    mtx = np.matrix(mtx)
    if (type(mtx) is not list) and nump == 0:
      mtx = mtx.tolist()
    return mtx
  
  def fixedCells(self, mtx, nump=0):
    fxd = []
    for r in range(len(mtx)):
      v = []
      for c in range(len(mtx[0])):
        if len(str(mtx[r][c])) == 2:
          v.append(1)
        else:
          v.append(0)
      fxd.append(v)
    fxd = np.matrix(fxd)
    if (type(fxd) is not list) and nump == 0:
      fxd = fxd.tolist()
    return fxd
  
  def s2x2(self, m2x):
    slP = 0
    slN = 0
    value = 0
    for r in range(2):
      for c in range(2):
        if len(str(m2x[r][c])) == 1:
          rw = r
          cl = c
        elif int(m2x[r][c]) < 0:
          slN += 1
        else:
          slP += 1
    if ((slP + slN) == 3) and (abs(int(m2x[0][0])) == abs(int(m2x[1][1]))) and (abs(int(m2x[0][1])) == abs(int(m2x[1][0]))):
      if slP % 2 == 1:
        value = 0
      else:
        value = 1
      return [rw, cl, value]
    else:
      return 0
  
  def solve(self, mtrx):
    slvd = []
    for mrow in mtrx:
      rww = []
      for mclm in mrow:
        rww.append(mclm)
      slvd.append(rww)
    while True:
      flse = False
      for Rsize in range(1, len(slvd)):
        for row in range(0, len(slvd)-Rsize):
          for Csize in range(1, len(slvd)):
            for clmn in range(0, len(slvd)-Csize):
              coord = [[(row, clmn), (row, clmn+Csize)], [(row+Rsize, clmn), (row+Rsize, clmn+Csize)]]
              mtx1 = [[slvd[row][clmn], slvd[row][clmn+Csize]], [slvd[row+Rsize][clmn], slvd[row+Rsize][clmn+Csize]]]
              solt = self.s2x2(mtx1)
              if (type(solt) is list):
                tple = coord[solt[0]][solt[1]]
                if solt[2] == 1:
                  slvd[tple[0]][tple[1]] = '+'+str(slvd[tple[0]][tple[1]])
                else:
                  slvd[tple[0]][tple[1]] = str(-int(slvd[tple[0]][tple[1]]))
                flse = True
      if flse == False:
        err = 0
        for bi in slvd:
          for bx in bi:
            if len(str(bx)) == 1:
              err = 1
        if err == 1:
          raise Exception("Matrix can not be solved.")
        else:
          return slvd

