# ☸️ Amazon EKS Infrastructure Provisioning & Verification Results (Step 7B Complete)

> [!IMPORTANT]
> **Active Billing Notice:** The EKS Cluster control plane (`diabetes-mlops`) and worker node (`diabetes-workers`) are **ACTIVE** in region `ap-south-1`.
> * **Billing Rate:** ~$0.1274 USD / hour (~$3.06 USD per 24 hours).
> * Billing continues while the infrastructure remains active.

---

## 1. EKS Cluster Configuration & Verification

* **Cluster Name:** `diabetes-mlops`
* **Cluster ARN:** [`arn:aws:eks:ap-south-1:122773994215:cluster/diabetes-mlops`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/policies/cluster-config.json)
* **Status:** `ACTIVE`
* **Kubernetes Version:** `1.36` (Patch: `1.36.4-eks-f4fc4f1`)
* **Support Policy:** `STANDARD` (End of Standard Support: `2027-08-02`)
* **Endpoint Access:**
  * Public Endpoint: `Enabled` (Restricted to operator IPv4: `112.134.247.58/32`)
  * Private Endpoint: `Enabled` (`endpointPrivateAccess: true`)
* **Control Plane API Endpoint:** `https://5085806332F5BBC27E8303314FF2E154.gr7.ap-south-1.eks.amazonaws.com`
* **Creation Timestamp:** `2026-10-01T17:21:10+05:30`

---

## 2. Networking & VPC Selection

* **VPC ID:** `vpc-09032bee8944c30d4` (`172.31.0.0/16`)
* **Subnets Selected (3 Availability Zones):**
  * `subnet-0bb4bd2e43958e6f1` (`172.31.32.0/20`, AZ: `ap-south-1a`, Public IP on Launch: `true`)
  * `subnet-09520f30aa76a511e` (`172.31.0.0/20`, AZ: `ap-south-1b`, Public IP on Launch: `true`)
  * `subnet-084d6fc4be8c753f0` (`172.31.16.0/20`, AZ: `ap-south-1c`, Public IP on Launch: `true`)
* **Internet Gateway:** Attached (`igw-085e3cb7386ea5f0a`).

---

## 3. Operator Access Configuration & SLR Verification

* **IAM Identity:** `arn:aws:iam::122773994215:user/diabetes-operator`
* **AWS CLI Profile:** `mlops-operator`
* **Authentication Mode:** `API_AND_CONFIG_MAP`
* **Cluster Access Entry:** Creator admin access entry automatically enabled (`bootstrapClusterCreatorAdminPermissions: true`).
* **Local Kubeconfig Context:** `arn:aws:eks:ap-south-1:122773994215:cluster/diabetes-mlops`
* **Client Tooling Version:** Local `./bin/kubectl` `v1.36.5` (`darwin/arm64`).
* **SLR Access Verification:** `aws iam get-role --role-name AWSServiceRoleForAmazonEKSNodegroup` **Verified OK** (`arn:aws:iam::122773994215:role/aws-service-role/eks-nodegroup.amazonaws.com/AWSServiceRoleForAmazonEKSNodegroup`).

---

## 4. Service Roles & Launch Template Configuration

### Service Roles
* **Cluster Role:** `arn:aws:iam::122773994215:role/diabetes-eks-cluster-role`
  * Trust: `eks.amazonaws.com`
  * Managed Policy: `arn:aws:iam::aws:policy/AmazonEKSClusterPolicy`
* **Node Role:** `arn:aws:iam::122773994215:role/diabetes-eks-node-role`
  * Trust: `ec2.amazonaws.com`
  * Managed Policies:
    * `arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy`
    * `arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly`
    * `arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy`
* **Service-Linked Role:** `arn:aws:iam::122773994215:role/aws-service-role/eks-nodegroup.amazonaws.com/AWSServiceRoleForAmazonEKSNodegroup`

### Launch Template
* **Launch Template Name:** `diabetes-node-lt`
* **Launch Template ID:** `lt-01f2f743e19153364`
* **Version:** `1`
* **Root Volume Specification (Verified on Instance `i-08c811812ae808cdc`):**
  * Device Name: `/dev/xvda`
  * Volume ID: `vol-03faa3b80bd036ad5`
  * Volume Type: `gp3`
  * Volume Size: `20` GiB
  * Encryption: `Enabled` (`Encrypted: true`)
  * Delete On Termination: `true` (`DeleteOnTermination: true`)
* **SSH Remote Access:** Disabled

---

## 5. Managed Node Group Status & Worker Instance Verification

* **Node Group Name:** `diabetes-workers`
* **Node Group ARN:** `arn:aws:eks:ap-south-1:122773994215:nodegroup/diabetes-mlops/diabetes-workers/2cd07bb3-2db2-2d93-7d55-a7bcb941471d`
* **Status:** **`ACTIVE`**
* **Backing Auto Scaling Group:** `eks-diabetes-workers-2cd07bb3-2db2-2d93-7d55-a7bcb941471d`
* **EC2 Instance ID:** `i-08c811812ae808cdc`
* **Instance Type:** `t3.small` (On-Demand, 1 node)
* **Architecture:** `x86_64` (`amd64`)
* **Subnet & Availability Zone:** `subnet-0bb4bd2e43958e6f1` (`ap-south-1a`)
* **Private IP:** `172.31.37.33`
* **Public IP:** `13.126.66.163`
* **Kubernetes Node Name:** `ip-172-31-37-33.ap-south-1.compute.internal`
* **Node Status:** **`Ready`**

### Previous Failure Correction Notice
> The initial nodegroup attempt with `t3.medium` failed with `AsgInstanceLaunchFailures: InvalidParameterCombination - The specified instance type is not eligible for Free Tier`. The operator's missing read permissions (`autoscaling:DescribeAutoScalingGroups`, `iam:ListInstanceProfilesForRole`) were diagnostic blockers, not the cause of the node launch failure. Deleting the failed nodegroup and recreating it with `t3.small` resolved the launch issue cleanly.

---

## 6. System Pod Health & Resource Capacity Verification

### System Pods (`kube-system`)
```
NAME                       READY   STATUS    RESTARTS   AGE     IP              NODE
aws-node-5rpf6             2/2     Running   0          3m45s   172.31.37.33    ip-172-31-37-33.ap-south-1.compute.internal
coredns-645b58c966-8v6gj   1/1     Running   0          73m     172.31.32.159   ip-172-31-37-33.ap-south-1.compute.internal
coredns-645b58c966-lhh7z   1/1     Running   0          73m     172.31.32.172   ip-172-31-37-33.ap-south-1.compute.internal
kube-proxy-rkg5c           1/1     Running   0          3m45s   172.31.37.33    ip-172-31-37-33.ap-south-1.compute.internal
```
* **VPC CNI (`aws-node`):** `2/2 Running` (Healthy)
* **CoreDNS:** `2/2 Running` (Healthy)
* **kube-proxy:** `1/1 Running` (Healthy)

### Node Capacity & Allocatable Verification
* **Allocatable CPU:** `1930m` (~1.93 vCPUs)
* **Allocatable Memory:** `1468148Ki` (~1433 MiB / ~1.43 GiB)
* **Max Pods Capacity:** `11`
* **Current System Allocation:** `350m CPU` (18%), `140Mi Memory` (9%)
* **Remaining Available Capacity:** `1580m CPU`, `1293Mi Memory` (~1.26 GiB)
* **Application Requirement ([`k8s-deploy.yml`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/k8s-deploy.yml)):** `100m CPU`, `128Mi Memory` (Requests) / `250m CPU`, `256Mi Memory` (Limits).
* **Capacity Verdict:** The `t3.small` worker node easily accommodates the application's deployment requests.

---

## 7. Resource Inventory & Official Pricing Summary (`ap-south-1`)

| Component | Resource / Instance Spec | Billable? | Hourly Rate | 4-Hour Lab Cost | 24-Hour Daily Cost |
| :--- | :--- | :--- | :-: | :-: | :-: |
| **EKS Control Plane** | `diabetes-mlops` (v1.36) | **YES** | $0.1000 | $0.4000 | $2.4000 |
| **EC2 Worker Node** | `i-08c811812ae808cdc` (`t3.small`) | **YES** | $0.0224 | $0.0896 | $0.5376 |
| **Root EBS Disk** | `vol-03faa3b80bd036ad5` (20 GB GP3 Encrypted) | **YES** | $0.0025 | $0.0100 | $0.0600 |
| **Public IPv4 Address** | `13.126.66.163` (Associated Public IP) | **YES** | $0.0050 | $0.0200 | $0.1200 |
| **ECR Image Storage** | `diabetes-api` (193.86 MB) | **YES** | < $0.0001 | < $0.0001 | < $0.0001 |
| **IAM & Networking** | Roles, Launch Template, Subnets | No | $0.0000 | $0.0000 | $0.0000 |
| **TOTAL GROSS COST** | — | — | **$0.1299 / hr** | **~$0.5196 USD** | **~$3.1176 USD** |

---

## 8. Exact Resource Cleanup Commands

To terminate all created infrastructure resources and stop billing:

```bash
# 1. Delete Managed Node Group
aws eks delete-nodegroup --cluster-name diabetes-mlops --nodegroup-name diabetes-workers --profile mlops-operator --region ap-south-1
aws eks wait nodegroup-deleted --cluster-name diabetes-mlops --nodegroup-name diabetes-workers --profile mlops-operator --region ap-south-1

# 2. Delete EKS Cluster Control Plane
aws eks delete-cluster --name diabetes-mlops --profile mlops-operator --region ap-south-1
aws eks wait cluster-deleted --name diabetes-mlops --profile mlops-operator --region ap-south-1

# 3. Delete EC2 Launch Template
aws ec2 delete-launch-template --launch-template-id lt-01f2f743e19153364 --profile mlops-operator --region ap-south-1

# 4. Detach Managed Policies and Delete IAM Roles
aws iam detach-role-policy --role-name diabetes-eks-cluster-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy --profile mlops-operator --region ap-south-1
aws iam delete-role --role-name diabetes-eks-cluster-role --profile mlops-operator --region ap-south-1

aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy --profile mlops-operator --region ap-south-1
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly --profile mlops-operator --region ap-south-1
aws iam detach-role-policy --role-name diabetes-eks-node-role --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy --profile mlops-operator --region ap-south-1
aws iam delete-role --role-name diabetes-eks-node-role --profile mlops-operator --region ap-south-1
```

---

## 9. Application Deployment Readiness State

> [!SUCCESS]
> **Deployment Readiness State:** **READY TO DEPLOY**
> The EKS infrastructure control plane and worker node are fully provisioned, active, healthy, and verified. The cluster is ready to deploy the digest-pinned ECR image `122773994215.dkr.ecr.ap-south-1.amazonaws.com/diabetes-api@sha256:5e88ae2f0a3d6a70bc1cb336f240c476e674911dcd2179b168e333ecca99bec8` using [`k8s-deploy.yml`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/k8s-deploy.yml) in Step 8.
