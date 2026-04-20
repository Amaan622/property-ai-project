import spacy
import re
from difflib import get_close_matches

nlp = spacy.load("en_core_web_sm")

KNOWN_LOCATIONS = [
    "whitefield",
    "electronic city",
    "hsr layout",
    "sarjapur road",
    "gollahalli",
    "begur",
    "hegde nagar",
    "channasandra",
    "chikkathoguru",
    "sadhguru layout",
    "sarjapur",
    "kammasandra",
    "marathahalli"
]

def normalize_text(value):
    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def extract_location(text, doc):
    normalized_text = normalize_text(text)

    # 1. direct known-location match
    for location in KNOWN_LOCATIONS:
        if normalize_text(location) in normalized_text:
            return location

    # 2. "in <location>" pattern
    in_match = re.search(r"(?:in|at|near)\s+([a-z\s]+)", normalized_text)
    if in_match:
        candidate = in_match.group(1).strip()
        match = get_close_matches(candidate, KNOWN_LOCATIONS, n=1, cutoff=0.6)
        if match:
            return match[0]
        return candidate

    # 3. NER fallback
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
            candidate = normalize_text(ent.text)
            match = get_close_matches(candidate, KNOWN_LOCATIONS, n=1, cutoff=0.6)
            if match:
                return match[0]
            return candidate

    # 4. whole query fuzzy fallback
    match = get_close_matches(normalized_text, KNOWN_LOCATIONS, n=1, cutoff=0.6)
    if match:
        return match[0]

    return None


def parse_preferences(query):
    text = query.lower()
    doc = nlp(text)

    bhk = None
    max_price = None

    bhk_match = re.search(r"(\d+)\s*bhk", text)
    if bhk_match:
        bhk = int(bhk_match.group(1))

    price_match = re.search(r"(\d+(?:\.\d+)?)\s*(lakh|lakhs|crore|crores)", text)
    if price_match:
        value = float(price_match.group(1))
        unit = price_match.group(2)

        if "crore" in unit:
            max_price = value * 10000000
        else:
            max_price = value * 100000

    location = extract_location(text, doc)

    intent = {
        "luxury": any(w in text for w in ["luxury", "premium", "high end"]),
        "budget_friendly": any(w in text for w in ["cheap", "budget", "affordable"]),
        "near_it_hub": any(w in text for w in ["it park", "it hub", "tech park"]),
        "investment": any(w in text for w in ["investment", "roi", "return"]),
    }

    return {
        "bhk": bhk,
        "max_price": max_price,
        "location": location,
        "intent": intent,
        "raw_query": query
    }
