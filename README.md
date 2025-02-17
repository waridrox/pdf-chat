# FastAPI React Starter Template

A modern, full-featured starter template featuring FastAPI backend and React 19 frontend with TypeScript, Tailwind CSS, and shadcn/ui components.

## Features

- **Backend (FastAPI)**
  - Fast and modern Python web framework
  - PostgreSQL/SQLite database with async SQLAlchemy ORM
  - JWT-based authentication system
  - Role-based access control
  - Async database operations
  - Proper connection pooling and cleanup
  - Environment configuration with pydantic
  - Structured logging
  - Health check endpoint
  - Graceful shutdown handling
  - Modular project structure

- **Frontend (React 19)**
  - Latest React features including `use` hook
  - TypeScript for type safety and better developer experience
  - React Router 7 for client-side routing
  - shadcn/ui components for beautiful, accessible UI
  - Component-based architecture
  - Custom hooks for data fetching
  - Modern error handling with Error Boundaries
  - Suspense for loading states
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
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   └── health.py       # Health check endpoint
│   │   ├── schemas/            # Pydantic models
│   │   │   ├── __init__.py
│   │   │   └── auth.py        # Authentication schemas
│   │   ├── services/          # Business logic
│   │   │   ├── __init__.py
│   │   │   └── auth.py       # Authentication services
│   │   └── utils/            # Utilities
│   │       ├── __init__.py
│   │       └── logger.py     # Logging configuration
│   ├── .env                  # Environment variables
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   │   └── ui/          # shadcn/ui components
│   │   │       ├── button.tsx
│   │   │       ├── card.tsx
│   │   │       └── status-dot.tsx
│   │   ├── features/         # Feature modules
│   │   │   ├── auth/        # Authentication feature
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   └── health/      # Health check feature
│   │   │       └── HealthStatus.tsx
│   │   ├── hooks/           # Custom React hooks
│   │   │   ├── useAuth.ts
│   │   │   └── useHealthStatus.ts
│   │   ├── layouts/         # Page layouts
│   │   │   └── MainLayout.tsx
│   │   ├── lib/             # Utility functions and configurations
│   │   │   └── utils.ts
│   │   ├── routes/          # Route components and configurations
│   │   │   └── root.tsx
│   │   ├── types/           # TypeScript type definitions
│   │   │   └── index.d.ts
│   │   └── App.tsx          # Main React component
│   ├── .env                 # Frontend environment variables
│   └── package.json         # Node.js dependencies
└── README.md               # Project documentation
```

## Quick Start

### Development

1. Backend Setup:

   First, create a `.env` file in the backend directory:
   ```env
   # Database Configuration (PostgreSQL)
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432

   # JWT Configuration
   JWT_SECRET_KEY=your-secret-key-for-production
   ```

   If you don't set database credentials, it will fall back to SQLite.

   Then set up the Python environment:
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

   The backend will be available at http://localhost:8000
   - API documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

2. Frontend Setup:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   The frontend will be available at http://localhost:5173

### Authentication System

The template includes a complete JWT-based authentication system with the following features:

- User registration with email and username
- Email-based login
- JWT token generation and validation
- Role-based access control (user, admin, moderator)
- Password reset functionality
- Email verification support (ready to implement)

### Database Support

The template supports both SQLite and PostgreSQL:

1. **SQLite** (Default):
   - No configuration needed
   - Great for development and small projects
   - Database file: `app.db` in the backend directory

2. **PostgreSQL**:
   - Production-ready, scalable database
   - Async support with asyncpg
   - Connection pooling and proper cleanup
   - Configure through environment variables

To use PostgreSQL, set the database environment variables in `.env` and ensure PostgreSQL is running.

### Frontend Components

The template uses shadcn/ui, a collection of beautifully designed, accessible components:

- Fully styled with Tailwind CSS
- Dark mode support
- TypeScript integration
- Customizable themes
- Accessible by default
- Easy to extend and modify

To add new shadcn/ui components:
```bash
cd frontend
npx shadcn-ui@latest add button
# Replace 'button' with any component name
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
