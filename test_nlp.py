import spacy

nlp = spacy.load("en_core_web_sm")

text = "I want 2 bhk in whitefield under 80 lakh near IT park"

doc = nlp(text)

print("ENTITIES:")
for ent in doc.ents:
    print(ent.text, "→", ent.label_)