import json
import random
import nltk
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

nltk.download('punkt', quiet=True)

# Load intents
with open("intents.json") as f:
    data = json.load(f)

# Prepare training data
sentences = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        sentences.append(pattern)
        labels.append(intent["tag"])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)
y = np.array(labels)

model = MultinomialNB()
model.fit(X, y)

def chatbot_response(text):
    X_test = vectorizer.transform([text])
    tag = model.predict(X_test)[0]
    for intent in data["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I'm not sure I understand that."
