# 🏫 School Management System

A comprehensive REST API built with **Django** + **PostgreSQL** featuring JWT authentication and role-based access control.

---

##  Tech Stack

- **Backend:** Django 4.2, Django REST Framework
- **Database:** PostgreSQL
- **Auth:** JWT (SimpleJWT) with role-based permissions
- **Docs:** Swagger UI (drf-yasg)

---

##  User Roles

| Role    | Access Level |
|---------|-------------|
| Admin   | Full access to all modules |
| Teacher | Attendance, Grades, Timetable (read) |
| Student | Own profile, grades, attendance |
| Parent  | Children's records |

---

##  Modules

- ✅ **Accounts** — User management, JWT login/logout, role-based auth
- ✅ **Students** — Student profiles, class management
- ✅ **Teachers** — Teacher profiles, subject assignments
- ✅ **Attendance** — Daily/bulk attendance, summaries, reports
- ✅ **Grades** — Exams, bulk grading, auto grade calculation, student reports
- ✅ **Timetable** — Weekly schedule with time slots
- ✅ **Fees** — Fee structures, payments (M-Pesa, cash, bank), reports
- ✅ **Library** — Book inventory, issue/return, overdue fines

---

##  Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/school-management-system.git
cd school-management-system
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

### 5. Create PostgreSQL database
```sql
CREATE DATABASE school_db;
CREATE USER school_user WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE school_db TO school_user;
```

### 6. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create superuser (Admin)
```bash
python manage.py createsuperuser
```

### 8. Run the server
```bash
python manage.py runserver
```

---

##  API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login & get JWT tokens |
| POST | `/api/auth/logout/` | Blacklist refresh token |
| POST | `/api/auth/token/refresh/` | Refresh access token |
| POST | `/api/auth/register/` | Register user (Admin only) |
| GET/PUT | `/api/auth/profile/` | View/update own profile |
| POST | `/api/auth/change-password/` | Change password |

### Students
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/students/` | List/create students |
| GET/PUT/DELETE | `/api/students/<id>/` | Student detail |
| GET/POST | `/api/students/classes/` | List/create classes |

### Teachers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/teachers/` | List/create teachers |
| GET/POST | `/api/teachers/subjects/` | List/create subjects |

### Attendance
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/attendance/` | List/create records |
| POST | `/api/attendance/bulk/` | Bulk mark attendance |
| GET | `/api/attendance/student/<id>/` | Student attendance report |

### Grades
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/grades/exams/` | List/create exams |
| GET/POST | `/api/grades/` | List/create grades |
| POST | `/api/grades/bulk/` | Bulk enter grades |
| GET | `/api/grades/report/<student_id>/` | Student report card |

### Timetable
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/timetable/` | List/create timetable |
| GET/POST | `/api/timetable/slots/` | Manage time slots |

### Fees
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/fees/structures/` | Fee structures |
| GET/POST | `/api/fees/payments/` | Record payments |
| GET | `/api/fees/student/<id>/` | Student fee statement |
| GET | `/api/fees/report/` | Overall fee report |

### Library
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/library/books/` | Book catalog |
| GET/POST | `/api/library/issues/` | Issue/track books |

---

## 📖 API Documentation

After running the server, visit:
- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/
- **Django Admin:** http://localhost:8000/admin/

---

## 🔐 Authentication

All endpoints (except login) require a Bearer token:

```http
Authorization: Bearer <your_access_token>
```

**Example login request:**
```json
POST /api/auth/login/
{
  "email": "admin@school.com",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "access": "eyJ...",
  "refresh": "eyJ...",
  "user": {
    "id": 1,
    "email": "admin@school.com",
    "role": "admin",
    "full_name": "John Doe"
  }
}
```

---

## 🧪 Running Tests

```bash
python manage.py test
# or with coverage
coverage run manage.py test
coverage report
```

---

## 📁 Project Structure

```
school_management/
├── apps/
│   ├── accounts/       # Auth, users, JWT
│   ├── students/       # Students, classes
│   ├── teachers/       # Teachers, subjects
│   ├── attendance/     # Attendance tracking
│   ├── grades/         # Exams, grades, reports
│   ├── timetable/      # Schedule management
│   ├── fees/           # Fee management
│   └── library/        # Library system
├── school_management/
│   ├── settings.py
│   └── urls.py
├── .env.example
├── requirements.txt
└── manage.py
```

---

## 📝 License

MIT License — feel free to use and modify.
