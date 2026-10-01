# Diabetes Prediction MLOps Pipeline on AWS EKS

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-linux%2Famd64-blue)](https://www.docker.com/)
[![Amazon EKS](https://img.shields.io/badge/Amazon%20EKS-v1.36-orange.svg)](https://aws.amazon.com/eks/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.36-blue.svg)](https://kubernetes.io/)

Production-ready MLOps end-to-end repository for training, containerizing, publishing, and deploying a **Diabetes Prediction ML API** on **Amazon EKS (Kubernetes 1.36)** with AWS Network Load Balancing.

---

## Architecture and Project Overview

```
                          [ Client / Web / Mobile ]
                                      │
                                      ▼
                        [ AWS Network Load Balancer ]
                    (<NLB_HOSTNAME>.elb.ap-south-1.amazonaws.com)
                                      │
                                      ▼
                           [ EKS Cluster v1.36 ]
                           (Region: ap-south-1)
                                      │
                         ┌────────────┴────────────┐
                         ▼                         ▼
            [ ClusterIP Service ]         [ Kubernetes Node ]
          (diabetes-api-service:80)      (t3.small / AL2023)
                         │                         │
                         └────────────┬────────────┘
                                      ▼
                             [ FastAPI Pod ]
                     (diabetes-api @ digest-pinned ECR)
```

### Key Highlights
* **Model**: Scikit-Learn Random Forest Classifier trained on the Pima Indians Diabetes Dataset.
* **REST API**: High-performance FastAPI server with input validation (Pydantic), readiness/liveness health probes, and automated OpenAPI `/docs`.
* **Containerization**: Multi-stage Docker build targeting `linux/amd64` architecture, published to Amazon ECR.
* **Infrastructure**: Provisioned AWS EKS Cluster (Kubernetes 1.36, `STANDARD` support), dedicated IAM Least-Privilege roles, EC2 Launch Template with encrypted `gp3` root volumes, and AWS Network Load Balancer (NLB).
* **Verification**: 100% automated smoke test coverage (11/11 tests passing against local container, port-forwarded cluster service, and live public NLB).

---

## Repository Structure

```
.
├── main.py                     # FastAPI REST application & predict endpoint
├── train.py                    # Model training pipeline & serialization script
├── test_api.py                 # Automated 11-point API smoke test suite
├── Dockerfile                  # Production Dockerfile (linux/amd64)
├── requirements.txt            # Python dependencies
├── requirements-lock.txt       # Pinned deterministic dependencies
├── k8s-deploy.yml              # Kubernetes Namespace, Deployment, and ClusterIP Service
├── k8s-public-service.yml       # Kubernetes LoadBalancer Service (AWS NLB)
├── sample-request.json         # Sample JSON request payload
├── policies/                   # IAM policies & cluster provisioning templates
│   ├── diabetes-provisioner-policy.json  # Operator IAM policy definition
│   ├── cluster-trust-policy.json        # EKS cluster role trust policy
│   ├── node-trust-policy.json           # Worker node role trust policy
│   ├── launch-template.json             # EC2 launch template specification (gp3 encrypted)
│   ├── cluster-config.json              # EKS cluster creation configuration
│   └── nodegroup-config.json            # Managed node group configuration
└── reports/                    # Comprehensive phase audit reports
    ├── mlops_pipeline_report.md         # Master pipeline execution & audit report
    ├── metrics.csv                      # Baseline model performance metrics
    ├── confusion_matrix.png             # Model evaluation confusion matrix
    └── roc_curve.png                    # Model evaluation ROC curve
```

---

## Dataset and Feature Requirements

The model predicts diabetes likelihood based on 5 clinical parameters:

| Parameter | Type | Range / Description |
| :--- | :--- | :--- |
| `Pregnancies` | `int` | Number of times pregnant |
| `Glucose` | `int` | Plasma glucose concentration (mg/dL) |
| `BloodPressure` | `int` | Diastolic blood pressure (mm Hg) |
| `BMI` | `float` | Body mass index ($\text{kg/m}^2$) |
| `Age` | `int` | Age in years |

### Sample Payload
```json
{
  "Pregnancies": 2,
  "Glucose": 130,
  "BloodPressure": 70,
  "BMI": 28.5,
  "Age": 45
}
```

---

## Quick Start Guide

### 1. Local Setup and Training

```bash
# Clone the repository
git clone https://github.com/suwickramanayaka/diabetes-prediction-mlops.git
cd diabetes-prediction-mlops

# Create & activate virtual environment
python3 -m venv .mlops
source .mlops/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train the model (generates diabetes_model.pkl)
python3 train.py

# Run FastAPI server locally
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### 2. Run Local Smoke Tests

In a separate terminal window:
```bash
python3 test_api.py --base-url http://127.0.0.1:8000
```

---

## Containerization and Amazon ECR

### Build Docker Image for `linux/amd64`

```bash
docker buildx build --platform linux/amd64 --load -t diabetes-api:v1 .
```

### Run Container Locally and Test

```bash
docker run -d --name diabetes-api-container -p 127.0.0.1:8000:8000 diabetes-api:v1
python3 test_api.py --base-url http://127.0.0.1:8000
docker stop diabetes-api-container && docker rm diabetes-api-container
```

### Publish to Private Amazon ECR

```bash
# 1. Authenticate Docker with ECR in ap-south-1
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com

# 2. Tag and push immutable image
docker tag diabetes-api:v1 <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api:v1
docker push <AWS_ACCOUNT_ID>.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api:v1
```

---

## Kubernetes Deployment on Amazon EKS

### 1. Deploy Internal Application Stack

```bash
kubectl apply -f k8s-deploy.yml
```

### 2. Verify Rollout and System Health

```bash
kubectl -n mlops rollout status deployment/diabetes-api --timeout=300s
kubectl -n mlops get pods -o wide
kubectl -n mlops get service diabetes-api-service
```

### 3. Local Port-Forwarding (Optional)

```bash
kubectl -n mlops port-forward service/diabetes-api-service 8000:80 --address 127.0.0.1
# Test via: python3 test_api.py --base-url http://127.0.0.1:8000
```

---

## Public Network Load Balancer (NLB) Access

To expose the API publicly across the internet:

```bash
kubectl apply -f k8s-public-service.yml
```

### Live Public Endpoints
* **Public Base URL:** `http://<NLB_HOSTNAME>.elb.ap-south-1.amazonaws.com`
* **Swagger UI Documentation:** `http://<NLB_HOSTNAME>.elb.ap-south-1.amazonaws.com/docs`

### Run Smoke Tests Against Live Public Endpoint

```bash
python3 test_api.py --base-url http://<NLB_HOSTNAME>.elb.ap-south-1.amazonaws.com
```

---

## Infrastructure Teardown and Cleanup

To remove public load balancing while leaving the application running internally:

```bash
kubectl delete -f k8s-public-service.yml
```

To tear down all AWS resources and stop all billing:

```bash
# 1. Delete Public Service & Internal Stack
kubectl delete -f k8s-public-service.yml
kubectl delete -f k8s-deploy.yml

# 2. Delete Managed Node Group
aws eks delete-nodegroup --cluster-name diabetes-mlops --nodegroup-name diabetes-workers --region ap-south-1
aws eks wait nodegroup-deleted --cluster-name diabetes-mlops --nodegroup-name diabetes-workers --region ap-south-1

# 3. Delete EKS Cluster Control Plane
aws eks delete-cluster --name diabetes-mlops --region ap-south-1
aws eks wait cluster-deleted --name diabetes-mlops --region ap-south-1

# 4. Delete Launch Template & IAM Service Roles
aws ec2 delete-launch-template --launch-template-name diabetes-node-lt --region ap-south-1
aws iam detach-role-policy --role-name diabetes-eks-cluster-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy
aws iam delete-role --role-name diabetes-eks-cluster-role
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy
aws iam delete-role --role-name diabetes-eks-node-role
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
