# MLOps Pipeline Execution and Audit Report

## Executive Summary

This report documents the end-to-end design, implementation, and deployment of the Diabetes Prediction MLOps pipeline on Amazon EKS. The pipeline spans dataset verification, machine learning model training, REST API packaging, containerization, Amazon ECR publication, infrastructure provisioning under IAM least privilege, Kubernetes deployment, public load balancing, and automated verification.

---

## 1. Machine Learning Model Training and Baseline Evaluation

### Dataset Provenance
* **Source Dataset**: Pima Indians Diabetes Dataset
* **Total Instances**: 768 samples
* **Features Selected**: `Pregnancies`, `Glucose`, `BloodPressure`, `BMI`, `Age`
* **Target Variable**: `Outcome` (0 = Non-diabetic, 1 = Diabetic)
* **Class Balance**: 500 Non-diabetic (65.10%), 268 Diabetic (34.90%)

### Model Architecture and Performance
* **Algorithm**: Random Forest Classifier (`n_estimators=100`, `random_state=42`)
* **Train/Test Split**: 80% Train (614 samples), 20% Test (154 samples)
* **Accuracy**: 76.62%
* **Precision**: 66.07%
* **Recall**: 68.52%
* **F1-Score**: 67.27%
* **ROC-AUC**: 0.8263

### Artifact Generation
* **Model Serialization**: `diabetes_model.pkl` (~1.75 MB)
* **Metrics Summary**: `reports/metrics.csv`
* **Evaluation Visualizations**:
  * Confusion Matrix: `reports/confusion_matrix.png`
  * ROC Curve: `reports/roc_curve.png`

---

## 2. FastAPI REST Application and Containerization

### API Architecture
The REST API is implemented using FastAPI with Pydantic request body validation.
* **Health Probes**: `GET /` returns status `"healthy"` and API version.
* **Prediction Endpoint**: `POST /predict` accepts 5 clinical parameters and returns binary prediction (`0` or `1`), probability score, and human-readable result.
* **Interactive Documentation**: `GET /docs` (Swagger UI).

### Container Build Specifications
* **Base Image**: `python:3.12-slim`
* **Target Architecture**: `linux/amd64` (`x86_64`)
* **Security Control**: Non-root container execution under `appuser` (`uid=1000`)
* **Image Size**: 594 MB

---

## 3. Amazon ECR Publication

### Repository Configuration
* **Registry**: Amazon ECR (Region: `ap-south-1`)
* **Repository Name**: `diabetes-api`
* **Tag Mutability**: `IMMUTABLE`
* **Encryption**: `AES256`

### Published Image Digest
* **Image Tag**: `v1`
* **Immutable Digest**: `sha256:5e88ae2f0a3d6a70bc1cb336f240c476e674911dcd2179b168e333ecca99bec8`

---

## 4. AWS EKS Infrastructure Provisioning and Governance

### IAM Security and Least Privilege
An operator IAM identity (`diabetes-operator`) was configured with a dedicated policy (`policies/diabetes-provisioner-policy.json`). IAM policy validation confirmed zero errors, zero warnings, and zero security notices.

### EKS Cluster Configuration
* **Cluster Name**: `diabetes-mlops`
* **Kubernetes Version**: `1.36` (`STANDARD` support lifecycle)
* **Networking**: AWS VPC with 3 Availability Zones
* **Cluster IAM Role**: `diabetes-eks-cluster-role` attached to `AmazonEKSClusterPolicy`

### Managed Worker Node Group
* **Node Group Name**: `diabetes-workers`
* **Instance Type**: `t3.small` (2 vCPUs, 2 GiB Memory, `x86_64`)
* **Operating System**: Amazon Linux 2023 (`AL2023_x86_64_STANDARD`)
* **Node IAM Role**: `diabetes-eks-node-role` (`AmazonEKSWorkerNodePolicy`, `AmazonEC2ContainerRegistryReadOnly`, `AmazonEKS_CNI_Policy`)
* **Root Volume**: 20 GiB `gp3` encrypted EBS volume with `DeleteOnTermination`

---

## 5. Kubernetes Deployment and System Health

### Kubernetes Manifest Architecture (`k8s-deploy.yml`)
* **Namespace**: `mlops`
* **Deployment**: `diabetes-api` (1 replica)
* **Resource Limits**: Requests (100m CPU, 256Mi RAM), Limits (500m CPU, 512Mi RAM)
* **Probes**: Startup, Readiness, and Liveness probes configured on `GET /`
* **Internal Service**: `diabetes-api-service` (Type: `ClusterIP`, Port 80 -> Container Port 8000)

### Automated Verification Results
An 11-point automated smoke test suite (`test_api.py`) was executed against the stack:
1. `GET /` Health Check -> HTTP 200 (Pass)
2. `GET /docs` OpenAPI Page -> HTTP 200 (Pass)
3. `POST /predict` Standard Sample Payload -> HTTP 200 (Pass)
4. `POST /predict` High Glucose / High Risk Payload -> HTTP 200 (Pass)
5. `POST /predict` Low Glucose / Low Risk Payload -> HTTP 200 (Pass)
6. `POST /predict` Missing Required Feature -> HTTP 422 (Pass)
7. `POST /predict` Invalid Feature Type -> HTTP 422 (Pass)
8. `POST /predict` Negative Feature Value -> HTTP 422 (Pass)
9. `POST /predict` Excessive Feature Value -> HTTP 422 (Pass)
10. `POST /predict` Extra Unknown Field -> HTTP 200 (Pass)
11. `POST /predict` Empty Body Payload -> HTTP 422 (Pass)

**Result**: 11/11 tests passed (100% success rate).

---

## 6. Public Access and Load Balancer Configuration

### AWS Network Load Balancer (`k8s-public-service.yml`)
* **Service Name**: `diabetes-api-public`
* **Service Type**: `LoadBalancer`
* **Controller**: AWS EKS Cloud Controller Manager
* **Load Balancer Type**: Network Load Balancer (`nlb`), internet-facing
* **Target Type**: Instance mode (Port 80 -> NodePort 30997 -> Container Port 8000)

### Cost Analysis (Mumbai Region `ap-south-1`)
* **EKS Control Plane**: $0.1000 USD / hour ($2.40 / day)
* **Worker Node (`t3.small`)**: $0.0224 USD / hour ($0.5376 / day)
* **EBS Storage (20 GiB `gp3`)**: $0.0025 USD / hour ($0.06 / day)
* **Worker Public IPv4**: $0.0050 USD / hour ($0.12 / day)
* **Public NLB + Public IPv4**: $0.0375 USD / hour ($0.90 / day)
* **Total Estimated Cost**: **~$0.1674 USD / hour** (~$4.02 USD / 24 hours)

---

## Conclusion

The end-to-end MLOps pipeline successfully fulfills all operational requirements. The ML model is containerized, stored immutably in Amazon ECR, deployed to a secure Amazon EKS 1.36 cluster under IAM least privilege, and verified with 100% test pass rate.
