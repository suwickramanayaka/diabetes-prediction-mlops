# 🚀 Amazon EKS Application Deployment & End-to-End Verification Results (Step 8)

> [!IMPORTANT]
> **Active Infrastructure Notice:** The diabetes prediction API is **LIVE** on Amazon EKS in namespace `mlops`.
> * **Cluster:** `diabetes-mlops` (Region: `ap-south-1`)
> * **Deployment Status:** `1/1` Replicas Ready & Available.

---

## 1. Kubernetes Deployment & Pod Verification

* **Namespace:** `mlops`
* **Deployment Name:** `diabetes-api`
* **Replica Count:** `1` Desired / `1` Updated / `1` Available
* **Pod Name:** `diabetes-api-5c6746b65c-gdznj`
* **Pod Status:** **`1/1 Ready`** (`Running`)
* **Pod IP:** `172.31.42.88`
* **Worker Node:** `ip-172-31-37-33.ap-south-1.compute.internal`
* **Container Image (Digest Pinned):**
  `122773994215.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api@sha256:5e88ae2f0a3d6a70bc1cb336f240c476e674911dcd2179b168e333ecca99bec8`

### Container Resource Specification & Verification
* **CPU Request:** `100m` (0.1 vCPU)
* **Memory Request:** `256Mi`
* **CPU Limit:** `500m` (0.5 vCPU)
* **Memory Limit:** `512Mi`
* **Resource Allocatable Check:** Confirmed that `t3.small` allocatable memory (`1433 MiB`) and CPU (`1930m`) comfortably satisfy these requests with system overhead.

---

## 2. Service & EndpointSlice Verification

* **Service Name:** `diabetes-api-service`
* **Service Type:** `ClusterIP`
* **Cluster IP:** `10.100.50.27`
* **Port Mapping:** `80/TCP` targeting container port `8000`
* **EndpointSlice Name:** `diabetes-api-service-bscd8`
* **Active Endpoints:** `172.31.42.88:8000` (**`Ready`**)

---

## 3. End-to-End API Smoke Test Results

All 11 automated smoke tests in [`test_api.py`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/test_api.py) were executed against the forwarded service endpoint `http://127.0.0.1:8000`:

| # | Test Name | Endpoint & Method | Status Code | Observed Result | Result |
| :- | :--- | :--- | :-: | :--- | :-: |
| 1 | GET / Root Endpoint | `GET /` | `200 OK` | `{"message": "Diabetes Prediction API is live"}` | **PASS** |
| 2 | GET /docs Documentation | `GET /docs` | `200 OK` | Swagger UI HTML Page Accessible | **PASS** |
| 3 | GET /openapi.json Schema | `GET /openapi.json` | `200 OK` | Valid OpenAPI 3.1 Schema with `/predict` | **PASS** |
| 4 | POST /predict Fixed Sample | `POST /predict` | `200 OK` | `{"diabetic": true}` | **PASS** |
| 5 | POST /predict Repeatability | `POST /predict` | `200 OK` | `{"diabetic": true}` | **PASS** |
| 6 | POST /predict Non-Diabetic | `POST /predict` | `200 OK` | `{"diabetic": false}` | **PASS** |
| 7 | Invalid Empty JSON | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 8 | Invalid Missing Field | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 9 | Invalid Non-numeric String | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 10 | Invalid Null Field | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 11 | Invalid Malformed Syntax | `POST /predict` | `422` | JSON Decode Error (Expected) | **PASS** |

**Summary:** **11 Total, 11 Passed, 0 Failed (100% Pass Rate)**.

---

## 4. Reopening Local API Access & Port Forwarding

The `ClusterIP` Service isolates the API securely inside the cluster VPC. To open local access for testing or interactive browsing:

```bash
./bin/kubectl -n mlops port-forward service/diabetes-api-service 8000:80 --address 127.0.0.1
```

> [!NOTE]
> The address `http://127.0.0.1:8000` is localhost-only and active **only while the port-forward process is running**.

---

## 5. Summary of Changed & Created Files

* [`k8s-deploy.yml`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/k8s-deploy.yml): Deployed Kubernetes manifest defining Namespace, Deployment, and ClusterIP Service.
* [`reports/eks_deployment_results.md`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/reports/eks_deployment_results.md): End-to-end verification report.
* [`reports/eks_provisioning_results.md`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/reports/eks_provisioning_results.md): Updated cost arithmetic breakdown.
* [`README.md`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/README.md): Updated with EKS deployment, port-forwarding, and testing instructions.

---

## 6. Unresolved Issues

* **None**. All components deployed cleanly, probes passed, endpoints bound, and 100% of smoke tests succeeded.
