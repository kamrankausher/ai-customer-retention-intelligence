import sys
import os
import streamlit as st

# --------------------------------------------------
# FIX PYTHON PATH
# --------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.logic.churn_logic import calculate_churn_risk, classify_risk
from app.genai.llm_engine import generate_retention_message


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI Customer Retention Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------------------------
# GLOBAL STYLES (PREMIUM DARK UI)
# --------------------------------------------------
st.markdown("""
<style>

/* BACKGROUND */
body, .main {
    background: linear-gradient(135deg, #0b0014, #000000);
    color: #f5f5f5;
}

/* HERO TITLE */
@keyframes glow {
    0% { text-shadow: 0 0 10px #d4af37; }
    50% { text-shadow: 0 0 28px #ffd700; }
    100% { text-shadow: 0 0 10px #d4af37; }
}

.hero-title {
    font-size: 54px;
    font-weight: 900;
    color: #ffd700;
    animation: glow 2.8s infinite;
    margin-bottom: 6px;
}

.subtitle {
    color: #e6c76a;
    font-size: 18px;
}

/* GLASS CARD */
.glass {
    background: rgba(60, 0, 90, 0.28);
    backdrop-filter: blur(18px);
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 0 40px rgba(255,215,0,0.15);
    margin-bottom: 26px;
}

/* SECTION DIVIDER */
.divider {
    height: 2px;
    background: linear-gradient(to right, #d4af37, transparent);
    margin: 38px 0;
}

/* BUTTON */
.stButton button {
    background: linear-gradient(135deg, #ffd700, #ff8c00);
    color: black;
    border-radius: 14px;
    font-weight: 700;
    padding: 0.7em 1.8em;
    border: none;
    transition: transform 0.2s ease;
}

.stButton button:hover {
    transform: scale(1.05);
}

/* PROGRESS BAR */
.progress-bar > div > div {
    background: linear-gradient(90deg, #ffd700, #ff8c00);
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<div class="hero-title">🧠 AI Customer Retention Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict • Explain • Retain</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# CUSTOMER PROFILE
# --------------------------------------------------
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("## 👤 Customer Profile")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    gender = st.selectbox("Gender", ["Male", "Female"])
    partner = st.selectbox("Partner", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["Yes", "No"])
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    tenure = st.slider("Tenure (Months)", 0, 72, 1)
    monthly = st.slider("Monthly Charges (₹)", 20, 150, 80)
    st.markdown('</div>', unsafe_allow_html=True)


profile = {
    "gender": gender,
    "partner": partner,
    "dependents": dependents,
    "tenure": tenure,
    "monthly_charges": monthly
}


# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

if st.button("🚀 Run Retention Intelligence"):
    score, reasons = calculate_churn_risk(profile)
    risk = classify_risk(score)
    ai = generate_retention_message(profile, risk, reasons)

    # ---------------- RISK SNAPSHOT ----------------
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown(f"### 🔥 Risk Level: **{risk}**")
    st.progress(score)
    st.markdown(f"**Churn Probability:** `{int(score * 100)}%`")
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- EXPLANATION ----------------
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🧠 Why This Customer May Leave")
    st.write(ai["explanation"])
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- ACTION ----------------
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 🎯 Recommended Business Action")
    st.write(ai["decision"])
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------- MESSAGE ----------------
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown("### 💬 Customer Retention Message")
    st.text_area("", ai["message"], height=160)
    st.markdown('</div>', unsafe_allow_html=True)
