# 💧 WaterBuddy – Desktop Hydration Tracker  
A Python + Tkinter desktop application designed for FA-2 (Python Programming).  
WaterBuddy helps users track their daily water intake with a premium UI, animated mascot, custom avatars, charts, and auto-saving progress.

---

## 🚀 Features

### 👤 User Onboarding
- Name input  
- Age selection  
- Gender selection (Male / Female)  
- Weight input  
- Personalized daily water goal calculated automatically  
- Goal can be changed later in **Settings**

---

## 🧍 Custom Avatar System
- Two fully illustrated avatars (male & female, transparent PNG)  
- Avatars resize dynamically for clean desktop layout  
- Centered inside a dedicated avatar panel  
- Hydration message printed on the avatar's shirt  

---

## 💧 Water Tracking
- Quick-add buttons: **250 ml, 350 ml, 500 ml**  
- Manual entry box  
- Daily progress bar (percentage + ml)  
- Remaining water displayed live  
- Auto-save progress for each day  

---

## 🎉 Mascot Reactions
The WaterBuddy mascot reacts based on percentage of goal:

| Progress | Reaction |
|---------|----------|
| 0–49%   | Neutral  |
| 50%     | Smile    |
| 75%     | Cheer    |
| 100%    | Celebration popup + confetti |

The celebration includes:
- Large “celebrate” mascot  
- Animated confetti  
- Motivational message  

---

## 📊 Weekly Progress Chart
- Automatically stores daily hydration totals in **weekly_data.csv**  
- Weekly bar chart (last 7 days)  
- Uses Matplotlib  
- Bars auto-scale based on user’s daily goal  

---

## ⚙️ Settings
- Change daily goal anytime  
- Everything updates instantly  
- Keeps progress saved  

---

## 📁 Project Structure

