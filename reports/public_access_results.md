# 🌐 Amazon EKS Public Access & Network Load Balancer Results (Step 9)

> [!IMPORTANT]
> **Active Public Access Notice:** The EKS diabetes prediction API is now accessible over the public internet via an AWS Network Load Balancer (NLB).
> * **Public API Base URL:** `http://a7e4c7a0bef2c49f092a59a812d8cf61-ad4075c41b4880ff.elb.ap-south-1.amazonaws.com`
> * **Public Interactive Swagger Documentation:** `http://a7e4c7a0bef2c49f092a59a812d8cf61-ad4075c41b4880ff.elb.ap-south-1.amazonaws.com/docs`
> * **Security Note:** This demonstration endpoint is HTTP unauthenticated & unencrypted. Do not send real personal data.

---

## 1. Public Infrastructure & Service Configuration

* **Namespace:** `mlops`
* **Service Name:** `diabetes-api-public`
* **Service Type:** `LoadBalancer`
* **Controller / Provider:** AWS EKS Cloud Controller Manager (Service Controller)
* **Load Balancer Class / Type:** Network Load Balancer (`nlb`)
* **Load Balancer Scheme:** `internet-facing` (`service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing`)
* **Target Type:** `instance` (`80:30997/TCP` -> container `8000/TCP`)
* **Cross-Zone Load Balancing:** Enabled (`service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: true`)
* **Explicit Subnet Selection:**
  * `subnet-0bb4bd2e43958e6f1` (`ap-south-1a`)
  * `subnet-09520f30aa76a511e` (`ap-south-1b`)
  * `subnet-084d6fc4be8c753f0` (`ap-south-1c`)
* **Public NLB DNS Name:** `a7e4c7a0bef2c49f092a59a812d8cf61-ad4075c41b4880ff.elb.ap-south-1.amazonaws.com`
* **Allocated Public IPv4 Addresses:** `15.207.189.201`, `13.204.176.173`, `13.205.59.231`

---

## 2. End-to-End Public API Verification Results

Executed all 11 automated smoke tests in [`test_api.py`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/test_api.py) directly against `http://a7e4c7a0bef2c49f092a59a812d8cf61-ad4075c41b4880ff.elb.ap-south-1.amazonaws.com` without port forwarding:

| # | Test Name | Endpoint & Method | Status Code | Observed Result | Result |
| :- | :--- | :--- | :-: | :--- | :-: |
| 1 | GET / Root Endpoint | `GET /` | `200 OK` | `{"message": "Diabetes Prediction API is live"}` | **PASS** |
| 2 | GET /docs Documentation | `GET /docs` | `200 OK` | Interactive Swagger UI HTML Page | **PASS** |
| 3 | GET /openapi.json Schema | `GET /openapi.json` | `200 OK` | OpenAPI 3.1 JSON Schema | **PASS** |
| 4 | POST /predict Fixed Sample | `POST /predict` | `200 OK` | `{"diabetic": true}` | **PASS** |
| 5 | POST /predict Repeatability | `POST /predict` | `200 OK` | `{"diabetic": true}` | **PASS** |
| 6 | POST /predict Non-Diabetic | `POST /predict` | `200 OK` | `{"diabetic": false}` | **PASS** |
| 7 | Invalid Empty JSON | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 8 | Invalid Missing Field | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 9 | Invalid Non-numeric String | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 10 | Invalid Null Field | `POST /predict` | `422` | Validation Error (Expected) | **PASS** |
| 11 | Invalid Malformed Syntax | `POST /predict` | `422` | JSON Decode Error (Expected) | **PASS** |

**Summary:** **11 Total, 11 Passed, 0 Failed (100% Pass Rate over Public Internet)**.

---

## 3. Official Sourced Pricing Breakdown (`ap-south-1` Mumbai)

| Component | Resource Spec | Hourly Rate | 4-Hour Lab Cost | 24-Hour Daily Cost |
| :--- | :--- | :-: | :-: | :-: |
| **EKS Control Plane** | `diabetes-mlops` (v1.36) | $0.1000 | $0.4000 | $2.4000 |
| **Worker Instance** | `t3.small` (2 vCPU, 2GB) | $0.0224 | $0.0896 | $0.5376 |
| **Worker Public IPv4** | Node Public IP (`13.126.66.163`) | $0.0050 | $0.0200 | $0.1200 |
| **Root EBS Volume** | 20 GB GP3 Encrypted | $0.0025 | $0.0100 | $0.0600 |
| **Public NLB Base** | Network Load Balancer | $0.0225 | $0.0900 | $0.5400 |
| **Public NLB IPv4s** | 3 x NLB Public IPs ($0.0050/ea) | $0.0150 | $0.0600 | $0.3600 |
| **NLB Capacity Units** | NLCU Usage (< 1 NLCU) | < $0.0001 | < $0.0001 | < $0.0001 |
| **TOTAL GROSS RUNNING COST** | — | **~$0.1674 / hr** | **~$0.6696 USD** | **~$4.0176 USD** |

> [!NOTE]
> **AWS Credit Coverage Uncertainty:** AWS Free Tier credits cover certain standard compute allowances (e.g. 750 hours `t2.micro`/`t3.micro` if eligible), but do **not** cover EKS control plane fees ($0.10/hr), Network Load Balancer base fees ($0.0225/hr), or In-Use Public IPv4 addresses ($0.0050/hr). These billable charges accumulate against credit or payment cards while resources are running.

---

## 4. Exact Public Access Cleanup Instructions

To remove the public load balancer while keeping the internal application running:

```bash
# 1. Delete Public LoadBalancer Service (Triggers AWS NLB Deletion)
./bin/kubectl delete -f k8s-public-service.yml

# 2. Verify NLB Service Deletion
./bin/kubectl -n mlops get service
```

To delete **all** infrastructure resources and stop all AWS billing:

```bash
# 1. Delete Public Service
./bin/kubectl delete -f k8s-public-service.yml

# 2. Delete Internal Application Deployment & Service
./bin/kubectl delete -f k8s-deploy.yml

# 3. Delete Managed Node Group
aws eks delete-nodegroup --cluster-name diabetes-mlops --nodegroup-name diabetes-workers --profile mlops-operator --region ap-south-1
aws eks wait nodegroup-deleted --cluster-name diabetes-mlops --nodegroup-name diabetes-workers --profile mlops-operator --region ap-south-1

# 4. Delete EKS Cluster Control Plane
aws eks delete-cluster --name diabetes-mlops --profile mlops-operator --region ap-south-1
aws eks wait cluster-deleted --name diabetes-mlops --profile mlops-operator --region ap-south-1

# 5. Delete EC2 Launch Template & IAM Roles
aws ec2 delete-launch-template --launch-template-id lt-01f2f743e19153364 --profile mlops-operator --region ap-south-1
aws iam detach-role-policy --role-name diabetes-eks-cluster-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --profile mlops-operator --region ap-south-1
aws iam delete-role --role-name diabetes-eks-cluster-role --profile mlops-operator --region ap-south-1

aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy --profile mlops-operator --region ap-south-1
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly --profile mlops-operator --region ap-south-1
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --profile mlops-operator --region ap-south-1
aws iam delete-role --role-name diabetes-eks-node-role --profile mlops-operator --region ap-south-1
```
