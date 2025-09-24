# NeuroQ Deployment Guide

This guide covers how to deploy the NeuroQ platform using Docker and various cloud providers.

## Prerequisites

- Docker and Docker Compose installed
- Git installed
- Basic knowledge of command line operations

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd NeuroQ
```

### 2. Environment Configuration

Create environment files for both frontend and backend:

#### Backend Environment (.env)
```bash
cp backend/env.example backend/.env
```

Edit `backend/.env` with your configuration:
```env
DATABASE_URL=postgresql://neuroq_user:neuroq_password@localhost:5432/neuroq_db
SECRET_KEY=your-super-secret-key-here
OPENAI_API_KEY=your-openai-api-key-here
REDIS_URL=redis://localhost:6379
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

#### Frontend Environment
Create `frontend/.env`:
```env
REACT_APP_API_URL=http://localhost:8000
```

### 3. Start the Application

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 4. Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Production Deployment

### Using Docker Compose

1. **Update Environment Variables**
   ```bash
   # Set production values
   export SECRET_KEY="your-production-secret-key"
   export DATABASE_URL="postgresql://user:password@db:5432/neuroq_prod"
   export DEBUG=False
   ```

2. **Deploy with Docker Compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Using Kubernetes

1. **Create Kubernetes Manifests**
   ```bash
   kubectl apply -f k8s/
   ```

2. **Expose Services**
   ```bash
   kubectl expose deployment neuroq-frontend --type=LoadBalancer --port=80
   kubectl expose deployment neuroq-backend --type=LoadBalancer --port=8000
   ```

### Cloud Provider Deployments

#### Heroku

1. **Install Heroku CLI**
2. **Create Heroku Apps**
   ```bash
   # Backend
   heroku create neuroq-backend
   heroku addons:create heroku-postgresql:hobby-dev
   heroku addons:create heroku-redis:hobby-dev
   
   # Frontend
   heroku create neuroq-frontend
   ```

3. **Deploy**
   ```bash
   # Backend
   cd backend
   git subtree push --prefix=backend heroku main
   
   # Frontend
   cd frontend
   git subtree push --prefix=frontend heroku main
   ```

#### AWS ECS

1. **Build and Push Images**
   ```bash
   # Build images
   docker build -t neuroq-backend ./backend
   docker build -t neuroq-frontend ./frontend
   
   # Tag for ECR
   docker tag neuroq-backend:latest <account>.dkr.ecr.<region>.amazonaws.com/neuroq-backend:latest
   docker tag neuroq-frontend:latest <account>.dkr.ecr.<region>.amazonaws.com/neuroq-frontend:latest
   
   # Push to ECR
   docker push <account>.dkr.ecr.<region>.amazonaws.com/neuroq-backend:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/neuroq-frontend:latest
   ```

2. **Create ECS Task Definitions**
3. **Deploy Services**

#### Google Cloud Run

1. **Build and Push Images**
   ```bash
   # Backend
   gcloud builds submit --tag gcr.io/PROJECT_ID/neuroq-backend ./backend
   
   # Frontend
   gcloud builds submit --tag gcr.io/PROJECT_ID/neuroq-frontend ./frontend
   ```

2. **Deploy Services**
   ```bash
   gcloud run deploy neuroq-backend --image gcr.io/PROJECT_ID/neuroq-backend
   gcloud run deploy neuroq-frontend --image gcr.io/PROJECT_ID/neuroq-frontend
   ```

## Environment Variables

### Backend (.env)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `SECRET_KEY` | JWT secret key | - | Yes |
| `OPENAI_API_KEY` | OpenAI API key for AI features | - | No |
| `REDIS_URL` | Redis connection string | redis://localhost:6379 | No |
| `DEBUG` | Debug mode | False | No |
| `HOST` | Server host | 0.0.0.0 | No |
| `PORT` | Server port | 8000 | No |
| `CORS_ORIGINS` | Allowed CORS origins | - | Yes |

### Frontend (.env)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `REACT_APP_API_URL` | Backend API URL | http://localhost:8000 | Yes |

## Database Migrations

### Using Alembic

```bash
# Create migration
cd backend
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

### Manual Database Setup

```bash
# Connect to database
psql -h localhost -U neuroq_user -d neuroq_db

# Run initialization script
\i database/init.sql
```

## Monitoring and Logging

### Health Checks

- Backend: `GET /health`
- Frontend: `GET /` (returns 200)

### Logging

```bash
# View application logs
docker-compose logs -f backend
docker-compose logs -f frontend

# View specific service logs
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Monitoring Setup

1. **Prometheus + Grafana**
   ```yaml
   # Add to docker-compose.yml
   prometheus:
     image: prom/prometheus
     ports:
       - "9090:9090"
   
   grafana:
     image: grafana/grafana
     ports:
       - "3001:3000"
   ```

2. **Application Metrics**
   - Custom metrics endpoint: `/metrics`
   - Health check endpoint: `/health`

## Security Considerations

### Production Security

1. **Environment Variables**
   - Use strong, unique secret keys
   - Rotate keys regularly
   - Never commit secrets to version control

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

3. **Network Security**
   - Use HTTPS in production
   - Configure proper CORS settings
   - Implement rate limiting

4. **Application Security**
   - Regular dependency updates
   - Input validation and sanitization
   - Proper error handling

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose ps postgres
   
   # Check logs
   docker-compose logs postgres
   ```

2. **Port Conflicts**
   ```bash
   # Check port usage
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8000
   ```

3. **Memory Issues**
   ```bash
   # Check resource usage
   docker stats
   ```

### Performance Optimization

1. **Database Optimization**
   - Add appropriate indexes
   - Regular VACUUM and ANALYZE
   - Connection pooling

2. **Application Optimization**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement caching strategies

## Backup and Recovery

### Database Backup

```bash
# Create backup
docker-compose exec postgres pg_dump -U neuroq_user neuroq_db > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U neuroq_user neuroq_db < backup.sql
```

### Application Backup

```bash
# Backup volumes
docker run --rm -v neuroq_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

## Scaling

### Horizontal Scaling

1. **Load Balancer Configuration**
2. **Database Read Replicas**
3. **Redis Cluster Setup**
4. **CDN Integration**

### Vertical Scaling

1. **Resource Allocation**
2. **Database Tuning**
3. **Caching Strategies**

## Support

For deployment issues or questions:

1. Check the logs: `docker-compose logs`
2. Review this documentation
3. Check GitHub issues
4. Contact the development team
