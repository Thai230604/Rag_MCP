# Cấu hình GitHub Secrets

## Bước 1: Tạo AWS IAM User

1. Truy cập **AWS Console** → **IAM** → **Users** → **Create user**
2. Tên user: `github-actions-deployer`
3. **Attach policies directly**:
   - `AmazonEC2ContainerRegistryFullAccess`
   - `AmazonECS_FullAccess`
   - `AmazonECSTaskExecutionRolePolicy`
   - Hoặc tạo custom policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecr:GetAuthorizationToken",
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload",
        "ecs:UpdateService",
        "ecs:DescribeServices",
        "ecs:DescribeTaskDefinition",
        "ecs:RegisterTaskDefinition"
      ],
      "Resource": "*"
    }
  ]
}
```

4. **Create access key**:
   - Chọn **Command Line Interface (CLI)**
   - Copy `Access Key ID` và `Secret Access Key`

## Bước 2: Thêm Secrets vào GitHub

### Cách 1: Qua GitHub Web UI

1. Vào repository trên GitHub
2. Click **Settings** (tab phía trên)
3. Sidebar trái: **Secrets and variables** → **Actions**
4. Click **New repository secret**
5. Thêm các secrets:

| Name | Value | Mô tả |
|------|-------|-------|
| `AWS_ACCESS_KEY_ID` | `AKIA...` | Access Key từ IAM user |
| `AWS_SECRET_ACCESS_KEY` | `wJalr...` | Secret Key từ IAM user |

### Cách 2: Qua GitHub CLI

```bash
# Cài đặt GitHub CLI
winget install --id GitHub.cli

# Login
gh auth login

# Thêm secrets
gh secret set AWS_ACCESS_KEY_ID
# Paste access key và Enter

gh secret set AWS_SECRET_ACCESS_KEY
# Paste secret key và Enter

# Verify
gh secret list
```

## Bước 3: Verify Secrets

```bash
# List all secrets (không hiển thị giá trị)
gh secret list

# Output:
# AWS_ACCESS_KEY_ID      Updated 2026-01-11
# AWS_SECRET_ACCESS_KEY  Updated 2026-01-11
```

## Bước 4: Test GitHub Actions

1. Commit code:
```bash
git add .
git commit -m "Add CI/CD for AWS deployment"
git push origin main
```

2. Kiểm tra workflow:
   - Vào tab **Actions** trên GitHub
   - Xem logs của workflow đang chạy

## ⚠️ Security Best Practices

1. **Không commit secrets** vào code
2. **Rotate keys định kỳ** (3-6 tháng)
3. **Principle of Least Privilege**: chỉ cấp quyền cần thiết
4. **Enable MFA** cho AWS account
5. **Monitor CloudTrail** logs

## 🔧 Troubleshooting

### Lỗi: "Error: Cannot find AWS credentials"
→ Kiểm tra secrets đã được add chưa: `gh secret list`

### Lỗi: "Access Denied" khi push image to ECR
→ Kiểm tra IAM policy có `ecr:PutImage` permission

### Lỗi: "Task definition not found"
→ Cần register task definition trước (xem DEPLOY.md)

## 📚 Thêm Secrets khác (Optional)

Nếu cần secrets cho Qdrant, OpenAI, etc:

```bash
# Qdrant credentials
gh secret set QDRANT_URL
gh secret set QDRANT_API_KEY

# OpenAI API Key
gh secret set OPENAI_API_KEY

# Environment variables
gh secret set COLLECTION_NAME
```

Sau đó update workflow `.github/workflows/deploy.yml` để sử dụng secrets này.
