# Salary Management System

A full-stack Salary Management System built with **React + TypeScript**, **FastAPI**, and **PostgreSQL**.

The application provides employee management, salary management, salary history, validation, search, pagination, analytics, centralized error handling, logging, database migrations, and automated testing.

---

## 📌 Project Overview

The Salary Management System is designed to demonstrate a production-oriented full-stack application with a clean separation between frontend, backend, business logic, and database layers.

### Core Architecture

```text
┌─────────────────────────────┐
│       React Frontend        │
│     TypeScript + MUI        │
└──────────────┬──────────────┘
               │
               │ REST API
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│          API Routes         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Service Layer         │
│       Business Logic        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Repository Layer       │
│      Database Operations    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        PostgreSQL           │
└─────────────────────────────┘
```

---

## 🚀 Features

### Employee Management

* Create employees
* View employee details
* Update employee information
* Search employees
* Paginate employee records
* Employee validation
* Duplicate employee handling

### Salary Management

* Add salary records
* View salary history
* Edit salary records
* Delete salary records
* Salary validation
* Salary period validation
* Currency validation

### Analytics

* Salary-related analytics
* Aggregated employee/salary information
* Dashboard reporting

### Reliability & Quality

* Health endpoint
* Readiness endpoint
* Centralized exception handling
* Structured error responses
* Application logging
* Request IDs
* Database connection pooling
* Environment-based configuration
* CORS configuration
* Security headers
* Graceful application shutdown

### Development Quality

* Automated API tests
* Pytest
* HTTPX
* Ruff
* mypy
* Alembic migrations
* TypeScript
* Zod validation
* React Hook Form

---

# 🛠️ Technology Stack

## Frontend

| Technology      | Purpose                 |
| --------------- | ----------------------- |
| React           | UI development          |
| TypeScript      | Type safety             |
| Vite            | Frontend build tooling  |
| React Router    | Application routing     |
| Material UI     | UI components           |
| TanStack Query  | Server-state management |
| Axios           | HTTP client             |
| React Hook Form | Form management         |
| Zod             | Form validation         |

## Backend

| Technology        | Purpose                  |
| ----------------- | ------------------------ |
| Python 3.13       | Backend language         |
| FastAPI           | REST API framework       |
| Uvicorn           | ASGI server              |
| SQLAlchemy        | ORM/database access      |
| Alembic           | Database migrations      |
| Pydantic          | Data validation          |
| pydantic-settings | Configuration management |

## Database

* PostgreSQL

## Testing & Code Quality

* Pytest
* HTTPX
* Ruff
* mypy

## Version Control

* Git
* GitHub

---

# 📁 Project Structure

```text
salary-management/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── routes/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── .env.example
│   ├── alembic.ini
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── routes/
│   │   └── types/
│   │
│   ├── package.json
│   └── vite.config.ts
│
├── docs/
│   └── PROJECT_DOCUMENTATION.md
│
├── .gitignore
└── README.md
```

---

# 🔌 API Overview

## Health & Readiness

```http
GET /health
GET /ready
```

## Employees

```http
POST  /api/v1/employees
GET   /api/v1/employees
GET   /api/v1/employees/{employee_id}
PATCH /api/v1/employees/{employee_id}
```

## Salaries

```http
POST   /api/v1/employees/{employee_id}/salaries
GET    /api/v1/employees/{employee_id}/salaries
GET    /api/v1/salaries/{salary_id}
PUT    /api/v1/salaries/{salary_id}
DELETE /api/v1/salaries/{salary_id}
```

## Analytics

```http
GET /api/v1/analytics
```

Interactive API documentation is available through FastAPI Swagger:

```text
/docs
```

---

# 🗄️ Database

The application uses **PostgreSQL** with **SQLAlchemy**.

Database schema changes are managed using **Alembic**.

Run the latest migrations:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "description"
```

---

# ⚙️ Backend Setup

Navigate to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -e .
```

Configure environment variables using:

```text
backend/.env.example
```

Create your local `.env` file and configure the database connection.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/salary_db
CORS_ORIGINS=http://localhost:5173
ENVIRONMENT=development
```

Run migrations:

```bash
alembic upgrade head
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

# 💻 Frontend Setup

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Configure the backend API URL using the frontend environment configuration.

Start the development server:

```bash
npm run dev
```

The Vite development server will provide the frontend URL.

---

# 🧪 Testing

## Backend Tests

From the `backend` directory:

```bash
pytest
```

The project includes tests for:

* Employee APIs
* Salary APIs
* Validation
* Duplicate records
* Error handling
* Health/readiness
* Analytics
* Database-related behavior

## Linting

```bash
ruff check .
```

## Type Checking

```bash
mypy app
```

---

# 🏗️ Production Build

## Frontend

Create the production build:

```bash
npm run build
```

Production files are generated in:

```text
frontend/dist
```

## Backend

Production server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Apply database migrations:

```bash
alembic upgrade head
```

---

# 🔐 Environment & Security

Sensitive configuration must **not** be committed to GitHub.

The repository uses:

```text
.env
```

for local/private environment configuration.

A safe template is provided through:

```text
backend/.env.example
```

The `.gitignore` excludes environment files and other local configuration.

Production secrets should be configured through the deployment platform's environment-variable management.

---

# ❤️ Health Checks

### Health

```http
GET /health
```

Example:

```json
{
  "status": "healthy"
}
```

### Readiness

```http
GET /ready
```

The readiness endpoint verifies that the application and required dependencies are ready to serve requests.

---

# 📊 Application Flow

### Create Employee

```text
React Form
    ↓
Zod Validation
    ↓
TanStack Query
    ↓
Axios
    ↓
FastAPI
    ↓
Service
    ↓
Repository
    ↓
PostgreSQL
```

### Create/Edit Salary

```text
Salary Form
    ↓
Client Validation
    ↓
FastAPI Validation
    ↓
Business Rules
    ↓
Database
    ↓
Updated Salary History
```

---

# ✅ Verification Status

The application has been verified for the following functionality:

### Backend

* [x] Health endpoint
* [x] Readiness endpoint
* [x] Employee APIs
* [x] Salary APIs
* [x] Analytics API
* [x] Validation
* [x] Error handling
* [x] Logging
* [x] Database migrations
* [x] PostgreSQL integration
* [x] Automated tests
* [x] Ruff
* [x] mypy

### Frontend

* [x] Dashboard
* [x] Employee listing
* [x] Employee search
* [x] Pagination
* [x] Add Employee
* [x] Employee Details
* [x] Salary History
* [x] Add Salary
* [x] Salary validation
* [x] Edit Salary
* [x] Delete Salary
* [x] Analytics
* [x] Loading states
* [x] Error states
* [x] Empty states
* [x] Production build

---

# 📚 Documentation

Detailed technical documentation is available here:

```text
docs/PROJECT_DOCUMENTATION.md
```

It contains:

* Detailed architecture
* Database design
* API documentation
* Validation rules
* Error handling
* Testing
* Security
* Logging
* Performance considerations
* Deployment
* Design decisions
* Future improvements

---

# 🚀 Deployment

The application can be deployed as separate frontend, backend, and database services.

```text
                  GitHub
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
      Frontend             Backend
       Hosting             Hosting
                              │
                              ▼
                         PostgreSQL
```

Production deployment should use:

* HTTPS
* Production environment variables
* Managed PostgreSQL
* Database migrations
* Production CORS configuration
* Secure secret management

---

# 🔮 Future Improvements

Potential future enhancements include:

* Authentication
* Role-based authorization
* Audit logging
* CSV/Excel export
* Advanced reporting
* CI/CD automation
* Cloud monitoring
* API rate limiting
* Background processing
* Expanded frontend automated tests
* Containerized deployment

---

# 👨‍💻 Project Purpose

This project demonstrates practical full-stack development using modern technologies and software engineering practices.

It focuses on:

* Clean architecture
* Maintainable code
* REST API design
* Database design
* Business validation
* Error handling
* Automated testing
* Type safety
* Production configuration
* Frontend/backend integration
* Git-based development workflow

---

## License

This project is intended for demonstration and assessment purposes.
