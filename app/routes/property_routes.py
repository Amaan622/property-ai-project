from flask import Blueprint, request, jsonify

from app.services.property_fetcher import filter_properties
from app.services.preference_parser import parse_preferences
from app.services.intent_router import is_property_query

property_bp = Blueprint("property", __name__)


@property_bp.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json() or {}


    query = (data.get("query") or "").strip()
    location = data.get("location")
    bhk = data.get("bhk")
    budget = data.get("budget")

  
    intent_type = is_property_query(query)

    # ================= GREETING HANDLING =================
    if intent_type == "greeting":
        return jsonify({
            "message": "👋 Hi! I am your Property AI Assistant 🏡\n\nTry asking:\n• 2 BHK in Whitefield under 1 crore\n• Luxury apartment in Sarjapur\n• Budget flat in Electronic City",
            "results": []
        }), 200

    

  
    if query:
        parsed = parse_preferences(query)

        location = parsed.get("location")
        bhk = parsed.get("bhk")
        max_price = parsed.get("max_price")
        intent = parsed.get("intent", {})

    else:
        max_price = float(budget) if budget else None
        intent = {}

    # ================= FILTER PROPERTIES =================
    results = filter_properties(
        location=location,
        bhk=int(bhk) if bhk else None,
        max_price=max_price,
        intent=intent
    )

    # ================= NO RESULTS =================
    if not results:
        return jsonify({
            "message": "❌ No matching properties found. Try different filters.",
            "results": []
        }), 200

    # ================= BEST MATCH =================
    best = results[0]

    message = (
        f"🏡 Found {len(results)} matching properties\n\n"
        f"⭐ Best Match:\n"
        f"📍 {best.get('location')} | {best.get('bhk')} BHK\n"
        f"💰 ₹{best.get('price')} Lakh\n"
        f"📊 Score: {best.get('score')}\n\n"
        f"🧠 Why this is recommended:\n{best.get('explanation')}\n\n"
        f"📍 Area Insight:\n{best.get('market_insight')}"
    )

    return jsonify({
        "message": message,
        "results": results
    }), 200