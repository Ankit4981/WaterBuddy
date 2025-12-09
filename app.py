"""
WaterBuddy - Final Tkinter app (Static mascot, static avatar)
Corrected version — NO crashes, NO MascotScreens key error
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import date, datetime
import csv, os, random
try:
    from PIL import Image, ImageTk, ImageGrab
    PIL_AVAILABLE = True
except:
    PIL_AVAILABLE = False

# ----------------------------
# Config
# ----------------------------

WEEKLY_CSV = "weekly_data.csv"
ASSETS_DIR = "assets"

AGE_GOALS = {
    "Children (4-8 yrs)": 1200,
    "Teens (9-13 yrs)": 1700,
    "Adults (14-64 yrs)": 2000,
    "Seniors (65+ yrs)": 1700,
}

QUICK_AMOUNTS = [100, 150, 250, 500]

# ----------------------------
# CSV Helpers
# ----------------------------

def init_weekly_csv():
    if not os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "total"])

def save_today(total):
    today = str(date.today())
    rows = []
    if os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "r") as f:
            rows = list(csv.reader(f))
    rows = [r for r in rows if len(r) > 0 and r[0] != today]
    rows.append([today, total])
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def load_weekly():
    if not os.path.exists(WEEKLY_CSV):
        return []
    with open(WEEKLY_CSV, "r") as f:
        rows = list(csv.reader(f))[1:]
    return [(r[0], int(r[1])) for r in rows[-7:] if len(r) >= 2]

def reset_week():
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "total"])

# ----------------------------
# Mascot Manager (static swap only)
# ----------------------------

class MascotManager:
    def __init__(self, parent, size=(180,180)):
        self.parent = parent
        self.width, self.height = size
        self.use_png = self._check_pngs()
        self.label = tk.Label(parent, bg="white")
        self.label.pack()

        if self.use_png:
            self._load_pngs()
            self.set_mood("neutral")
        else:
            self.label.config(text="💧", font=("Arial", 40))

    def _check_pngs(self):
        needed = ["neutral.png","smile.png","cheer.png","celebrate.png"]
        if not os.path.isdir(ASSETS_DIR): return False
        for n in needed:
            if not os.path.exists(os.path.join(ASSETS_DIR, n)):
                return False
        return PIL_AVAILABLE

    def _load_pngs(self):
        self.photos = {}
        for name in ("neutral","smile","cheer","celebrate"):
            path = os.path.join(ASSETS_DIR, f"{name}.png")
            img = Image.open(path).resize((self.width, self.height))
            self.photos[name] = ImageTk.PhotoImage(img)

    def set_mood(self, mood="neutral"):
        if self.use_png:
            self.label.configure(image=self.photos.get(mood, self.photos["neutral"]))
        else:
            text_map = {"neutral":"💧","smile":"😊","cheer":"👏","celebrate":"🎉"}
            self.label.configure(text=text_map.get(mood,"💧"))

    def celebrate(self):
        self.set_mood("celebrate")

# ----------------------------
# Human Avatar Loader
# ----------------------------

class HumanAvatar:
    def __init__(self, parent, width=220, height=360, gender="Male"):
        self.parent = parent
        self.width = width
        self.height = height
        self.gender = gender

        self.use_png = self._check_pngs()
        self.label = tk.Label(parent, bg="white")
        self.label.pack()

        if self.use_png:
            self._load_pngs()
            self.set_gender(gender)
        else:
            self.label.config(text="👤", font=("Arial", 40))

    def _check_pngs(self):
        if not os.path.isdir(ASSETS_DIR): return False
        return (
            os.path.exists(os.path.join(ASSETS_DIR, "male.png")) and
            os.path.exists(os.path.join(ASSETS_DIR, "female.png")) and
            PIL_AVAILABLE
        )

    def _load_pngs(self):
        self.photo_male = ImageTk.PhotoImage(
            Image.open(os.path.join(ASSETS_DIR, "male.png")).resize((self.width, self.height))
        )
        self.photo_female = ImageTk.PhotoImage(
            Image.open(os.path.join(ASSETS_DIR, "female.png")).resize((self.width, self.height))
        )

    def set_gender(self, gender):
        if not self.use_png:
            return
        if gender.lower().startswith("m"):
            self.label.configure(image=self.photo_male)
        else:
            self.label.configure(image=self.photo_female)

# ----------------------------
# Main Application
# ----------------------------

class WaterBuddyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaterBuddy")
        self.geometry("420x760")
        self.resizable(False, False)

        init_weekly_csv()

        self.state = {
            "name": "",
            "age_group": "Adults (14-64 yrs)",
            "goal": AGE_GOALS["Adults (14-64 yrs)"],
            "gender": "Male",
            "weight": 70,
            "total": 0,
            "history": [],
        }

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (Welcome, NameScreen, AgeScreen, GenderScreen, WeightScreen,
                  GoalScreen, Dashboard, MascotScreen, SettingsScreen, WeeklyScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Welcome")

    def show_frame(self, name):
        f = self.frames[name]
        f.tkraise()
        if hasattr(f, "on_show"):
            f.on_show()

    def set_state(self, key, val):
        self.state[key] = val

    def log_amount(self, amt):
        now = datetime.now().strftime("%I:%M %p")
        self.state["total"] += amt
        self.state["history"].append((now, amt))
        self.frames["Dashboard"].update_display()

    def reset_day(self):
        save_today(self.state["total"])
        self.state["total"] = 0
        self.state["history"] = []
        self.frames["Dashboard"].update_display()

# ----------------------------
# Screens
# ----------------------------

class Welcome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="💧", font=("Arial", 50), bg="white").pack(pady=20)
        tk.Label(self, text="Welcome to WaterBuddy", font=("Arial", 20, "bold"), bg="white").pack()
        tk.Button(self, text="Continue", command=lambda: controller.show_frame("NameScreen")).pack(pady=20)

class NameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="What is your name?", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack()
        tk.Button(self, text="Continue", command=self.save).pack(pady=20)
        self.controller = controller

    def save(self):
        self.controller.set_state("name", self.entry.get())
        self.controller.show_frame("AgeScreen")

class AgeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Select your age group", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        self.controller = controller
        for grp, ml in AGE_GOALS.items():
            tk.Button(self, text=f"{grp} (~{ml}ml)",
                      command=lambda g=grp: self.select_age(g)).pack(pady=5)
        tk.Button(self, text="Continue", command=lambda: controller.show_frame("GenderScreen")).pack(pady=20)

    def select_age(self, grp):
        self.controller.set_state("age_group", grp)
        self.controller.set_state("goal", AGE_GOALS[grp])

class GenderScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Choose your gender", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        tk.Button(self, text="Male", command=lambda: self.set_gender("Male")).pack(pady=5)
        tk.Button(self, text="Female", command=lambda: self.set_gender("Female")).pack(pady=5)
        tk.Button(self, text="Continue", command=lambda: controller.show_frame("WeightScreen")).pack(pady=20)

    def set_gender(self, g):
        self.controller.set_state("gender", g)

class WeightScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Your weight (kg)", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.insert(0, "70")
        self.entry.pack()
        tk.Button(self, text="Continue", command=self.save).pack(pady=20)

    def save(self):
        try:
            w = float(self.entry.get())
        except:
            w = 70
        base = AGE_GOALS[self.controller.state["age_group"]]
        self.controller.set_state("weight", w)
        self.controller.set_state("goal", base)
        self.controller.show_frame("GoalScreen")

class GoalScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="Your Daily Goal", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

        self.goal_var = tk.IntVar(value=controller.state["goal"])
        tk.Label(self, textvariable=self.goal_var, font=("Arial", 26, "bold"), bg="white").pack()

        tk.Button(self, text="-100", command=lambda: self.change(-100)).pack(pady=5)
        tk.Button(self, text="+100", command=lambda: self.change(100)).pack(pady=5)

        tk.Button(self, text="Start Tracking",
                  command=self.save).pack(pady=20)

    def change(self, amt):
        new = self.goal_var.get() + amt
        if new < 500:
            new = 500
        self.goal_var.set(new)

    def save(self):
        self.controller.set_state("goal", self.goal_var.get())
        self.controller.show_frame("Dashboard")

class Dashboard(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text=datetime.now().strftime("%A, %d %b"), bg="white").pack(pady=5)

        main = tk.Frame(self, bg="white")
        main.pack()

        left = tk.Frame(main, bg="white")
        left.pack(side="left", padx=10)

        right = tk.Frame(main, bg="white")
        right.pack(side="left", padx=10)

        self.avatar = HumanAvatar(left, gender=controller.state["gender"])
        self.mascot = MascotManager(right)

        self.msg = tk.Label(self, text="Let's stay hydrated!", bg="white", font=("Arial", 12))
        self.msg.pack(pady=10)

        self.pvar = tk.IntVar(value=0)
        ttk.Progressbar(self, length=350, variable=self.pvar, maximum=100).pack(pady=10)

        self.stats = tk.Label(self, text="", bg="white")
        self.stats.pack()

        # Quick buttons
        for amt in QUICK_AMOUNTS:
            tk.Button(self, text=f"+{amt}ml", command=lambda a=amt: self.add(a)).pack(pady=3)

        # Manual input
        self.manual = tk.Entry(self)
        self.manual.pack(pady=4)
        tk.Button(self, text="Add", command=self.add_manual).pack()

        self.remaining = tk.Label(self, text="", bg="white")
        self.remaining.pack()

        tk.Button(self, text="New Day (Save)", command=self.reset_day).pack(pady=10)
        tk.Button(self, text="Weekly Summary",
                  command=lambda: controller.show_frame("WeeklyScreen")).pack()

        self.history = tk.Text(self, width=40, height=6)
        self.history.pack(pady=10)

        self.update_display()

    def on_show(self):
        self.avatar.set_gender(self.controller.state["gender"])
        self.update_display()

    def add(self, amt):
        self.controller.log_amount(amt)

    def add_manual(self):
        try:
            v = int(self.manual.get())
            if v > 0:
                self.controller.log_amount(v)
                self.manual.delete(0, tk.END)
        except:
            messagebox.showwarning("Invalid", "Enter a valid number")

    def reset_day(self):
        if messagebox.askyesno("New Day", "Save and reset today?"):
            self.controller.reset_day()

    def update_display(self):
        total = self.controller.state["total"]
        goal = self.controller.state["goal"]
        pct = min(100, int((total / goal) * 100)) if goal > 0 else 0

        self.pvar.set(pct)
        self.stats.config(text=f"Total: {total} ml ({pct}%)")
        self.remaining.config(text=f"Remaining: {max(0, goal-total)} ml")

        # mascot logic
        if pct >= 100:
            self.mascot.set_mood("celebrate")
            self.msg.config(text="Goal Completed! 🎉")
        elif pct >= 75:
            self.mascot.set_mood("cheer")
            self.msg.config(text="Almost there! Keep going!")
        elif pct >= 50:
            self.mascot.set_mood("smile")
            self.msg.config(text="Nice progress!")
        else:
            self.mascot.set_mood("neutral")
            self.msg.config(text="Let's stay hydrated!")

        # history
        self.history.delete("1.0", tk.END)
        for t, amt in reversed(self.controller.state["history"][-8:]):
            self.history.insert(tk.END, f"{t} — {amt}ml\n")

class MascotScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Mascot Test", font=("Arial", 16, "bold"), bg="white").pack(pady=20)
        holder = tk.Frame(self, bg="white")
        holder.pack()
        self.mascot = MascotManager(holder)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("Dashboard")).pack(pady=20)

class SettingsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        tk.Label(self, text="Settings", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        tk.Button(self, text="Reset Week", command=self.reset_week).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("Dashboard")).pack(pady=20)

    def reset_week(self):
        reset_week()
        messagebox.showinfo("Reset", "Weekly history cleared.")

class WeeklyScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Weekly Summary", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        self.listbox = tk.Listbox(self, width=45, height=12)
        self.listbox.pack()
        tk.Button(self, text="Back", command=lambda: controller.show_frame("Dashboard")).pack(pady=20)

    def on_show(self):
        self.update_week()

    def update_week(self):
        self.listbox.delete(0, tk.END)
        rows = load_weekly()
        if not rows:
            self.listbox.insert(tk.END, "No weekly data yet.")
            return
        maxv = max(t for _, t in rows)
        for d, t in rows:
            bar = "█" * int((t / maxv) * 20) if maxv else ""
            self.listbox.insert(tk.END, f"{d}: {bar} {t}ml")

# ----------------------------
# Run App
# ----------------------------

if __name__ == "__main__":
    app = WaterBuddyApp()
    app.mainloop()
