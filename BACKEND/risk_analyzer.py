def analyze_risk(results):

    risky_keywords = [
        "password", "secret", "credit card",
        "ssn", "confidential", "private"
    ]

    score = 0

    for item in results:
        text = str(item["response"]).lower()

        for word in risky_keywords:
            if word in text:
                score += 1

    if score >= 3:
        return "High Risk"
    elif score >= 1:
        return "Medium Risk"
    else:
        return "Low Risk"