# Python Full-Stack Monorepo Starter

> **Note:** This is a **starter kit**, not a minimal scaffold. It provides a fully wired FastAPI + React + SQLAlchemy stack with migrations, tooling, and frontend build pipeline. Clone when you want a production-shaped monorepo from day one.

A modern Python full-stack application starter featuring FastAPI backend, React frontend, SQLAlchemy ORM, and comprehensive development tooling.

## Features

- **Backend**: FastAPI with async support
- **Database**: SQLAlchemy 2.0 with Alembic migrations
- **Frontend**: React SPA (TypeScript)
- **Package Management**: UV for fast Python dependency management
- **Code Quality**: Ruff for linting and formatting, Vulture for dead code detection
- **Testing**: Pytest with coverage reporting
- **Development**: Hot reload, comprehensive Makefile, modular architecture

## Project Structure

```
.
├── backend/           # FastAPI backend application
├── common/            # Shared utilities and models
├── core/              # Core business logic modules
├── frontend/          # React SPA application
├── scripts/           # Utility scripts
├── tests/             # Test suite
├── alembic/           # Database migrations
├── Makefile           # Development commands
└── pyproject.toml     # Python dependencies and configuration
```

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+ (for frontend)
- UV package manager (`pip install uv`)

### Setup
```bash
# Install Python dependencies
make dev-install

# Install frontend dependencies
make install-frontend

# Set up database
make db-upgrade
make seed-database

# Start development servers
make full-stack  # Starts both backend and frontend
```

### Development

```bash
# Backend only
make serve-backend

# Frontend only
make dev-frontend

# Run tests
make test
make test-cov

# Code quality
make lint
make format
make dead-code

# Database operations
make db-upgrade
make db-downgrade
make db-history
```

## Development Workflow

1. **Install dependencies**: `make dev-install`
2. **Run tests**: `make test`
3. **Format code**: `make format`
4. **Run linting**: `make lint`
5. **Start servers**: `make full-stack`

## Architecture

### Backend (FastAPI)
- RESTful API with automatic OpenAPI documentation
- Async/await support for database operations
- Pydantic models for request/response validation
- SQLAlchemy 2.0 for database operations

### Frontend (React)
- TypeScript for type safety
- Modern React with hooks
- API client integration
- Component-based architecture

### Database
- SQLAlchemy 2.0 with async support
- Alembic for database migrations
- Pydantic models for data validation

### Code Organization
- `common/`: Shared utilities, models, and database configuration
- `core/`: Business logic modules
- `backend/`: FastAPI application and API routes
- `frontend/`: React SPA application

## Available Commands

Run `make help` to see all available commands:

```bash
make help
```

## Configuration

- Python configuration in `pyproject.toml`
- Database configuration in `alembic.ini`
- Frontend configuration in `frontend/package.json`
- Environment variables in `.env` (create from `.env.example`)

## Testing

- Unit tests in `tests/`
- Integration tests included
- Coverage reporting with HTML output
- Watch mode for continuous testing

```bash
make test-cov    # Run with coverage
make test-watch  # Watch mode
```

## Deployment

```bash
# Build for production
make build-frontend

# Run production backend
uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000
```
