import re

class PropertyAgent:

    def __init__(self):
        # 🏠 Sample property dataset
        self.properties = [
            {"bhk": 2, "location": "Whitefield", "price": 7500000},
            {"bhk": 3, "location": "Whitefield", "price": 8200000},
            {"bhk": 2, "location": "Marathahalli", "price": 6000000},
            {"bhk": 3, "location": "Indiranagar", "price": 9000000},
            {"bhk": 2, "location": "Electronic City", "price": 7000000},
        ]

        # 📊 Market intelligence
        self.market_data = {
            "Whitefield": "High IT demand, strong appreciation",
            "Indiranagar": "Premium locality, high ROI",
            "Marathahalli": "Affordable + good connectivity",
            "Electronic City": "IT hub, growing fast"
        }

    # 💰 Extract budget from query
    def extract_budget(self, query):
        match = re.search(r"(\d+)", query)

        if match:
            value = int(match.group())

            if "lakh" in query.lower():
                return value * 100000
            elif "crore" in query.lower():
                return value * 10000000

        return None

    # 🧠 MAIN AI LOGIC
    def get_recommendations(self, query):

        query_lower = query.lower()
        budget = self.extract_budget(query)

        results = []

        for p in self.properties:
            score = 0
            explanation = []

            # 🏠 BHK match (IMPORTANT)
            if f"{p['bhk']}bhk" in query_lower:
                score += 50
                explanation.append("Matches BHK requirement")

            # 📍 LOCATION smart handling
            if "bangalore" in query_lower:
                score += 20  # general city match

            elif p["location"].lower() in query_lower:
                score += 40
                explanation.append("Matches preferred location")

            # 💰 Budget match
            if budget and p["price"] <= budget:
                score += 30
                explanation.append("Within budget")

            # 🧠 Market insight
            market_info = self.market_data.get(
                p["location"],
                "Stable market conditions"
            )

            # 🧠 Final explanation logic
            if score >= 80:
                final_exp = "Excellent match: " + ", ".join(explanation)
            elif score >= 50:
                final_exp = "Good match: " + ", ".join(explanation)
            elif score > 0:
                final_exp = "Low match: partial alignment with preferences"
            else:
                final_exp = "Not a good match for your preferences"

            results.append({
                "bhk": p["bhk"],
                "location": p["location"],
                "price": p["price"],
                "score": score,
                "explanation": final_exp,
                "market_insight": market_info
            })

        # 🔥 SORT RESULTS (VERY IMPORTANT)
        results.sort(key=lambda x: x["score"], reverse=True)

        return results