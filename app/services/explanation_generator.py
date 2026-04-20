def generate_explanation(prop, preferences, score):
    reasons = []

    if preferences["bhk"] and prop["bhk"] == preferences["bhk"]:
        reasons.append("matches your BHK requirement")

    if preferences["max_price"] and prop["price"] <= preferences["max_price"]:
        reasons.append("fits within your budget")

    if preferences["location"] and preferences["location"].lower() in prop["location"].lower():
        reasons.append("located in your preferred area")

  
    if not reasons:
        return f"This property does not match your preferences well. Score: {score}"

    return f"This property is recommended because it {', '.join(reasons)}. Score: {score}"