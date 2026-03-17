# Production Deployment

This guide covers deploying the ynym Portal Backend to production.

## Prerequisites

- PostgreSQL 12+ running
- Python 3.12+ environment
- Server with Docker support (recommended)

## Environment Configuration

### 1. Set Production Environment Variables

`.env.sample` を `.env` にコピーして本番の値を設定します:

```bash
cp .env.sample .env
```

`.env` の設定例:

```env
# データベース
DB_HOST=db-host
DB_PORT=5432
DB_NAME=ynym_db
DB_USER=ynym_user
DB_PASSWORD=<strong-password>

# JWT
JWT_SECRET_KEY=<strong-random-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# Google認証
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>

# URL設定
FRONTEND_URL=https://your-frontend-domain.com
BACKEND_URL=https://api.your-domain.com

# CORS設定 (カンマ区切りで複数指定可能)
ALLOWED_ORIGINS=https://your-frontend-domain.com

# 環境
ENVIRONMENT=production
LOG_LEVEL=INFO
```

**Important**: Generate a strong secret key for JWT:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Deployment Methods

### Option 1: Docker (Recommended)

プロジェクトルートの `Dockerfile` を使用してビルド・起動します:

```bash
docker build -t ynym-portal-backend .
docker run -p 80:80 --env-file .env ynym-portal-backend
```

`compose.yml` を使用する場合:

```bash
docker compose up -d
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
