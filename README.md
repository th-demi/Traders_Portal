# Traders Portal Backend

A production-ready Django backend for a stock watchlist and company search platform, featuring JWT and Google authentication, efficient APIs, async CSV ingestion, and robust error handling.

---

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

---

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

---

## API Documentation
- Swagger UI: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)
- Redoc: [http://localhost:8000/redoc/](http://localhost:8000/redoc/)

---

## CSV Watcher (Async Company Import)
- Place CSV files (with columns: `company_name`, `symbol`, `scripcode`) in `companies/csv_uploads/`.
- Run the watcher:
```bash
python companies/csv_watcher.py
```
- Companies will be auto-imported/updated on file change.

---

## Testing
```bash
python manage.py test
```

---

## Deployment (Render)
1. Add your environment variables (e.g., `SECRET_KEY`, `DEBUG=0`, `ALLOWED_HOSTS`, `DATABASE_URL`, etc.)
2. Use Gunicorn for WSGI serving.
3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```
4. See Render docs for Django deployment specifics.

---

## Security Checklist
- Uses JWT for API auth
- Google Auth via Firebase
- Input validation and DRF protections
- CSRF, SQL injection, and XSS protections (Django defaults)
- Production cache and static/media settings

---

## License
MIT 