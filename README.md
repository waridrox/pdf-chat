# FastAPI React Starter Template

A modern, full-featured starter template featuring FastAPI backend and React 19 frontend with Tailwind CSS.

## Features

- **Backend (FastAPI)**
  - Fast and modern Python web framework
  - SQLite database with SQLAlchemy ORM
  - Async database operations
  - Proper connection pooling and cleanup
  - Environment configuration with pydantic
  - Structured logging
  - Health check endpoint
  - Graceful shutdown handling
  - Modular project structure

- **Frontend (React 19)**
  - Latest React features including `use` hook
  - Component-based architecture
  - Custom hooks for data fetching
  - Modern error handling with Error Boundaries
  - Suspense for loading states
  - Reusable UI components
  - Tailwind CSS for styling
  - Environment configuration
  - Vite for fast development

## Project Structure

```
fastapi-react-starter/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application entry
│   │   ├── config/              # Configuration management
│   │   │   ├── __init__.py
│   │   │   └── config.py        # Environment settings
│   │   ├── db/                  # Database
│   │   │   ├── __init__.py
│   │   │   ├── database.py      # Database connection
│   │   │   └── models.py        # SQLAlchemy models
│   │   ├── routes/              # API routes
│   │   │   ├── __init__.py
│   │   │   ├── health.py        # Health check endpoint
│   │   │   └── notes.py         # Notes CRUD endpoints
│   │   └── utils/               # Utilities
│   │       ├── __init__.py
│   │       └── logger.py        # Logging configuration
│   ├── .env                     # Environment variables
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   └── ui/
│   │   │       ├── Card.jsx     # Card component
│   │   │       └── StatusDot.jsx # Status indicator
│   │   ├── features/            # Feature modules
│   │   │   └── health/          # Health check feature
│   │   │       ├── HealthStatus.jsx
│   │   │       ├── LoadingStatus.jsx
│   │   │       └── ErrorBoundary.jsx
│   │   ├── hooks/              # Custom React hooks
│   │   │   └── useHealthStatus.js
│   │   ├── layouts/            # Page layouts
│   │   │   └── MainLayout.jsx
│   │   ├── utils/              # Utility functions
│   │   └── App.jsx             # Main React component
│   ├── .env                    # Frontend environment variables
│   └── package.json            # Node.js dependencies
└── README.md                   # Project documentation
```

## Quick Start

### Development

1. Backend Setup:
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix:
   source venv/bin/activate
   
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. Frontend Setup:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Environment Variables

1. Backend (.env):
   ```env
   APP_VERSION=1.0.0
   APP_NAME="FastAPI React Starter"
   APP_DESCRIPTION="FastAPI React Starter Template"
   DATABASE_URL="sqlite+aiosqlite:///./app.db"
   CORS_ORIGINS=["http://localhost:5173"]
   ```

2. Frontend (.env):
   ```env
   VITE_API_URL=http://localhost:8000
   ```

## Access Points

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Organization

### Backend

- **Config Module**: Handles environment variables and application settings using pydantic
- **Database Module**: Manages SQLite database with SQLAlchemy, including connection pooling
- **Routes Module**: Contains API endpoints organized by feature
- **Utils Module**: Houses utility functions like logging

### Frontend

- **Components**: Reusable UI components like Card and StatusDot
- **Features**: Feature-specific components organized by domain
- **Hooks**: Custom React hooks for data fetching and state management
- **Layouts**: Page layout components
- **Utils**: Utility functions and helpers

## Roadmap

### Planned Features

1. **Database Enhancements**
   - [ ] Database migrations with Alembic
   - [ ] Support for PostgreSQL
   - [ ] Enhanced connection pooling options
   - [ ] More comprehensive CRUD operations

2. **Authentication & Authorization**
   - [ ] JWT authentication
   - [ ] OAuth2 support (Google, GitHub)
   - [ ] Role-based access control
   - [ ] Session management
   - [ ] Password reset flow

3. **Frontend Enhancements**
   - [ ] State management solution
   - [ ] Form handling
   - [ ] More reusable components
   - [ ] Testing setup
   - [ ] Progressive Web App support

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
