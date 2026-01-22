def calculate_churn_risk(profile):
    score = 0
    reasons = []

    if profile["tenure"] <= 3:
        score += 0.35
        reasons.append("Very low tenure")

    if profile["monthly_charges"] > 80:
        score += 0.30
        reasons.append("High monthly charges")

    if profile["partner"] == "No":
        score += 0.15
        reasons.append("No partner")

    if profile["dependents"] == "No":
        score += 0.10
        reasons.append("No dependents")

    return min(score, 1.0), reasons


def classify_risk(score):
    if score >= 0.7:
        return "HIGH"
    elif score >= 0.4:
        return "MEDIUM"
    return "LOW"
