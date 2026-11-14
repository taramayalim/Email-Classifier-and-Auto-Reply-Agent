
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "processed_emails.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

print("Loading processed dataset...")
df = pd.read_csv(DATA_PATH)

# Split into 80% training and 20% testing
train_df, test_df = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    shuffle=True
)

# Reset row indexes
train_df = train_df.reset_index(drop=True)
test_df = test_df.reset_index(drop=True)

# Save training and testing datasets
train_csv = OUTPUT_DIR / "train_emails.csv"
test_csv = OUTPUT_DIR / "test_emails.csv"

train_excel = OUTPUT_DIR / "train_emails.xlsx"
test_excel = OUTPUT_DIR / "test_emails.xlsx"

train_df.to_csv(train_csv, index=False, encoding="utf-8-sig")
test_df.to_csv(test_csv, index=False, encoding="utf-8-sig")

train_df.to_excel(train_excel, index=False)
test_df.to_excel(test_excel, index=False)

# Count individual category occurrences
def get_category_counts(data):
    counts = {}

    for labels in data["labels"].dropna():
        for label in str(labels).split(";"):
            label = label.strip()
            if label:
                counts[label] = counts.get(label, 0) + 1

    return counts

train_counts = get_category_counts(train_df)
test_counts = get_category_counts(test_df)

print("\nDATASET SPLITTING COMPLETED!")

print("\nTraining dataset:")
print("Total emails:", len(train_df))

print("\nTesting dataset:")
print("Total emails:", len(test_df))

print("\nTotal emails:", len(df))

print("\nTraining category distribution:")
for category, count in sorted(train_counts.items()):
    print(f"{category}: {count}")

print("\nTesting category distribution:")
for category, count in sorted(test_counts.items()):
    print(f"{category}: {count}")

print("\nCategories missing from testing data:")
missing = set(train_counts) - set(test_counts)

if missing:
    print(missing)
else:
    print("None")

print("\nSaved files:")
print(train_csv)
print(test_csv)
print(train_excel)
print(test_excel)
