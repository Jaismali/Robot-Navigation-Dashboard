import re
import joblib

# Load model
model = joblib.load("voice_command_classifier.joblib")

# Word to digit conversion
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

def predict_command(text):
    cleaned = normalize(text)
    pred = model.predict([cleaned])[0]  # [intent_go, location]
    intent = "go" if pred[0] == 1 else "deliver"
    location = str(pred[1])
    return intent, location
