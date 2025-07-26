# PM Dashboard Backend

Django REST API backend for the Project Management Dashboard with AI integration.

## Project Structure

This backend works with the Vue.js frontend located in `../frontend/`.

## Setup

1. Create virtual environment (from backend directory):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Edit .env with your settings
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Create sample data:
```bash
python manage.py create_sample_data
```

7. Run development server:
```bash
python manage.py runserver
```

The backend will be available at: http://localhost:8000
The frontend should run at: http://localhost:8080

## API Endpoints

- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `GET /api/projects/` - List projects
- `POST /api/feedback/slider/` - Submit slider feedback
- `POST /api/ai/chat/` - AI chat endpoint
- `GET /api/dashboard/analytics/` - Dashboard analytics

## Sample Users

After running `create_sample_data`:
- Executive: executive@company.com (password123)
- Manager: manager1@company.com (password123)
- Team Member: john@company.com (password123)

## Development

Frontend: `cd ../frontend && npm run serve`
Backend: `cd backend && python manage.py runserver`
