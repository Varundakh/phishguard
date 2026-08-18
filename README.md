# PhishGuard - Main README
# Complete project documentation

# PhishGuard 🛡️ - Intelligent Phishing URL & Website Risk Analyzer

**PhishGuard** is a production-style cybersecurity application that analyzes URLs and estimates their phishing risk level using rule-based detection and optional machine learning classification.

## 🎯 Features

### Core Functionality
- **URL Analysis Engine**: Extract and analyze 15+ security features from URLs
- **Risk Scoring**: Transparent 0-100 risk score with explainable indicators
- **Real-time Detection**: Rule-based detection of phishing characteristics
- **Scan History**: SQLite database stores all scans for historical analysis
- **RESTful API**: Clean FastAPI endpoints for programmatic access
- **Professional Dashboard**: Dark-themed cybersecurity interface

### Security Features Analyzed
- IP address usage vs. domain names
- HTTPS/HTTP protocol detection
- Suspicious keyword detection (login, verify, confirm, etc.)
- Excessive subdomains and URL structure analysis
- Punycode/IDN domain detection
- URL shortener detection
- Suspicious query parameters
- Special character analysis
- URL length analysis
- And more...

### Web Interface
- **Analyzer**: Real-time URL analysis with instant feedback
- **Dashboard**: Statistics and risk distribution charts
- **History**: Search, filter, and manage scan history
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

```
phishguard/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # API endpoint definitions
│   │   └── middleware.py       # Security and logging middleware
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration and constants
│   │   └── logging_config.py   # Logging setup
│   ├── database/
│   │   ├── __init__.py
│   │   └── database.py         # SQLAlchemy setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── models.py           # Database ORM models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── schemas.py          # Pydantic validation schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── analyzer.py         # Main URL analysis service
│   │   ├── scoring_engine.py   # Risk scoring logic
│   │   ├── statistics.py       # Statistics generation
│   │   └── database.py         # Database operations
│   └── utils/
│       ├── __init__.py
│       ├── url_parser.py       # URL parsing utilities
│       └── feature_extractor.py # Feature extraction
├── frontend/
│   ├── index.html              # Main analyzer page
│   ├── dashboard.html          # Statistics dashboard
│   ├── history.html            # Scan history page
│   ├── css/
│   │   └── style.css           # Complete stylesheet
│   └── js/
│       ├── app.js              # Analyzer functionality
│       ├── dashboard.js        # Dashboard logic
│       └── history.js          # History management
├── tests/
│   ├── __init__.py
│   └── test_api.py             # Comprehensive test suite
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── run.py                      # Application entry point
├── ARCHITECTURE.md             # Detailed architecture diagrams
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Varundakh/phishguard.git
   cd phishguard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create .env file**
   ```bash
   cp .env.example .env
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Web Interface: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs
   - ReDoc: http://localhost:8000/api/redoc

## 📡 API Documentation

### Endpoints

#### Analyze URL
```http
POST /api/analyze
Content-Type: application/json

{
    "url": "https://example.com/login"
}
```

**Response (200 OK):**
```json
{
    "scan_id": "550e8400-e29b-41d4-a716-446655440000",
    "url": "https://example.com/login",
    "risk_score": 42,
    "risk_level": "MODERATE",
    "indicators": [
        "Missing security headers",
        "Long URL length"
    ],
    "scoring_breakdown": [
        {
            "feature": "Missing HTTPS",
            "weight": 18,
            "reason": "Unencrypted connection - credentials could be intercepted"
        }
    ],
    "recommendations": "Verify domain independently before entering credentials",
    "technical_details": {
        "url_length": 35,
        "domain": "example.com",
        "uses_https": true
    },
    "timestamp": "2024-01-15T10:30:00"
}
```

#### Get Scan History
```http
GET /api/scans?skip=0&limit=50&risk_level=HIGH
```

#### Get Specific Scan
```http
GET /api/scans/{scan_id}
```

#### Delete Scan
```http
DELETE /api/scans/{scan_id}
```

#### Get Statistics
```http
GET /api/statistics
```

**Response:**
```json
{
    "total_scans": 100,
    "safe_scans": 45,
    "moderate_scans": 30,
    "suspicious_scans": 15,
    "high_risk_scans": 10,
    "average_risk_score": 38.5
}
```

#### Health Check
```http
GET /api/health
```

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=app --cov-report=html
```

### Test Coverage Includes
- URL parsing and validation
- Feature extraction
- Risk scoring algorithm
- API endpoints
- Input validation
- Database operations

## 🛡️ Security Considerations

### Implemented Security Measures
1. **Input Validation**: Strict URL format validation using Pydantic
2. **URL Normalization**: Safe parsing prevents injection attacks
3. **Parameterized Queries**: All database operations use parameterized queries
4. **Error Handling**: Generic error messages prevent information leakage
5. **Logging**: Sensitive data is never logged
6. **Security Headers**: CORS, CSP, and other security headers implemented
7. **Rate Limiting**: Can be enabled in configuration
8. **No Malicious Activity**: Application is purely defensive

### Safe Analysis Methods
- **Static Analysis**: No actual website visits
- **Pattern Matching**: Uses regex and rule-based detection
- **Feature Extraction**: Analyzes URL structure, not content
- **Safe Defaults**: Treats unknown URLs as suspicious

### Limitations
- Cannot detect 0-day phishing techniques
- Domain reputation checking not implemented
- No machine learning model included by default
- SQLite not suitable for high-concurrency production use

## 📊 Risk Scoring System

### Score Ranges
- **0-25**: Low Risk (✅ Safe)
- **26-50**: Moderate Risk (⚠️ Moderate)
- **51-75**: Suspicious (⚠️ Suspicious)
- **76-100**: High Risk (🚨 Phishing)

### Scoring Factors
| Feature | Weight | Risk |
|---------|--------|------|
| IP-based URL | 20 | Very High |
| No HTTPS | 18 | Very High |
| Punycode Domain | 16 | Very High |
| Suspicious Keywords | 15 | High |
| Long URL | 15 | High |
| URL Shortener | 14 | High |
| Suspicious Query Params | 12 | High |
| Excessive Subdomains | 10 | Medium |
| Special Characters | 9 | Medium |
| Excessive Dots | 8 | Medium |

## 🎨 Frontend Features

### Analyzer Page
- Real-time URL analysis
- Interactive risk score display
- Detailed indicator breakdown
- Security recommendations
- Technical analysis details
- Score calculation transparency

### Dashboard
- Summary statistics cards
- Risk distribution chart
- Real-time data updates
- Responsive grid layout

### History Page
- Search functionality
- Risk level filtering
- Pagination support
- Delete individual scans
- Bulk delete all scans
- Scan details modal

## 📝 Configuration

### Environment Variables (.env)
```env
# Database
DATABASE_URL=sqlite:///./phishguard.db

# FastAPI
DEBUG=True
API_TITLE=PhishGuard API
API_VERSION=1.0.0

# Security
SECRET_KEY=your-secret-key-change-in-production

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/phishguard.log
```

## 🔄 Development Workflow

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement feature with tests
3. Run test suite: `pytest tests/ -v`
4. Commit changes: `git commit -m "Add new feature"`
5. Push to GitHub: `git push origin feature/new-feature`
6. Create Pull Request

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings for public functions
- Keep functions small and focused
- Use meaningful variable names

## 📚 Technology Stack

### Backend
- **FastAPI** 0.104.1 - Modern async web framework
- **Uvicorn** 0.24.0 - ASGI server
- **SQLAlchemy** 2.0.23 - ORM
- **Pydantic** 2.5.0 - Data validation

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive styling
- **Vanilla JavaScript** - No framework dependencies

### Testing
- **pytest** 7.4.3 - Testing framework
- **pytest-asyncio** - Async test support

### Database
- **SQLite** - Lightweight relational database

## 🚀 Production Deployment

### Recommended Setup
1. Replace SQLite with PostgreSQL
2. Use Gunicorn with multiple workers
3. Implement Redis for caching
4. Add reverse proxy (Nginx)
5. Enable HTTPS/SSL
6. Set up monitoring and logging
7. Implement rate limiting
8. Add API authentication

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

## 📖 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Tutorial](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [OWASP Phishing Prevention](https://owasp.org/)
- [URL Security Best Practices](https://tools.ietf.org/html/rfc3986)

## ⚠️ Disclaimer

PhishGuard is an educational cybersecurity project. While it implements security best practices:
- It should not be the sole defense against phishing attacks
- Always verify suspicious URLs through official channels
- No security tool is 100% accurate
- Use in conjunction with email security tools and user training

## 📄 License

This project is provided as-is for educational purposes.

## 👤 Author

**Varun Dakh**
- GitHub: [@Varundakh](https://github.com/Varundakh)
- Portfolio Project for Cybersecurity Learning

## 🎓 Educational Value

This project demonstrates:
- Full-stack web application development
- Cybersecurity detection techniques
- Clean code architecture
- RESTful API design
- Testing best practices
- Frontend/Backend integration
- Security-first development

## 📞 Support

For issues, questions, or suggestions:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include steps to reproduce bugs
4. Provide screenshots or logs when relevant

---

**PhishGuard** - Making the internet safer, one URL at a time. 🛡️
