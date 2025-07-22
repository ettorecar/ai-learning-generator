# Deployment Guide

This guide provides instructions for deploying the AI-Powered E-Learning Generator in various environments.

## Local Development

### Prerequisites
- Python 3.7 or higher
- Node.js (optional, for development tools)
- OpenAI API key

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/ettorecar/ai-learning-generator.git
cd ai-learning-generator
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_PORT=8080
CORS_ORIGIN=http://127.0.0.1:5500
```

5. **Start the backend server**
```bash
python openai_mw.py
```

6. **Serve the frontend**
Open `index.html` in a web browser or use a local server:
```bash
# Using Python
python -m http.server 5500

# Using Node.js
npx serve . -p 5500
```

## Production Deployment

### Environment Variables

Set the following environment variables:

```env
OPENAI_API_KEY=your_production_api_key
FLASK_ENV=production
FLASK_PORT=8080
CORS_ORIGIN=https://yourdomain.com
SECRET_KEY=your_secret_key_here
```

### Using Docker

1. **Create Dockerfile**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "openai_mw.py"]
```

2. **Build and run**
```bash
docker build -t ai-learning-generator .
docker run -p 8080:8080 --env-file .env ai-learning-generator
```

### Using Cloud Platforms

#### Heroku Deployment

1. **Create Procfile**
```
web: python openai_mw.py
```

2. **Deploy**
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

#### AWS EC2 Deployment

1. **Setup EC2 instance** with Python 3.7+
2. **Install dependencies** and clone repository
3. **Configure nginx** as reverse proxy
4. **Use systemd** for service management

#### Google Cloud Platform

1. **Create app.yaml**
```yaml
runtime: python39

env_variables:
  OPENAI_API_KEY: your_key

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

2. **Deploy**
```bash
gcloud app deploy
```

## Security Considerations

### Production Checklist

- [ ] Use HTTPS in production
- [ ] Set secure CORS policies
- [ ] Implement rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable proper logging
- [ ] Set up monitoring
- [ ] Configure firewall rules
- [ ] Regular security updates

### Recommended Security Headers

```python
# Add to Flask app
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

## Monitoring and Maintenance

### Health Checks

Add health check endpoint:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### Logging

Configure proper logging:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Backup Strategy

- Regular database backups (if using database)
- Configuration file backups
- Log file rotation
- API key rotation schedule

## Troubleshooting

### Common Issues

1. **CORS Errors**: Check CORS configuration in Flask app
2. **API Rate Limits**: Implement retry logic and rate limiting
3. **Memory Issues**: Monitor memory usage and optimize
4. **File Permissions**: Ensure proper file permissions

### Performance Optimization

- Use caching for repeated API calls
- Implement request queuing for high load
- Optimize frontend assets (minification, compression)
- Use CDN for static assets

## Scaling Considerations

### Horizontal Scaling

- Use load balancer (nginx, AWS ALB)
- Implement session management
- Consider microservices architecture
- Use container orchestration (Kubernetes)

### Database Integration

For production use, consider adding:
- PostgreSQL or MySQL for data persistence
- Redis for caching and session storage
- Database connection pooling

## Support

For deployment issues, please:
1. Check the troubleshooting section
2. Review logs for error messages
3. Open an issue on GitHub with deployment details
4. Contact the development team

---

**Note**: Always test deployment in a staging environment before production release.
