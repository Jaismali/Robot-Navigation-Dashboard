import re
import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier

# Training samples: (text, (intent, location))
samples = [
    ("go to lab zero", ("go", "0")),
    ("navigate to lab 1", ("go", "1")),
    ("please go to lab two", ("go", "2")),
    ("go to the third lab", ("go", "3")),
    ("head to lab four", ("go", "4")),
    ("go to lab five", ("go", "5")),
    ("go to lab number six", ("go", "6")),
    ("proceed to lab seven", ("go", "7")),
    ("go to lab eight", ("go", "8")),

    ("deliver to lab zero", ("deliver", "0")),
    ("send package to lab 1", ("deliver", "1")),
    ("can you deliver to lab two", ("deliver", "2")),
    ("drop this at lab 3", ("deliver", "3")),
    ("deliver this to lab four", ("deliver", "4")),
    ("please deliver to lab five", ("deliver", "5")),
    ("send item to lab number six", ("deliver", "6")),
    ("deliver something to lab seven", ("deliver", "7")),
    ("package delivery to lab eight", ("deliver", "8")),
]

# Convert words like "four" to digits
word_to_digit = {
    "zero": "0", "one": "1", "two": "2", "three": "3",
    "four": "4", "for": "4", "five": "5", "six": "6",
    "seven": "7", "eight": "8"
}

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]", "", text)
    for word, digit in word_to_digit.items():
        text = text.replace(f"lab {word}", f"lab {digit}")
        text = text.replace(f"number {word}", f"{digit}")
    return text

X = [normalize(x[0]) for x in samples]
y = [[1 if x[1][0] == "go" else 0, int(x[1][1])] for x in samples]

# Pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultiOutputClassifier(RandomForestClassifier(n_estimators=100)))
])

# Train & save
pipeline.fit(X, y)
joblib.dump(pipeline, "voice_command_classifier.joblib")
print("✅ Trained and saved as voice_command_classifier.joblib")