
import joblib
from pathlib import Path

# Locate and load the trained model
ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "email_classifier.joblib"

print("Loading trained email classifier...")
model = joblib.load(MODEL_PATH)

vectorizer = model["vectorizer"]
classifier = model["classifier"]
mlb = model["mlb"]
threshold = model["threshold"]

# Example email
subject = "Reminder: Project Meeting Tomorrow"
body = """
Dear Team,

This is a reminder that our project meeting
will take place tomorrow at 10 AM.
Please bring your project progress reports.

Regards,
Project Manager
"""

# Combine subject and body
email_text = subject + " " + body

# Convert email into numerical features
email_features = vectorizer.transform([email_text])

# Predict category probabilities
probabilities = classifier.predict_proba(email_features)[0]

# Select categories above the threshold
predicted_labels = [
    mlb.classes_[i]
    for i, probability in enumerate(probabilities)
    if probability >= threshold
]

print("\n========== EMAIL CLASSIFICATION ==========")
print("Subject:", subject)

print("\nPredicted categories:")

if predicted_labels:
    for label in predicted_labels:
        print("-", label)
else:
    print("No category reached the prediction threshold.")

print("\nCategory confidence scores:")

for label, probability in zip(mlb.classes_, probabilities):
    print(f"{label}: {probability:.2%}")
