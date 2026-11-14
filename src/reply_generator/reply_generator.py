
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

TEMPLATE_PATH = (
    ROOT / "src" / "reply_generator" / "reply_templates.csv"
)


def load_templates():
    """Load reply templates from the CSV file."""

    templates = {}

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            templates[row["category"]] = row["reply_template"]

    return templates


def generate_reply(predicted_labels):
    """Generate a suggested reply using the predicted categories."""

    templates = load_templates()

    # Prefer a specific category when an email has multiple labels
    category_order = [
        "Customer Support",
        "Job Application",
        "Finance & Bills",
        "Travel & Bookings",
        "Events & Invitations",
        "Reminders",
        "Promotions",
        "Newsletters",
        "Personal",
        "Business"
    ]

    selected_category = next(
        (category for category in category_order
         if category in predicted_labels),
        None
    )

    if selected_category is None:
        return {
            "category": None,
            "reply": "No suitable reply template found. Manual review is required."
        }

    return {
        "category": selected_category,
        "reply": templates[selected_category]
    }
