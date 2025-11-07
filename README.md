# ynym Portal Backend

FastAPI backend system for ynym portal using modern Python practices.

## Features

- **FastAPI**: High-performance async web framework
- **SQLModel**: SQLAlchemy ORM with Pydantic validation
- **PostgreSQL**: Robust relational database with asyncpg
- **JWT Authentication**: Secure token-based authentication
- **Async/Await**: Full async support for non-blocking I/O
- **Type Safety**: Full type hints with mypy support
- **Testing**: Comprehensive test suite with pytest
- **Documentation**: Auto-generated API docs with Swagger UI and ReDoc

## Quick Start

### Prerequisites

- Python 3.12+
- uv package manager
- PostgreSQL 12+

### Installation

```bash
# Clone repository
git clone <repository-url>
cd ynym-portal-backend

# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Configure .env with your settings
# Edit .env and update database URL, JWT secret, etc.
```

### Run Development Server

```bash
uvicorn app.main:app --reload
```

Access the application:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Run Tests

```bash
pytest
```

### Run Linting and Type Checking

```bash
ruff check app
mypy app
```

### Generate Documentation

```bash
mkdocs serve
```

## Project Structure

```
app/
├── api/              # API endpoints
├── models/           # Database models (SQLModel)
├── schemas/          # Pydantic request/response schemas
├── services/         # Business logic
├── security/         # Authentication and JWT
├── utils/            # Utilities and exceptions
├── config.py         # Configuration management
├── database.py       # Database connection and session
└── main.py          # FastAPI application instance

tests/
├── unit/            # Unit tests
└── integration/     # Integration tests

docs/                # Project documentation
```

## Development

### Code Quality

- **Linting**: ruff
- **Type Checking**: mypy (strict mode)
- **Formatting**: ruff format

### Testing

- **Framework**: pytest
- **Async Testing**: pytest-asyncio
- **Test Client**: FastAPI TestClient

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret key for JWT tokens
- `ENVIRONMENT`: Application environment (development/production)
- `LOG_LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

## Documentation

Full documentation is available in the `docs/` directory:

- Setup and installation instructions
- Architecture and design patterns
- API endpoint documentation
- Testing guide

## License

[Add your license information here]
