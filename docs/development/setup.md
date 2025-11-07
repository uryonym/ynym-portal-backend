# Development Setup

## Prerequisites

- Python 3.12+
- uv package manager
- PostgreSQL 12+

## Installation

### 1. Install dependencies

```bash
uv sync
```

### 2. Set up environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

### 3. Initialize database

```bash
# Create database
createdb ynym_db

# Run migrations (if using Alembic in the future)
```

## Running the application

### Development server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

Swagger UI: `http://localhost:8000/docs`
ReDoc: `http://localhost:8000/redoc`

## Running tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app
```

## Code quality

### Linting

```bash
ruff check app
```

### Formatting

```bash
ruff format app
```

### Type checking

```bash
mypy app
```

## Documentation

Generate and serve documentation:

```bash
mkdocs serve
```

Documentation will be available at `http://localhost:8000`
