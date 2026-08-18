# PhishGuard - Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in PhishGuard, please:

1. **Do NOT** create a public GitHub issue
2. Email security concerns to the repository owner
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Considerations

### What PhishGuard Does
- ✅ Performs static URL analysis
- ✅ Extracts security features from URLs
- ✅ Provides risk assessment
- ✅ Stores scan history safely
- ✅ Uses parameterized queries
- ✅ Implements security headers

### What PhishGuard Does NOT Do
- ❌ Visit actual websites
- ❌ Execute code
- ❌ Download files
- ❌ Perform network scans
- ❌ Access system files
- ❌ Bypass security mechanisms

### Limitations
- **No Real-time Detection**: Relies on static analysis
- **No Reputation Checking**: Cannot check domain/IP reputation
- **No ML Model**: Optional ML module not included
- **Local Database**: SQLite for development only
- **No Authentication**: Not designed for multi-user production

## Security Best Practices for Users

1. **Keep Updated**: Regularly update dependencies
2. **Use HTTPS**: Always run behind HTTPS in production
3. **Environment Variables**: Never hardcode secrets
4. **Database**: Use PostgreSQL in production
5. **Monitoring**: Implement logging and monitoring
6. **Backups**: Regular database backups

## Dependency Security

Dependencies are intentionally minimal:
- FastAPI - Web framework
- SQLAlchemy - ORM
- Pydantic - Validation
- scikit-learn - Optional ML

All dependencies are well-maintained and widely used.

## Testing Security

Run security tests:
```bash
pytest tests/test_api.py::TestInputValidation -v
pytest tests/test_api.py::TestAPIEndpoints -v
```

## Compliance

- Follows OWASP top 10 principles
- Implements input validation
- Uses parameterized queries
- No hardcoded secrets
- Proper error handling

---

For more information, see README.md and ARCHITECTURE.md
