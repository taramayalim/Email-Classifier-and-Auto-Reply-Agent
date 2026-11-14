import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "multi_class_email_dataset.csv"

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# 1. Dataset dimensions
print("\n--- DATASET INFORMATION ---")
print("Total emails:", len(df))
print("Total columns:", len(df.columns))
print("Column names:", list(df.columns))

# 2. Missing values
print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

# 3. Empty text fields
print("\n--- EMPTY FIELDS ---")
for column in ["subject", "body", "labels"]:
    empty_count = df[column].fillna("").astype(str).str.strip().eq("").sum()
    print(f"{column}: {empty_count} empty records")

# 4. Duplicate records
print("\n--- DUPLICATE RECORDS ---")
print("Duplicate rows:", df.duplicated().sum())

# 5. Email length information
print("\n--- EMAIL LENGTH ---")
print("Average body length:", round(df["body"].fillna("").str.len().mean(), 2))
print("Shortest body length:", df["body"].fillna("").str.len().min())
print("Longest body length:", df["body"].fillna("").str.len().max())

# 6. Category distribution
print("\n--- CATEGORY DISTRIBUTION ---")

all_labels = df["labels"].dropna().apply(
    lambda x: [label.strip() for label in str(x).split(";") if label.strip()]
)

category_counts = {}

for labels in all_labels:
    for label in labels:
        category_counts[label] = category_counts.get(label, 0) + 1

for category, count in sorted(category_counts.items()):
    print(f"{category}: {count} emails")

print("\nTotal individual categories:", len(category_counts))
print("\nDATASET QUALITY CHECK COMPLETED!")