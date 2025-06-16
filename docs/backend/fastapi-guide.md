# FastAPI Guide for Backend Development

This guide provides an overview of how FastAPI is used in this project and key concepts for backend development.

## Why FastAPI?

FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints. Key benefits include:

*   **High Performance:** On par with NodeJS and Go, thanks to Starlette and Pydantic.
*   **Fast to Code:** Increase the speed to develop features by about 200% to 300%.
*   **Fewer Bugs:** Reduce about 40% of human-induced errors (thanks to type hints).
*   **Intuitive:** Great editor support. Completion everywhere. Less time debugging.
*   **Easy:** Designed to be easy to use and learn. Less time reading docs.
*   **Short:** Minimize code duplication. Multiple features from each parameter declaration.
*   **Robust:** Get production-ready code. With automatic interactive documentation.
*   **Standards-based:** Based on (and fully compatible with) the open standards for APIs: OpenAPI and JSON Schema.

## Backend Project Structure

Our backend is organized to promote modularity and maintainability. A typical structure (located in `backend/app/`) might look like this:

```
backend/
├── app/
│   ├── config/           # Configuration settings (from .env)
│   ├── db/               # Database models and sessions
│   ├── logs/           # Log files
│   ├── routes/           # API routes and endpoints
│   ├── schemas/          # Pydantic schemas (data validation)
│   ├── services/         # Business logic services
│   ├── utils/            # Utility functions and constants
│   └── main.py           # FastAPI application instance and main router
├── alembic/           # Alembic migrations (if using Alembic)
├── tests/                # Unit and integration tests
├── .env.example          # Example environment variables
├── .gitignore
├── alembic.ini           # Alembic configuration (if used)
├── Dockerfile            # Dockerfile for containerization
├── pyproject.toml        # pyproject.toml for Poetry
├── README.md             # This file
└── requirements.txt      # Project dependencies 
```

## Defining Endpoints

Endpoints are defined using path operation decorators (`@router.get`, `@router.post`, etc.) on functions within modules in `app/api/v1/endpoints/`. These routers are then included in the main FastAPI app instance in `app/main.py`.

**Example (`app/api/v1/endpoints/items.py`):**
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api.v1 import deps # Assuming deps.py for get_db

router = APIRouter()

@router.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(deps.get_db)):
    return crud.item.create(db=db, item=item)

@router.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(deps.get_db)):
    db_item = crud.item.get(db, id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

## Data Validation with Pydantic

Pydantic is used extensively for data validation, serialization, and settings management.

*   **Request Bodies:** Define a Pydantic model (schema) that inherits from `BaseModel`. FastAPI will automatically validate incoming request data against this schema.
*   **Response Models:** Use the `response_model` parameter in path operation decorators to define the schema for the response. FastAPI will filter and serialize the output data to match this schema.
*   **Path and Query Parameters:** Type hints for path and query parameters are also validated.

**Example (`app/schemas/item.py`):**
```python
from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True # or from_attributes = True for Pydantic v2
```

## Dependency Injection

FastAPI's dependency injection system is a powerful feature used for:

*   **Database Sessions:** Providing a database session to path operation functions (e.g., `db: Session = Depends(deps.get_db)`).
*   **Authentication & Authorization:** Getting the current user or validating security scopes (e.g., `current_user: models.User = Depends(deps.get_current_active_user)`).
*   **Shared Logic:** Reusing common logic or parameters.

Dependencies are defined as functions (often in `app/api/v1/deps.py`) that FastAPI will call.

## Asynchronous Operations (`async`/`await`)

FastAPI supports asynchronous path operation functions using `async def`. This is crucial for I/O-bound operations (like database calls or external API requests) to prevent blocking the server.

```python
@router.get("/async-items/")
async def read_async_items():
    # Example: await some_async_io_operation()
    return [{"name": "Async Item 1"}, {"name": "Async Item 2"}]
```
Ensure your database drivers and other I/O libraries support `async` operations (e.g., `asyncpg` for PostgreSQL with SQLAlchemy).

## Authentication

This project typically uses JWT (JSON Web Tokens) for authentication. The flow usually involves:
1.  An endpoint (e.g., `/login/access-token`) where users submit credentials.
2.  If valid, the server generates and returns an access token.
3.  The client includes this token in the `Authorization` header (e.g., `Bearer <token>`) for subsequent requests to protected endpoints.
4.  A dependency (`get_current_user`) validates the token and retrieves the user.

Security utilities for password hashing and JWT management are often in `app/core/security.py`.

## Automatic API Documentation

FastAPI automatically generates interactive API documentation based on your code, Pydantic models, and OpenAPI schema.

*   **Swagger UI:** Accessible at `/docs` (e.g., `http://localhost:8000/docs`).
*   **ReDoc:** Accessible at `/redoc` (e.g., `http://localhost:8000/redoc`).

This documentation is invaluable for frontend developers and API consumers.

## Further Reading

*   [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/)
*   [Pydantic Documentation](https://docs.pydantic.dev/)
