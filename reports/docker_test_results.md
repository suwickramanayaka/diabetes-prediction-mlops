# 🐳 Docker Packaging & Container Test Report

## 1. Build Specifications & Image Details

* **Build Command:**
  ```bash
  docker buildx build --platform linux/amd64 --load -t diabetes-api:v1 .
  ```
* **Image Tag:** `diabetes-api:v1`
* **Image ID:** `59c0c4f6bcc0d0c8f06926a1346cc5c82be0fe77fd060`
* **Target Architecture:** `linux/amd64` (`x86_64`)
* **Base Image:** `python:3.12-slim`
* **Image Size:** `594MB`
* **Configured User:** `appuser` (`uid=1000(appuser)`, non-root)

---

## 2. Dependency & Model Integrity Checks

### Package Version Consistency

| Package | Local `.venv` Version | Container Image Version | Consistency Check |
| :--- | :--- | :--- | :--- |
| **`scikit-learn`** | `1.9.1` | `1.9.1` | ✅ Exact Match |
| **`pandas`** | `3.0.6` | `3.0.6` | ✅ Exact Match |
| **`numpy`** | `2.5.3` | `2.5.3` | ✅ Exact Match |
| **`scipy`** | `1.18.1` | `1.18.1` | ✅ Exact Match |
| **`joblib`** | `1.6.0` | `1.6.0` | ✅ Exact Match |
| **`fastapi`** | `0.142.2` | `0.142.2` | ✅ Exact Match |
| **`uvicorn`** | `0.54.0` | `0.54.0` | ✅ Exact Match |

* **Container `pip check`:** Executed inside image — **0 broken requirements**.

### Model File SHA-256 Hash Comparison

| Location | SHA-256 Checksum | Match Status |
| :--- | :--- | :--- |
| **Local Host (`diabetes_model.pkl`)** | `af2fc2a01d6a46dda4803ba6d524952006ca8339aceaac628912bf759651790d` | Base Reference |
| **Inside Docker Image (`/app/diabetes_model.pkl`)** | `af2fc2a01d6a46dda4803ba6d524952006ca8339aceaac628912bf759651790d` | ✅ 100% Identical |

---

## 3. Container Run & Smoke Test Results

* **Run Command:**
  ```bash
  docker run -d --name diabetes-api-test-container -p 127.0.0.1:8000:8000 diabetes-api:v1
  ```
* **Smoke Test Command:**
  ```bash
  python3 test_api.py --base-url http://127.0.0.1:8000
  ```

### Smoke Test Suite Results

| Test Case | Description | Status | Result |
| :--- | :--- | :--- | :--- |
| **Test 1** | `GET /` Root Health Check | 200 OK | ✅ PASS |
| **Test 2** | `GET /docs` Swagger UI | 200 OK | ✅ PASS |
| **Test 3** | `GET /openapi.json` Schema | 200 OK | ✅ PASS |
| **Test 4** | `POST /predict` Fixed Sample | 200 OK | ✅ PASS (`{"diabetic": true}`) |
| **Test 5** | `POST /predict` Repeatability | 200 OK | ✅ PASS (`{"diabetic": true}`) |
| **Test 6** | `POST /predict` Non-Diabetic Sample | 200 OK | ✅ PASS (`{"diabetic": false}`) |
| **Test 7** | Invalid POST: Empty JSON `{}` | 422 Unprocessable Entity | ✅ PASS |
| **Test 8** | Invalid POST: Missing Field (`Glucose`) | 422 Unprocessable Entity | ✅ PASS |
| **Test 9** | Invalid POST: Non-numeric String | 422 Unprocessable Entity | ✅ PASS |
| **Test 10** | Invalid POST: Null Field | 422 Unprocessable Entity | ✅ PASS |
| **Test 11** | Invalid POST: Malformed JSON Syntax | 422 Unprocessable Entity | ✅ PASS |

* **Container Restart Test:** Stopped container (`docker stop`), restarted (`docker start`), and re-executed `test_api.py`. **11/11 tests passed**, confirming container self-sufficiency and independence from local host processes.

---

## 4. Container Log Inspection

Container logs were completely clean:
```text
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```
No feature-name warnings, model load errors, or unhandled exceptions occurred.
