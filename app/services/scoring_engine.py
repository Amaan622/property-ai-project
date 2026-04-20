def score_properties(properties, preferences):
    results = []

    for prop in properties:
        score = 0

        if preferences["bhk"] and prop["bhk"] == preferences["bhk"]:
            score += 30

        if preferences["max_price"] and prop["price"] <= preferences["max_price"]:
            score += 40

        if preferences["location"] and preferences["location"].lower() in prop["location"].lower():
            score += 30

        results.append((prop, score))

    results.sort(key=lambda x: x["score"], reverse=True)
    return results