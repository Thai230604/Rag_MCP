# Deploy RAG API to AWS

## 📋 Prerequisites

1. **AWS Account** with ECS, ECR permissions
2. **Qdrant** service deployed (EC2, ECS, or managed)
3. **GitHub Secrets** configured:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

## 🚀 Deploy Steps

### 1. Setup AWS Resources

```bash
# Create ECR repository
aws ecr create-repository \
  --repository-name rag-api \
  --region ap-southeast-1

# Create ECS Cluster
aws ecs create-cluster \
  --cluster-name rag-cluster \
  --region ap-southeast-1

# Create CloudWatch Log Group
aws logs create-log-group \
  --log-group-name /ecs/rag-api \
  --region ap-southeast-1
```

### 2. Update Task Definition

Edit `.aws/task-definition.json`:
- Replace `YOUR_ACCOUNT_ID` with your AWS account ID
- Update `QDRANT_URL` to your Qdrant service endpoint
- Update secrets ARN if needed

### 3. Create ECS Service

```bash
# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://.aws/task-definition.json

# Create service
aws ecs create-service \
  --cluster rag-cluster \
  --service-name rag-api-service \
  --task-definition rag-api-task \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### 4. Configure GitHub Secrets

Go to GitHub repo → Settings → Secrets → Actions:
- Add `AWS_ACCESS_KEY_ID`
- Add `AWS_SECRET_ACCESS_KEY`

### 5. Deploy

```bash
git add .
git commit -m "Deploy RAG API to AWS"
git push origin main
```

## 🧪 Test on Dify

### API Endpoints for Dify:

**Base URL**: `http://your-alb-url.amazonaws.com`

**1. Ingest Documents** (Custom Tool)
```json
POST /api/v1/ingest
{
  "file_paths": ["doc/file1.md", "doc/file2.md"]
}
```

**2. Retrieve Documents** (Knowledge Base)
```json
POST /api/v1/retrieve
{
  "query": "what is RAG?",
  "top_k": 5
}
```

**3. Health Check**
```json
GET /api/v1/health
```

### Add to Dify:

1. **Tools → Custom Tool → HTTP Request**
   - URL: `http://your-alb-url.amazonaws.com/api/v1/retrieve`
   - Method: POST
   - Body: 
     ```json
     {
       "query": "{{query}}",
       "top_k": 5
     }
     ```

2. **Or use as Knowledge Base API**
   - Configure External Knowledge Base
   - API: `/api/v1/retrieve`

## 🔧 Architecture

```
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   Dify      │─────▶│  AWS ALB     │─────▶│   ECS Task   │
│  Platform   │      │              │      │   RAG API    │
└─────────────┘      └──────────────┘      └──────┬───────┘
                                                   │
                                                   ▼
                                            ┌──────────────┐
                                            │   Qdrant     │
                                            │   Service    │
                                            └──────────────┘
```

## 📝 Environment Variables

Update in `.aws/task-definition.json`:
- `QDRANT_URL`: Qdrant service endpoint
- `COLLECTION_NAME`: Vector collection name
- `EMBEDDING_MODEL`: Model for embeddings
- `PORT`: API port (default: 8000)

## 🔍 Monitoring

```bash
# View logs
aws logs tail /ecs/rag-api --follow

# Check service status
aws ecs describe-services \
  --cluster rag-cluster \
  --services rag-api-service
```
