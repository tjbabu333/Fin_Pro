# Salary Management System

A full-stack salary management application built with **FastAPI, PostgreSQL, SQLAlchemy, Alembic, React, TypeScript, and Material UI**.

## Architecture

```text
React + TypeScript
        ↓
Axios / TanStack Query
        ↓
FastAPI REST API
        ↓
Service Layer
        ↓
Repository Layer
        ↓
SQLAlchemy
        ↓
PostgreSQL
```

## Features

### Backend

* Employee management
* Employee search and pagination
* Salary record management
* Add, update, and delete salary records
* Salary history
* Salary analytics
* Input validation
* Standardized API error responses
* Global exception handling
* Request ID tracking
* Application logging
* Health and readiness endpoints
* PostgreSQL connection pooling
* Environment-based configuration
* CORS configuration
* Security response headers
* Graceful application shutdown
* Database migrations with Alembic
* Employee seed script
* Automated tests
* Ruff linting
* mypy type checking

### Frontend

* Dashboard
* Employee listing
* Employee search
* Employee pagination
* Employee details
* Add employee
* Salary history
* Add salary
* Edit salary
* Delete salary
* Salary validation
* Salary analytics
* Loading states
* Error states
* Empty states
* Responsive Material UI interface

## Technology Stack

### Backend

* Python 3.13
* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* Pydantic
* pytest
* Ruff
* mypy

### Frontend

* React
* TypeScript
* Vite
* React Router
* TanStack Query
* Axios
* Material UI
* React Hook Form
* Zod

## Project Structure

```text
salary-management/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   ├── alembic/
│   ├── Scripts/
│   ├── tests/
│   ├── .env.example
│   ├── .gitignore
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── package-lock.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
└── .gitignore
```

## Backend Setup

Go to the backend directory:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -e ".[dev]"
```

Create your environment file:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your PostgreSQL credentials.

Run database migrations:

```powershell
alembic upgrade head
```

Start the API:

```powershell
uvicorn app.main:app --reload
```

API:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

Health check:

```text
http://127.0.0.1:8000/health
```

Readiness check:

```text
http://127.0.0.1:8000/ready
```

## Running Backend Tests

From the `backend` directory:

```powershell
pytest
```

Lint:

```powershell
ruff check .
```

Type checking:

```powershell
mypy app
```

## Seed Employees

The project includes a seed script for generating employee data.

```powershell
python Scripts/seed_employees.py
```

Do not run the seed script repeatedly against the same database unless additional seed data is intended.

## Frontend Setup

Open another terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend normally runs at:

```text
http://localhost:5173
```

## Production Build

From the frontend directory:

```powershell
npm run build
```

Preview the production build:

```powershell
npm run preview
```

## API Endpoints

### Employees

```text
POST   /api/v1/employees
GET    /api/v1/employees
GET    /api/v1/employees/{id}
PATCH  /api/v1/employees/{id}
```

### Salaries

```text
POST   /api/v1/employees/{employee_id}/salaries
GET    /api/v1/employees/{employee_id}/salaries
GET    /api/v1/employees/{employee_id}/salaries/latest
GET    /api/v1/salaries/{salary_id}
PUT    /api/v1/salaries/{salary_id}
DELETE /api/v1/salaries/{salary_id}
```

### Analytics

```text
GET /api/v1/analytics
```

## Configuration

Sensitive configuration is stored in `.env` and is intentionally excluded from Git.

Use:

```text
backend/.env.example
```

as the template for local configuration.

Never commit:

```text
.env
.env.*
```

except for the provided:

```text
.env.example
```

## Development Principles

The backend follows a layered architecture:

```text
Route
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL


Business logic is kept in the service layer, database access is handled by repositories, and API routes are responsible for HTTP-level concerns.

## Status

The project includes:

* Backend API implementation
* PostgreSQL persistence
* Database migrations
* Employee management
* Salary management
* Analytics
* Validation and error handling
* Logging
* Automated backend tests
* Static analysis
* Frontend application
* Production frontend build
* Production-readiness configuration
