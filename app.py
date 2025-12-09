import streamlit as st
from datetime import datetime, date
import csv
import os
import pandas as pd
import random


# -----------------------------
# CONSTANTS
# -----------------------------
AGE_GOALS = {
    "Children (4–8 yrs)": 1200,
    "Teens (9–13 yrs)": 1700,
    "Adults (14–64 yrs)": 2000,
    "Seniors (65+ yrs)": 1800,
}

TIPS = [
    "Drink a glass of water right after waking up!",
    "Carry a bottle throughout the day.",
    "Add lemon or mint to make water more refreshing.",
    "Warm water boosts digestion.",
    "Small sips throughout the day keep you hydrated."
]

WEEKLY_CSV = "weekly_data.csv"


# -----------------------------
# CSV STORAGE / WEEKLY HISTORY
# -----------------------------
def init_weekly_csv():
    if not os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "total"])   # header


def save_today(total):
    today = str(date.today())
    rows = []

    # read previous data
    if os.path.exists(WEEKLY_CSV):
        with open(WEEKLY_CSV, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)

    # remove old entry if exists
    rows = [r for r in rows if len(r) > 0 and r[0] != today]

    # append today's entry
    rows.append([today, total])

    # write back
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def load_weekly_data():
    if not os.path.exists(WEEKLY_CSV):
        return pd.DataFrame({"date": [], "total": []})

    df = pd.read_csv(WEEKLY_CSV)
    return df.tail(7)   # keep only last 7 days


def reset_week_csv():
    with open(WEEKLY_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "total"])


# -----------------------------
# SESSION INIT
# -----------------------------
def init_state():
    if "total" not in st.session_state:
        st.session_state.total = 0
    if "goal" not in st.session_state:
        st.session_state.goal = AGE_GOALS["Adults (14–64 yrs)"]
    if "age_group" not in st.session_state:
        st.session_state.age_group = "Adults (14–64 yrs)"
    if "history" not in st.session_state:
        st.session_state.history = []
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False


# -----------------------------
# LOG WATER
# -----------------------------
def log(amount):
    st.session_state.total += amount
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.history.append((now, amount))


# -----------------------------
# MASCOT LOGIC
# -----------------------------
def mascot(percent):
    if percent >= 100:
        return "🎉💧🎉", "Goal Achieved! Amazing!"
    elif percent >= 75:
        return "👏💧", "You're almost there!"
    elif percent >= 50:
        return "😊💧", "Great progress!"
    else:
        return "👋💧", "Keep sipping!"


# -----------------------------
# MAIN APP
# -----------------------------
def main():

    st.set_page_config(page_title="WaterBuddy", page_icon="💧")
    init_state()
    init_weekly_csv()

    st.title("💧 WaterBuddy – Hydration Companion")

    st.checkbox("🌙 Dark Mode", key="dark_mode")

    # ----------------------------
    # Profile
    # ----------------------------
    st.subheader("Profile & Goal Settings")
    col1, col2 = st.columns(2)

    with col1:
        st.session_state.age_group = st.selectbox("Select Age Group", list(AGE_GOALS.keys()))

    with col2:
        recommended = AGE_GOALS[st.session_state.age_group]
        st.session_state.goal = st.number_input(
            "Daily Goal (ml)", min_value=500, max_value=6000, value=recommended
        )

    st.write(f"**Standard Target:** {recommended} ml")
    st.write(f"**Your Goal:** {st.session_state.goal} ml")

    # ----------------------------
    # Unit Converter
    # ----------------------------
    st.subheader("Unit Converter (cups ↔ ml)")
    choice = st.radio("Conversion Type:", ["ml → cups", "cups → ml"])
    value = st.number_input("Enter Value:")

    if choice == "ml → cups":
        st.write(f"{value} ml = {value / 250:.2f} cups")
    else:
        st.write(f"{value} cups = {value * 250:.0f} ml")

    # ----------------------------
    # Log Water
    # ----------------------------
    st.subheader("Log Water Intake")
    colA = st.columns(4)
    for i, amt in enumerate([100, 150, 250, 500]):
        if colA[i].button(f"+{amt} ml"):
            log(amt)

    manual = st.number_input("Custom Amount (ml)", min_value=0)
    if st.button("Add"):
        log(manual)

    # ----------------------------
    # Progress
    # ----------------------------
    total = st.session_state.total
    goal = st.session_state.goal
    pct = min(int((total / goal) * 100), 100)

    st.progress(pct)
    st.write(f"**Total:** {total} ml | **Remaining:** {goal - total} ml")

    mascot_face, msg = mascot(pct)
    st.markdown(f"<h1 style='text-align:center'>{mascot_face}</h1>", unsafe_allow_html=True)
    st.write(f"**{msg}**")

    # ----------------------------
    # Reset Day (auto-save)
    # ----------------------------
    if st.button("Reset Day (Save to Weekly Data)"):
        save_today(total)
        st.session_state.total = 0
        st.session_state.history = []
        st.success("Day saved to weekly chart!")
        st.experimental_rerun()

    # ----------------------------
    # Weekly Chart
    # ----------------------------
    st.subheader("📊 Weekly Progress Chart")

    weekly_df = load_weekly_data()

    if len(weekly_df) > 0:
        st.bar_chart(weekly_df.set_index("date"))
    else:
        st.info("No weekly data yet. Log water and press Reset Day to save daily totals!")

    if st.button("Reset Weekly Chart"):
        reset_week_csv()
        st.success("Weekly chart cleared!")
        st.experimental_rerun()

    # ----------------------------
    # Logs
    # ----------------------------
    st.subheader("Today's Logs")
    if st.session_state.history:
        for t, amt in st.session_state.history[::-1]:
            st.write(f"• {t} — {amt} ml")
    else:
        st.write("_No logs yet_")

    # Daily tips
    st.sidebar.header("💡 Daily Tip")
    st.sidebar.info(random.choice(TIPS))


if __name__ == "__main__":
    main()
