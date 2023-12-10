from tkinter import *
import time

class ReplayManager:
    def __init__(self, app):
        self.app = app
    def records(self):
        self.app.able = False
        self.app.Ron = False
        self.app.DB.db.commit()
        self.app.scores = []
        self.app.DB.cr.execute("SELECT date, score, id FROM Games"); rslt = self.app.DB.cr.fetchall()
        if len(rslt) == 0:
            self.app.scores.append("Empty")
        else:
            self.app.DB.cr.execute("SELECT MIN(score) FROM GAMES"); maxS = self.app.DB.cr.fetchall()
            for i in rslt:
                item = "  {} || {} sec. _{}".format(str(i[0])[:len(str(i[0]))-3], str(i[1]), str(i[2]))
                self.app.scores.append(item)
        self.app.win3 = Toplevel(self.app.root)
        self.app.cntrW(self.app.win3, 275, 155)
        self.app.win3.title("Records")
        self.app.win3.attributes('-topmost', 1)
        self.app.win3.protocol("WM_DELETE_WINDOW", self.app.win3close)
        Label(self.app.win3, text="Games:", font = "Helvetica 20").pack()
        Label(self.app.win3, text="Double click or select a record and hit Enter").pack()
        self.app.Rbox = Listbox(self.app.win3, fg="dark red")
        self.app.Rbox.pack(fill=BOTH, expand=True)

        self.app.scores = list(reversed(self.app.scores))
        for x in range(len(self.app.scores)):
            self.app.Rbox.insert(END, (self.app.scores[x]).split("_")[0])
            if len(rslt) != 0 and len(maxS) != 0:
                if int((self.app.scores[x]).split(" || ")[1].split(" sec.")[0]) == int(maxS[0][0]):
                    self.app.Rbox.itemconfig(x, {'bg':'gold'})
                    self.app.Rbox.itemconfig(x, {'fg':"blue"})
        self.app.Rbox.bind('<Return>', self.Replay)
        self.app.Rbox.bind('<Double-Button-1>', self.Replay)
        
    def Rclose(self):
        self.app.Ron = False
        self.app.rply.destroy()
  
    def Replay(self, event):
        if self.app.Ron == True:
            return
        self.app.reptime = StringVar()
        self.app.reptime.set("0.0")
        self.app.Rnowtime = time.time()
        self.app.Ron = True
        self.app.RBtxt = StringVar()
        self.app.RBtxt.set(">")
        self.app.info = self.app.scores[self.app.Rbox.curselection()[0]]
        
        if self.app.info == "Empty":
            return
        self.app.rply = Toplevel(self.app.win3)
        self.app.rply.title("Replay")
        self.app.cntrW(self.app.rply, 208, 235)
        self.app.rply.resizable(0, 0)
        self.app.rply.wm_attributes("-topmost", 1)
        self.app.rply.protocol("WM_DELETE_WINDOW", self.Rclose)
        Rfrm = Frame(self.app.rply)
        Rfrm.pack()
        Label(Rfrm, text="Replay:          ", fg="red").pack(side = LEFT)
        self.app.play = Button(Rfrm, textvariable = self.app.RBtxt, font="Times 20 bold", relief = FLAT, command = self.RBcom)
        self.app.play.pack(side = RIGHT)
        self.app.Rcan = Canvas(self.app.rply, width=200, height=200, bg="LightBlue")
        self.app.Rcan.pack()
        self.app.PrBrC = Canvas(self.app.rply, width=200, height=15, bg="LightGray")
        self.app.PrBrC.pack()
        self.app.prgrs()
        self.repcalc()
    def repcalc(self):
        self.app.DB.db.commit()
        self.app.DB.cr.execute("SELECT matrix, moves, times FROM Games WHERE id = {}".format(str(self.app.info.split("_")[1]))); rslt = self.app.DB.cr.fetchall()
        self.app.Mvs = []
        for i in range(len(rslt[0][1])-1):
            if i%2 == 0:
                self.app.Mvs.append(rslt[0][1][i:i+2])
        self.app.Tms = rslt[0][2].split("-")
        self.app.Umtx = []; v=[]; msplit = rslt[0][0].split("_")
        for i in msplit:
            v.append(str(i))
            if len(v) == 4:
                self.app.Umtx.append(v)
                v = []
        self.app.RFC = self.app.fixedCells(self.app.Umtx)
        self.app.Rsol = self.app.solve(self.app.Umtx)
        self.app.RPmtx = []
        for x in self.app.Umtx:
            v = []
            for n in x:
                v.append(n)
            self.app.RPmtx.append(v)
        self.Rdraw()
        
    
    def Rmove(self, move):
        if self.app.play["text"] == ">":
            return
        cell = self.app.RPmtx[int(move[0])][int(move[1])]
        if str(cell)[0] != '+':
            self.app.RPmtx[int(move[0])][int(move[1])] = '+'+str(abs(int(cell)))
        else:
            self.app.RPmtx[int(move[0])][int(move[1])] = str(-int(cell))
        self.Rdraw()
        self.app.x += 1
        if self.app.x == len(self.app.Mvs):
            return
        if self.app.play["text"] == '||':
            self.app.root.after(int(self.app.Tms[self.app.x]), lambda:self.Rmove(self.app.Mvs[self.app.x]))
        
    def RTmePass(self, sett=2):
        if sett == 1:
            return
        if sett == 0:
            self.app.reptime.set("0.0")
            self.app.Rnowtime = 0
        settt = str(self.app.Rnowtime)+".0"
        self.app.reptime.set(settt)
        self.app.Rnowtime += 1
        self.app.root.after(1000, self.RTmePass())
        
    def Rdraw(self):
        self.app.Rcan.delete("all")
        for x in range(0, 4):
            for y in range(0, 4):
                diff, CBclr = 4, "LightGrey"
                cell = self.app.RPmtx[y][x]
                if str(self.app.RPmtx[y][x])[0] == '+':
                    cell = self.app.RPmtx[y][x][1]
                    clr = 'VioletRed'
                elif int(self.app.RPmtx[y][x]) < 0:
                    cell = str(self.app.RPmtx[y][x])[1]
                    clr = 'Blue'
                else:
                    cell = str(self.app.RPmtx[y][x])
                    clr = 'Black'
                if self.app.RFC[y][x] == 1:
                    diff, CBclr = 0, "DarkGrey"
                self.app.Rcan.create_rectangle(x*50+1, y*50+1, x*50+52, y*50+52)
                self.app.Rcan.create_rectangle(x*50+5, y*50+5, x*50+48, y*50+48, fill = CBclr)
                if int(cell) == 1:
                    self.app.Rcan.create_rectangle(x*50+15+diff, y*50+15+diff, x*50+36-diff, y*50+36-diff, fill = clr)
                elif int(cell) == 2:
                    self.app.Rcan.create_oval(x*50+15+diff, y*50+15+diff, x*50+36-diff, y*50+36-diff, fill = clr)
                elif int(cell) == 3:
                    self.app.Rcan.create_polygon(x*50+25, y*50+15+diff, x*50+15+diff, y*50+36-diff, x*50+36-diff, y*50+36-diff, outline = "black", fill = clr)
                else:
                    self.app.Rcan.create_line(x*50+14+diff, y*50+14+diff, x*50+36-diff, y*50+36-diff, width = 3, fill = clr)
                    self.app.Rcan.create_line(x*50+36-diff, y*50+14+diff, x*50+14+diff, y*50+36-diff, width = 3, fill = clr)
        
    
    def RBcom(self):
        if self.app.play["text"] == ">":
            self.app.RBtxt.set("||")
            self.app.x = 0
            self.app.root.after(int(self.app.Tms[self.app.x]), lambda:self.Rmove(self.app.Mvs[self.app.x]))
        else:
            self.app.RBtxt.set(">")
            self.repcalc()
    

