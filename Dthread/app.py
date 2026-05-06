import streamlit as st
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import hashlib

st.set_page_config(page_title="THE THREAD", page_icon="🧵", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500;700&family=DM+Mono:wght@300;400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
body, .main { background: #0c0c0c; color: #e8e8e8; }

h1,h2,h3 { font-family: 'Bebas Neue', sans-serif; letter-spacing: 2px; }

[data-testid="stSidebar"] {
    background: #080808 !important;
    border-right: 1px solid #ffffff !important;
}

/* THREAD HEADER */
.thread-hero {
    background: #0c0c0c;
    border-bottom: 1px solid #1c1c1c;
    padding: 2rem 0 1.5rem;
    margin-bottom: 2rem;
}

.thread-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    color: #fff;
    letter-spacing: 8px;
    line-height: 1;
}

.thread-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #ffffff;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

.thread-line {
    width: 60px;
    height: 2px;
    background: #e8ff00;
    margin: 1rem 0;
}

/* MODULE HEADERS */
.mod-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #fff;
    letter-spacing: 4px;
    border-left: 4px solid #e8ff00;
    padding-left: 1rem;
    margin-bottom: 1.5rem;
}

.section-tag {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #e8ff00;
    border-bottom: 1px solid #1c1c1c;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* CARDS */
.t-card {
    background: #111;
    border: 1px solid #1c1c1c;
    border-radius: 2px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}

.t-card-accent {
    background: #111;
    border: 1px solid #1c1c1c;
    border-left: 3px solid #e8ff00;
    border-radius: 2px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}

.t-card-red {
    background: #110a0a;
    border: 1px solid #2a1515;
    border-left: 3px solid #ff4444;
    border-radius: 2px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}

.t-card-green {
    background: #0a110a;
    border: 1px solid #152a15;
    border-left: 3px solid #44ff88;
    border-radius: 2px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}

.t-card-blue {
    background: #0a0a11;
    border: 1px solid #15152a;
    border-left: 3px solid #4488ff;
    border-radius: 2px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
}

/* METRIC BLOCKS */
.metric-block {
    background: #111;
    border: 1px solid #1c1c1c;
    padding: 1.5rem 1rem;
    text-align: center;
    border-radius: 2px;
}

.metric-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    color: #e8ff00;
    letter-spacing: 2px;
    line-height: 1;
}

.metric-val.red { color: #ff4444; }
.metric-val.green { color: #44ff88; }
.metric-val.blue { color: #4488ff; }
.metric-val.white { color: #fff; }

.metric-lbl {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #ffffff;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

/* PILL BADGES */
.pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.pill-yellow { background: rgba(232,255,0,0.1); color: #e8ff00; border: 1px solid rgba(232,255,0,0.3); }
.pill-red { background: rgba(255,68,68,0.1); color: #ff4444; border: 1px solid rgba(255,68,68,0.3); }
.pill-green { background: rgba(68,255,136,0.1); color: #44ff88; border: 1px solid rgba(68,255,136,0.3); }
.pill-blue { background: rgba(68,136,255,0.1); color: #4488ff; border: 1px solid rgba(68,136,255,0.3); }

/* PROGRESS BAR */
.t-progress-wrap { background: #1c1c1c; height: 4px; border-radius: 2px; margin: 0.5rem 0; }
.t-progress-fill { height: 4px; border-radius: 2px; background: #e8ff00; }
.t-progress-fill.red { background: #ff4444; }
.t-progress-fill.green { background: #44ff88; }

/* SIDEBAR */
.sidebar-brand {
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid #1c1c1c;
    margin-bottom: 1rem;
}

.sidebar-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #fff;
    letter-spacing: 6px;
}

.sidebar-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.55rem;
    color: #333;
    letter-spacing: 3px;
    text-transform: uppercase;
}

/* INPUTS */
.stTextInput>div>div>input,
.stTextArea>div>div>textarea,
.stNumberInput>div>div>input {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #e8e8e8 !important;
    border-radius: 2px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
}

.stSelectbox>div>div {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 2px !important;
}

/* BUTTONS */
.stButton>button {
    background: #e8ff00 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 2px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1rem !important;
    letter-spacing: 3px !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
}

.stButton>button:hover {
    background: #fff !important;
    transform: translateY(-1px) !important;
}

[data-testid="stMetric"] {
    background: #111 !important;
    border: 1px solid #1c1c1c !important;
    border-radius: 2px !important;
    padding: 1rem !important;
}

.row-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.6rem 0;
    border-bottom: 1px solid #1a1a1a;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
}

.row-label { color: #ffffff; font-family: 'DM Mono', monospace; font-size: 0.7rem; letter-spacing: 1px; }
.row-value { color: #e8e8e8; }
.row-value.yellow { color: #e8ff00; }
.row-value.red { color: #ff4444; }
.row-value.green { color: #44ff88; }

.thought-card {
    background: #0f0f0f;
    border: 1px solid #1c1c1c;
    border-top: 2px solid #e8ff00;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    border-radius: 2px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.85rem;
    color: #ccc;
    line-height: 1.7;
}

.thought-meta {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: #333;
    margin-top: 0.5rem;
    letter-spacing: 1px;
}

.idea-card {
    background: #0a0a11;
    border: 1px solid #15152a;
    padding: 1rem;
    margin-bottom: 0.6rem;
    border-radius: 2px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.82rem;
    color: #aaa;
}

.idea-link {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: #4488ff;
    margin-top: 0.3rem;
}

.footer-thread {
    text-align: center;
    padding: 2rem;
    color: #1c1c1c;
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    border-top: 1px solid #141414;
    margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================
FILES = {
    "health": "thread_health.json",
    "finance": "thread_finance.json",
    "goals": "thread_goals.json",
    "thoughts": "thread_thoughts.json",
    "ideas": "thread_ideas.json",
    "social": "thread_social.json",
    "log": "thread_log.json",
    "decisions": "thread_decisions.json",
    "subs": "thread_subs.json",
    "meals": "thread_meals.json",
    "meds": "thread_meds.json",
}

def load(path, default):
    try:
        if os.path.exists(path):
            with open(path, 'r') as f: return json.load(f)
    except: pass
    return default

def save(path, data):
    with open(path, 'w') as f: json.dump(data, f, indent=2)

now = datetime.now()

health = load(FILES["health"], {"water":0,"caffeine":0,"caffeine_time":None,"sleep_hrs":0,"mood":5,"heart_rate":70,"steps":0,"weight":0,"temp":36.6,"last_break":None,"hydration_goal":8})
finance = load(FILES["finance"], {"salary":0,"assets":[],"debts":[],"subs":[],"transactions":[],"net_worth":0})
goals = load(FILES["goals"], [])
thoughts = load(FILES["thoughts"], [])
ideas = load(FILES["ideas"], [])
social = load(FILES["social"], {"contacts":[],"events":[]})
decisions = load(FILES["decisions"], [])
meals = load(FILES["meals"], [])
meds = load(FILES["meds"], [])

# ============================================================
# GREETING
# ============================================================
hour = now.hour
if hour < 6: time_greet = "YOU'RE UP EARLY"
elif hour < 12: time_greet = "GOOD MORNING"
elif hour < 17: time_greet = "GOOD AFTERNOON"
elif hour < 21: time_greet = "GOOD EVENING"
else: time_greet = "NIGHT MODE"

st.markdown(f"""
<div class="thread-hero">
    <div class="thread-title">THE THREAD</div>
    <div class="thread-subtitle">YOUR LIFE · ONE INTERFACE · ZERO NOISE</div>
    <div class="thread-line"></div>
    <div style='font-family:DM Mono,monospace;font-size:0.7rem;color:#00ff00;letter-spacing:3px;'>
        {time_greet} &nbsp;·&nbsp; {now.strftime("%A, %B %d, %Y").upper()} &nbsp;·&nbsp; {now.strftime("%H:%M")}
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="sidebar-title">🧵 THREAD</div>
        <div class="sidebar-sub">Personal OS v1.0</div>
    </div>
    """, unsafe_allow_html=True)

    module = st.radio("", [
        "⚡ Dashboard",
        "🫀 Health & Body",
        "💊 Medications",
        "🍽️ Nutrition",
        "💰 Finance",
        "📋 Subscriptions",
        "🎯 Goals",
        "🧠 Mind & Thoughts",
        "💡 Ideas Lab",
        "👥 Social",
        "⚖️ Decision Engine",
        "📊 Life Log",
    ], label_visibility="collapsed")

# ============================================================
# DASHBOARD
# ============================================================
if module == "⚡ Dashboard":
    st.markdown('<div class="mod-header">DASHBOARD</div>', unsafe_allow_html=True)

    # Status row
    water_pct = min(health['water'] / health.get('hydration_goal', 8), 1.0)
    mood_color = "green" if health['mood'] >= 7 else ("yellow" if health['mood'] >= 4 else "red")
    mood_label = "OPTIMAL" if health['mood'] >= 7 else ("MODERATE" if health['mood'] >= 4 else "LOW")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.markdown(f'<div class="metric-block"><div class="metric-val">{health["water"]}/{health.get("hydration_goal",8)}</div><div class="metric-lbl">Hydration (glasses)</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-block"><div class="metric-val {mood_color}">{health["mood"]}/10</div><div class="metric-lbl">Mood · {mood_label}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-block"><div class="metric-val white">{health["heart_rate"]}</div><div class="metric-lbl">Heart Rate BPM</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-block"><div class="metric-val blue">{health["steps"]}</div><div class="metric-lbl">Steps Today</div></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="metric-block"><div class="metric-val">{health["sleep_hrs"]}h</div><div class="metric-lbl">Last Sleep</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3,2], gap="large")

    with col_left:
        # Active goals
        st.markdown('<div class="section-tag">Active Goals</div>', unsafe_allow_html=True)
        active_goals = [g for g in goals if g['status'] == 'Active']
        if active_goals:
            for g in active_goals[:4]:
                pct = min(g.get('progress', 0) / 100, 1.0)
                color = "green" if pct >= 0.7 else ("yellow" if pct >= 0.3 else "red")
                st.markdown(f"""
                <div class="t-card-accent">
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='font-family:DM Sans,sans-serif;font-size:0.85rem;color:#e8e8e8;'>{g['name']}</span>
                        <span class='pill pill-yellow'>{int(pct*100)}%</span>
                    </div>
                    <div class="t-progress-wrap" style='margin-top:0.6rem;'>
                        <div class="t-progress-fill {color}" style='width:{int(pct*100)}%;'></div>
                    </div>
                    <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#333;margin-top:0.3rem;'>Target: {g.get("target","—")} · Due: {g.get("due","—")}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="t-card"><span style="color:#333;font-size:0.8rem;">No active goals. Set one in Goals module.</span></div>', unsafe_allow_html=True)

        # Recent thoughts
        st.markdown('<div class="section-tag" style="margin-top:1.5rem;">Recent Thoughts</div>', unsafe_allow_html=True)
        if thoughts:
            for t in reversed(thoughts[-3:]):
                st.markdown(f'<div class="thought-card">{t["text"]}<div class="thought-meta">{t["mood_tag"]} · {t["date"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="t-card"><span style="color:#333;font-size:0.8rem;">No thoughts logged yet.</span></div>', unsafe_allow_html=True)

    with col_right:
        # Alerts
        st.markdown('<div class="section-tag">Alerts & Nudges</div>', unsafe_allow_html=True)
        alerts = []

        # Hydration alert
        if health['water'] < health.get('hydration_goal', 8) * 0.5:
            alerts.append(("💧", "HYDRATION LOW", f"You've had {health['water']} glasses. Drink more.", "red"))

        # Vision break alert
        if health.get('last_break'):
            try:
                last = datetime.strptime(health['last_break'], "%Y-%m-%d %H:%M")
                mins_since = (now - last).seconds // 60
                if mins_since >= 20:
                    alerts.append(("👁️", "20-20-20 RULE", f"{mins_since} mins since last break. Look 20ft away for 20 sec.", "yellow"))
            except: pass

        # Caffeine alert
        if health.get('caffeine_time') and health['caffeine'] > 0:
            try:
                caf_time = datetime.strptime(health['caffeine_time'], "%Y-%m-%d %H:%M")
                hrs_since = (now - caf_time).seconds // 3600
                hrs_left = max(0, 6 - hrs_since)
                if hrs_left > 0:
                    alerts.append(("☕", "CAFFEINE ACTIVE", f"~{hrs_left}h until metabolized. Avoid more caffeine.", "yellow"))
            except: pass

        # Mood alert
        if health['mood'] <= 3:
            alerts.append(("🧠", "LOW MOOD DETECTED", "Consider a short walk, hydration, or rest.", "red"))

        # Sleep alert
        if health['sleep_hrs'] < 6:
            alerts.append(("😴", "SLEEP DEBT", f"Only {health['sleep_hrs']}h logged. Prioritize rest tonight.", "red"))

        # Medication reminders
        for med in meds:
            alerts.append(("💊", f"MEDICATION: {med['name'].upper()}", f"Dose: {med['dose']} · {med['frequency']}", "blue"))

        if alerts:
            for icon, title, msg, color in alerts[:6]:
                card_class = f"t-card-{'red' if color=='red' else ('green' if color=='green' else ('blue' if color=='blue' else 'accent'))}"
                st.markdown(f"""
                <div class="{card_class}">
                    <div style='font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px;color:#e8e8e8;'>{icon} {title}</div>
                    <div style='font-family:DM Sans,sans-serif;font-size:0.78rem;color:#888;margin-top:0.3rem;'>{msg}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="t-card-green"><div style="font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px;color:#44ff88;">✅ ALL CLEAR</div><div style="font-family:DM Sans,sans-serif;font-size:0.78rem;color:#888;margin-top:0.3rem;">No alerts. You\'re on track.</div></div>', unsafe_allow_html=True)

        # Finance snapshot
        st.markdown('<div class="section-tag" style="margin-top:1.5rem;">Finance Snapshot</div>', unsafe_allow_html=True)
        total_assets = sum(a.get('value',0) for a in finance.get('assets',[]))
        total_debts = sum(d.get('amount',0) for d in finance.get('debts',[]))
        net_worth = total_assets - total_debts
        nw_color = "green" if net_worth >= 0 else "red"
        st.markdown(f"""
        <div class="t-card">
            <div class="row-item"><span class="row-label">Assets</span><span class="row-value green">${total_assets:,.2f}</span></div>
            <div class="row-item"><span class="row-label">Debts</span><span class="row-value red">${total_debts:,.2f}</span></div>
            <div class="row-item"><span class="row-label">Net Worth</span><span class="row-value {nw_color}">${net_worth:,.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# HEALTH & BODY
# ============================================================
elif module == "🫀 Health & Body":
    st.markdown('<div class="mod-header">HEALTH & BODY</div>', unsafe_allow_html=True)

    t1,t2,t3 = st.tabs(["📊 Vitals", "💧 Hydration & Sleep", "☕ Caffeine & Alcohol"])

    with t1:
        st.markdown('<div class="section-tag">Log Vitals</div>', unsafe_allow_html=True)
        col1,col2,col3 = st.columns(3)
        with col1:
            health['heart_rate'] = st.number_input("Heart Rate (BPM)", min_value=40, max_value=200, value=health['heart_rate'])
            health['steps'] = st.number_input("Steps Today", min_value=0, value=health['steps'])
        with col2:
            health['weight'] = st.number_input("Weight (kg)", min_value=0.0, value=float(health['weight']), format="%.1f")
            health['temp'] = st.number_input("Body Temp (°C)", min_value=35.0, max_value=42.0, value=float(health['temp']), format="%.1f")
        with col3:
            health['mood'] = st.slider("Mood (1-10)", 1, 10, health['mood'])
            health['sleep_hrs'] = st.number_input("Last Sleep (hrs)", min_value=0.0, max_value=24.0, value=float(health['sleep_hrs']), format="%.1f")

        if st.button("SAVE VITALS"):
            save(FILES["health"], health)
            st.success("Vitals saved.")
            st.rerun()

        # Illness detection
        st.markdown('<div class="section-tag" style="margin-top:1.5rem;">Early Illness Detection</div>', unsafe_allow_html=True)
        flags = []
        if health['temp'] > 37.5: flags.append(f"🌡️ Elevated temperature: {health['temp']}°C — possible fever")
        if health['heart_rate'] > 100: flags.append(f"💓 Elevated heart rate: {health['heart_rate']} BPM")
        if health['mood'] <= 3: flags.append("🧠 Very low mood — monitor mental state")
        if health['sleep_hrs'] < 5: flags.append(f"😴 Insufficient sleep: {health['sleep_hrs']}h")
        if flags:
            for f in flags:
                st.markdown(f'<div class="t-card-red"><span style="font-family:DM Sans,sans-serif;font-size:0.82rem;">{f}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="t-card-green"><span style="font-family:DM Sans,sans-serif;font-size:0.82rem;color:#44ff88;">✅ Vitals look normal.</span></div>', unsafe_allow_html=True)

        # Vision break
        st.markdown('<div class="section-tag" style="margin-top:1.5rem;">20-20-20 Vision Break</div>', unsafe_allow_html=True)
        if st.button("LOG VISION BREAK NOW"):
            health['last_break'] = now.strftime("%Y-%m-%d %H:%M")
            save(FILES["health"], health)
            st.success("Break logged. Next reminder in 20 minutes.")
            st.rerun()
        if health.get('last_break'):
            st.markdown(f'<div class="t-card"><span style="color:#ffffff;font-size:0.75rem;font-family:DM Mono,monospace;">Last break: {health["last_break"]}</span></div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="section-tag">Hydration Tracker</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        health['hydration_goal'] = col1.number_input("Daily Goal (glasses)", min_value=1, max_value=20, value=health.get('hydration_goal',8))
        health['water'] = col2.number_input("Glasses Today", min_value=0, max_value=30, value=health['water'])
        pct = min(health['water'] / health['hydration_goal'], 1.0)
        color = "green" if pct >= 0.8 else ("yellow" if pct >= 0.5 else "red")
        st.markdown(f"""
        <div class="t-card" style="margin-top:0.5rem;">
            <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem;'>
                <span style='font-family:DM Mono,monospace;font-size:0.7rem;color:#ffffff;'>HYDRATION LEVEL</span>
                <span style='font-family:Bebas Neue,sans-serif;font-size:1.2rem;color:#e8ff00;'>{int(pct*100)}%</span>
            </div>
            <div class="t-progress-wrap"><div class="t-progress-fill {color}" style='width:{int(pct*100)}%;'></div></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("ADD GLASS 💧"):
            health['water'] += 1
            save(FILES["health"], health)
            st.rerun()

        st.markdown('<div class="section-tag" style="margin-top:1.5rem;">Sleep Tracker</div>', unsafe_allow_html=True)
        health['sleep_hrs'] = st.number_input("Hours Slept", min_value=0.0, max_value=24.0, value=float(health['sleep_hrs']), format="%.1f")
        sleep_status = "OPTIMAL" if health['sleep_hrs'] >= 7 else ("ADEQUATE" if health['sleep_hrs'] >= 6 else "INSUFFICIENT")
        sleep_color = "green" if health['sleep_hrs'] >= 7 else ("yellow" if health['sleep_hrs'] >= 6 else "red")
        st.markdown(f'<div class="t-card"><div class="row-item"><span class="row-label">Status</span><span class="pill pill-{sleep_color}">{sleep_status}</span></div><div class="row-item"><span class="row-label">Hours</span><span class="row-value {sleep_color}">{health["sleep_hrs"]}h</span></div></div>', unsafe_allow_html=True)
        if st.button("SAVE SLEEP & HYDRATION"):
            save(FILES["health"], health)
            st.success("Saved.")
            st.rerun()

    with t3:
        st.markdown('<div class="section-tag">Caffeine Countdown</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        health['caffeine'] = col1.number_input("Caffeine Units Today", min_value=0, value=health['caffeine'])
        if col2.button("LOG CAFFEINE NOW"):
            health['caffeine_time'] = now.strftime("%Y-%m-%d %H:%M")
            save(FILES["health"], health)
            st.rerun()
        if health.get('caffeine_time') and health['caffeine'] > 0:
            try:
                caf_time = datetime.strptime(health['caffeine_time'], "%Y-%m-%d %H:%M")
                hrs_since = (now - caf_time).seconds // 3600
                hrs_left = max(0, 6 - hrs_since)
                pct_left = hrs_left / 6
                st.markdown(f"""
                <div class="t-card-accent">
                    <div style='font-family:Bebas Neue,sans-serif;font-size:1.5rem;color:#e8ff00;'>~{hrs_left}h REMAINING</div>
                    <div style='font-family:DM Sans,sans-serif;font-size:0.78rem;color:#ffffff;margin-top:0.3rem;'>Last caffeine: {health["caffeine_time"]} · {health["caffeine"]} unit(s)</div>
                    <div class="t-progress-wrap" style='margin-top:0.5rem;'><div class="t-progress-fill red" style='width:{int(pct_left*100)}%;'></div></div>
                </div>
                """, unsafe_allow_html=True)
            except: pass

# ============================================================
# MEDICATIONS
# ============================================================
elif module == "💊 Medications":
    st.markdown('<div class="mod-header">MEDICATIONS</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Add Medication</div>', unsafe_allow_html=True)
    with st.form("add_med", clear_on_submit=True):
        col1,col2,col3 = st.columns(3)
        med_name = col1.text_input("Medication Name")
        med_dose = col2.text_input("Dose (e.g. 500mg)")
        med_freq = col3.selectbox("Frequency", ["Once daily","Twice daily","Three times daily","As needed","Weekly"])
        med_notes = st.text_input("Notes / Warnings")
        if st.form_submit_button("ADD MEDICATION"):
            if med_name:
                meds.append({"name":med_name,"dose":med_dose,"frequency":med_freq,"notes":med_notes,"added":now.strftime("%Y-%m-%d")})
                save(FILES["meds"], meds)
                st.rerun()

    st.markdown("---")
    st.markdown('<div class="section-tag">Active Medications</div>', unsafe_allow_html=True)
    if meds:
        for i,med in enumerate(meds):
            col1,col2 = st.columns([5,1])
            col1.markdown(f"""
            <div class="t-card-blue">
                <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:2px;color:#4488ff;'>💊 {med['name'].upper()}</div>
                <div class="row-item"><span class="row-label">Dose</span><span class="row-value">{med['dose']}</span></div>
                <div class="row-item"><span class="row-label">Frequency</span><span class="row-value">{med['frequency']}</span></div>
                {f'<div class="row-item"><span class="row-label">Notes</span><span class="row-value" style="color:#ffffff;">{med["notes"]}</span></div>' if med.get('notes') else ''}
            </div>
            """, unsafe_allow_html=True)
            if col2.button("Remove", key=f"rem_med_{i}"):
                meds.pop(i); save(FILES["meds"], meds); st.rerun()
    else:
        st.markdown('<div class="t-card"><span style="color:#333;">No medications logged.</span></div>', unsafe_allow_html=True)

# ============================================================
# NUTRITION
# ============================================================
elif module == "🍽️ Nutrition":
    st.markdown('<div class="mod-header">NUTRITION</div>', unsafe_allow_html=True)
    with st.form("log_meal", clear_on_submit=True):
        col1,col2,col3 = st.columns(3)
        meal_name = col1.text_input("Meal / Food Item")
        meal_cal = col2.number_input("Calories (est.)", min_value=0)
        meal_time = col3.selectbox("Meal Type", ["Breakfast","Lunch","Dinner","Snack"])
        meal_notes = st.text_input("Ingredients / Notes")
        if st.form_submit_button("LOG MEAL"):
            if meal_name:
                meals.append({"name":meal_name,"calories":meal_cal,"type":meal_time,"notes":meal_notes,"date":now.strftime("%Y-%m-%d %H:%M")})
                save(FILES["meals"], meals)
                st.rerun()

    st.markdown("---")
    today_meals = [m for m in meals if m['date'].startswith(now.strftime("%Y-%m-%d"))]
    total_cal = sum(m['calories'] for m in today_meals)

    c1,c2,c3 = st.columns(3)
    c1.markdown(f'<div class="metric-block"><div class="metric-val">{total_cal}</div><div class="metric-lbl">Calories Today</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-block"><div class="metric-val white">{len(today_meals)}</div><div class="metric-lbl">Meals Logged</div></div>', unsafe_allow_html=True)
    remaining = max(0, 2000 - total_cal)
    c3.markdown(f'<div class="metric-block"><div class="metric-val {"green" if remaining>0 else "red"}">{remaining}</div><div class="metric-lbl">Cal Remaining (2000 base)</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Today\'s Meals</div>', unsafe_allow_html=True)
    if today_meals:
        for m in today_meals:
            st.markdown(f'<div class="t-card-accent"><div style="display:flex;justify-content:space-between;"><span style="font-family:DM Sans,sans-serif;color:#e8e8e8;">{m["name"]}</span><span class="pill pill-yellow">{m["calories"]} kcal</span></div><div style="font-family:DM Mono,monospace;font-size:0.65rem;color:#ffffff;margin-top:0.3rem;">{m["type"]} · {m["date"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="t-card"><span style="color:#333;">No meals logged today.</span></div>', unsafe_allow_html=True)

# ============================================================
# FINANCE
# ============================================================
elif module == "💰 Finance":
    st.markdown('<div class="mod-header">FINANCE</div>', unsafe_allow_html=True)
    fin_tabs = st.tabs(["💼 Assets & Debts","💸 Transactions","⚖️ True Cost Calculator","📉 Burn Rate"])

    with fin_tabs[0]:
        col1,col2 = st.columns(2)
        with col1:
            st.markdown('<div class="section-tag">Add Asset</div>', unsafe_allow_html=True)
            with st.form("add_asset", clear_on_submit=True):
                a_name = st.text_input("Asset Name")
                a_val = st.number_input("Value ($)", min_value=0.0)
                a_type = st.selectbox("Type", ["Cash","Property","Vehicle","Investment","Crypto","Other"])
                if st.form_submit_button("ADD ASSET"):
                    if a_name:
                        finance['assets'].append({"name":a_name,"value":a_val,"type":a_type})
                        save(FILES["finance"], finance); st.rerun()
        with col2:
            st.markdown('<div class="section-tag">Add Debt</div>', unsafe_allow_html=True)
            with st.form("add_debt", clear_on_submit=True):
                d_name = st.text_input("Debt Name")
                d_amt = st.number_input("Amount ($)", min_value=0.0)
                d_rate = st.number_input("Interest Rate (%)", min_value=0.0)
                if st.form_submit_button("ADD DEBT"):
                    if d_name:
                        finance['debts'].append({"name":d_name,"amount":d_amt,"rate":d_rate})
                        save(FILES["finance"], finance); st.rerun()

        total_assets = sum(a.get('value',0) for a in finance['assets'])
        total_debts = sum(d.get('amount',0) for d in finance['debts'])
        net_worth = total_assets - total_debts
        nw_color = "green" if net_worth >= 0 else "red"

        st.markdown("---")
        c1,c2,c3 = st.columns(3)
        c1.markdown(f'<div class="metric-block"><div class="metric-val green">${total_assets:,.0f}</div><div class="metric-lbl">Total Assets</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-block"><div class="metric-val red">${total_debts:,.0f}</div><div class="metric-lbl">Total Debts</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="metric-block"><div class="metric-val {nw_color}">${net_worth:,.0f}</div><div class="metric-lbl">Net Worth</div></div>', unsafe_allow_html=True)

        if finance['assets']:
            st.markdown('<div class="section-tag" style="margin-top:1.5rem;">Assets</div>', unsafe_allow_html=True)
            for a in finance['assets']:
                st.markdown(f'<div class="t-card-green"><div class="row-item"><span class="row-label">{a["name"]}</span><span class="row-value green">${a["value"]:,.2f}</span></div><div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#333;">{a["type"]}</div></div>', unsafe_allow_html=True)

        if finance['debts']:
            st.markdown('<div class="section-tag" style="margin-top:1rem;">Debts</div>', unsafe_allow_html=True)
            for d in finance['debts']:
                monthly_interest = d['amount'] * (d['rate']/100) / 12
                st.markdown(f'<div class="t-card-red"><div class="row-item"><span class="row-label">{d["name"]}</span><span class="row-value red">${d["amount"]:,.2f}</span></div><div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#555;">Interest: {d["rate"]}% · Monthly cost: ${monthly_interest:,.2f}</div></div>', unsafe_allow_html=True)

    with fin_tabs[1]:
        st.markdown('<div class="section-tag">Log Transaction</div>', unsafe_allow_html=True)
        with st.form("add_txn", clear_on_submit=True):
            col1,col2,col3 = st.columns(3)
            t_name = col1.text_input("Description")
            t_amt = col2.number_input("Amount ($)", min_value=0.0)
            t_type = col3.selectbox("Type", ["Expense","Income","Investment","Transfer"])
            t_cat = st.text_input("Category (e.g. Food, Transport, Bills)")
            if st.form_submit_button("LOG TRANSACTION"):
                if t_name:
                    finance['transactions'].insert(0,{"desc":t_name,"amount":t_amt,"type":t_type,"category":t_cat,"date":now.strftime("%Y-%m-%d %H:%M")})
                    save(FILES["finance"], finance); st.rerun()

        if finance['transactions']:
            st.markdown("---")
            total_in = sum(t['amount'] for t in finance['transactions'] if t['type']=='Income')
            total_out = sum(t['amount'] for t in finance['transactions'] if t['type']=='Expense')
            c1,c2 = st.columns(2)
            c1.markdown(f'<div class="metric-block"><div class="metric-val green">${total_in:,.2f}</div><div class="metric-lbl">Total Income</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="metric-block"><div class="metric-val red">${total_out:,.2f}</div><div class="metric-lbl">Total Expenses</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            for t in finance['transactions'][:15]:
                color = "green" if t['type']=='Income' else "red"
                sign = "+" if t['type']=='Income' else "-"
                st.markdown(f'<div class="t-card"><div class="row-item"><span style="font-family:DM Sans,sans-serif;color:#e8e8e8;">{t["desc"]}</span><span class="row-value {color}">{sign}${t["amount"]:,.2f}</span></div><div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#333;">{t["type"]} · {t.get("category","—")} · {t["date"]}</div></div>', unsafe_allow_html=True)

    with fin_tabs[2]:
        st.markdown('<div class="section-tag">True Cost Calculator</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-family:DM Sans,sans-serif;font-size:0.82rem;color:#ffffff;margin-bottom:1rem;">See any purchase in hours of your life, not just dollars.</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        hourly = col1.number_input("Your Hourly Rate ($)", min_value=0.01, value=20.0)
        item_price = col2.number_input("Item Price ($)", min_value=0.0, value=100.0)
        uses = st.number_input("Expected Uses / Times Used", min_value=1, value=10)
        hours_to_earn = item_price / hourly
        cost_per_use = item_price / uses
        st.markdown(f"""
        <div class="t-card-accent" style="margin-top:1rem;">
            <div class="row-item"><span class="row-label">Hours to Earn</span><span class="row-value yellow">{hours_to_earn:.1f} hours of your life</span></div>
            <div class="row-item"><span class="row-label">Cost Per Use</span><span class="row-value">${cost_per_use:.2f}</span></div>
            <div class="row-item"><span class="row-label">Worth It?</span><span class="pill {'pill-green' if cost_per_use < 10 else 'pill-red'}">{'YES — GOOD VALUE' if cost_per_use < 10 else 'RECONSIDER'}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with fin_tabs[3]:
        st.markdown('<div class="section-tag">Monthly Burn Rate</div>', unsafe_allow_html=True)
        monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=float(finance.get('monthly_income',3800)))
        monthly_expense = st.number_input("Monthly Expenses ($)", min_value=0.0, value=float(finance.get('monthly_expense',2500)))
        burn_rate = monthly_expense / monthly_income if monthly_income > 0 else 0
        days_left = now.day
        days_in_month = 30
        daily_burn = monthly_expense / days_in_month
        projected = daily_burn * days_in_month
        color = "green" if burn_rate < 0.7 else ("yellow" if burn_rate < 0.9 else "red")
        st.markdown(f"""
        <div class="t-card">
            <div class="row-item"><span class="row-label">Burn Rate</span><span class="metric-val {color}" style="font-size:1.5rem;">{int(burn_rate*100)}%</span></div>
            <div class="t-progress-wrap"><div class="t-progress-fill {color}" style='width:{min(int(burn_rate*100),100)}%;'></div></div>
            <div class="row-item" style="margin-top:0.5rem;"><span class="row-label">Daily Spend Rate</span><span class="row-value">${daily_burn:.2f}/day</span></div>
            <div class="row-item"><span class="row-label">Monthly Surplus</span><span class="row-value {'green' if monthly_income>monthly_expense else 'red'}">${monthly_income-monthly_expense:,.2f}</span></div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# SUBSCRIPTIONS
# ============================================================
elif module == "📋 Subscriptions":
    st.markdown('<div class="mod-header">SUBSCRIPTIONS</div>', unsafe_allow_html=True)
    with st.form("add_sub", clear_on_submit=True):
        col1,col2,col3,col4 = st.columns(4)
        s_name = col1.text_input("Service Name")
        s_cost = col2.number_input("Monthly Cost ($)", min_value=0.0)
        s_last_use = col3.text_input("Last Used (YYYY-MM-DD)")
        s_category = col4.selectbox("Category", ["Entertainment","Productivity","Health","Finance","News","Other"])
        if st.form_submit_button("ADD SUBSCRIPTION"):
            if s_name:
                finance['subs'].append({"name":s_name,"cost":s_cost,"last_use":s_last_use,"category":s_category,"added":now.strftime("%Y-%m-%d")})
                save(FILES["finance"], finance); st.rerun()

    st.markdown("---")
    if finance['subs']:
        total_sub = sum(s['cost'] for s in finance['subs'])
        annual = total_sub * 12
        c1,c2 = st.columns(2)
        c1.markdown(f'<div class="metric-block"><div class="metric-val red">${total_sub:,.2f}</div><div class="metric-lbl">Monthly Subscriptions</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="metric-block"><div class="metric-val red">${annual:,.2f}</div><div class="metric-lbl">Annual Cost</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        unused = []
        for i,s in enumerate(finance['subs']):
            days_unused = 999
            if s.get('last_use'):
                try:
                    last = datetime.strptime(s['last_use'], "%Y-%m-%d")
                    days_unused = (now - last).days
                except: pass
            flag = days_unused > 30
            card = "t-card-red" if flag else "t-card-accent"
            if flag: unused.append(s)
            col1,col2 = st.columns([5,1])
            col1.markdown(f"""
            <div class="{card}">
                <div style='display:flex;justify-content:space-between;'>
                    <span style='font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px;color:#e8e8e8;'>{s['name'].upper()}</span>
                    <span class='pill pill-{"red" if flag else "yellow"}'>${s['cost']:.2f}/mo</span>
                </div>
                <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#ffffff;margin-top:0.3rem;'>
                    {s['category']} · Last used: {s.get('last_use','unknown')} {'· ⚠️ CONSIDER CANCELLING' if flag else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if col2.button("Remove", key=f"rem_sub_{i}"):
                finance['subs'].pop(i); save(FILES["finance"], finance); st.rerun()

        if unused:
            st.markdown(f'<div class="t-card-red"><div style="font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px;color:#ff4444;">⚠️ {len(unused)} UNUSED SUBSCRIPTION(S) DETECTED</div><div style="font-family:DM Sans,sans-serif;font-size:0.78rem;color:#888;margin-top:0.3rem;">These services haven\'t been used in 30+ days. Consider cancelling to save ${sum(s["cost"] for s in unused):.2f}/month.</div></div>', unsafe_allow_html=True)

# ============================================================
# GOALS
# ============================================================
elif module == "🎯 Goals":
    st.markdown('<div class="mod-header">GOALS</div>', unsafe_allow_html=True)
    with st.form("add_goal", clear_on_submit=True):
        col1,col2 = st.columns(2)
        g_name = col1.text_input("Goal Name")
        g_category = col2.selectbox("Category", ["Health","Finance","Career","Learning","Personal","Relationships","Other"])
        col3,col4 = st.columns(2)
        g_target = col3.text_input("Target / Milestone")
        g_due = col4.text_input("Due Date (YYYY-MM-DD)")
        if st.form_submit_button("ADD GOAL"):
            if g_name:
                goals.append({"name":g_name,"category":g_category,"target":g_target,"due":g_due,"progress":0,"status":"Active","created":now.strftime("%Y-%m-%d"),"wins":[]})
                save(FILES["goals"], goals); st.rerun()

    st.markdown("---")
    active = [g for g in goals if g['status']=='Active']
    complete = [g for g in goals if g['status']=='Complete']

    if active:
        st.markdown(f'<div class="section-tag">Active — {len(active)}</div>', unsafe_allow_html=True)
        for i,g in enumerate(goals):
            if g['status'] != 'Active': continue
            pct = g.get('progress',0)
            color = "green" if pct >= 70 else ("yellow" if pct >= 30 else "red")
            col1,col2,col3 = st.columns([4,2,1])
            col1.markdown(f"""
            <div class="t-card-accent">
                <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:2px;'>{g['name'].upper()}</div>
                <div class="t-progress-wrap" style='margin:0.5rem 0;'><div class="t-progress-fill {color}" style='width:{pct}%;'></div></div>
                <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#333;'>{g['category']} · Due: {g.get('due','—')} · {pct}% complete</div>
                {f'<div style="font-family:DM Sans,sans-serif;font-size:0.75rem;color:#ffffff;margin-top:0.3rem;">🏆 {len(g.get("wins",[]))} micro-wins</div>' if g.get('wins') else ''}
            </div>
            """, unsafe_allow_html=True)
            new_progress = col2.slider("Progress %", 0, 100, pct, key=f"prog_{i}")
            if new_progress != pct:
                goals[i]['progress'] = new_progress
                save(FILES["goals"], goals); st.rerun()
            if col3.button("✅ Done", key=f"done_g_{i}"):
                goals[i]['status'] = 'Complete'
                save(FILES["goals"], goals); st.rerun()

            # Micro win
            win_text = st.text_input("Log a micro-win", key=f"win_{i}", placeholder="Small win today...")
            if st.button("LOG WIN 🏆", key=f"log_win_{i}"):
                if win_text:
                    goals[i].setdefault('wins',[]).append({"text":win_text,"date":now.strftime("%Y-%m-%d")})
                    save(FILES["goals"], goals); st.rerun()

    if complete:
        st.markdown(f'<div class="section-tag" style="margin-top:1.5rem;">Completed — {len(complete)}</div>', unsafe_allow_html=True)
        for g in complete:
            st.markdown(f'<div class="t-card-green"><span style="font-family:Bebas Neue,sans-serif;letter-spacing:2px;color:#44ff88;">✅ {g["name"].upper()}</span></div>', unsafe_allow_html=True)

# ============================================================
# MIND & THOUGHTS
# ============================================================
elif module == "🧠 Mind & Thoughts":
    st.markdown('<div class="mod-header">MIND & THOUGHTS</div>', unsafe_allow_html=True)
    t1,t2,t3 = st.tabs(["📔 Thought Log","⚖️ Decision Framework","📈 Sentiment Trend"])

    with t1:
        moods = ["😊 Positive","😐 Neutral","😔 Low","😤 Frustrated","🤩 Energized","😰 Anxious","😌 Calm"]
        with st.form("add_thought", clear_on_submit=True):
            thought_text = st.text_area("What's on your mind?", height=120, placeholder="Write freely. No judgment.")
            mood_tag = st.selectbox("Mood Tag", moods)
            if st.form_submit_button("LOCK THOUGHT"):
                if thought_text:
                    thoughts.append({"text":thought_text,"mood_tag":mood_tag,"date":now.strftime("%Y-%m-%d %H:%M")})
                    save(FILES["thoughts"], thoughts); st.rerun()

        st.markdown("---")
        if thoughts:
            for t in reversed(thoughts[-10:]):
                st.markdown(f'<div class="thought-card">{t["text"]}<div class="thought-meta">{t["mood_tag"]} · {t["date"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="t-card"><span style="color:#333;">No thoughts logged yet.</span></div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="section-tag">Decision Engine</div>', unsafe_allow_html=True)
        with st.form("add_decision", clear_on_submit=True):
            d_title = st.text_input("Decision to Make")
            col1,col2,col3 = st.columns(3)
            d_pros = col1.text_area("Pros", height=100, placeholder="+ Benefits")
            d_cons = col2.text_area("Cons", height=100, placeholder="- Drawbacks")
            d_risk = col3.text_area("Risks", height=100, placeholder="⚠️ Risks")
            d_score = st.slider("Gut Score (1=Don't do it, 10=Do it)", 1, 10, 5)
            if st.form_submit_button("ANALYZE DECISION"):
                if d_title:
                    decisions.append({"title":d_title,"pros":d_pros,"cons":d_cons,"risks":d_risk,"gut":d_score,"date":now.strftime("%Y-%m-%d %H:%M"),"recommendation":"DO IT" if d_score >= 7 else ("CAUTION" if d_score >= 4 else "AVOID")})
                    save(FILES["decisions"], decisions); st.rerun()

        if decisions:
            st.markdown("---")
            for d in reversed(decisions[-5:]):
                rec_color = "green" if d['recommendation']=="DO IT" else ("yellow" if d['recommendation']=="CAUTION" else "red")
                st.markdown(f"""
                <div class="t-card-accent">
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:2px;'>{d['title'].upper()}</span>
                        <span class='pill pill-{rec_color}'>{d['recommendation']}</span>
                    </div>
                    <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.5rem;margin-top:0.8rem;'>
                        <div style='font-family:DM Sans,sans-serif;font-size:0.78rem;color:#44ff88;'>{d['pros']}</div>
                        <div style='font-family:DM Sans,sans-serif;font-size:0.78rem;color:#ff4444;'>{d['cons']}</div>
                        <div style='font-family:DM Sans,sans-serif;font-size:0.78rem;color:#f0c040;'>{d['risks']}</div>
                    </div>
                    <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#333;margin-top:0.5rem;'>Gut: {d['gut']}/10 · {d['date']}</div>
                </div>
                """, unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="section-tag">Sentiment Over Time</div>', unsafe_allow_html=True)
        if thoughts:
            mood_map = {"😊 Positive":8,"😐 Neutral":5,"😔 Low":2,"😤 Frustrated":3,"🤩 Energized":9,"😰 Anxious":3,"😌 Calm":7}
            df = pd.DataFrame([{"date":t['date'][:10],"score":mood_map.get(t['mood_tag'],5)} for t in thoughts])
            df = df.groupby('date')['score'].mean().reset_index()
            if not df.empty:
                st.line_chart(df.set_index('date')['score'])
        else:
            st.info("Log thoughts to see sentiment trends.")

# ============================================================
# IDEAS LAB
# ============================================================
elif module == "💡 Ideas Lab":
    st.markdown('<div class="mod-header">IDEAS LAB</div>', unsafe_allow_html=True)
    with st.form("add_idea", clear_on_submit=True):
        idea_title = st.text_input("Idea Title")
        idea_body = st.text_area("Describe the idea", height=120)
        idea_tags = st.text_input("Tags (comma separated)")
        if st.form_submit_button("CAPTURE IDEA"):
            if idea_title:
                new_idea = {"title":idea_title,"body":idea_body,"tags":idea_tags,"date":now.strftime("%Y-%m-%d %H:%M"),"links":[]}
                # Auto-link to existing ideas by matching tags
                new_tags = [t.strip().lower() for t in idea_tags.split(",") if t.strip()]
                for existing in ideas:
                    ex_tags = [t.strip().lower() for t in existing.get('tags','').split(",") if t.strip()]
                    overlap = set(new_tags) & set(ex_tags)
                    if overlap:
                        new_idea['links'].append(f"Linked to: '{existing['title']}' via [{', '.join(overlap)}]")
                ideas.insert(0, new_idea)
                save(FILES["ideas"], ideas); st.rerun()

    st.markdown("---")
    if ideas:
        st.markdown(f'<div class="section-tag">{len(ideas)} Ideas Captured</div>', unsafe_allow_html=True)
        search = st.text_input("Search ideas...", placeholder="Filter by keyword or tag")
        filtered = [i for i in ideas if not search or search.lower() in i['title'].lower() or search.lower() in i['body'].lower() or search.lower() in i.get('tags','').lower()]
        for idea in filtered:
            st.markdown(f"""
            <div class="idea-card">
                <div style='font-family:Bebas Neue,sans-serif;font-size:1.1rem;letter-spacing:2px;color:#4488ff;'>{idea['title'].upper()}</div>
                <div style='font-family:DM Sans,sans-serif;font-size:0.82rem;color:#888;margin-top:0.4rem;line-height:1.6;'>{idea['body']}</div>
                {f'<div class="idea-link">🔗 {" · ".join(idea["links"])}</div>' if idea.get('links') else ''}
                <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#222;margin-top:0.5rem;'>Tags: {idea.get("tags","—")} · {idea["date"]}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="t-card"><span style="color:#333;">No ideas yet. Capture your first one above.</span></div>', unsafe_allow_html=True)

# ============================================================
# SOCIAL
# ============================================================
elif module == "👥 Social":
    st.markdown('<div class="mod-header">SOCIAL INTELLIGENCE</div>', unsafe_allow_html=True)
    t1,t2 = st.tabs(["👤 Contacts","📅 Events & Reminders"])

    with t1:
        with st.form("add_contact", clear_on_submit=True):
            col1,col2,col3 = st.columns(3)
            c_name = col1.text_input("Name")
            c_relation = col2.selectbox("Relationship", ["Friend","Family","Colleague","Client","Mentor","Other"])
            c_birthday = col3.text_input("Birthday (MM-DD)")
            c_last = st.text_input("Last Contact (YYYY-MM-DD)")
            c_notes = st.text_area("Notes / Interests", height=60)
            if st.form_submit_button("ADD CONTACT"):
                if c_name:
                    social['contacts'].append({"name":c_name,"relation":c_relation,"birthday":c_birthday,"last_contact":c_last,"notes":c_notes,"added":now.strftime("%Y-%m-%d")})
                    save(FILES["social"], social); st.rerun()

        st.markdown("---")
        if social['contacts']:
            # Check who needs contact
            needs_touch = []
            for c in social['contacts']:
                if c.get('last_contact'):
                    try:
                        last = datetime.strptime(c['last_contact'], "%Y-%m-%d")
                        if (now - last).days > 30: needs_touch.append(c)
                    except: pass

            if needs_touch:
                st.markdown(f'<div class="t-card-red"><div style="font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px;color:#ff4444;">📞 {len(needs_touch)} CONTACT(S) NEED ATTENTION</div><div style="font-family:DM Sans,sans-serif;font-size:0.78rem;color:#888;margin-top:0.3rem;">{", ".join(c["name"] for c in needs_touch[:5])}</div></div>', unsafe_allow_html=True)

            for c in social['contacts']:
                birthday_soon = False
                if c.get('birthday'):
                    try:
                        bday = datetime.strptime(f"{now.year}-{c['birthday']}", "%Y-%m-%d")
                        if 0 <= (bday - now).days <= 14: birthday_soon = True
                    except: pass
                card = "t-card-accent" if birthday_soon else "t-card"
                st.markdown(f"""
                <div class="{card}">
                    <div style='display:flex;justify-content:space-between;'>
                        <span style='font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px;'>{c['name'].upper()}</span>
                        <span class='pill pill-blue'>{c['relation']}</span>
                    </div>
                    <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#333;margin-top:0.3rem;'>
                        Last contact: {c.get('last_contact','—')} · Birthday: {c.get('birthday','—')} {' 🎂 SOON!' if birthday_soon else ''}
                    </div>
                    {f'<div style="font-family:DM Sans,sans-serif;font-size:0.75rem;colorffffff;margin-top:0.3rem;">{c["notes"]}</div>' if c.get('notes') else ''}
                </div>
                """, unsafe_allow_html=True)

    with t2:
        with st.form("add_event", clear_on_submit=True):
            col1,col2,col3 = st.columns(3)
            e_name = col1.text_input("Event Name")
            e_date = col2.text_input("Date (YYYY-MM-DD)")
            e_type = col3.selectbox("Type", ["Birthday","Anniversary","Meeting","Deadline","Social","Other"])
            if st.form_submit_button("ADD EVENT"):
                if e_name:
                    social['events'].append({"name":e_name,"date":e_date,"type":e_type})
                    save(FILES["social"], social); st.rerun()

        if social['events']:
            upcoming = sorted(social['events'], key=lambda x: x.get('date','9999'))
            for e in upcoming[:10]:
                st.markdown(f'<div class="t-card-blue"><div class="row-item"><span style="font-family:DM Sans,sans-serif;color:#e8e8e8;">{e["name"]}</span><span class="pill pill-blue">{e["type"]}</span></div><div style="font-family:DM Mono,monospace;font-size:0.6rem;color:#333;">{e["date"]}</div></div>', unsafe_allow_html=True)

# ============================================================
# DECISION ENGINE
# ============================================================
elif module == "⚖️ Decision Engine":
    st.markdown('<div class="mod-header">DECISION ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:DM Sans,sans-serif;font-size:0.85rem;color:#fff;margin-bottom:1.5rem;">Weighted analysis. Risk assessment. Clearer outcomes.</div>', unsafe_allow_html=True)
    
    with st.form("full_decision", clear_on_submit=True):
        d_title = st.text_input("What decision are you making?")
        
        col1, col2 = st.columns(2)
        d_pros = col1.text_area("✅ Pros (one per line)", height=120)
        # NEW: Weighting for Pros
        pro_weight = col1.select_slider("Importance of Pros", options=[1, 2, 3, 4, 5], value=3)
        
        d_cons = col2.text_area("❌ Cons (one per line)", height=120)
        # NEW: Weighting for Cons
        con_weight = col2.select_slider("Weight of Cons", options=[1, 2, 3, 4, 5], value=3)
        
        col3, col4 = st.columns(2)
        d_risks = col3.text_area("⚠️ Potential Risks", height=80)
        # NEW: Risk Impact Level
        risk_impact = col3.selectbox("Risk Severity", ["Minimal", "Manageable", "Significant", "Critical"])
        
        d_values = col4.text_area("💎 Alignment with Values", height=80)
        
        col_gut, col_urg = st.columns(2)
        d_gut = col_gut.slider("Gut feeling (1=No, 10=Absolutely)", 1, 10, 5)
        d_urgency = col_urg.selectbox("Urgency", ["Low — I have weeks", "Medium — I have days", "High — I need to decide now"])
        
        if st.form_submit_button("RUN DEEP ANALYSIS"):
            if d_title:
                pros_list = [p.strip() for p in d_pros.split('\n') if p.strip()]
                cons_list = [c.strip() for c in d_cons.split('\n') if c.strip()]
                
                # --- NEW LOGIC ---
                # Calculate weighted score
                total_pro_score = len(pros_list) * pro_weight
                total_con_score = len(cons_list) * con_weight
                
                # Risk Multiplier (Critical risk penalizes the score heavily)
                risk_map = {"Minimal": 1.0, "Manageable": 0.9, "Significant": 0.7, "Critical": 0.4}
                multiplier = risk_map.get(risk_impact, 1.0)
                
                # Final Score Calculation
                # We add the Gut feeling to the Pro side and divide by Cons (plus a safety 1 to avoid /0)
                final_score = ((total_pro_score + d_gut) / (total_con_score + 1)) * multiplier
                
                # Smarter Recommendation
                if final_score >= 5:
                    rec = "DO IT"
                elif final_score >= 3:
                    rec = "PROCEED WITH CAUTION"
                elif final_score >= 1.5:
                    rec = "THINK MORE"
                else:
                    rec = "AVOID"
                
                decisions.append({
                    "title": d_title,
                    "pros": d_pros,
                    "cons": d_cons,
                    "risks": d_risks,
                    "risk_lvl": risk_impact,
                    "gut": d_gut,
                    "recommendation": rec,
                    "urgency": d_urgency,
                    "date": now.strftime("%Y-%m-%d %H:%M")
                })
                save(FILES["decisions"], decisions)
                st.rerun()

    # --- DISPLAY CARDS ---
    if decisions:
        st.markdown("---")
        for d in reversed(decisions[:5]):
            # Color logic for the new recommendation labels
            rec_color = "green" if d['recommendation'] == "DO IT" else (
                "orange" if d['recommendation'] == "PROCEED WITH CAUTION" else (
                "yellow" if d['recommendation'] == "THINK MORE" else "red")
            )
            
            st.markdown(f"""
            <div class="t-card-accent">
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='font-family:Bebas Neue,sans-serif;font-size:1.2rem;letter-spacing:3px;'>{d['title'].upper()}</span>
                    <span class='pill pill-{rec_color}' style='font-size:0.8rem;padding:4px 14px;'>{d['recommendation']}</span>
                </div>
                <div style='display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-top:1rem;'>
                    <div>
                        <div style='color:#44ff88;font-family:DM Mono,monospace;font-size:0.6rem;letter-spacing:2px;margin-bottom:0.3rem;'>PROS</div>
                        <div style='color:#888;font-family:DM Sans,sans-serif;font-size:0.78rem;'>{d['pros']}</div>
                    </div>
                    <div>
                        <div style='color:#ff4444;font-family:DM Mono,monospace;font-size:0.6rem;letter-spacing:2px;margin-bottom:0.3rem;'>CONS</div>
                        <div style='color:#888;font-family:DM Sans,sans-serif;font-size:0.78rem;'>{d['cons']}</div>
                    </div>
                </div>
                <div style='margin-top:0.8rem; border-top: 1px solid #222; padding-top: 0.5rem;'>
                     <div style='color:#ffaa00;font-family:DM Mono,monospace;font-size:0.6rem;letter-spacing:2px;'>RISK ASSESSMENT</div>
                     <div style='color:#777;font-family:DM Sans,sans-serif;font-size:0.75rem;'>{d.get('risk_lvl', 'N/A')} Risk: {d['risks']}</div>
                </div>
                <div style='font-family:DM Mono,monospace;font-size:0.6rem;color:#444;margin-top:0.8rem;'>
                    Gut: {d['gut']}/10 · {d.get('urgency','—')} · {d['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# LIFE LOG
# ============================================================
elif module == "📊 Life Log":
    st.markdown('<div class="mod-header">LIFE LOG</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:DM Sans,sans-serif;font-size:0.82rem;color:#ffffff;margin-bottom:1.5rem;">Your personal data over time.</div>', unsafe_allow_html=True)

    col1,col2,col3,col4 = st.columns(4)
    col1.markdown(f'<div class="metric-block"><div class="metric-val white">{len(thoughts)}</div><div class="metric-lbl">Thoughts Logged</div></div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="metric-block"><div class="metric-val white">{len(ideas)}</div><div class="metric-lbl">Ideas Captured</div></div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="metric-block"><div class="metric-val white">{len(goals)}</div><div class="metric-lbl">Goals Set</div></div>', unsafe_allow_html=True)
    col4.markdown(f'<div class="metric-block"><div class="metric-val white">{len(decisions)}</div><div class="metric-lbl">Decisions Made</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Export everything
    st.markdown('<div class="section-tag">Export All Data</div>', unsafe_allow_html=True)
    all_data = {
        "exported": now.strftime("%Y-%m-%d %H:%M"),
        "health": health,
        "finance": finance,
        "goals": goals,
        "thoughts": thoughts,
        "ideas": ideas,
        "social": social,
        "decisions": decisions,
        "meals": meals,
        "meds": meds,
    }
    st.download_button(
        "EXPORT LIFE DATA",
        json.dumps(all_data, indent=2),
        f"thread_export_{now.strftime('%Y%m%d')}.json",
        "application/json"
    )

    st.markdown("---")
    st.markdown('<div class="section-tag">Reset Modules</div>', unsafe_allow_html=True)
    col1,col2,col3 = st.columns(3)
    if col1.button("CLEAR THOUGHTS"): save(FILES["thoughts"],[]); st.rerun()
    if col2.button("CLEAR IDEAS"): save(FILES["ideas"],[]); st.rerun()
    if col3.button("CLEAR DECISIONS"): save(FILES["decisions"],[]); st.rerun()

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div class="footer-thread" style="color:#ffffff;">
    THE THREAD &nbsp;·&nbsp; PERSONAL OS v1.0 &nbsp;·&nbsp; BUILT IN 2026 &nbsp;·&nbsp; {now.strftime("%B %Y").upper()}
</div>
""", unsafe_allow_html=True)

