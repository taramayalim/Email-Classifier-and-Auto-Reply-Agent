
import pandas as pd
import re
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "multi_class_email_dataset.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("Loading original dataset...")
df = pd.read_csv(RAW_PATH)

# Expected email categories
EXPECTED_CATEGORIES = {
    "Business",
    "Customer Support",
    "Events & Invitations",
    "Finance & Bills",
    "Job Application",
    "Newsletters",
    "Personal",
    "Promotions",
    "Reminders",
    "Travel & Bookings"
}

# Clean unnecessary spaces and line breaks
def clean_text(text):
    text = str(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text

# Clean subject and body
df["subject"] = df["subject"].apply(clean_text)
df["body"] = df["body"].apply(clean_text)

# Combine subject and body for classification
df["email_text"] = (
    df["subject"] + " " + df["body"]
).str.strip()

# Convert labels into lists for validation and counting
def process_labels(labels):
    return [
        label.strip()
        for label in str(labels).split(";")
        if label.strip()
    ]

df["label_list"] = df["labels"].apply(process_labels)

# Check for unexpected categories
found_categories = {
    label
    for labels in df["label_list"]
    for label in labels
}

unexpected = found_categories - EXPECTED_CATEGORIES

if unexpected:
    raise ValueError(f"Unexpected categories found: {unexpected}")

# Count how many labels each email has
df["label_count"] = df["label_list"].apply(len)

# Save labels in consistent semicolon-separated format
df["labels"] = df["label_list"].apply(
    lambda labels: "; ".join(labels)
)

# Keep the useful columns
processed_df = df[
    ["subject", "body", "email_text", "labels", "label_count"]
].copy()

# Save processed datasets
csv_output = PROCESSED_DIR / "processed_emails.csv"
excel_output = PROCESSED_DIR / "processed_emails.xlsx"

processed_df.to_csv(
    csv_output,
    index=False,
    encoding="utf-8-sig"
)

processed_df.to_excel(
    excel_output,
    index=False
)

# Display summary
print("\nPREPROCESSING COMPLETED!")
print("Total emails:", len(processed_df))
print("Total categories:", len(found_categories))
print("Average labels per email:", round(
    processed_df["label_count"].mean(), 2
))

print("\nLabel count distribution:")
print(processed_df["label_count"].value_counts().sort_index())

print("\nFirst three processed emails:")
print(
    processed_df[
        ["email_text", "labels", "label_count"]
    ].head(3).to_string(index=False)
)

print("\nSaved files:")
print(csv_output)
print(excel_output)
