# FastAPI React Starter Template

A modern, minimal starter template featuring FastAPI backend and React 19 frontend with Tailwind CSS.

## Features

- **Backend (FastAPI)**
  - Fast and modern Python web framework
  - CORS middleware configured
  - Modular project structure
  - Health check endpoint
  - Ready for database integration

- **Frontend (React 19)**
  - Latest React features including `use` hook
  - Native Fetch API integration
  - Modern error handling with Error Boundaries
  - Suspense for loading states
  - Tailwind CSS for styling
  - Vite for fast development

## Project Structure

```
fastapi-react-starter/
├── backend/
│   ├── app/
│   │   └── main.py         # FastAPI application
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container configuration
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   └── index.jsx     # React entry point
│   ├── package.json      # Node.js dependencies
│   └── Dockerfile       # Frontend container configuration
├── docker-compose.yml   # Docker services configuration
└── README.md           # Project documentation
```

## Quick Start

### Development

1. Backend Setup:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

2. Frontend Setup:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Docker Setup

Run both services using Docker Compose:
```bash
docker-compose up --build
```

Access the applications:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Environment Variables

### Frontend
Create `.env` in the frontend directory:
```env
VITE_API_URL=http://localhost:8000
```

## Roadmap

### Planned Features

1. **Database Integration**
   - [ ] Initial SQLite setup with SQLAlchemy
   - [ ] Support for multiple database backends (PostgreSQL, MySQL)
   - [ ] Database migration system
   - [ ] Connection pooling
   - [ ] Database configuration via environment variables
   - [ ] Basic CRUD operations
   - [ ] Data models and schemas

2. **Authentication & Authorization**
   - [ ] JWT authentication
   - [ ] OAuth2 support (Google, GitHub)
   - [ ] Role-based access control
   - [ ] Session management
   - [ ] Password reset flow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
