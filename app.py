# Paste this entire code into app.py (overwrite existing)
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import turtle
from turtle import RawTurtle, TurtleScreen
from datetime import date, datetime
import csv, os, threading, random
from PIL import ImageGrab, Image, ImageTk  # Pillow (optional) - used for screenshot & PNG mascot

WEEKLY_CSV = "weekly_data.csv"
ASSETS_DIR = "assets"  # optional folder for PNG mascots

AGE_GOALS = {
    "Children (4-8 yrs)": 1200,
    "Teens (9-13 yrs)": 1700,
    "Adults (14-64 yrs)": 2000,
    "Seniors (65+ yrs)": 1700,
}
QUICK_AMOUNTS = [100, 150, 250, 500]
DEFAULT_QUICK = 250
TIPS = [
    "Keep a bottle on your desk to sip often.",
    "Drink a glass before meals.",
    "Add lemon to water for flavor.",
    "Small sips throughout the day add up.",
]

# ---------- CSV helpers ----------
def init_weekly_csv():
    if not os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "total"])

def save_today(total):
    today = str(date.today())
    rows = []
    if os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "r", newline="") as f:
            rows = list(csv.reader(f))
    rows = [r for r in rows if len(r)>0 and r[0]!=today]
    rows.append([today, total])
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def load_weekly():
    if not os.path.exists(WEEKLY_CSV):
        return []
    with open(WEEKLY_CSV, "r", newline="") as f:
        rows = list(csv.reader(f))[1:]
    return [(r[0], int(r[1])) for r in rows[-7:] if len(r)>=2]

def reset_week():
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date","total"])

# ---------- Mascot (Turtle) ----------
class MascotCanvas:
    def __init__(self, parent, width=220, height=220, use_png=False):
        self.parent = parent
        self.width = width
        self.height = height
        self.use_png = use_png and self._find_png()
        if self.use_png:
            # PNG handling via PIL's ImageTk
            self.img_label = tk.Label(parent, bg="white")
            self.img_label.pack()
            self._set_png("neutral")
        else:
            self.canvas = tk.Canvas(parent, width=width, height=height, bg="white", highlightthickness=0)
            self.canvas.pack()
            self.screen = TurtleScreen(self.canvas)
            self.t = RawTurtle(self.screen)
            self.t.hideturtle()
            self.screen.tracer(0,0)

    def _find_png(self):
        # check assets folder for mascots: neutral.png, smile.png, cheer.png, celebrate.png
        if not os.path.isdir(ASSETS_DIR):
            return False
        for name in ("neutral.png","smile.png","cheer.png","celebrate.png"):
            if not os.path.exists(os.path.join(ASSETS_DIR, name)):
                return False
        return True

    def _set_png(self, mood):
        # load the appropriate PNG
        path = os.path.join(ASSETS_DIR, f"{mood}.png")
        try:
            img = Image.open(path).resize((self.width, self.height))
            self.photo = ImageTk.PhotoImage(img)
            self.img_label.configure(image=self.photo)
        except Exception as e:
            print("PNG load failed:", e)

    def clear(self):
        if self.use_png:
            self._set_png("neutral")
        else:
            self.t.clear()
            self.screen.clear()
            self.screen = TurtleScreen(self.canvas)
            self.t = RawTurtle(self.screen)
            self.t.hideturtle()
            self.screen.tracer(0,0)

    def draw_drop_base(self):
        t = self.t
        t.pu()
        t.goto(0,-40)
        t.setheading(0)
        t.pd()
        t.color("#0ea5e9", "#0ea5e9")
        t.begin_fill()
        t.circle(40)
        t.left(90)
        t.forward(60)
        t.right(135)
        t.forward(45)
        t.right(90)
        t.forward(45)
        t.end_fill()
        t.pu()
        t.home()

    def draw_face(self, mood="neutral"):
        t = self.t
        t.pu()
        t.goto(-15,0); t.pd(); t.color("black"); t.begin_fill(); t.circle(4); t.end_fill(); t.pu()
        t.goto(15,0); t.pd(); t.begin_fill(); t.circle(4); t.end_fill(); t.pu()
        t.goto(0,-10); t.pd(); t.width(3)
        if mood=="smile": t.setheading(-60); t.circle(15,120)
        elif mood=="cheer": t.setheading(-50); t.circle(20,100)
        elif mood=="surprise": t.pu(); t.goto(0,-14); t.pd(); t.begin_fill(); t.circle(5); t.end_fill()
        else: t.setheading(-90); t.forward(4)
        t.pu(); t.home()

    def animate(self, mood="neutral"):
        if self.use_png:
            self._set_png({"neutral":"neutral","smile":"smile","cheer":"cheer","celebrate":"celebrate"}.get(mood,"neutral"))
        else:
            self.clear()
            self.draw_drop_base()
            self.draw_face(mood=mood)
            self.screen.update()

    def celebration(self):
        if self.use_png:
            self._set_png("celebrate")
            return
        t = self.t
        for scale in (1.0,1.08,1.15,1.08,1.0):
            self.clear()
            t.pu(); t.goto(0,-40*scale); t.pd()
            t.color("#0ea5e9","#0ea5e9"); t.begin_fill(); t.circle(40*scale)
            t.left(90); t.forward(60*scale); t.right(135); t.forward(45*scale); t.right(90); t.forward(45*scale); t.end_fill()
            t.pu(); t.home()
            t.goto(-15*scale,0); t.pd(); t.color("black"); t.begin_fill(); t.circle(4*scale); t.end_fill(); t.pu()
            t.goto(15*scale,0); t.pd(); t.begin_fill(); t.circle(4*scale); t.end_fill(); t.pu()
            t.goto(0,-10*scale); t.pd(); t.width(3); t.setheading(-60); t.circle(15*scale,120); t.pu()
            self.screen.update()
            self.screen.ontimer(lambda: None, 120)
        for i in range(12):
            x = random.randint(-80,80); y = random.randint(-80,80)
            t.pu(); t.goto(x,y); t.pd(); t.color(random.choice(["#ff006e","#ffd166","#06d6a0","#118ab2"])); t.begin_fill(); t.circle(3); t.end_fill(); t.pu()
            self.screen.update()

# ---------- App ----------
class WaterBuddyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaterBuddy")
        self.geometry("420x760")
        self.resizable(False,False)
        init_weekly_csv()

        # app state
        self.state = {
            "name": "",
            "age_group": "Adults (14-64 yrs)",
            "goal": AGE_GOALS["Adults (14-64 yrs)"],
            "gender": "Male",
            "weight": 70,
            "unit": "kg",
            "total": 0,
            "history": [],
        }

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=8, pady=8)
        self.frames = {}
        for F in (WelcomeScreen, NameScreen, AgeScreen, GenderScreen, WeightScreen,
                  GoalScreen, DashboardScreen, MascotScreens, SettingsScreen, WeeklyScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame("WelcomeScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame,"on_show"): frame.on_show()

    def set_state(self,key,value): self.state[key]=value
    def log_amount(self, amount):
        if amount<=0: return
        now = datetime.now().strftime("%I:%M %p")
        self.state["total"] += int(amount)
        self.state["history"].append((now,int(amount)))
        self.frames["DashboardScreen"].update_display()
    def reset_day(self):
        save_today(self.state["total"])
        self.state["total"]=0
        self.state["history"]=[]
        messagebox.showinfo("Reset","Day saved and reset.")
        self.show_frame("DashboardScreen")
    def reset_week(self):
        reset_week(); messagebox.showinfo("Reset","Weekly data cleared."); self.show_frame("DashboardScreen")

# ---------- Screens (kept similar to prior version but text/fonts tuned) ----------
class WelcomeScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white")
        self.controller=controller
        tk.Label(self,text="💧",font=("Helvetica",50),bg="white").pack(pady=(40,10))
        tk.Label(self,text="Welcome to WaterBuddy",font=("Helvetica",20,"bold"),bg="white").pack()
        tk.Label(self,text="Your friendly hydration companion",bg="white").pack(pady=(4,18))
        tk.Button(self,text="Continue",bg="#CAF0F8",width=20,command=lambda:controller.show_frame("NameScreen")).pack(pady=20)

class NameScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="What is your name?",font=("Helvetica",18,"bold"),bg="white").pack(pady=(30,6))
        tk.Label(self,text="(optional, used to personalize messages)",bg="white").pack()
        self.entry=tk.Entry(self,font=("Arial",14)); self.entry.pack(pady=18,ipadx=20,ipady=6)
        tk.Button(self,text="Continue",bg="#CAF0F8",command=self.save).pack()
    def save(self):
        self.controller.set_state("name",self.entry.get().strip()); self.controller.show_frame("AgeScreen")

class AgeScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="Select your age group",font=("Helvetica",14,"bold"),bg="white").pack(pady=14)
        self.buttons=[]
        for grp,ml in AGE_GOALS.items():
            b=tk.Button(self,text=f"{grp}\n~{ml} ml",width=22,height=2,command=lambda g=grp:self.select(g))
            b.pack(pady=6); self.buttons.append(b)
        tk.Button(self,text="Continue",bg="#CAF0F8",command=lambda:controller.show_frame("GenderScreen")).pack(pady=12)
    def select(self,grp):
        self.controller.set_state("age_group",grp)
        self.controller.set_state("goal",AGE_GOALS.get(grp,2000))
        for b in self.buttons:
            if b.cget("text").startswith(grp): b.config(bg="#dbeafe")
            else: b.config(bg="SystemButtonFace")

class GenderScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="Select Gender (optional)",font=("Helvetica",16,"bold"),bg="white").pack(pady=18)
        tk.Button(self,text="Male",width=20,command=lambda:controller.set_state("gender","Male")).pack(pady=6)
        tk.Button(self,text="Female",width=20,command=lambda:controller.set_state("gender","Female")).pack(pady=6)
        tk.Button(self,text="Continue",bg="#CAF0F8",command=lambda:controller.show_frame("WeightScreen")).pack(pady=12)

class WeightScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="Your weight (optional)",font=("Helvetica",16,"bold"),bg="white").pack(pady=12)
        self.unit=tk.StringVar(value="kg"); uf=tk.Frame(self,bg="white"); uf.pack(pady=6)
        tk.Radiobutton(uf,text="kg",variable=self.unit,value="kg",bg="white").pack(side="left",padx=8)
        tk.Radiobutton(uf,text="lbs",variable=self.unit,value="lbs",bg="white").pack(side="left",padx=8)
        self.entry=tk.Entry(self); self.entry.insert(0,"70"); self.entry.pack(pady=10)
        tk.Button(self,text="Continue",bg="#CAF0F8",command=self.save).pack()
    def save(self):
        try: w=float(self.entry.get())
        except: w=70
        if self.unit.get()=="lbs": w=w*0.453592
        base=AGE_GOALS.get(self.controller.state["age_group"],2000)
        tweak=int((w-70)*10)
        new_goal=max(1000,base+tweak)
        self.controller.set_state("weight",int(w)); self.controller.set_state("unit",self.unit.get())
        self.controller.set_state("goal",new_goal); self.controller.show_frame("GoalScreen")

class GoalScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="Daily Goal",font=("Helvetica",18,"bold"),bg="white").pack(pady=12)
        tk.Label(self,text="Tap +/- to adjust or continue to start tracking.",bg="white").pack()
        self.var=tk.IntVar(value=self.controller.state.get("goal",2000))
        tk.Label(self,textvariable=self.var,font=("Helvetica",28,"bold"),bg="white").pack(pady=8)
        bf=tk.Frame(self,bg="white"); bf.pack()
        tk.Button(bf,text="-100",command=lambda:self.change(-100)).pack(side="left",padx=6)
        tk.Button(bf,text="+100",command=lambda:self.change(100)).pack(side="left",padx=6)
        tk.Button(self,text="Start Tracking",bg="#CAF0F8",command=self.save).pack(pady=14)
    def change(self,d):
        v=self.var.get()+d
        if v<500: v=500
        self.var.set(v)
    def save(self):
        self.controller.set_state("goal",int(self.var.get())); self.controller.show_frame("DashboardScreen")

class DashboardScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        top=tk.Frame(self,bg="white"); top.pack(fill="x")
        self.date_label=tk.Label(top,text="",bg="white"); self.date_label.pack(side="left",padx=6)
        tk.Button(top,text="Settings",command=lambda:controller.show_frame("SettingsScreen")).pack(side="right",padx=6)
        self.mascot_holder=tk.Frame(self,bg="white"); self.mascot_holder.pack(pady=6)
        use_png = os.path.isdir(ASSETS_DIR)
        self.mascot = MascotCanvas(self.mascot_holder,220,220,use_png)
        self.msg_label=tk.Label(self,text="Let's stay hydrated!",bg="white",font=("Helvetica",12)); self.msg_label.pack(pady=6)
        pf = tk.Frame(self,bg="white"); pf.pack(pady=6)
        self.pvar = tk.IntVar(value=0)
        self.pbar = ttk.Progressbar(pf,orient="horizontal",length=320,mode="determinate",maximum=100,variable=self.pvar)
        self.pbar.pack()
        self.stat_label=tk.Label(self,text="",bg="white"); self.stat_label.pack(pady=6)
        qf=tk.Frame(self,bg="white"); qf.pack(pady=8)
        for amt in QUICK_AMOUNTS:
            tk.Button(qf,text=f"+{amt} ml",width=8,command=lambda a=amt: self.quick(a)).pack(side="left",padx=4)
        tk.Button(self,text="+250 ml (Quick)",bg="#CAF0F8",width=20,command=lambda: self.quick(DEFAULT_QUICK)).pack(pady=8)
        mf=tk.Frame(self,bg="white"); mf.pack(pady=6)
        tk.Label(mf,text="Add custom amount (ml):",bg="white").pack(side="left")
        self.manual=tk.Entry(mf,width=8); self.manual.pack(side="left",padx=6)
        tk.Button(mf,text="Add",command=self.add_manual).pack(side="left")
        self.rem_label=tk.Label(self,text="",bg="white"); self.rem_label.pack(pady=6)
        tk.Button(self,text="Reset / New Day (Save)",command=self.reset_confirm).pack(pady=6)
        tk.Button(self,text="Weekly Summary",command=lambda:controller.show_frame("WeeklyScreen")).pack()
        self.hist=tk.Text(self,height=6,width=42); self.hist.pack(pady=6)
        self.update_display()
    def on_show(self): self.update_display()
    def update_display(self):
        self.date_label.config(text=datetime.now().strftime("%A, %d %b %Y"))
        total=self.controller.state["total"]; goal=self.controller.state["goal"]
        rem=max(goal-total,0); pct=int((total/goal)*100) if goal>0 else 0; pct=max(0,min(100,pct))
        self.pvar.set(pct); self.stat_label.config(text=f"{total} ml   •   {pct}%"); self.rem_label.config(text=f"Remaining: {rem} ml")
        if pct>=100:
            threading.Thread(target=self.controller.frames["MascotScreens"].celebrate_mascot).start(); msg="You did it! Goal completed! 🎉"
        elif pct>=75:
            self.controller.frames["MascotScreens"].set_mood("cheer"); msg="Amazing! Just a little more!"
        elif pct>=50:
            self.controller.frames["MascotScreens"].set_mood("smile"); msg="Great! You're halfway!"
        else:
            self.controller.frames["MascotScreens"].set_mood("wave"); msg="Small sips add up!"
        self.msg_label.config(text=msg)
        self.hist.delete("1.0",tk.END)
        for t,amt in reversed(self.controller.state["history"][-8:]):
            self.hist.insert(tk.END,f"{t} — {amt} ml\n")
    def quick(self,amt):
        self.controller.log_amount(amt); self.update_display()
    def add_manual(self):
        try:
            v=int(float(self.manual.get())); 
            if v>0: self.controller.log_amount(v); self.manual.delete(0,tk.END); self.update_display()
            else: messagebox.showwarning("Amount","Enter amount > 0")
        except:
            messagebox.showwarning("Invalid","Enter a valid number")
    def reset_confirm(self):
        if messagebox.askyesno("Reset Day","Save today's total and reset the day?"):
            save_today(self.controller.state["total"]); self.controller.reset_day(); self.update_display()

class MascotScreens(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        self.canvas_holder=tk.Frame(self,bg="white"); self.canvas_holder.pack(pady=10)
        use_png = os.path.isdir(ASSETS_DIR)
        self.mascot = MascotCanvas(self.canvas_holder,220,220,use_png)
        tf=tk.Frame(self,bg="white"); tf.pack(pady=6)
        tk.Button(tf,text="Test Smile",command=lambda: self.set_mood("smile")).pack(side="left",padx=4)
        tk.Button(tf,text="Test Cheer",command=lambda: self.set_mood("cheer")).pack(side="left",padx=4)
        tk.Button(tf,text="Celebrate",command=self.celebrate_mascot).pack(side="left",padx=4)
        tk.Button(self,text="Back to Dashboard",command=lambda: controller.show_frame("DashboardScreen")).pack(pady=8)
    def set_mood(self,m):
        if m=="smile": self.mascot.animate("smile")
        elif m=="cheer": self.mascot.animate("cheer")
        else: self.mascot.animate("neutral")
    def celebrate_mascot(self): self.mascot.celebration()

class SettingsScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="Settings",font=("Helvetica",18,"bold"),bg="white").pack(pady=8)
        prof=tk.Frame(self,bg="#e6f7ff",padx=8,pady=8); prof.pack(pady=6,fill="x")
        tk.Label(prof,text=self.controller.state.get("name","User"),font=("Helvetica",14,"bold"),bg="#e6f7ff").pack()
        tk.Label(prof,text=f"Goal: {self.controller.state.get('goal',2000)} ml",bg="#e6f7ff").pack()
        tk.Button(self,text="Set Reminder (demo)",command=self.set_reminder).pack(pady=6)
        tk.Button(self,text="Export Screenshot (PNG)",command=self.export_screenshot).pack(pady=6)
        tk.Button(self,text="Reset Weekly Chart",command=self.reset_week_confirm).pack(pady=6)
        tk.Button(self,text="Back",command=lambda: controller.show_frame("DashboardScreen")).pack(pady=8)
    def set_reminder(self):
        sec=simpledialog.askinteger("Reminder","Remind me in how many seconds? (demo)",minvalue=5,maxvalue=86400)
        if sec: self.after(sec*1000,lambda: messagebox.showinfo("Hydration Reminder","Time to take a sip!")); messagebox.showinfo("Set","Reminder set.")
    def export_screenshot(self):
        # try to capture the window and save as PNG (requires Pillow/ImageGrab)
        try:
            x=self.controller.winfo_rootx(); y=self.controller.winfo_rooty()
            w=self.controller.winfo_width(); h=self.controller.winfo_height()
            img=ImageGrab.grab(bbox=(x,y,x+w,y+h))
            path = filedialog.asksaveasfilename(defaultextension=".png",filetypes=[("PNG","*.png")],initialfile="waterbuddy_screenshot.png")
            if path:
                img.save(path); messagebox.showinfo("Saved",f"Screenshot saved to {path}")
        except Exception as e:
            messagebox.showerror("Error",f"Screenshot failed: {e}")
    def reset_week_confirm(self):
        if messagebox.askyesno("Reset Week","Clear weekly data?"): reset_week(); messagebox.showinfo("Done","Weekly cleared.")

class WeeklyScreen(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white"); self.controller=controller
        tk.Label(self,text="Weekly Summary",font=("Helvetica",18,"bold"),bg="white").pack(pady=8)
        self.listbox=tk.Listbox(self,width=40,height=12); self.listbox.pack(pady=6)
        tk.Button(self,text="Back",command=lambda:controller.show_frame("DashboardScreen")).pack(pady=8)
    def on_show(self): self.update_week()
    def update_week(self):
        self.listbox.delete(0,tk.END)
        rows=load_weekly()
        if not rows: self.listbox.insert(tk.END,"No weekly data yet. Save a day first.")
        else:
            maxv=max([t for (_,t) in rows])
            for d,t in rows:
                self.listbox.insert(tk.END,f"{d} — {t} ml")
            self.listbox.insert(tk.END,"-"*30)
            for d,t in rows:
                length=int((t/maxv)*30) if maxv>0 else 0
                self.listbox.insert(tk.END,f"{d[-5:]} | {'█'*length} {t} ml")

# ---------- Run ----------
if __name__ == "__main__":
    app = WaterBuddyApp(); app.mainloop()
