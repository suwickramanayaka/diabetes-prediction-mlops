# 🌐 FastAPI Service Test & Verification Report

## 1. Local Server Environment & Address

* **Server Command:** `uvicorn main:app --host 127.0.0.1 --port 8000` (executed via `.venv`)
* **Local Address:** `http://127.0.0.1:8000`
* **Startup Result:** Launched successfully with zero startup errors.

---

## 2. API Verification Test Suite Results

Smoke test command executed:
```bash
python3 test_api.py --base-url http://127.0.0.1:8000
```

### Valid Request Endpoints

| Test Case | Method & Endpoint | Expected Status | Actual Status | Result | Response Payload |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Root Health Check** | `GET /` | 200 | 200 | ✅ PASS | `{"message": "Diabetes Prediction API is live"}` |
| **Swagger UI Documentation** | `GET /docs` | 200 | 200 | ✅ PASS | HTML UI Page Loaded |
| **OpenAPI Schema** | `GET /openapi.json` | 200 | 200 | ✅ PASS | Schema contains `/predict` path |
| **Fixed Sample Prediction** | `POST /predict` | 200 | 200 | ✅ PASS | `{"diabetic": true}` |
| **Repeatability Check** | `POST /predict` | 200 | 200 | ✅ PASS | `{"diabetic": true}` |
| **Non-Diabetic Control Sample** | `POST /predict` | 200 | 200 | ✅ PASS | `{"diabetic": false}` |

---

## 3. Invalid Request & Validation Edge Cases

All invalid request payloads were rejected with **HTTP 422 Unprocessable Entity** under FastAPI's default request validation (`Pydantic` schema enforcement):

| Invalid Test Case | Request Payload | Status | Response Detail / Message |
| :--- | :--- | :--- | :--- |
| **Empty JSON Object** | `{}` | 422 | `Field required` for all 5 features (`Pregnancies`, `Glucose`, `BloodPressure`, `BMI`, `Age`) |
| **Missing Field** | `{"Pregnancies": 2, "BloodPressure": 70, "BMI": 28.5, "Age": 45}` | 422 | `Field required` (`Glucose`) |
| **Non-numeric String** | `{"Pregnancies": 2, "Glucose": "not-a-number", ...}` | 422 | `Input should be a valid number, unable to parse string` |
| **Null Value** | `{"Pregnancies": 2, "Glucose": null, ...}` | 422 | `Input should be a valid number` |
| **Malformed JSON Syntax** | `{"Pregnancies": 2,` | 422 | `JSON decode error` (`json_invalid`) |

---

## 4. Model Direct Inference vs HTTP Prediction Agreement

| Test Sample Inputs | Direct Model (`joblib`) Prediction | HTTP API (`POST /predict`) Response | Agreement |
| :--- | :--- | :--- | :--- |
| **Fixed Sample:** `Pregnancies=2`, `Glucose=130`, `BloodPressure=70`, `BMI=28.5`, `Age=45` | Class `1` (`Diabetic`) [Prob = 0.7300] | `{"diabetic": true}` | **100% Match** |
| **Control Sample:** `Pregnancies=0`, `Glucose=85`, `BloodPressure=66`, `BMI=22.0`, `Age=22` | Class `0` (`Non-Diabetic`) [Prob = 0.9600] | `{"diabetic": false}` | **100% Match** |

---

## 5. Input Validation Gaps & Observations

1. **Pydantic Type Coercion:** String representations of numbers (e.g. `"Glucose": "130"`) are automatically coerced to `float` by Pydantic v2 without error.
2. **Negative Values:** The current Pydantic schema (`DiabetesInput`) uses unconstrained `int` and `float`. Negative values (e.g., `BMI: -15.0`) pass type validation and reach the model.
3. **Missing Value Encoding:** Zero values (e.g. `Glucose: 0`) pass validation and are processed by the Random Forest baseline model without runtime error.

---

## 6. How to Run local API & Smoke Tests

### 1. Start the API locally:
```bash
source .venv/bin/activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 2. Run the smoke tests:
```bash
python3 test_api.py --base-url http://127.0.0.1:8000
```
