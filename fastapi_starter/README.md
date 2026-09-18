# FastAPI Starter Template

A production-ready, async-first FastAPI boilerplate adhering to clean architecture, modern dependency injection, Pydantic v2, and Async SQLAlchemy.

---

## Features

- **FastAPI 0.115+**: High-performance REST APIs with auto-generated Swagger/OpenAPI docs.
- **Lifespan Context**: Modern application startup and shutdown lifecycle management using `asynccontextmanager`.
- **Async SQLAlchemy 2.0**: Asynchronous ORM with non-blocking database queries.
- **SQLite Out-of-the-Box**: Configured with `sqlite+aiosqlite` for instant local development without installing extra services.
- **PostgreSQL Ready**: Easily switch to PostgreSQL (`asyncpg`) by simply toggling environment variables.
- **Pydantic v2 & `pydantic-settings`**: Strict typing, fast validation, and clean `.env` config loading.
- **Authentication & Security**: Secure bcrypt password hashing and OAuth2 Bearer JWT token generation.
- **Database Migrations**: Pre-configured async Alembic migrations (`alembic/`).
- **Async Testing**: Pytest suite using `httpx.AsyncClient` with in-memory SQLite database isolation.
- **Containerized**: Production-grade `Dockerfile` and multi-service `docker-compose.yml`.

---

## Directory Structure

```text
fastapi_starter/
├── alembic/                       # Database migrations (Alembic)
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── app/
│   ├── __init__.py
│   ├── main.py                    # App entrypoint & lifespan
│   ├── api/                       # API routing & dependencies
│   │   ├── deps.py                # Reusable dependencies (DB sessions, auth)
│   │   └── v1/
│   │       ├── router.py          # Master v1 router
│   │       └── endpoints/
│   │           ├── auth.py        # /login, /register
│   │           ├── users.py       # /users, /users/me
│   │           └── items.py       # /items CRUD
│   ├── core/                      # Settings & infrastructure
│   │   ├── config.py              # Pydantic v2 BaseSettings
│   │   ├── database.py            # Async engine & sessionmaker
│   │   └── security.py            # Password hashing & JWT helpers
│   ├── models/                    # SQLAlchemy ORM models
│   │   ├── base.py                # DeclarativeBase & TimestampMixin
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/                   # Pydantic validation schemas (DTOs)
│   │   ├── token.py
│   │   ├── user.py
│   │   └── item.py
│   └── services/                  # Business logic layer
│       ├── user_service.py
│       └── item_service.py
├── tests/                         # Pytest test suite
│   ├── conftest.py                # Async client fixtures & test DB
│   ├── test_health.py
│   └── api/
│       ├── test_auth.py
│       └── test_users.py
├── .env.example
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

---

## Getting Started

### 1. Create a Virtual Environment

```bash
cd fastapi_starter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

### 3. Run the Development Server

```bash
uvicorn app.main:app --reload
```

The application will be running at `http://127.0.0.1:8000`.

- Interactive API Docs (Swagger): [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Alternative Docs (ReDoc): [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## Database Migrations (Alembic)

To create a new migration after editing models:

```bash
alembic revision --autogenerate -m "create initial tables"
```

To apply migrations:

```bash
alembic upgrade head
```

---

## Running Tests

```bash
pytest
```

---

## Docker Deployment

To run the app alongside a PostgreSQL instance:

```bash
docker compose up --build
```
