import tkinter as tk
from tkinter import ttk
from datetime import datetime
import os
from PIL import Image, ImageTk

ASSETS = "assets"

class WaterBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WaterBuddy")
        self.root.configure(bg="white")
        self.root.geometry("420x780")      # Mobile portrait layout

        # USER VALUES
        self.total_intake = 0
        self.goal = 2700
        self.remaining = self.goal
        self.gender = "male"

        # LOAD ASSETS
        self.load_images()

        # BUILD UI
        self.build_topbar()
        self.build_avatar_area()
        self.build_add_buttons()
        self.build_progress_area()
        self.build_bottom_nav()

        self.update_progress()

    # ----------------------------------------------------
    # LOAD ALL IMAGES
    # ----------------------------------------------------
    def load_images(self):
        def load(name, size=None):
            path = os.path.join(ASSETS, name)
            img = Image.open(path)
            if size:
                img = img.resize(size)
            return ImageTk.PhotoImage(img)

        # avatars
        self.img_male = load("male.png", (220, 360))
        self.img_female = load("female.png", (220, 360))

        # mascots
        self.img_neutral = load("neutral.png", (60, 60))
        self.img_smile = load("smile.png", (60, 60))
        self.img_cheer = load("cheer.png", (60, 60))
        self.img_celebrate = load("celebrate.png", (60, 60))

    # ----------------------------------------------------
    #  TOP BAR
    # ----------------------------------------------------
    def build_topbar(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="x", pady=10, padx=20)

        # DATE BOX
        today = datetime.now().strftime("%d")
        label_day = tk.Label(frame, text=today, bg="#A3D4FF",
                             fg="black", font=("Helvetica", 20, "bold"),
                             width=3, height=1)
        label_day.pack(side="left", anchor="w")

        # MASCOT ICON (top right)
        self.mascot_label = tk.Label(frame, image=self.img_neutral, bg="white")
        self.mascot_label.pack(side="right", anchor="e")

    # ----------------------------------------------------
    #  AVATAR AREA
    # ----------------------------------------------------
    def build_avatar_area(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=10)

        self.avatar_label = tk.Label(frame, image=self.img_male, bg="white")
        self.avatar_label.pack()

    # ----------------------------------------------------
    #  ADD WATER BUTTONS
    # ----------------------------------------------------
    def build_add_buttons(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=15)

        # BIG + BUTTON
        add_btn = tk.Button(frame, text="+", font=("Helvetica", 28, "bold"),
                            bg="#4DA6FF", fg="white", width=3,
                            command=lambda: self.add_intake(250))
        add_btn.pack(pady=10)

        # DRINK AMOUNT BUTTONS
        row = tk.Frame(self.root, bg="white")
        row.pack(pady=5)

        for amount in [250, 350, 500]:
            b = tk.Button(row, text=f"{amount}ml", font=("Helvetica", 12),
                          bg="#EAF4FF", width=8,
                          command=lambda a=amount: self.add_intake(a))
            b.pack(side="left", padx=10)

    # ----------------------------------------------------
    #  PROGRESS BAR AREA
    # ----------------------------------------------------
    def build_progress_area(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(pady=20)

        # TEXT ROW
        text_row = tk.Frame(frame, bg="white")
        text_row.pack(fill="x")

        self.lbl_progress = tk.Label(text_row, text="0ml • 0%", bg="white",
                                     font=("Helvetica", 12))
        self.lbl_progress.pack(side="left", padx=10)

        self.lbl_remaining = tk.Label(text_row,
                                      text=f"Remaining: {self.goal}ml",
                                      bg="white", font=("Helvetica", 12))
        self.lbl_remaining.pack(side="right", padx=10)

        # PROGRESS BAR
        self.pb = ttk.Progressbar(frame, orient="horizontal",
                                  length=350, mode="determinate")
        self.pb.pack(pady=10)

    # ----------------------------------------------------
    #  BOTTOM NAV
    # ----------------------------------------------------
    def build_bottom_nav(self):
        frame = tk.Frame(self.root, bg="white")
        frame.pack(side="bottom", pady=20)

        tk.Button(frame, text="📊", font=("Helvetica", 24), bg="white",
                  bd=0).pack(side="left", padx=40)

        tk.Button(frame, text="💧", font=("Helvetica", 24), bg="white",
                  bd=0).pack(side="left", padx=40)

        tk.Button(frame, text="⚙️", font=("Helvetica", 24), bg="white",
                  bd=0).pack(side="left", padx=40)

    # ----------------------------------------------------
    #  WATER INTAKE LOGIC
    # ----------------------------------------------------
    def add_intake(self, amount):
        self.total_intake += amount
        if self.total_intake > self.goal:
            self.total_intake = self.goal

        self.update_progress()
        self.update_mascot()

    def update_progress(self):
        percent = int((self.total_intake / self.goal) * 100)
        self.pb["value"] = percent

        self.remaining = self.goal - self.total_intake

        self.lbl_progress.configure(text=f"{self.total_intake}ml • {percent}%")
        self.lbl_remaining.configure(text=f"Remaining: {self.remaining}ml")

    # ----------------------------------------------------
    #  MASCOT REACTIONS
    # ----------------------------------------------------
    def update_mascot(self):
        percent = int((self.total_intake / self.goal) * 100)

        if percent == 100:
            self.mascot_label.configure(image=self.img_celebrate)
        elif percent >= 75:
            self.mascot_label.configure(image=self.img_cheer)
        elif percent >= 50:
            self.mascot_label.configure(image=self.img_smile)
        else:
            self.mascot_label.configure(image=self.img_neutral)


# ----------------------------------------------------
# RUN APP
# ----------------------------------------------------
root = tk.Tk()
app = WaterBuddyApp(root)
root.mainloop()
