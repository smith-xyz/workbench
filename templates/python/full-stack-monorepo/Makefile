.PHONY: help test test-cov test-watch lint lint-scripts lint-all dead-code format format-scripts format-all format-check format-check-all clean install dev-install update-deps add-dep add-dev-dep serve-backend build-frontend dev-frontend db-upgrade db-downgrade db-history seed-database

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# === Dependencies ===
install:  ## Install production dependencies
	uv sync --no-dev

dev-install:  ## Install development dependencies
	uv sync

update-deps:  ## Update all dependencies to latest versions
	uv lock --upgrade

add-dep:  ## Add a new dependency (usage: make add-dep DEP=package-name)
	uv add $(DEP)

add-dev-dep:  ## Add a new dev dependency (usage: make add-dev-dep DEP=package-name)
	uv add --dev $(DEP)

# === Testing ===
test:  ## Run all tests
	uv run pytest tests/

test-cov:  ## Run tests with coverage report
	uv run pytest tests/ --cov=core --cov=common --cov=backend --cov-report=term-missing --cov-report=html

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	uv run ptw -- tests/

test-integration:  ## Run only integration tests
	uv run pytest tests/test_integration.py -v

test-unit:  ## Run only unit tests (exclude integration)
	uv run pytest tests/ -v --ignore=tests/test_integration.py

# === Code Quality ===
lint:  ## Run linting with ruff
	uv run ruff check core/ common/ backend/ tests/

lint-scripts:  ## Run linting on scripts (optional)
	uv run ruff check scripts/

lint-all:  ## Run linting on all code including scripts
	uv run ruff check core/ common/ backend/ tests/ scripts/

dead-code:  ## Find dead code with vulture
	uv run vulture common core backend scripts tests --min-confidence 80

format:  ## Format code with ruff
	uv run ruff format core/ common/ backend/ tests/
	uv run ruff check --fix core/ common/ backend/ tests/

format-scripts:  ## Format scripts (optional)
	uv run ruff format scripts/
	uv run ruff check --fix scripts/

format-all:  ## Format all code including scripts
	uv run ruff format core/ common/ backend/ tests/ scripts/
	uv run ruff check --fix core/ common/ backend/ tests/ scripts/

format-check:  ## Check if code formatting is correct
	uv run ruff format --check core/ common/ backend/ tests/
	uv run ruff check core/ common/ backend/ tests/

format-check-all:  ## Check formatting on all code including scripts
	uv run ruff format --check core/ common/ backend/ tests/ scripts/
	uv run ruff check core/ common/ backend/ tests/ scripts/

# === Database ===
db-upgrade:  ## Run database migrations
	uv run alembic upgrade head

db-downgrade:  ## Downgrade database by one revision
	uv run alembic downgrade -1

db-history:  ## Show migration history
	uv run alembic history

seed-database:  ## Seed database with initial data (via Alembic migration)
	uv run alembic upgrade head

# === Backend ===
serve-backend:  ## Start the backend server
	uv run uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# === Frontend ===
build-frontend:  ## Build the React frontend for production
	cd frontend && yarn build

dev-frontend:  ## Start the React frontend in development mode
	cd frontend && yarn dev

install-frontend:  ## Install frontend dependencies
	cd frontend && yarn

# === Cleanup ===
clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

# === Development Shortcuts ===
dev: dev-install test lint  ## Full development setup and validation

ci: test-cov format-check lint  ## Run CI checks

full-stack: serve-backend dev-frontend  ## Start both backend and frontend

quick-test:  ## Quick test run (fastest tests only)
	uv run pytest tests/test_core.py -v
