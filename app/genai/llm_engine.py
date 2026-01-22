import os
import json
import random
from dotenv import load_dotenv

load_dotenv()

USE_LLM = bool(os.getenv("GROQ_API_KEY"))

# ---------------- FALLBACK AI (NO API) ----------------
def fallback_ai(profile, risk_level, reasons):
    tone_map = {
        "HIGH": [
            "This customer exhibits strong indicators of potential churn.",
            "Multiple high-risk signals suggest urgent intervention is needed.",
            "Customer behavior reflects elevated disengagement risk."
        ],
        "MEDIUM": [
            "Customer shows moderate churn indicators.",
            "Early signs of dissatisfaction are visible.",
            "Retention opportunity exists with timely action."
        ],
        "LOW": [
            "Customer engagement appears stable.",
            "Minimal churn indicators detected.",
            "Customer usage patterns are healthy."
        ]
    }

    action_map = {
        "HIGH": [
            "Initiate proactive outreach with loyalty incentives.",
            "Offer personalized discount and premium support.",
            "Assign customer success manager immediately."
        ],
        "MEDIUM": [
            "Recommend targeted promotions.",
            "Share usage optimization tips.",
            "Monitor customer closely."
        ],
        "LOW": [
            "Continue standard engagement.",
            "No immediate action required.",
            "Maintain existing plan."
        ]
    }

    explanation = f"""
{random.choice(tone_map[risk_level])}

Key churn drivers:
• Tenure: {profile['tenure']} months  
• Monthly Charges: ₹{profile['monthly_charges']}  
• Partner: {profile['partner']}  
• Dependents: {profile['dependents']}
"""

    return {
        "explanation": explanation.strip(),
        "decision": random.choice(action_map[risk_level]),
        "message": (
            "Hello,\n\n"
            "We truly value your association with us and want to ensure "
            "you receive the best possible experience.\n\n"
            "Warm regards,\nCustomer Success Team"
        )
    }


# ---------------- REAL LLM (OPTIONAL) ----------------
def llm_ai(profile, risk_level, reasons):
    from groq import Groq

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""
You are a senior telecom customer retention strategist.

Context:
Risk Level: {risk_level}
Risk Factors: {', '.join(reasons)}

Customer Profile:
{json.dumps(profile, indent=2)}

TASK:
1. Explain why the customer may churn
2. Recommend a retention action
3. Write a customer-facing message

RULES:
- Output valid JSON only
- No markdown
- Sign message as Customer Success Team

FORMAT:
{{
  "explanation": "...",
  "decision": "...",
  "message": "..."
}}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",  # ✅ ACTIVE MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return json.loads(response.choices[0].message.content)


# ---------------- MAIN ENTRY ----------------
def generate_retention_message(profile, risk_level, reasons):
    if USE_LLM:
        try:
            return llm_ai(profile, risk_level, reasons)
        except Exception:
            return fallback_ai(profile, risk_level, reasons)

    return fallback_ai(profile, risk_level, reasons)
