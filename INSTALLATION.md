# PhishGuard - Installation & Deployment Guide

## System Requirements

- Python 3.8 or higher
- pip (Python package manager)
- 100MB disk space
- Modern web browser

## Local Development Setup

### Step 1: Clone Repository
```bash
git clone https://github.com/Varundakh/phishguard.git
cd phishguard
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

### Step 4: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` if needed (defaults are fine for development).

### Step 6: Initialize Database
```bash
python -c "from app.database.database import init_db; init_db()"
```

### Step 7: Run Application
```bash
python run.py
```

Application will start at http://localhost:8000

## Accessing the Application

- **Web Interface**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/api/docs
- **API Docs (ReDoc)**: http://localhost:8000/api/redoc

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
```

### Run with Coverage Report
```bash
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t phishguard:latest .
```

### Run Container
```bash
docker run -p 8000:8000 phishguard:latest
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker Compose
```yaml
version: '3.8'
services:
  web:
    image: phishguard:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/phishguard
      - DEBUG=False
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=phishguard
    volumes:
      - postgres_data:/var/lib/postgresql/data
volumes:
  postgres_data:
```

### Using Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Troubleshooting

### ModuleNotFoundError
```bash
# Ensure you're in virtual environment
# Re-install dependencies
pip install -r requirements.txt
```

### Database Locked (SQLite)
```bash
# Delete and recreate database
rm phishguard.db
python -c "from app.database.database import init_db; init_db()"
```

### Port Already in Use
```bash
# Run on different port
python run.py --port 8001
```

### CORS Issues
Ensure CORS middleware is properly configured in `app/api/middleware.py`

## Performance Optimization

1. **Database**: Use PostgreSQL instead of SQLite
2. **Caching**: Implement Redis caching
3. **Workers**: Use multiple Gunicorn workers
4. **CDN**: Serve static files from CDN
5. **Monitoring**: Implement application monitoring

## Backup and Recovery

### Backup Database
```bash
cp phishguard.db phishguard.db.backup
```

### Backup with PostgreSQL
```bash
pg_dump phishguard > backup.sql
```

## Monitoring

### Check Application Logs
```bash
tail -f logs/phishguard.log
```

### Health Check
```bash
curl http://localhost:8000/api/health
```

## Updates

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Update Application
```bash
git pull origin main
pip install -r requirements.txt
python -c "from app.database.database import init_db; init_db()"
```

---

For more information, see README.md and ARCHITECTURE.md
