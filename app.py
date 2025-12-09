"""
WaterBuddy - Final Tkinter app (Option B, static mascot)
- Uses assets/male.png and assets/female.png if present (keeps shirt text)
- Mascot uses assets/neutral.png, smile.png, cheer.png, celebrate.png if present (static swaps)
- Falls back to turtle drawings if PNGs or Pillow not available
- Weekly CSV save, reset day/week, reminders, screenshot (Pillow required)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import date, datetime
import csv, os, threading, random
try:
    from PIL import Image, ImageTk, ImageGrab
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

# ----------------------------
# Config / Constants
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
DEFAULT_QUICK = 250
TIPS = [
    "Keep a bottle on your desk to sip often.",
    "Drink a glass before meals.",
    "Add lemon or mint to make water more refreshing.",
    "Small sips throughout the day add up.",
]

# ----------------------------
# CSV utilities
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
        with open(WEEKLY_CSV, "r", newline="") as f:
            rows = list(csv.reader(f))
    rows = [r for r in rows if len(r)>0 and r[0] != today]
    rows.append([today, total])
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def load_weekly():
    if not os.path.exists(WEEKLY_CSV):
        return []
    with open(WEEKLY_CSV, "r", newline="") as f:
        rows = list(csv.reader(f))[1:]
    rows = rows[-7:]
    return [(r[0], int(r[1])) for r in rows if len(r) >= 2]

def reset_week():
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "total"])

# ----------------------------
# Mascot manager (static swaps)
# ----------------------------
class MascotManager:
    def __init__(self, parent, size=(180,180)):
        self.parent = parent
        self.width, self.height = size
        self.use_png = self._check_pngs()
        self.photos = {}
        if self.use_png and PIL_AVAILABLE:
            self.label = tk.Label(parent, bg="white")
            self.label.pack()
            self._load_pngs()
            self.set_mood("neutral")
        else:
            # if Pillow not available, use a placeholder label
            self.label = tk.Label(parent, text="💧", font=("Arial", 36), bg="white")
            self.label.pack()

    def _check_pngs(self):
        needed = ["neutral.png","smile.png","cheer.png","celebrate.png"]
        if not os.path.isdir(ASSETS_DIR): return False
        for n in needed:
            if not os.path.exists(os.path.join(ASSETS_DIR, n)):
                return False
        if not PIL_AVAILABLE: return False
        return True

    def _load_pngs(self):
        for name in ("neutral","smile","cheer","celebrate"):
            path = os.path.join(ASSETS_DIR, f"{name}.png")
            try:
                img = Image.open(path).resize((self.width, self.height))
                self.photos[name] = ImageTk.PhotoImage(img)
            except Exception as e:
                print("Mascot PNG load error:", e)
                self.use_png = False
                return

    def set_mood(self, mood="neutral"):
        if self.use_png and PIL_AVAILABLE:
            img = self.photos.get(mood, self.photos.get("neutral"))
            self.label.configure(image=img)
            self.label.image = img
        else:
            # text fallback (static)
            fallback_map = {"neutral":"💧","smile":"😊","cheer":"👏","celebrate":"🎉"}
            self.label.configure(text=fallback_map.get(mood,"💧"))

    def celebrate(self):
        # static celebrate (no animation), just swap image
        self.set_mood("celebrate")

# ----------------------------
# Human avatar (PNG fallback or drawn canvas)
# ----------------------------
class HumanAvatar:
    def __init__(self, parent, width=220, height=360, gender="Male"):
        self.parent = parent
        self.width = width
        self.height = height
        self.gender = gender
        self.use_png = self._check_pngs()
        self.photo_male = None
        self.photo_female = None
        if self.use_png and PIL_AVAILABLE:
            self.label = tk.Label(parent, bg="white")
            self.label.pack()
            self._load_pngs()
            self.set_gender(gender)
        else:
            self.canvas = tk.Canvas(parent, width=width, height=height, bg="white", highlightthickness=0)
            self.canvas.pack()
            self.draw(gender)

    def _check_pngs(self):
        male_path = os.path.join(ASSETS_DIR, "male.png")
        female_path = os.path.join(ASSETS_DIR, "female.png")
        if not os.path.isdir(ASSETS_DIR):
            return False
        if not (os.path.exists(male_path) and os.path.exists(female_path)):
            return False
        if not PIL_AVAILABLE:
            return False
        return True

    def _load_pngs(self):
        try:
            male_path = os.path.join(ASSETS_DIR, "male.png")
            female_path = os.path.join(ASSETS_DIR, "female.png")
            male_img = Image.open(male_path).resize((self.width, self.height))
            female_img = Image.open(female_path).resize((self.width, self.height))
            self.photo_male = ImageTk.PhotoImage(male_img)
            self.photo_female = ImageTk.PhotoImage(female_img)
        except Exception as e:
            print("Avatar load failed:", e)
            self.use_png = False

    def set_gender(self, gender):
        self.gender = gender
        if self.use_png and PIL_AVAILABLE and self.photo_male and self.photo_female:
            if gender.lower().startswith("m"):
                self.label.configure(image=self.photo_male)
                self.label.image = self.photo_male
            else:
                self.label.configure(image=self.photo_female)
                self.label.image = self.photo_female
        else:
            self.draw(gender)

    def draw(self, gender="Male"):
        self.canvas.delete("all")
        cx = self.width // 2
        # head
        self.canvas.create_oval(cx-24, 30, cx+24, 78, fill="#f1c9b6", outline="")
        # body
        fill_color = "#e6f2ff" if gender.lower().startswith("m") else "#ffe6f0"
        self.canvas.create_rectangle(cx-30, 78, cx+30, 220, fill=fill_color, outline="")
        # arms
        self.canvas.create_line(cx-30, 110, cx-70, 160, width=8)
        self.canvas.create_line(cx+30, 110, cx+70, 160, width=8)
        # legs
        self.canvas.create_line(cx-15, 220, cx-15, 320, width=8)
        self.canvas.create_line(cx+15, 220, cx+15, 320, width=8)
        # shirt area (we won't overlay text — we assume PNG has text if you wanted it)
        if gender.lower().startswith("m"):
            self.canvas.create_rectangle(cx-30, 160, cx+30, 200, fill="#cfe0ff", outline="")
        else:
            self.canvas.create_rectangle(cx-30, 160, cx+30, 200, fill="#ffd6e8", outline="")
        self.canvas.create_text(cx, 130, text="Let's stay hydrated!", font=("Helvetica", 9, "bold"))

# ----------------------------
# Main App
# ----------------------------
class WaterBuddyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WaterBuddy")
        self.geometry("420x760")
        self.resizable(False, False)
        init_weekly_csv()

        # state
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
        container.pack(fill="both", expand=True)
        self.frames = {}
        for F in (Welcome, NameScreen, AgeScreen, GenderScreen, WeightScreen, GoalScreen,
                  Dashboard, MascotScreen, SettingsScreen, WeeklyScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Welcome")

    def show_frame(self, name):
        f = self.frames[name]
        f.tkraise()
        if hasattr(f, "on_show"):
            f.on_show()

    def set_state(self, key, value):
        self.state[key] = value

    def log_amount(self, amount):
        if amount <= 0:
            return
        now = datetime.now().strftime("%I:%M %p")
        self.state["total"] += int(amount)
        self.state["history"].append((now, int(amount)))
        if "Dashboard" in self.frames:
            self.frames["Dashboard"].update_display()

    def reset_day(self):
        save_today(self.state["total"])
        self.state["total"] = 0
        self.state["history"] = []
        messagebox.showinfo("Saved", "Today's total saved to weekly history and reset.")
        self.show_frame("Dashboard")

    def reset_week(self):
        reset_week()
        messagebox.showinfo("Reset", "Weekly history cleared.")
        self.show_frame("Dashboard")

# ---------- Frames ----------
class Welcome(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="💧", font=("Helvetica", 50), bg="white").pack(pady=(40,10))
        tk.Label(self, text="Welcome To WaterBuddy", font=("Helvetica", 20, "bold"), bg="white").pack()
        tk.Label(self, text="Stay fresh through the day\nlet WaterBuddy guide your way", bg="white").pack(pady=(6,18))
        tk.Button(self, text="Continue", bg="#CAF0F8", width=20, command=lambda: controller.show_frame("NameScreen")).pack(pady=20)

class NameScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="What is your name?", font=("Helvetica", 18, "bold"), bg="white").pack(pady=(30,6))
        tk.Label(self, text="Only used to personalize your experience.", bg="white").pack()
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack(pady=18, ipadx=20, ipady=6)
        tk.Button(self, text="Continue", bg="#CAF0F8", command=self.save).pack()

    def save(self):
        name = self.entry.get().strip()
        self.controller.set_state("name", name)
        self.controller.show_frame("AgeScreen")

class AgeScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Select your age group", font=("Helvetica", 14, "bold"), bg="white").pack(pady=12)
        self.btns = []
        for grp, ml in AGE_GOALS.items():
            b = tk.Button(self, text=f"{grp}\n~{ml} ml", width=22, height=2, command=lambda g=grp: self.select_age(g))
            b.pack(pady=6)
            self.btns.append(b)
        tk.Button(self, text="Continue", bg="#CAF0F8", command=lambda: controller.show_frame("GenderScreen")).pack(pady=12)

    def select_age(self, grp):
        self.controller.set_state("age_group", grp)
        self.controller.set_state("goal", AGE_GOALS.get(grp, 2000))
        for b in self.btns:
            if b.cget("text").startswith(grp):
                b.config(bg="#dbeafe")
            else:
                b.config(bg="SystemButtonFace")

class GenderScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Choose your gender", font=("Helvetica", 16, "bold"), bg="white").pack(pady=16)
        tk.Label(self, text="We use your body type to tailor your daily water intake.", bg="white").pack(pady=6)
        tk.Button(self, text="Male", width=20, command=lambda: self.set_gender("Male")).pack(pady=6)
        tk.Button(self, text="Female", width=20, command=lambda: self.set_gender("Female")).pack(pady=6)
        tk.Button(self, text="Continue", bg="#CAF0F8", command=lambda: controller.show_frame("WeightScreen")).pack(pady=12)

    def set_gender(self, g):
        self.controller.set_state("gender", g)

class WeightScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="What is your weight?", font=("Helvetica", 18, "bold"), bg="white").pack(pady=12)
        tk.Label(self, text="Your ideal daily water intake is tied to your body weight.", bg="white").pack(pady=6)
        self.unit = tk.StringVar(value="kg")
        uf = tk.Frame(self, bg="white"); uf.pack(pady=8)
        tk.Radiobutton(uf, text="kg", variable=self.unit, value="kg", bg="white").pack(side="left", padx=8)
        tk.Radiobutton(uf, text="lbs", variable=self.unit, value="lbs", bg="white").pack(side="left", padx=8)
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.insert(0, "70")
        self.entry.pack(pady=10)
        tk.Button(self, text="Continue", bg="#CAF0F8", command=self.save).pack(pady=8)

    def save(self):
        try:
            w = float(self.entry.get())
        except:
            w = 70.0
        if self.unit.get() == "lbs":
            w = w * 0.453592
        base = AGE_GOALS.get(self.controller.state["age_group"], 2000)
        tweak = int((w - 70) * 10)
        new_goal = max(1000, base + tweak)
        self.controller.set_state("weight", int(w))
        self.controller.set_state("unit", self.unit.get())
        self.controller.set_state("goal", new_goal)
        self.controller.show_frame("GoalScreen")

class GoalScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Your Daily Goal", font=("Helvetica", 18, "bold"), bg="white").pack(pady=12)
        tk.Label(self, text="You can tap value and setup your own manual daily goal", bg="white").pack(pady=6)
        self.var = tk.IntVar(value=self.controller.state.get("goal", 2000))
        tk.Label(self, textvariable=seslf.var, font=("Helvetica", 28, "bold"), bg="white").pack(pady=8)
        bf = tk.Frame(self, bg="white"); bf.pack(pady=6)
        tk.Button(bf, text="-100", command=lambda: self.change(-100)).pack(side="left", padx=6)
        tk.Button(bf, text="+100", command=lambda: self.change(100)).pack(side="left", padx=6)
        tk.Button(self, text="Start Tracking", bg="#CAF0F8", command=self.save).pack(pady=12)

    def change(self, delta):
        v = self.var.get() + delta
        if v < 500:
            v = 500
        self.var.set(v)

    def save(self):
        self.controller.set_state("goal", int(self.var.get()))
        self.controller.show_frame("Dashboard")

class Dashboard(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        top = tk.Frame(self, bg="white"); top.pack(fill="x", pady=6)
        self.date_label = tk.Label(top, text="", bg="white"); self.date_label.pack(side="left", padx=6)
        tk.Button(top, text="Settings", command=lambda: controller.show_frame("SettingsScreen")).pack(side="right", padx=6)
        main = tk.Frame(self, bg="white"); main.pack(pady=6)
        left = tk.Frame(main, bg="white"); left.pack(side="left", padx=6)
        right = tk.Frame(main, bg="white"); right.pack(side="left", padx=6)
        # avatar uses male/female PNGs if available
        self.avatar = HumanAvatar(left, width=200, height=320, gender=self.controller.state["gender"])
        # mascot (static)
        self.mascot = MascotManager(right, size=(160,160))
        self.msg_label = tk.Label(self, text="Let's stay hydrated! Small sips add up", bg="white", font=("Helvetica", 11))
        self.msg_label.pack(pady=6)
        pf = tk.Frame(self, bg="white"); pf.pack(pady=6)
        self.pvar = tk.IntVar(value=0)
        self.pbar = ttk.Progressbar(pf, orient="horizontal", length=360, mode="determinate", maximum=100, variable=self.pvar)
        self.pbar.pack()
        self.stats = tk.Label(self, text="", bg="white")
        self.stats.pack(pady=4)
        qf = tk.Frame(self, bg="white"); qf.pack(pady=6)
        for amt in QUICK_AMOUNTS:
            tk.Button(qf, text=f"+{amt} ml", width=8, command=lambda a=amt: self.quick(a)).pack(side="left", padx=4)
        tk.Button(self, text="+250 ml (Quick)", bg="#CAF0F8", width=24, command=lambda: self.quick(DEFAULT_QUICK)).pack(pady=8)
        mf = tk.Frame(self, bg="white"); mf.pack(pady=6)
        tk.Label(mf, text="Add custom amount (ml):", bg="white").pack(side="left")
        self.manual = tk.Entry(mf, width=8); self.manual.pack(side="left", padx=6)
        tk.Button(mf, text="Add", command=self.add_manual).pack(side="left")
        self.remaining_label = tk.Label(self, text="", bg="white")
        self.remaining_label.pack(pady=6)
        tk.Button(self, text="Reset / New Day (Save)", command=self.reset_confirm).pack(pady=6)
        tk.Button(self, text="Weekly Summary", command=lambda: controller.show_frame("WeeklyScreen")).pack()
        self.history_box = tk.Text(self, height=6, width=48)
        self.history_box.pack(pady=6)
        self.update_display()

    def on_show(self):
        self.avatar.set_gender(self.controller.state.get("gender","Male"))
        self.update_display()

    def update_display(self):
        self.date_label.config(text=datetime.now().strftime("%A, %d %b %Y"))
        total = self.controller.state["total"]
        goal = self.controller.state["goal"]
        remaining = max(goal - total, 0)
        pct = int((total / goal) * 100) if goal > 0 else 0
        pct = max(0, min(100, pct))
        self.pvar.set(pct)
        self.stats.config(text=f"Total: {total} ml   •   {pct}%")
        self.remaining_label.config(text=f"Remaining: {remaining} ml")
        # mascot swap (static)
        if pct >= 100:
            # celebrate static
            self.mascot.set_mood("celebrate")
            msg = "You did it! Goal completed! 🎉"
        elif pct >= 75:
            self.mascot.set_mood("cheer")
            msg = "Amazing! Just a little more to reach your goal!"
        elif pct >= 50:
            self.mascot.set_mood("smile")
            msg = "Great job! You're halfway there!"
        else:
            self.mascot.set_mood("neutral")
            msg = "Let's stay hydrated! Small sips add up"
        self.msg_label.config(text=msg)
        # history text
        self.history_box.delete("1.0", tk.END)
        for t, amt in reversed(self.controller.state["history"][-8:]):
            self.history_box.insert(tk.END, f"{t} — {amt} ml\n")

    def quick(self, amt):
        self.controller.log_amount(amt)
        self.update_display()

    def add_manual(self):
        try:
            v = int(float(self.manual.get()))
            if v > 0:
                self.controller.log_amount(v)
                self.manual.delete(0, tk.END)
                self.update_display()
            else:
                messagebox.showwarning("Value", "Enter an amount > 0")
        except:
            messagebox.showwarning("Invalid", "Enter a valid number")

    def reset_confirm(self):
        if messagebox.askyesno("Reset Day", "Save today's total to weekly history and reset the day?"):
            save_today(self.controller.state["total"])
            self.controller.reset_day()
            self.update_display()

class MascotScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Mascot", font=("Helvetica", 16, "bold"), bg="white").pack(pady=8)
        holder = tk.Frame(self, bg="white"); holder.pack()
        self.mascot = MascotManager(holder, size=(220,220))
        controls = tk.Frame(self, bg="white"); controls.pack(pady=6)
        tk.Button(controls, text="Neutral", command=lambda: self.mascot.set_mood("neutral")).pack(side="left", padx=4)
        tk.Button(controls, text="Smile", command=lambda: self.mascot.set_mood("smile")).pack(side="left", padx=4)
        tk.Button(controls, text="Cheer", command=lambda: self.mascot.set_mood("cheer")).pack(side="left", padx=4)
        tk.Button(controls, text="Celebrate", command=lambda: self.mascot.set_mood("celebrate")).pack(side="left", padx=4)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("Dashboard")).pack(pady=8)

class SettingsScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Settings", font=("Helvetica", 18, "bold"), bg="white").pack(pady=8)
        prof = tk.Frame(self, bg="#e6f7ff", padx=8, pady=8); prof.pack(pady=6, fill="x")
        tk.Label(prof, text=self.controller.state.get("name", "User"), font=("Helvetica", 14, "bold"), bg="#e6f7ff").pack()
        tk.Label(prof, text=f"Daily Goal: {self.controller.state.get('goal', 2000)} ml", bg="#e6f7ff").pack()
        tk.Button(self, text="Set Reminder (demo)", command=self.set_reminder).pack(pady=6)
        tk.Button(self, text="Export Screenshot (PNG)", command=self.export_screenshot).pack(pady=6)
        tk.Button(self, text="Reset Weekly Chart", command=self.reset_week_confirm).pack(pady=6)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("Dashboard")).pack(pady=8)

    def set_reminder(self):
        sec = simpledialog.askinteger("Reminder", "Remind me in how many seconds? (demo)", minvalue=5, maxvalue=86400)
        if sec:
            self.after(sec * 1000, lambda: messagebox.showinfo("Hydration Reminder", "Time to take a sip!"))
            messagebox.showinfo("Set", f"Reminder will show in {sec} seconds (demo)")

    def export_screenshot(self):
        if not PIL_AVAILABLE:
            messagebox.showerror("Screenshot", "Pillow required for screenshots. Install Pillow.")
            return
        try:
            x = self.controller.winfo_rootx(); y = self.controller.winfo_rooty()
            w = self.controller.winfo_width(); h = self.controller.winfo_height()
            img = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")], initialfile="waterbuddy_screenshot.png")
            if path:
                img.save(path); messagebox.showinfo("Saved", f"Screenshot saved to {path}")
        except Exception as e:
            messagebox.showerror("Error", f"Screenshot failed: {e}")

    def reset_week_confirm(self):
        if messagebox.askyesno("Reset Week", "Clear weekly data?"):
            reset_week()
            messagebox.showinfo("Reset", "Weekly history cleared.")

class WeeklyScreen(tk.Frame):
    def __init__(self, parent, controller: WaterBuddyApp):
        super().__init__(parent, bg="white")
        self.controller = controller
        tk.Label(self, text="Weekly Summary", font=("Helvetica", 18, "bold"), bg="white").pack(pady=8)
        self.listbox = tk.Listbox(self, width=40, height=12)
        self.listbox.pack(pady=6)
        tk.Button(self, text="Back", command=lambda: controller.show_frame("Dashboard")).pack(pady=8)

    def on_show(self):
        self.update_week()

    def update_week(self):
        self.listbox.delete(0, tk.END)
        rows = load_weekly()
        if not rows:
            self.listbox.insert(tk.END, "No weekly data yet. Save a day to populate this.")
            return
        maxv = max([t for (_, t) in rows])
        for d, t in rows:
            self.listbox.insert(tk.END, f"{d} — {t} ml")
        self.listbox.insert(tk.END, "-" * 30)
        for d, t in rows:
            length = int((t / maxv) * 30) if maxv > 0 else 0
            bar = "█" * length
            self.listbox.insert(tk.END, f"{d[-5:]} |{bar} {t} ml")

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app = WaterBuddyApp()
    app.show_frame("Dashboard")
    app.mainloop()
