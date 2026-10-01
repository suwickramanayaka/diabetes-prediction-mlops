# ☁️ Amazon ECR Publication & Verification Report

## 1. AWS Identity & Regional Configuration

* **AWS Profile:** `mlops`
* **AWS Region:** `ap-south-1` (Mumbai)
* **AWS Account ID:** `122773994215`
* **IAM Caller Identity:** `arn:aws:iam::122773994215:root`

---

## 2. Private ECR Repository Provisioning

* **Repository Name:** `diabetes-api`
* **Status:** Created (`aws ecr create-repository`)
* **Repository ARN:** `arn:aws:ecr:ap-south-1:122773994215:repository/diabetes-api`
* **Repository URI:** `122773994215.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api`
* **Image Tag Mutability:** `IMMUTABLE`
* **Encryption:** `AES256`

---

## 3. Publication & Image Identifiers

* **Local Image Tag:** `diabetes-api:v1`
* **Local Docker Image ID:** `sha256:59c0c4f6bcc0d0c8f06926a1346cc5c82be0fe77fd06029f3a46bd1dd171b106`
* **Target Architecture:** `linux/amd64` (`x86_64`)
* **Published Remote Tag:** `v1`
* **ECR Image Manifest Digest:** `sha256:5e88ae2f0a3d6a70bc1cb336f240c476e674911dcd2179b168e333ecca99bec8`
* **Tagged Image URI:**
  `122773994215.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api:v1`
* **Digest-Pinned Image URI:**
  `122773994215.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api@sha256:5e88ae2f0a3d6a70bc1cb336f240c476e674911dcd2179b168e333ecca99bec8`

### Size Comparison

* **ECR Stored Compressed Size (`imageSizeInBytes`):** `193,862,777` bytes (~193.86 MB)
* **Local Uncompressed Docker Image Size:** `594 MB`

---

## 4. Pull & Local Container Verification

1. **Digest Pull:**
   ```bash
   docker pull --platform linux/amd64 122773994215.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api@sha256:5e88ae2f0a3d6a70bc1cb336f240c476e674911dcd2179b168e333ecca99bec8
   ```
2. **Image Content Verification:**
   * Pulled Docker Image ID: `sha256:59c0c4f6bcc0d0c8f06926a1346cc5c82be0fe77fd06029f3a46bd1dd171b106`
   * Architecture: `linux/amd64`
   * Result: **100% exact match with local image content**.

3. **Container Smoke Test Suite:**
   Ran temporary test container from digest-pinned ECR URI (`diabetes-ecr-test-container`):
   * `python3 test_api.py --base-url http://127.0.0.1:8000`
   * **Results:** **11/11 tests passed**. Fixed sample returned `{"diabetic": true}`.
   * **Container Logs:** Clean (zero errors, warnings, or missing model issues).
   * **Cleanup:** Test container stopped and removed cleanly.
