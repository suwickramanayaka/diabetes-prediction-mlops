# train.py
import os
import hashlib
import urllib.request
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)

# 1. Download dataset & compute SHA-256 hash
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
dataset_bytes = urllib.request.urlopen(url).read()
sha256_hash = hashlib.sha256(dataset_bytes).hexdigest()

df = pd.read_csv(url)

print(f"✅ Dataset downloaded from {url}")
print(f"✅ Dataset SHA-256 Hash: {sha256_hash}")
print(f"✅ Shape: {df.shape}")

# Features and target
feature_names = ["Pregnancies", "Glucose", "BloodPressure", "BMI", "Age"]
X = df[feature_names]
y = df["Outcome"]

# 2. Train/Test Split (80/20, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Train Model with random_state=42
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# 4. Save Model
model_filename = "diabetes_model.pkl"
joblib.dump(model, model_filename)
print(f"✅ Model saved as {model_filename}")

# 5. Evaluate Model on Held-Out Test Set
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]

accuracy = float(accuracy_score(y_test, y_pred))
precision = float(precision_score(y_test, y_pred))
recall = float(recall_score(y_test, y_pred))
f1 = float(f1_score(y_test, y_pred))
roc_auc = float(roc_auc_score(y_test, y_prob))

print(f"📊 Test Accuracy:  {accuracy:.4f}")
print(f"📊 Test Precision: {precision:.4f}")
print(f"📊 Test Recall:    {recall:.4f}")
print(f"📊 Test F1-Score:  {f1:.4f}")
print(f"📊 Test ROC-AUC:   {roc_auc:.4f}")

# Create reports directory
os.makedirs("reports", exist_ok=True)

# Save metrics.csv
metrics_df = pd.DataFrame({
    "metric": ["accuracy", "precision", "recall", "f1_score", "roc_auc"],
    "value": [accuracy, precision, recall, f1, roc_auc]
})
metrics_df.to_csv("reports/metrics.csv", index=False)
print("✅ Saved reports/metrics.csv")

# Save Confusion Matrix Plot
fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, display_labels=["Non-Diabetic", "Diabetic"], cmap=plt.cm.Blues, ax=ax
)
ax.set_title("Confusion Matrix - Diabetes Prediction Baseline")
plt.tight_layout()
plt.savefig("reports/confusion_matrix.png", dpi=300)
plt.close()
print("✅ Saved reports/confusion_matrix.png")

# Save ROC Curve Plot
fig, ax = plt.subplots(figsize=(6, 5))
RocCurveDisplay.from_predictions(
    y_test, y_prob, name=f"Random Forest (AUC = {roc_auc:.4f})", ax=ax
)
ax.plot([0, 1], [0, 1], "k--", label="Random Classifier (AUC = 0.5000)")
ax.set_title("ROC Curve - Diabetes Prediction Baseline")
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.legend(loc="lower right")
plt.tight_layout()
plt.savefig("reports/roc_curve.png", dpi=300)
plt.close()
print("✅ Saved reports/roc_curve.png")

# 6. Verify Saved Model Reloading
reloaded_model = joblib.load(model_filename)
reloaded_preds = reloaded_model.predict(X_test)
assert np.array_equal(y_pred, reloaded_preds), "Reloaded model predictions mismatch!"
print("✅ Reloaded model predictions perfectly match in-memory model predictions.")

# Fixed Sample Prediction
sample_input = pd.DataFrame([{
    "Pregnancies": 2,
    "Glucose": 130.0,
    "BloodPressure": 70.0,
    "BMI": 28.5,
    "Age": 45
}])
sample_prediction = reloaded_model.predict(sample_input)[0]
sample_prob = reloaded_model.predict_proba(sample_input)[0]
print(f"🔮 Fixed Sample Prediction:")
print(f"   Input: {sample_input.to_dict(orient='records')[0]}")
print(f"   Predicted Class: {sample_prediction} ({'Diabetic' if sample_prediction == 1 else 'Non-Diabetic'})")
print(f"   Class Probabilities: Non-Diabetic={sample_prob[0]:.4f}, Diabetic={sample_prob[1]:.4f}")
