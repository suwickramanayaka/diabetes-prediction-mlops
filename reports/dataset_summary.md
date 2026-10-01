# 🩺 Dataset Summary & Baseline Model Evaluation Report

## 1. Dataset Provenance & Integrity

* **Source URL:** `https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv`
* **SHA-256 Hash:** `698c203a14aa31941d2251175330c9199f3ccdb31597abbba2a3e35416257a72`
* **Dataset Shape:** 768 rows × 9 columns
* **Explicit Missing Values (`isna()`):** 0
* **Duplicate Rows:** 0

### Target Distribution (`Outcome`)
* **Class 0 (Non-Diabetic):** 500 samples (65.10%)
* **Class 1 (Diabetic):** 268 samples (34.90%)
* **Total:** 768 samples

---

## 2. Feature Summary Statistics & Data Quality Checks

The baseline model utilizes 5 features from the dataset: `Pregnancies`, `Glucose`, `BloodPressure`, `BMI`, and `Age`.

| Feature | Data Type | Count | Mean | Std | Min | 25% | 50% | 75% | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Pregnancies** | `int64` | 768 | 3.85 | 3.37 | 0.0 | 1.0 | 3.0 | 6.0 | 17.0 |
| **Glucose** | `int64` | 768 | 120.89 | 31.97 | 0.0 | 99.0 | 117.0 | 140.25 | 199.0 |
| **BloodPressure** | `int64` | 768 | 69.11 | 19.36 | 0.0 | 62.0 | 72.0 | 80.0 | 122.0 |
| **BMI** | `float64` | 768 | 31.99 | 7.88 | 0.0 | 27.3 | 32.0 | 36.6 | 67.1 |
| **Age** | `int64` | 768 | 33.24 | 11.76 | 21.0 | 24.0 | 29.0 | 41.0 | 81.0 |

### Zero Value Analysis

| Feature | Zero Count | Percentage | Plausibility Assessment |
| :--- | :--- | :--- | :--- |
| **Pregnancies** | 111 | 14.45% | **Plausible** (women who have never been pregnant). |
| **Glucose** | 5 | 0.65% | **Implausible** (plasma glucose concentration cannot be 0 in a living individual; indicates missing measurement). |
| **BloodPressure** | 35 | 4.56% | **Implausible** (diastolic blood pressure cannot be 0 mmHg; indicates missing measurement). |
| **BMI** | 11 | 1.43% | **Implausible** (body mass index cannot be 0; indicates missing measurement). |
| **Age** | 0 | 0.00% | **Plausible** (minimum age is 21). |

> **Baseline Decision:** To preserve the baseline specification of the repository, raw feature values were retained without automated imputation for this first evaluation. Data-quality limitations are documented here.

---

## 3. Training & Evaluation Methodology

* **Train / Test Split:** 80% Training ($N=614$), 20% Test ($N=154$) using `random_state=42`.
* **Model Algorithm:** `RandomForestClassifier(random_state=42)`.
* **Positive Class:** `Outcome = 1` (Diabetic).
* **Model Artifact:** Saved to `diabetes_model.pkl` via `joblib.dump()`.

---

## 4. Measured Performance Metrics on Held-Out Test Set ($N=154$)

| Metric | Measured Value | Description |
| :--- | :--- | :--- |
| **Accuracy** | **0.7662** | 76.62% of all test predictions were correct. |
| **Precision** | **0.6727** | 67.27% of positive predictions were true positive diabetic cases. |
| **Recall** | **0.6727** | 67.27% of actual diabetic cases were correctly identified. |
| **F1-Score** | **0.6727** | Harmonic mean of precision and recall. |
| **ROC-AUC** | **0.8260** | 82.60% area under the receiver operating characteristic curve. |

---

## 5. Artifacts Generated

* `reports/metrics.csv` — CSV summary of evaluation metrics.
* `reports/confusion_matrix.png` — Visual confusion matrix plot.
* `reports/roc_curve.png` — Visual ROC curve plot showing AUC = 0.8260.
* `requirements-lock.txt` — Frozen environment lockfile for Python 3.12.

---

## 6. Baseline Limitations & Recommendations

1. **Unimputed Missing Measurements:** Implausible zero values in `Glucose` (5), `BloodPressure` (35), and `BMI` (11) act as noise. Imputing these with median values per outcome class could improve stability.
2. **Feature Exclusions:** Features present in the raw CSV (`Insulin`, `SkinThickness`, `DiabetesPedigreeFunction`) were omitted in the initial repository design. Including them may boost model sensitivity.
3. **Hyperparameter Tuning:** The baseline uses default Random Forest parameters. Hyperparameter optimization (e.g. `n_estimators`, `max_depth`, `min_samples_leaf`) can further enhance recall.
