
import pandas as pd
import joblib

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# Project paths
ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "processed" / "train_emails.csv"
TEST_PATH = ROOT / "data" / "processed" / "test_emails.csv"
MODEL_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "evaluation" / "results"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
print("Loading datasets...")
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

# Extract email text
X_train_text = train_df["email_text"].fillna("")
X_test_text = test_df["email_text"].fillna("")

# Convert labels into lists
def convert_labels(labels):
    return [x.strip() for x in str(labels).split(";") if x.strip()]

y_train_labels = train_df["labels"].apply(convert_labels)
y_test_labels = test_df["labels"].apply(convert_labels)

# Encode multiple labels
mlb = MultiLabelBinarizer()
y_train = mlb.fit_transform(y_train_labels)
y_test = mlb.transform(y_test_labels)

print("Categories:", list(mlb.classes_))

# Convert text into numerical features
print("\nExtracting TF-IDF features...")

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english",
    ngram_range=(1, 2),
    max_features=20000,
    min_df=2
)

X_train = vectorizer.fit_transform(X_train_text)
X_test = vectorizer.transform(X_test_text)

print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)

# Train multi-label classifier
print("\nTraining model...")

classifier = OneVsRestClassifier(
    LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42
    )
)

classifier.fit(X_train, y_train)

print("Training completed!")

# Predict test emails
probabilities = classifier.predict_proba(X_test)
y_pred = (probabilities >= 0.5).astype(int)

# Evaluate model
print("\nMODEL EVALUATION")

metrics = {
    "Exact-match accuracy": accuracy_score(y_test, y_pred),
    "Micro precision": precision_score(
        y_test, y_pred, average="micro", zero_division=0
    ),
    "Micro recall": recall_score(
        y_test, y_pred, average="micro", zero_division=0
    ),
    "Micro F1": f1_score(
        y_test, y_pred, average="micro", zero_division=0
    ),
    "Macro F1": f1_score(
        y_test, y_pred, average="macro", zero_division=0
    )
}

for name, score in metrics.items():
    print(f"{name}: {score:.4f}")

# Category-level evaluation
report = classification_report(
    y_test,
    y_pred,
    target_names=mlb.classes_,
    zero_division=0
)

print("\nCATEGORY REPORT")
print(report)

# Save metrics
pd.DataFrame(
    list(metrics.items()),
    columns=["Metric", "Score"]
).to_csv(RESULTS_DIR / "model_metrics.csv", index=False)

with open(
    RESULTS_DIR / "classification_report.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write(report)

# Save complete model bundle
model_bundle = {
    "vectorizer": vectorizer,
    "classifier": classifier,
    "mlb": mlb,
    "threshold": 0.5
}

model_path = MODEL_DIR / "email_classifier.joblib"
joblib.dump(model_bundle, model_path)

print("\nMODEL SAVED SUCCESSFULLY!")
print(model_path)
