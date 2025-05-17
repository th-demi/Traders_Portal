# Traders Portal Backend

A production-ready Django backend for a stock watchlist and company search platform, featuring JWT and Google authentication, efficient APIs, async CSV ingestion, and robust error handling.

## Live Demo & Documentation
- **Deployed Backend**: [https://traders-portal.onrender.com/](https://traders-portal.onrender.com/)
- **Postman Documentation**: [API Collection](https://postman.co/workspace/My-Workspace~6b4ded8c-d4f2-47ee-891d-601a5dbe0922/collection/39450369-65beef12-5ad9-406d-9aee-48f768c8584f?action=share&creator=39450369)

## Accessing the Application

### Server-Side Rendered (SSR) Pages
Access these through your browser at the root URL:
- `/` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/watchlist` - Watchlist management
- `/companies` - Company search and listing

### REST API Endpoints
All API endpoints are prefixed with `/api/`:
- `/api/users/` - User management
- `/api/companies/` - Company search and data
- `/api/watchlist/` - Watchlist operations
- `/api/swagger/` - API documentation (Swagger UI)
- `/api/redoc/` - Alternative API documentation (ReDoc)

## Features
- User registration, JWT login, and Google Auth (Firebase)
- Company search/filter API (by name, symbol)
- User watchlist API (add/remove/list)
- Efficient DB queries and indexes
- Robust error handling and logging
- Automated tests
- Swagger/OpenAPI docs
- Asynchronous CSV watcher (auto-imports companies)
- Production-ready settings and security best practices
- Rate limiting for API protection

## Rate Limiting
The API implements the following rate limits to prevent abuse:

### Authentication Endpoints
- Login/Register: 5 requests per minute
- Token Refresh: 5 requests per minute

### User Operations
- Anonymous users: 100 requests per day
- Authenticated users: 1000 requests per day
- Burst rate: 5 requests per minute
- Sustained rate: 100 requests per hour

### Watchlist Operations
- Add/Remove companies: 10 requests per minute
- List operations: Global limits + burst protection

### Search Operations
- Company search: 20 requests per minute
- List operations: Global limits + burst protection

## Setup

### 1. Clone & Environment
```bash
git clone <your-repo-url>
cd Traders_Portal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Database
- By default uses SQLite for dev. For prod, configure PostgreSQL in `config/settings.py` and set `DATABASE_URL` in your environment.

### 3. Firebase Credentials
- Download your Firebase service account JSON.
- Save as `firebase_credentials.json` in the project root.

### 4. Migrate & Create Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 5. Run Server
```bash
python manage.py runserver
```

## API Documentation
- Swagger UI: [http://localhost:8000/api/swagger/](http://localhost:8000/api/swagger/)
- Redoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

## CSV Watcher (Async Company Import)
- Place CSV files (with columns: `company_name`, `symbol`, `scripcode`) in `companies/csv_uploads/`.
- Run the watcher:
```bash
python companies/csv_watcher.py
```
- Companies will be auto-imported/updated on file change.

## Testing
```bash
python manage.py test
```

## Deployment (Render)
1. Add your environment variables (e.g., `SECRET_KEY`, `DEBUG=0`, `ALLOWED_HOSTS`, `DATABASE_URL`, etc.)
2. Use Gunicorn for WSGI serving.
3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
4. See Render docs for Django deployment specifics.

## Security Checklist
- Uses JWT for API auth
- Google Auth via Firebase
- Input validation and DRF protections
- CSRF, SQL injection, and XSS protections (Django defaults)
- Production cache and static/media settings
- Rate limiting for API protection
- Content Security Policy (CSP) headers
- Secure cookie settings
- CORS configuration

## License
MIT 