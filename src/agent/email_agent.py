
import joblib
from pathlib import Path

from agent.priority_detector import detect_priority
from agent.decision_engine import decide_action
from reply_generator.reply_generator import generate_reply
from memory.database import initialize_database, save_email


# Locate and load the trained ML model
ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT / "models" / "email_classifier.joblib"

model = joblib.load(MODEL_PATH)

vectorizer = model["vectorizer"]
classifier = model["classifier"]
mlb = model["mlb"]
threshold = model["threshold"]


class EmailAgent:

    def __init__(self):
        initialize_database()

    def process_email(self, subject, body):

        # 1. Classify the email using the ML model
        email_text = subject + " " + body
        features = vectorizer.transform([email_text])

        probabilities = classifier.predict_proba(features)[0]

        predicted_labels = [
            mlb.classes_[i]
            for i, probability in enumerate(probabilities)
            if probability >= threshold
        ]

        # 2. Detect email priority
        priority_result = detect_priority(subject, body)
        priority = priority_result["priority"]

        # 3. Decide what action to take
        decision = decide_action(predicted_labels, priority)

        action = decision["action"]
        suggested_reply = ""

        # 4. Generate a reply only when appropriate
        if action == "draft_reply":
            reply_result = generate_reply(predicted_labels)
            suggested_reply = reply_result["reply"]

        # 5. Save email and agent results in SQLite
        email_id = save_email(
            subject,
            body,
            predicted_labels,
            priority,
            action,
            suggested_reply
        )

        # 6. Return the complete result
        return {
            "email_id": email_id,
            "subject": subject,
            "categories": predicted_labels,
            "priority": priority,
            "priority_reason": priority_result["reason"],
            "action": action,
            "action_reason": decision["reason"],
            "suggested_reply": suggested_reply
        }
