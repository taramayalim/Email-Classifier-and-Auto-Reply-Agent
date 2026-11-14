
from datasets import load_dataset
import pandas as pd
from pathlib import Path

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Create the dataset output folder
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 50)
print("MULTI-CLASS EMAIL DATASET DOWNLOADER")
print("=" * 50)

# Download the dataset from Hugging Face
print("\nDownloading dataset... Please wait.")

dataset = load_dataset(
    "imnim/multiclass-email-classification",
    split="train"
)

# Convert the downloaded dataset into a Pandas DataFrame
df = dataset.to_pandas()

# Check that the required columns exist
required_columns = ["subject", "body", "labels"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Missing required column: {column}")

# Convert multiple labels into semicolon-separated text
df["labels"] = df["labels"].apply(
    lambda labels: "; ".join(labels)
    if isinstance(labels, (list, tuple))
    else str(labels)
)

# Keep only the columns needed for our project
df = df[["subject", "body", "labels"]]

# Save the CSV file
csv_path = DATA_DIR / "multi_class_email_dataset.csv"

df.to_csv(
    csv_path,
    index=False,
    encoding="utf-8-sig"
)

# Save the Excel file
excel_path = DATA_DIR / "multi_class_email_dataset.xlsx"

df.to_excel(
    excel_path,
    index=False
)

# Display dataset information
print("\nDOWNLOAD AND CONVERSION COMPLETED!")
print("-" * 50)

print("Total emails:", len(df))

print("\nDataset columns:")
print(df.columns.tolist())

print("\nAvailable categories:")

all_categories = set()

for labels in df["labels"]:
    for label in labels.split(";"):
        all_categories.add(label.strip())

for category in sorted(all_categories):
    print("-", category)

print("\nCSV saved at:")
print(csv_path)

print("\nExcel saved at:")
print(excel_path)

print("\nFirst five records:")
print(df.head().to_string(index=False))

print("\n" + "=" * 50)
