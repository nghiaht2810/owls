# 🎓 Online Learning Platform - Backend

A modern Django REST API for an online learning platform with course management, user authentication, and progress tracking.

## 🚀 Features

- **Course Management**: Create and manage courses, modules, and lessons
- **User Authentication**: JWT-based authentication with refresh tokens
- **Enrollment System**: Users can enroll in courses
- **Progress Tracking**: Track lesson completion and watch progress
- **Reviews & Ratings**: Rate and review courses
- **Admin Panel**: Full-featured Django admin interface
- **API Documentation**: Auto-generated Swagger/ReDoc documentation
- **Media Upload**: Support for course thumbnails and user avatars

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL (or SQLite for development)
- pip and virtualenv

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/nghiaht2810/owls.git
cd owls/backend
```

### 2. Create virtual environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Copy `.env.sample` to `.env` and configure:

```bash
cp .env.sample .env
```

Edit `.env` with your settings:
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://user:password@host:port/dbname
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/me/` - Get current user profile

### Courses
- `GET /api/courses/` - List all courses
- `GET /api/courses/{slug}/` - Get course details
- `POST /api/courses/{slug}/enroll/` - Enroll in course

### Lessons
- `POST /api/lessons/{id}/complete/` - Mark lesson as completed
- `POST /api/lessons/{id}/update-progress/` - Update watch progress

## 🗂️ Project Structure

```
backend/
├── apps/
│   ├── courses/        # Course management
│   ├── enrollments/    # User enrollments
│   └── users/          # User profiles & auth
├── backend/
│   ├── settings.py     # Django settings
│   └── urls.py         # URL routing
├── media/              # Uploaded files
├── scripts/            # Utility scripts
├── .env                # Environment variables (not in git)
├── .env.sample         # Example env file
├── manage.py
└── requirements.txt
```

## 🔧 Development

### Running tests

```bash
python manage.py test
```

### Creating migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Collecting static files

```bash
python manage.py collectstatic
```

## 🚢 Deployment

1. Set `DJANGO_DEBUG=False` in production
2. Generate a strong `DJANGO_SECRET_KEY`
3. Configure proper `DJANGO_ALLOWED_HOSTS`
4. Use PostgreSQL database
5. Set up proper CORS origins
6. Configure static/media file serving (e.g., AWS S3, Cloudinary)

## 📝 License

This project is licensed under the MIT License.

## 👥 Contributors

- Nghia Hoang (@nghiaht2810)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

Built with ❤️ using Django REST Framework
