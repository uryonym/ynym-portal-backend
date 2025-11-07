# Production Deployment

This guide covers deploying the ynym Portal Backend to production.

## Prerequisites

- PostgreSQL 12+ running
- Python 3.12+ environment
- Server with Docker support (recommended)

## Environment Configuration

### 1. Set Production Environment Variables

Create `.env` file with production values:

```env
ENVIRONMENT=production
LOG_LEVEL=INFO
DATABASE_URL=postgresql+asyncpg://user:password@db-host:5432/ynym_db
JWT_SECRET_KEY=<strong-random-secret-key>
JWT_EXPIRATION_HOURS=24
```

**Important**: Generate a strong secret key for JWT:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Deployment Methods

### Option 1: Docker (Recommended)

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN pip install uv && uv sync --no-dev

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t ynym-portal-backend .
docker run -p 8000:8000 --env-file .env ynym-portal-backend
```

### Option 2: Direct Server Deployment

```bash
# Install dependencies
uv sync --no-dev

# Run with production ASGI server (gunicorn + uvicorn)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Database Setup

```bash
# Create database
createdb ynym_db

# Set up database user
createuser ynym_user
ALTER USER ynym_user WITH PASSWORD 'strong-password';
GRANT ALL PRIVILEGES ON DATABASE ynym_db TO ynym_user;
```

## Reverse Proxy Configuration

### Nginx Example

```nginx
upstream ynym_backend {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://ynym_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL/TLS Configuration

Use Let's Encrypt with Certbot:

```bash
sudo certbot certonly --standalone -d api.example.com
```

Update Nginx configuration to use SSL certificates.

## Monitoring

### Health Check

```bash
curl http://localhost:8000/health
```

### Logging

Configure centralized logging for production (e.g., ELK Stack, Datadog, New Relic).

## Scaling

- Use multiple worker processes: `-w 4` with gunicorn
- Deploy behind load balancer for horizontal scaling
- Use connection pooling for database
- Consider caching layer (Redis)

## Security Considerations

1. **HTTPS Only**: Always use HTTPS in production
2. **CORS**: Configure CORS appropriately
3. **Rate Limiting**: Implement rate limiting for API endpoints
4. **Input Validation**: Validate all user inputs (already handled by Pydantic)
5. **Dependencies**: Keep dependencies updated
6. **Secrets**: Never commit `.env` file, use environment variables
7. **Database**: Use strong passwords, limit database user permissions

## Maintenance

### Updates

```bash
git pull
uv sync
# Restart application
```

### Backups

Set up regular PostgreSQL backups:

```bash
# Daily backup
pg_dump ynym_db > backup_$(date +%Y%m%d).sql
```

### Monitoring and Alerting

Set up monitoring for:

- Application uptime
- Database performance
- Error rates
- Response times
- Resource utilization
