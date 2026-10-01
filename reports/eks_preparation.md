# ☸️ Amazon EKS Deployment Preparation & Governance Review (Validated)

## 1. IAM Access Analyzer Policy Validation Results

* **Policy File:** [`policies/diabetes-provisioner-policy.json`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/policies/diabetes-provisioner-policy.json)
* **Validation Command Executed:**
  ```bash
  aws accessanalyzer validate-policy \
    --policy-document file://policies/diabetes-provisioner-policy.json \
    --policy-type IDENTITY_POLICY \
    --profile mlops \
    --region ap-south-1
  ```
* **Validation Findings Output:**
  ```json
  {
      "findings": []
  }
  ```
* **Validation Summary:** **0 Errors, 0 Warnings, 0 Security Notices**. The policy document is 100% syntactically and semantically valid under AWS IAM Authorization standards.

---

## 2. Policy Refinements & Governance Improvements

1. **Invalid Action Removed:** Removed invalid string `iam:SignInLocalDevelopmentAccess` and `sts:GetServiceBearerToken` from custom policy JSON.
2. **Managed Policy Decoupling:** Documented that AWS-managed policy `arn:aws:iam::aws:policy/SignInLocalDevelopmentAccess` must be attached separately to user `diabetes-operator`.
3. **Strict Policy Attachment Restrictions:** `iam:AttachRolePolicy` and `iam:DetachRolePolicy` are strictly conditioned on:
   * `arn:aws:iam::aws:policy/AmazonEKSClusterPolicy`
   * `arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy`
   * `arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly`
   * `arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy`
4. **Strict `iam:PassRole` Scoping:** Restricted `iam:PassRole` exclusively to `diabetes-eks-cluster-role` and `diabetes-eks-node-role` passed to `eks.amazonaws.com` and `ec2.amazonaws.com`.
5. **EKS Actions Expanded:** Added explicit coverage for `eks:TagResource`, `eks:UntagResource`, `eks:ListTagsForResource`, `eks:ListAccessEntries`, and `eks:ListAssociatedAccessPolicies`.

---

## 3. Exact Console Setup & Authentication Guide for Operator (`diabetes-operator`)

### Step 1: Create IAM User in AWS Console
1. Log into AWS Console as root user for account `122773994215` (`https://122773994215.signin.aws.amazon.com/console`).
2. Navigate to **IAM Console** $\rightarrow$ **Users** $\rightarrow$ **Create user**.
3. Set **User name:** `diabetes-operator`.
4. Check **Provide user access to the AWS Management Console - optional**.
5. Select **I want to create an IAM user**. Set initial password.
6. Do **NOT** generate long-term Access Keys or Secret Keys.

### Step 2: Attach Policies
1. Under Permissions, select **Attach policies directly**.
2. Click **Create policy**, paste contents of [`policies/diabetes-provisioner-policy.json`](file:///Users/sithumuthsara/On%20My%20Mac%20Documents/Development/diabetes-prediction-mlops/policies/diabetes-provisioner-policy.json), and name it `DiabetesProvisionerPolicy`. Attach it to `diabetes-operator`.
3. Search for and attach AWS-managed policy: `arn:aws:iam::aws:policy/SignInLocalDevelopmentAccess`.

### Step 3: Password Change & Separate MFA Enrollment
* *Important:* Requiring a password change on initial login does **not** automatically enroll or enforce MFA.
* Open an incognito browser window, navigate to `https://122773994215.signin.aws.amazon.com/console`, and log in as `diabetes-operator`. Change password.
* Navigate to **IAM Console** $\rightarrow$ **Users** $\rightarrow$ `diabetes-operator` $\rightarrow$ **Security credentials** tab.
* Under **Multi-factor authentication (MFA)**, click **Assign MFA device** and complete authenticator app registration.

### Step 4: CLI Login (`aws login`)
With the browser session active as `diabetes-operator`, configure local profile in `~/.aws/config`:
```ini
[profile mlops-operator]
region = ap-south-1
output = json
```
Run in terminal:
```bash
aws login --profile mlops-operator
```

### Step 5: Verify Identity with STS
Verify identity in terminal:
```bash
aws sts get-caller-identity --profile mlops-operator --region ap-south-1
```
Expected Output:
```json
{
    "UserId": "AIDAZFPGPLTT...",
    "Account": "122773994215",
    "Arn": "arn:aws:iam::122773994215:user/diabetes-operator"
}
```

---

## 4. Official Sourced Pricing (Mumbai `ap-south-1`)

Sourced directly from official AWS Price List API (`us-east-1` endpoint, Location: `Asia Pacific (Mumbai)`) on `2026-10-01`:

* **EKS Control Plane:** $0.1000 / hour ($0.4000 / 4-hr lab, $2.4000 / 24-hr run)
* **Linux On-Demand `t3.medium`:** $0.0448 / hour ($0.1792 / 4-hr lab, $1.0752 / 24-hr run)
* **20 GB GP3 EBS Disk:** $0.0912 / GB-month ($0.0100 / 4-hr lab, $0.0600 / 24-hr run)
* **Public IPv4 Address:** $0.0050 / hour ($0.0200 / 4-hr lab, $0.1200 / 24-hr run)
* **ECR Storage (193.86 MB):** $0.1000 / GB-month (< $0.0001)
* **TOTAL VERIFIED GROSS COST:** **~$0.6093 USD** (4-Hour Lab) | **~$3.6553 USD** (24-Hour Run)
