# Beauty SaaS Backend

A scalable FastAPI backend for beauty and wellness businesses.  
Built with JWT authentication, role-based permissions, PostgreSQL, automated testing, and Docker support.

---
## Preview

```txt
FastAPI + PostgreSQL + JWT + Docker + Pytest
```
---

## Features

- JWT Authentication
- Role-Based Authorization (Admin/User)
- Clients Management
- Services Management
- Appointments Scheduling
- Payments Management
- Protected Routes
- PostgreSQL Integration
- Automated Testing with Pytest
- Dockerized Environment
- REST API Architecture

---
## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Backend Framework |
| SQLModel | ORM & Data Validation |
| PostgreSQL | Database |
| SQLAlchemy | Database Engine |
| JWT | Authentication |
| Pytest | Automated Testing |
| Docker | Containerization |
| Python 3.13 | Programming Language |

---
## Project Structure

```bash
.
├── models/
├── routers/
├── schemas/
├── db/
├── tests/
├── main.py
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## Getting Started

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/beauty-saas-backend.git
```

### Enter Project

```bash
cd beauty-saas-backend
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Linux / macOS

```bash
source venv/bin/activate
```

#### Windows

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---
## Environment Variables

Create a `.env` file:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/app_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---
## Run Locally
```bash
uvicorn main:app --reload
```
API available at:
```txt
http://localhost:8000
```
---

## Docker

Build and run containers:

```bash
docker compose up --build
```

---

## API Documentation
### Swagger UI

```txt
http://localhost:8000/docs
```
### ReDoc
```txt
http://localhost:8000/redoc
```
---
## Testing

Run tests:

```bash
pytest
```
---
## Authentication

Protected endpoints require JWT Bearer Token authentication.
Example:
```http
Authorization: Bearer your_token_here
```
---

### Completed

- Authentication System
- JWT Authorization
- Admin Permissions
- Clients CRUD
- Services CRUD
- Appointments CRUD
- Payments Structure
- Automated Tests
- Docker Setup
