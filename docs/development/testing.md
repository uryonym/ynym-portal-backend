# Testing Guide

## Test Structure

Tests are organized into two categories:

- **Unit Tests** (`tests/unit/`): Test individual functions and services
- **Integration Tests** (`tests/integration/`): Test API endpoints and database interactions

## Running Tests

### Run all tests

```bash
pytest
```

### Run specific test file

```bash
pytest tests/unit/test_user_service.py
```

### Run with coverage

```bash
pytest --cov=app --cov-report=html
```

### Run in watch mode

```bash
pytest-watch
```

## Writing Tests

### Unit Test Example

```python
import pytest
from app.services.user_service import UserService


@pytest.mark.asyncio
async def test_create_user():
    """Test user creation."""
    service = UserService()
    user = await service.create({"name": "John", "email": "john@example.com"})
    assert user.name == "John"
```

### Integration Test Example

```python
@pytest.mark.asyncio
async def test_create_user_endpoint(async_client):
    """Test user creation endpoint."""
    response = await async_client.post(
        "/api/users",
        json={"name": "John", "email": "john@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John"
```

## Fixtures

Common fixtures are defined in `tests/conftest.py`:

- `client`: Synchronous FastAPI test client
- `async_client`: Asynchronous FastAPI test client

## Best Practices

1. One test per function/scenario
2. Use descriptive test names
3. Arrange-Act-Assert pattern
4. Use fixtures for setup/teardown
5. Mock external dependencies
6. Aim for >80% code coverage
