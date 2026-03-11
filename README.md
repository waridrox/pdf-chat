# PDF RAG Chat Application

A modern, full-featured PDF Chat application utilizing a Retrieval-Augmented Generation (RAG) architecture. Built with a FastAPI backend and a React 19 frontend, it allows users to upload PDF documents, process them into embeddings, and chat with their content in real-time.

## Features

- **Backend (FastAPI)**
  - Fast and modern Python web framework
  - PostgreSQL with `pgvector` for efficient vector similarity search
  - PDF Text Extraction & Processing (PyMuPDF)
  - Smart Token Chunking (tiktoken)
  - OpenAI Embeddings and Chat Models integration
  - Real-time WebSocket streaming for chat responses
  - Async database operations and proper connection pooling
  - Environment configuration with pydantic
  - Structured logging and modular architecture

- **Frontend (React 19)**
  - Real-time chat interface with WebSocket streaming
  - PDF document upload pipeline
  - Latest React features including the `use` hook
  - TypeScript for type safety
  - React Router 7 for client-side routing
  - shadcn/ui components for a beautiful, accessible UI
  - Tailwind CSS for modern styling
  - Vite for fast development

## Setup & Installation

### Using Docker (Recommended)

1. Clone the repository:

   ```bash
   git clone https://github.com/raythurman2386/fastapi-react-starter.git
   cd fastapi-react-starter
   ```

2. Create environment files:

   Create a `.env` file in the root directory (you can copy `.env.example` if available) and configure your database and OpenAI API key:

   ```env
   # Database Configuration
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_NAME=fastapi_db

   # OpenAI API Key for embeddings and chat model
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. Start the application with Docker Compose:

   ```bash
   docker compose up --build
   ```

   This will:
   - Start the PostgreSQL database with the necessary `pgvector` extension.
   - Apply migrations to a fresh database.
   - Start the FastAPI backend at http://localhost:8000
   - Start the React frontend at http://localhost:5173
   
   The Swagger API docs will be available at http://localhost:8000/docs.

### Manual Setup (Alternative)

#### 1. Backend Setup

a. Ensure you have PostgreSQL installed with the `pgvector` extension.

b. Create a `.env` file in the `backend/` directory:

```env
# Database Configuration
DB_NAME=fastapi_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CORS_ORIGINS=["http://localhost:5173"]
ENVIRONMENT=development

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here
```

c. Install Python dependencies and run the server:

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
uvicorn app.main:app --reload
```

#### 2. Frontend Setup

Ensure you are using a recent version of Node.js.

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at http://localhost:5173.

## Usage Guide

1. **Upload a PDF**: Navigate to the document upload section to ingest a new PDF. The backend system will extract text, chunk it intelligently, and generate vector embeddings using OpenAI.
2. **Chat**: Once ingested, you can easily open a chat session. The backend uses `pgvector` to perform similarity searches against the document embeddings and streams the prompt responses back to the UI via WebSockets for a snappy, real-time feel.

## Database Management Commands

The project includes several management wrapper commands (from within the `backend/` directory):

```bash
# Generate new database migrations
python manage.py makemigrations "description of changes"

# Apply pending migrations
python manage.py migrate

# Apply all migrations to a fresh database (runs 'alembic upgrade head')
python manage.py reset_db

# Check migration status
python manage.py db-status
```

If you encounter database errors using Docker and need a full reset:
1. Stop all services: `docker compose down`
2. Remove the volume: `docker volume rm fastapi-react-starter_postgres_data`
3. Restart services: `docker compose up -d --build`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
