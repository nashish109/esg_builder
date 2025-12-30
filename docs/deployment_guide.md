# ESG Builder FastAPI Backend Deployment Guide

This guide provides detailed step-by-step instructions for deploying the ESG Builder FastAPI backend. It covers Docker containerization (primary method), local development alternatives, and cloud deployment options.

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Git (for version control)
- For cloud deployment: AWS CLI, Heroku CLI, or respective cloud accounts

## 1. Docker Containerization (Primary Method)

### 1.1 Build and Run with Docker Compose

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd esg_builder
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

3. **Build and run the application**:
   ```bash
   # Build the Docker image
   docker-compose build

   # Start the services
   docker-compose up -d
   ```

4. **Verify deployment**:
   ```bash
   curl http://localhost:8000/health
   # Should return: {"status": "healthy"}
   ```

### 1.2 Docker Commands for Different Platforms

#### Windows (Command Prompt/WSL):
```cmd
# Build
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

#### Linux:
```bash
# Build
sudo docker-compose build

# Run in background
sudo docker-compose up -d

# View logs
sudo docker-compose logs -f backend

# Stop
sudo docker-compose down
```

### 1.3 Manual Docker Commands (Alternative)

If you prefer not to use docker-compose:

```bash
# Build image
docker build -t esg-builder-backend .

# Run container
docker run -p 8000:8000 --env-file .env -v $(pwd)/esg_builder.db:/app/esg_builder.db -v $(pwd)/data:/app/data esg-builder-backend
```

## 2. Local Development Deployment

### 2.1 Basic Local Run (Development)

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env

# Run the application
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2.2 Production-Ready Local Deployment with Process Managers

#### Using Gunicorn (Python WSGI server)

1. **Install Gunicorn**:
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn** (multiple workers for concurrency):
   ```bash
   gunicorn backend.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

#### Using systemd (Linux only)

1. **Create systemd service file** (`/etc/systemd/system/esg-builder.service`):
   ```ini
   [Unit]
   Description=ESG Builder FastAPI Backend
   After=network.target

   [Service]
   User=your-user
   WorkingDirectory=/path/to/esg_builder
   Environment=PATH=/path/to/venv/bin
   ExecStart=/path/to/venv/bin/gunicorn backend.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable esg-builder
   sudo systemctl start esg-builder
   sudo systemctl status esg-builder
   ```

## 3. Cloud Deployment

### 3.1 Heroku Deployment

1. **Install Heroku CLI and login**:
   ```bash
   # Install CLI from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create Heroku app**:
   ```bash
   heroku create esg-builder-backend
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set NEWS_API_KEY=your_key_here
   heroku config:set SQLALCHEMY_DATABASE_URL=sqlite:///./esg_builder.db
   ```

4. **Deploy**:
   ```bash
   # Push to Heroku
   git push heroku main

   # Or if using different branch
   git push heroku your-branch:main
   ```

5. **View logs**:
   ```bash
   heroku logs --tail -a esg-builder-backend
   ```

6. **Access the app**:
   ```bash
   heroku open -a esg-builder-backend
   ```

**Note**: For Heroku, you may need a `Procfile`:
```
web: gunicorn backend.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

### 3.2 AWS ECS Deployment

1. **Prerequisites**:
   - AWS CLI configured
   - Docker installed locally
   - ECR repository created

2. **Build and push Docker image to ECR**:
   ```bash
   # Authenticate Docker with ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin your-account-id.dkr.ecr.us-east-1.amazonaws.com

   # Build image
   docker build -t esg-builder-backend .

   # Tag for ECR
   docker tag esg-builder-backend:latest your-account-id.dkr.ecr.us-east-1.amazonaws.com/esg-builder-backend:latest

   # Push to ECR
   docker push your-account-id.dkr.ecr.us-east-1.amazonaws.com/esg-builder-backend:latest
   ```

3. **Create ECS Cluster and Service**:
   - Go to AWS ECS Console
   - Create cluster (EC2 or Fargate)
   - Create task definition with the ECR image
   - Create service with load balancer

4. **Set environment variables in task definition**:
   ```json
   {
     "name": "NEWS_API_KEY",
     "value": "your_key_here"
   }
   ```

5. **Configure security groups and ALB** for port 8000.

## 4. Database Configuration

### 4.1 SQLite (Default)

- Database file: `esg_builder.db`
- Automatically created if it doesn't exist
- Suitable for development and small-scale production

### 4.2 PostgreSQL Setup

1. **Update docker-compose.yml** for PostgreSQL:
   ```yaml
   services:
     backend:
       # ... existing config
       depends_on:
         - postgres

     postgres:
       image: postgres:13
       environment:
         POSTGRES_DB: esg_db
         POSTGRES_USER: user
         POSTGRES_PASSWORD: password
       volumes:
         - postgres_data:/var/lib/postgresql/data
       ports:
         - "5432:5432"

   volumes:
     postgres_data:
   ```

2. **Set environment variables** in `.env`:
   ```env
   SQLALCHEMY_DATABASE_URL=postgresql://user:password@postgres:5432/esg_db
   ```

3. **Run migrations** if needed:
   ```bash
   # Inside container or locally
   python -c "from database.create_tables import create_all_tables; create_all_tables()"
   ```

## 5. Monitoring and Logging

### 5.1 Basic Logging

The application uses Python's built-in logging. To configure:

1. **Add logging configuration** in `config/settings.py`:
   ```python
   import logging

   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

2. **For production, use structured logging**:
   ```python
   import structlog

   # Configure structured logging
   structlog.configure(
       processors=[
           structlog.stdlib.filter_by_level,
           structlog.stdlib.add_logger_name,
           structlog.stdlib.add_log_level,
           structlog.stdlib.PositionalArgumentsFormatter(),
           structlog.processors.TimeStamper(fmt="iso"),
           structlog.processors.StackInfoRenderer(),
           structlog.processors.format_exc_info,
           structlog.processors.UnicodeDecoder(),
           structlog.processors.JSONRenderer()
       ],
       context_class=dict,
       logger_factory=structlog.stdlib.LoggerFactory(),
       wrapper_class=structlog.stdlib.BoundLogger,
       cache_logger_on_first_use=True,
   )
   ```

### 5.2 Health Checks and Monitoring

1. **Health endpoint** is available at `/health`

2. **Add Prometheus metrics** (optional):
   - Install: `pip install prometheus-client`
   - Add metrics in your FastAPI app:
     ```python
     from prometheus_client import make_asgi_app, Counter, Histogram
     from fastapi import FastAPI

     REQUEST_COUNT = Counter('request_count', 'Request count', ['method', 'endpoint'])
     REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

     app = FastAPI()
     app.mount("/metrics", make_asgi_app())
     ```

3. **Use tools like Grafana + Prometheus** for dashboard monitoring.

## 6. Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Find process using port 8000
   netstat -tulpn | grep :8000
   # Kill the process or change port
   ```

2. **Database connection errors**:
   - Check `.env` file
   - Ensure database is running (if PostgreSQL)
   - Check file permissions for SQLite

3. **Import errors**:
   - Ensure all dependencies are installed
   - Check Python path: `PYTHONPATH=/app`

4. **Docker build failures**:
   - Clear Docker cache: `docker system prune`
   - Check Dockerfile syntax

### Logs

- **Docker logs**: `docker-compose logs -f backend`
- **Application logs**: Check console output or configure file logging
- **Cloud logs**: Use respective cloud logging services (CloudWatch for AWS, Heroku logs)

## 7. Security Considerations

1. **Environment Variables**: Never commit `.env` files to version control
2. **CORS**: Configure allowed origins in production
3. **Secrets Management**: Use cloud secret managers (AWS Secrets Manager, etc.)
4. **HTTPS**: Enable SSL/TLS in production
5. **Firewall**: Restrict access to necessary ports only
6. **Updates**: Regularly update dependencies and base images

## 8. Performance Optimization

1. **Use Gunicorn with multiple workers** in production
2. **Enable gzip compression** in FastAPI
3. **Database indexing** for better query performance
4. **Caching** with Redis if needed
5. **Container optimization**: Use multi-stage builds for smaller images

This guide covers the essential deployment aspects for the ESG Builder backend. For more advanced configurations, refer to the official documentation of the respective tools and platforms.