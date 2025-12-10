import streamlit as st
from datetime import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Water Buddy - Hydration Tracker",
    page_icon="💧",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #DBEAFE 0%, #93C5FD 50%, #60A5FA 100%);
    }
    
    .main-header {
        text-align: center;
        color: #1E40AF;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .tagline {
        text-align: center;
        color: #1E3A8A;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .stat-box {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        padding: 2rem;
        border-radius: 1.5rem;
        border: 3px solid #000000;
        color: white;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    .stat-number {
        font-size: 3.5rem;
        font-weight: bold;
        margin: 0;
    }
    .stat-label {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 500;
    }
    .message-box {
        background: white;
        padding: 1.25rem;
        border-radius: 1rem;
        border: 3px solid #000000;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #60A5FA 0%, #3B82F6 100%);
        color: white;
        font-weight: bold;
        border: 3px solid #000000 !important;
        border-radius: 2rem;
        padding: 0.85rem;
        font-size: 1.05rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
        border: 3px solid #000000 !important;
    }
    
    /* Text input styling */
    .stTextInput input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 0.75rem;
        border: 3px solid #000000 !important;
        background: white;
    }
    
    /* Number input styling */
    .stNumberInput input {
        font-size: 1.1rem;
        padding: 0.75rem;
        border-radius: 0.75rem;
        border: 3px solid #000000 !important;
        background: white;
    }
    
    /* Radio button styling */
    .stRadio > div {
        border: 3px solid #000000;
        border-radius: 1rem;
        padding: 0.5rem;
        background: white;
    }
    
    /* Content boxes */
    .content-box {
        background: white;
        border: 3px solid #000000;
        border-radius: 1.5rem;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'screen' not in st.session_state:
    st.session_state.screen = 'welcome'
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'age_group' not in st.session_state:
    st.session_state.age_group = ''
if 'gender' not in st.session_state:
    st.session_state.gender = ''
if 'weight' not in st.session_state:
    st.session_state.weight = 70
if 'daily_goal' not in st.session_state:
    st.session_state.daily_goal = 2700
if 'total_intake' not in st.session_state:
    st.session_state.total_intake = 0

# Age group data
AGE_GROUPS = {
    'Kids (4-8 years)': {'goal': 1200, 'range': '~1200 ml', 'emoji': '👶'},
    'Teens (9-13 years)': {'goal': 1700, 'range': '~1700 ml', 'emoji': '🧒'},
    'Adults (14-64 years)': {'goal': 2000, 'range': '~2000 ml', 'emoji': '🧑'},
    'Seniors (65+ years)': {'goal': 1800, 'range': '~1800 ml', 'emoji': '👴'}
}

# Helper functions
def calculate_goal(age_group, weight):
    base_goal = AGE_GROUPS[age_group]['goal']
    adjusted_goal = base_goal + (weight * 10)
    return int(adjusted_goal)

def get_percentage():
    if st.session_state.daily_goal == 0:
        return 0
    return min((st.session_state.total_intake / st.session_state.daily_goal) * 100, 100)

def get_remaining():
    return max(st.session_state.daily_goal - st.session_state.total_intake, 0)

def get_droppy_message(percentage):
    if percentage >= 100:
        return "🎉 Goal Achieved! Amazing job staying hydrated!", "#10B981", "😄"
    elif percentage >= 75:
        return "💪 Keep it up! Almost there!", "#0EA5E9", "😊"
    elif percentage >= 50:
        return "👍 Great progress! Stay hydrated!", "#06B6D4", "🙂"
    else:
        return "💧 Let's stay hydrated! Small sips add up", "#38BDF8", "😐"

def get_droppy_mascot(percentage):
    """Returns ASCII art water droplet mascot with different expressions"""
    if percentage >= 100:
        # Happy/Celebrating
        return """
        <div style='text-align: center; font-family: monospace; color: #3B82F6; font-size: 1rem; line-height: 1.2;'>
            <pre style='display: inline-block; text-align: left;'>
    ⭐ ✨ ⭐
     ╱◕ ◕╲
    │  ▽  │
    │ ╰─╯ │
     ╲   ╱
      ╰─╯
   🎉 💧 🎉
            </pre>
        </div>
        """
    elif percentage >= 75:
        # Motivated/Pumped
        return """
        <div style='text-align: center; font-family: monospace; color: #3B82F6; font-size: 1rem; line-height: 1.2;'>
            <pre style='display: inline-block; text-align: left;'>
      💪    
     ╱◕ ◕╲
    │  ◡  │
    │     │
     ╲   ╱
      ╰─╯
      💧
            </pre>
        </div>
        """
    elif percentage >= 50:
        # Happy/Smiling
        return """
        <div style='text-align: center; font-family: monospace; color: #3B82F6; font-size: 1rem; line-height: 1.2;'>
            <pre style='display: inline-block; text-align: left;'>
     ╱◕ ◕╲
    │  ◡  │
    │     │
     ╲   ╱
      ╰─╯
      💧
            </pre>
        </div>
        """
    else:
        # Neutral/Encouraging
        return """
        <div style='text-align: center; font-family: monospace; color: #3B82F6; font-size: 1rem; line-height: 1.2;'>
            <pre style='display: inline-block; text-align: left;'>
     ╱• •╲
    │  ─  │
    │     │
     ╲   ╱
      ╰─╯
      💧
            </pre>
        </div>
        """

def add_water(amount):
    st.session_state.total_intake += amount

def reset_intake():
    st.session_state.total_intake = 0

# Screen Navigation Functions
def go_to_name():
    st.session_state.screen = 'name'

def go_to_age():
    if st.session_state.name:
        st.session_state.screen = 'age'

def go_to_gender():
    if st.session_state.age_group:
        st.session_state.screen = 'gender'

def go_to_weight():
    if st.session_state.gender:
        st.session_state.screen = 'weight'

def go_to_goal():
    st.session_state.screen = 'goal'
    st.session_state.daily_goal = calculate_goal(
        st.session_state.age_group, 
        st.session_state.weight
    )

def go_to_tracker():
    st.session_state.screen = 'tracker'

def go_to_settings():
    st.session_state.screen = 'welcome'

# WELCOME SCREEN
if st.session_state.screen == 'welcome':
    st.markdown("""
    <div class='content-box' style='text-align: center; margin-top: 3rem;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>💧</div>
        <h1 class='main-header'>Water Buddy</h1>
        <p class='tagline'>Stay fresh through the day<br>let Water Buddy guide your way</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue", key="welcome_btn"):
        go_to_name()

# NAME SCREEN
elif st.session_state.screen == 'name':
    st.markdown("""
    <div class='content-box' style='text-align: center; padding-top: 2rem;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>👤</div>
        <h2 style='color: #000000; font-weight: bold; font-size: 2rem;'>What is your name?</h2>
        <p style='color: #1F2937; font-size: 1.1rem; margin-top: 0.5rem;'>Only used to personalize your experience</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    name_input = st.text_input("", value=st.session_state.name, placeholder="Enter your name", label_visibility="collapsed")
    st.session_state.name = name_input
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue", key="name_btn", disabled=not st.session_state.name):
        go_to_age()

# AGE GROUP SCREEN
elif st.session_state.screen == 'age':
    st.markdown("""
    <div class='content-box' style='text-align: center; padding-top: 2rem;'>
        <h2 style='color: #000000; font-weight: bold; font-size: 2rem;'>Select your age group</h2>
        <p style='color: #1F2937; font-size: 1.1rem;'>Water intake is based on age-specific health standards</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    for group, data in AGE_GROUPS.items():
        button_text = f"{data['emoji']} {group} - {data['range']}"
        if st.button(button_text, key=f"age_{group}", use_container_width=True):
            st.session_state.age_group = group
            go_to_gender()

# GENDER SCREEN
elif st.session_state.screen == 'gender':
    st.markdown("""
    <div class='content-box' style='text-align: center; padding-top: 2rem;'>
        <h2 style='color: #000000; font-weight: bold; font-size: 2rem;'>Choose your gender</h2>
        <p style='color: #1F2937; font-size: 1.1rem;'>We use your body type to tailor your daily water intake</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div style='text-align: center; font-size: 4rem; margin-bottom: 1rem;'>👨</div>", unsafe_allow_html=True)
        if st.button("Male", key="male_btn", use_container_width=True):
            st.session_state.gender = 'Male'
            go_to_weight()
    with col2:
        st.markdown("<div style='text-align: center; font-size: 4rem; margin-bottom: 1rem;'>👩</div>", unsafe_allow_html=True)
        if st.button("Female", key="female_btn", use_container_width=True):
            st.session_state.gender = 'Female'
            go_to_weight()

# WEIGHT SCREEN
elif st.session_state.screen == 'weight':
    st.markdown("""
    <div class='content-box' style='text-align: center; padding: 2rem;'>
        <h2 style='color: #000000; font-weight: bold; font-size: 2rem;'>What is your weight?</h2>
        <p style='color: #1F2937; font-size: 1.1rem; margin-bottom: 2rem;'>Your ideal daily water intake is closely tied to your body weight</p>
    """, unsafe_allow_html=True)
    
    unit = st.radio("Unit", ["kg", "lbs"], horizontal=True, label_visibility="collapsed")
    
    st.markdown("<br>", unsafe_allow_html=True)
    weight = st.number_input(
        "Weight",
        min_value=1,
        max_value=300,
        value=st.session_state.weight,
        step=1,
        label_visibility="collapsed"
    )
    st.session_state.weight = weight
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Continue", key="weight_btn"):
        go_to_goal()

# GOAL SCREEN
elif st.session_state.screen == 'goal':
    st.markdown("""
    <div class='content-box' style='text-align: center; padding: 2rem;'>
        <div style='font-size: 5rem; margin-bottom: 1rem;'>🎯</div>
        <h2 style='color: #000000; font-weight: bold; font-size: 2rem;'>Your Daily Goal</h2>
        <p style='color: #1F2937; font-size: 1.1rem; margin-bottom: 2rem;'>You can adjust your own manual daily goal</p>
    """, unsafe_allow_html=True)
    
    goal = st.number_input(
        "Daily Goal (ml)",
        min_value=500,
        max_value=5000,
        value=st.session_state.daily_goal,
        step=100,
        label_visibility="collapsed"
    )
    st.session_state.daily_goal = goal
    
    st.markdown(f"<p style='text-align: center; font-size: 4rem; font-weight: bold; color: #3B82F6; margin: 1rem 0;'>{goal} ml</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1F2937; font-size: 1.2rem; font-weight: 600;'>per day</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Tracking", key="goal_btn"):
        go_to_tracker()

# TRACKER SCREEN (Main App)
elif st.session_state.screen == 'tracker':
    # Header
    st.markdown("""
    <div class='content-box'>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(f"<h2 style='color: #000000; margin-bottom: 0; font-size: 2rem;'>{st.session_state.name}</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: #1F2937; font-size: 1.1rem; font-weight: 600;'>{datetime.now().strftime('%A')}</p>", unsafe_allow_html=True)
    with col2:
        if st.button("⚙️", key="settings_btn"):
            go_to_settings()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Main Stats
    percentage = get_percentage()
    remaining = get_remaining()
    message, color, emoji = get_droppy_message(percentage)
    mascot = get_droppy_mascot(percentage)
    
    # Progress Display
    st.markdown(f"""
    <div class='stat-box'>
        <div class='stat-number'>{st.session_state.total_intake} ml</div>
        <div class='stat-label'>{percentage:.0f}% of daily goal</div>
        <div class='stat-label'>Remaining: {remaining} ml</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Bar
    st.progress(percentage / 100)
    
    # Droppy Mascot
    st.markdown(mascot, unsafe_allow_html=True)
    
    # Motivational Message
    st.markdown(f"""
    <div class='message-box'>
        <p style='color: #000000; font-size: 1.2rem; font-weight: 700; margin: 0; text-align: center;'>{message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Add Section
    st.markdown("""
    <div class='content-box'>
        <h3 style='color: #000000; font-size: 1.5rem;'>⚡ Quick Add Water</h3>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💧 +250ml", key="add250", use_container_width=True):
            add_water(250)
            st.rerun()
    
    with col2:
        if st.button("💧💧 +500ml", key="add500", use_container_width=True):
            add_water(500)
            st.rerun()
    
    with col3:
        if st.button("💧💧💧 +750ml", key="add750", use_container_width=True):
            add_water(750)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Custom Amount
    st.markdown("""
    <div class='content-box'>
        <h3 style='color: #000000; font-size: 1.5rem;'>✏️ Custom Amount</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        custom_amount = st.number_input("Custom ml", min_value=1, max_value=2000, value=250, step=50, label_visibility="collapsed")
    with col2:
        if st.button("➕ Add", key="add_custom", use_container_width=True):
            add_water(custom_amount)
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Reset Button
    if st.button("🔄 Reset Today's Progress", key="reset_btn", use_container_width=True):
        reset_intake()
        st.rerun()
    
    # Footer Info
    st.markdown(f"""
    <div class='content-box' style='text-align: center;'>
        <p style='font-weight: 700; color: #000000; font-size: 1.2rem; margin-bottom: 0.5rem;'>Daily Goal: {st.session_state.daily_goal} ml</p>
        <p style='color: #1F2937; font-size: 1.1rem;'>{st.session_state.age_group}</p>
    </div>
    """, unsafe_allow_html=True)
