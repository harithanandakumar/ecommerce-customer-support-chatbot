# Deployment Guide

## Overview

Complete guide for deploying the e-commerce customer support chatbot to production environments using Docker, Kubernetes, and cloud platforms.

## System Requirements

### Hardware Specifications

**Minimum Requirements**:
- CPU: 2 cores @ 2.0 GHz
- RAM: 4 GB
- Disk: 20 GB SSD
- Network: 100 Mbps connectivity

**Recommended Production**:
- CPU: 4 cores @ 2.5 GHz
- RAM: 8 GB
- Disk: 100 GB SSD
- Network: 1 Gbps connectivity

### Software Dependencies

- Python 3.9+
- Docker 20.10+
- Docker Compose 1.29+
- PostgreSQL 13+
- Redis 6.0+
- Kubernetes 1.20+ (for K8s deployments)

## Local Development Deployment

### Using Docker Compose

```bash
# Clone repository
git clone https://github.com/harithanandakumar/ecommerce-customer-support-chatbot.git
cd ecommerce-customer-support-chatbot

# Copy environment configuration
cp .env.example .env

# Edit configuration
vim .env

# Build and start services
docker-compose up -d

# Verify services
docker-compose ps

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Docker Compose Services

```yaml
services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/chatbot
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      - POSTGRES_USER=chatbot_user
      - POSTGRES_PASSWORD=secure_password
      - POSTGRES_DB=chatbot_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Production Deployment

### Multi-Stage Docker Build

```dockerfile
# Stage 1: Builder
FROM python:3.9-slim as builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-slim
WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "app:app"]
```

### Kubernetes Deployment

**Deployment YAML**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: chatbot-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: chatbot
  template:
    metadata:
      labels:
        app: chatbot
    spec:
      containers:
      - name: chatbot
        image: chatbot:latest
        ports:
        - containerPort: 5000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: redis-config
              key: url
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: chatbot-service
spec:
  selector:
    app: chatbot
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
```

**Deployment Steps**:
```bash
# Create namespace
kubectl create namespace chatbot

# Create secrets
kubectl create secret generic db-secret \
  --from-literal=url='postgresql://user:pass@db:5432/chatbot' \
  -n chatbot

# Create config maps
kubectl create configmap redis-config \
  --from-literal=url='redis://redis:6379/0' \
  -n chatbot

# Deploy application
kubectl apply -f deployment.yaml -n chatbot

# Check deployment status
kubectl get deployments -n chatbot
kubectl get pods -n chatbot

# View logs
kubectl logs -f deployment/chatbot-app -n chatbot

# Scale replicas
kubectl scale deployment/chatbot-app --replicas=5 -n chatbot
```

## Cloud Platform Deployments

### AWS Deployment

**Using ECS**:
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name chatbot-cluster

# Register task definition
aws ecs register-task-definition \
  --cli-input-json file://task-definition.json

# Create service
aws ecs create-service \
  --cluster chatbot-cluster \
  --service-name chatbot-service \
  --task-definition chatbot:1 \
  --desired-count 3
```

### GCP Deployment

**Using Cloud Run**:
```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT_ID/chatbot

# Deploy to Cloud Run
gcloud run deploy chatbot \
  --image gcr.io/PROJECT_ID/chatbot \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 1 \
  --allow-unauthenticated
```

### Azure Deployment

**Using App Service**:
```bash
# Create resource group
az group create --name chatbot-rg --location eastus

# Create app service plan
az appservice plan create \
  --name chatbot-plan \
  --resource-group chatbot-rg \
  --sku B2 --is-linux

# Create web app
az webapp create \
  --resource-group chatbot-rg \
  --plan chatbot-plan \
  --name chatbot-app \
  --deployment-container-image-name chatbot:latest
```

## Database Initialization

### PostgreSQL Setup

```bash
# Connect to database
psql -h localhost -U chatbot_user -d chatbot_db

# Run migrations
python scripts/migrate_database.py

# Seed initial data
python scripts/seed_data.py

# Verify tables
\dt
```

## Configuration Management

### Environment Variables

```bash
# Core Configuration
FLASK_ENV=production
FLASK_DEBUG=0
LOG_LEVEL=INFO

# Database
DATABASE_URL=postgresql://user:pass@host:5432/chatbot_db
DATABASE_POOL_SIZE=20

# Redis
REDIS_URL=redis://host:6379/0
REDIS_CLUSTER_ENABLED=true

# Security
SECRET_KEY=your-secure-key-here
JWT_SECRET=your-jwt-secret
SSL_CERT_PATH=/path/to/cert.pem
SSL_KEY_PATH=/path/to/key.pem

# Application
WORKERS=4
THREADS=2
TIMEOUT=120
```

## Monitoring & Health Checks

### Health Endpoint

```bash
curl http://localhost:5000/health

# Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime_seconds": 3600,
  "database": "connected",
  "cache": "connected",
  "timestamp": "2026-01-15T10:30:00Z"
}
```

### Metrics Endpoint

```bash
curl http://localhost:5000/metrics

# Prometheus format metrics available
```

## SSL/TLS Configuration

### Self-Signed Certificate

```bash
# Generate certificate
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Configure in application
SSL_CERT_PATH=/etc/ssl/certs/cert.pem
SSL_KEY_PATH=/etc/ssl/private/key.pem
```

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot certonly --standalone -d chatbot.example.com

# Configure auto-renewal
sudo systemctl enable certbot.timer
```

## Backup & Recovery

### Database Backup

```bash
# Full backup
pg_dump -h localhost -U chatbot_user chatbot_db > backup.sql

# Compressed backup
pg_dump -h localhost -U chatbot_user chatbot_db | gzip > backup.sql.gz

# Restore from backup
psql -h localhost -U chatbot_user chatbot_db < backup.sql
```

### Automated Backups

```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/chatbot"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -h $DB_HOST -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://chatbot-backups/

# Keep last 30 days
find $BACKUP_DIR -mtime +30 -delete
```

## Rolling Deployments

### Blue-Green Deployment

```bash
# Deploy new version (green)
kubectl apply -f deployment-v2.yaml

# Verify new version works
kubectl port-forward svc/chatbot-green 5000:5000
curl localhost:5000/health

# Switch traffic to new version
kubectl patch service chatbot-service -p '{"spec":{"selector":{"version":"v2"}}}'

# Keep old version (blue) running for rollback
```

## Troubleshooting

### Common Deployment Issues

**Issue: Pod CrashLoopBackOff**
```bash
kubectl logs POD_NAME -n chatbot
kubectl describe pod POD_NAME -n chatbot
```

**Issue: Service unreachable**
```bash
kubectl get endpoints -n chatbot
kubectl get ingress -n chatbot
```

**Issue: Database connection failed**
```bash
# Check database service
kubectl get svc -n chatbot
# Verify credentials
kubectl get secrets -n chatbot
```

## Related Documentation

- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Operational troubleshooting
- [PERFORMANCE_OPTIMIZATION.md](PERFORMANCE_OPTIMIZATION.md) - Performance tuning
- [ADVANCED_CACHING_GUIDE.md](ADVANCED_CACHING_GUIDE.md) - Caching strategy
