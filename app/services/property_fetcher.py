import math
import os
import re
from difflib import SequenceMatcher, get_close_matches

import pandas as pd

# ================= LOAD DATA =================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
CSV_PATH = os.path.join(BASE_DIR, "data", "housing.csv")

df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip().str.lower()


# ================= SAFE FLOAT =================
def safe_float(value):
    try:
        if value is None:
            return None
        if isinstance(value, float) and math.isnan(value):
            return None
        return float(value)
    except Exception:
        return None


#CLEAN JSON 
def clean_nan(obj):
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_nan(i) for i in obj]
    if isinstance(obj, float) and math.isnan(obj):
        return None
    return obj


# CLEAN DATA
if "size" in df.columns:
    df["bhk"] = df["size"].astype(str).str.extract(r"(\d+)")[0]
    df["bhk"] = pd.to_numeric(df["bhk"], errors="coerce")

df["location"] = df["location"].astype(str).str.strip().str.lower()
df["price_num"] = pd.to_numeric(df.get("price"), errors="coerce")
df["sqft_num"] = pd.to_numeric(df.get("total_sqft"), errors="coerce")
df["bath_num"] = pd.to_numeric(df.get("bath"), errors="coerce")
df["bhk_num"] = pd.to_numeric(df.get("bhk"), errors="coerce")
df["value_index"] = df["sqft_num"] / df["price_num"].replace(0, pd.NA)


# LOCATION MATCH
def normalize_location_name(value):
    if value is None:
        return None

    value = str(value).strip().lower()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value or None


def get_closest_location(user_location):
    if not user_location:
        return None

    normalized_input = normalize_location_name(user_location)
    if not normalized_input:
        return None

    locations = df["location"].dropna().unique().tolist()
    normalized_map = {}

    for location in locations:
        normalized_location = normalize_location_name(location)
        if normalized_location and normalized_location not in normalized_map:
            normalized_map[normalized_location] = location

    normalized_locations = list(normalized_map.keys())
    match = get_close_matches(normalized_input, normalized_locations, n=1, cutoff=0.6)

    if match:
        return normalized_map[match[0]]

    return None


def similarity_score(a, b):
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


#FILTER 
def apply_filters(dataframe, location, bhk, max_price):
    filtered = dataframe.copy()

    if location:
        normalized_location = normalize_location_name(location)
        filtered = filtered[
            filtered["location"].apply(normalize_location_name) == normalized_location
        ]

    if bhk:
        filtered = filtered[filtered["bhk_num"] == float(bhk)]

    if max_price:
        filtered = filtered[filtered["price_num"] <= float(max_price)]

    return filtered


# TAG SYSTEM 
def get_tag(score):
    if score >= 85:
        return "Highly Recommended"
    if score >= 70:
        return "Recommended"
    if score >= 55:
        return "Good Match"
    return "Consider"


def add_candidate_metrics(filtered_df):
    candidates = filtered_df.copy()

    if candidates.empty:
        return candidates

    candidates["price_rank"] = 1 - candidates["price_num"].rank(pct=True, method="average")
    candidates["sqft_rank"] = candidates["sqft_num"].rank(pct=True, method="average")
    candidates["value_rank"] = candidates["value_index"].rank(pct=True, method="average")

    bath_gap = (candidates["bath_num"] - candidates["bhk_num"]).abs()
    candidates["bath_fit_rank"] = 1 - bath_gap.rank(pct=True, method="average")

    for col in ["price_rank", "sqft_rank", "value_rank", "bath_fit_rank"]:
        candidates[col] = candidates[col].fillna(0.5)

    return candidates


# ================= SCORING ENGINE =================
def score_property(row, location, bhk, max_price, intent):
    score = 0.0
    explanation = []

    row_location = str(row.get("location", "")).strip().lower()
    row_bhk = safe_float(row.get("bhk_num"))
    price = safe_float(row.get("price_num"))
    sqft = safe_float(row.get("sqft_num"))
    bath = safe_float(row.get("bath_num"))

    # LOCATION
    if location:
        if normalize_location_name(row_location) == normalize_location_name(location):
            score += 30
            explanation.append("Exact location match")
        else:
            close_ratio = similarity_score(row_location, location)
            score += round(close_ratio * 12, 2)
            explanation.append("Similar location")

    # BHK
    if bhk is not None and row_bhk is not None:
        diff = abs(row_bhk - float(bhk))
        if diff == 0:
            score += 22
            explanation.append("Exact BHK match")
        elif diff == 1:
            score += 10
            explanation.append("Close BHK match")
        else:
            score += max(0, 6 - (diff * 2))
            explanation.append("Loose BHK match")

    # BUDGET
    if max_price is not None and price is not None and float(max_price) > 0:
        budget_ratio = price / float(max_price)
        if budget_ratio <= 1:
            budget_score = (1 - budget_ratio) * 18 + 7
            score += budget_score
            explanation.append("Within budget")
        else:
            penalty = min((budget_ratio - 1) * 30, 20)
            score -= penalty
            explanation.append("Over budget")

    # RANK-BASED DIFFERENTIATORS
    score += float(row.get("price_rank", 0.5)) * 12
    score += float(row.get("sqft_rank", 0.5)) * 14
    score += float(row.get("value_rank", 0.5)) * 14
    score += float(row.get("bath_fit_rank", 0.5)) * 8

    if float(row.get("price_rank", 0.5)) >= 0.75:
        explanation.append("Better price than most matches")
    if float(row.get("sqft_rank", 0.5)) >= 0.75:
        explanation.append("Larger area than most matches")
    if float(row.get("value_rank", 0.5)) >= 0.75:
        explanation.append("Strong value for money")
    if bath is not None and sqft is not None:
        explanation.append(f"{int(sqft)} sqft with {int(bath)} bath")

    # INTENT BOOST
    if intent:
        if intent.get("luxury") and price is not None and price >= df["price_num"].quantile(0.75):
            score += 4
            explanation.append("Matches luxury preference")

        if intent.get("budget_friendly") and float(row.get("price_rank", 0.5)) >= 0.7:
            score += 4
            explanation.append("Matches budget-friendly preference")

        if intent.get("family_friendly") and bath is not None and row_bhk is not None and bath >= max(2, row_bhk - 1):
            score += 3
            explanation.append("Suitable for family needs")

    score = max(0, min(score, 100))
    return round(score, 2), explanation


# ================= MAIN FUNCTION =================
def filter_properties(location=None, bhk=None, max_price=None, intent=None):
    if location:
        location = get_closest_location(location)

    filtered_df = apply_filters(df, location, bhk, max_price)
    filtered_df = add_candidate_metrics(filtered_df)

    results = []

    for _, row in filtered_df.iterrows():
        score, explanation = score_property(row, location, bhk, max_price, intent)

        if score < 15:
            continue

        item = row.to_dict()
        item["score"] = score
        item["explanation"] = explanation
        item["tag"] = get_tag(score)

        row_location = str(row.get("location", "")).strip().lower()
        if row_location in ["whitefield", "electronic city", "sarjapur road"]:
            item["market_insight"] = "High IT corridor -> strong rental demand"
        else:
            item["market_insight"] = "Stable growth area"

        results.append(item)

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return clean_nan(results[:10])
