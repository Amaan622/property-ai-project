def is_property_query(text):
    if not text:
        return "unknown"

    text = text.lower().strip()

    # greetings
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    if any(g in text for g in greetings):
        return "greeting"

    # property indicators 
    property_keywords = [
        "bhk", "flat", "house", "apartment", "villa",
        "rent", "buy", "sale",
        "crore", "lakh",
        "whitefield", "sarjapur", "electronic city",
        "hsr", "layout", "price", "budget"
    ]

    if any(k in text for k in property_keywords):
        return "property"

    return "unknown"