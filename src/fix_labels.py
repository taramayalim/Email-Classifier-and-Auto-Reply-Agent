import pandas as pd
import re
from pathlib import Path

# Locate the project data folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"

csv_path = DATA_DIR / "multi_class_email_dataset.csv"
excel_path = DATA_DIR / "multi_class_email_dataset.xlsx"

print("Reading original dataset...")

df = pd.read_csv(csv_path)

# Convert NumPy-style label strings into readable categories
def clean_labels(labels):
    labels = str(labels).strip()

    matches = re.findall(r"'([^']*)'|\"([^\"]*)\"", labels)

    categories = [
        single if single else double
        for single, double in matches
    ]

    return "; ".join(categories)


# Correct the labels
df["labels"] = df["labels"].apply(clean_labels)

# Save the corrected dataset in CSV and Excel formats
df.to_csv(csv_path, index=False, encoding="utf-8-sig")
df.to_excel(excel_path, index=False)

# Extract individual categories
categories = set()

for labels in df["labels"]:
    for category in labels.split(";"):
        if category.strip():
            categories.add(category.strip())

print("\nLABEL CORRECTION COMPLETED!")
print("Total emails:", len(df))

print("\nIndividual categories:")

for category in sorted(categories):
    print("-", category)

print("\nTotal individual categories:", len(categories))

print("\nFirst five corrected labels:")

for labels in df["labels"].head():
    print(labels)

print("\nUpdated files:")
print(csv_path)
print(excel_path)