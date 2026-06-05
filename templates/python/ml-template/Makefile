.PHONY: help test test-cov test-watch lint format format-check clean install dev-install update-deps add-dep add-dev-dep jupyter lab notebook train evaluate serve experiments data-check

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

# === ML Commands ===
train-linear:  ## Train linear regression model
	uv run ml train linear_regression

train-logistic:  ## Train logistic regression model  
	uv run ml train logistic_regression

train-rf:  ## Train random forest model
	uv run ml train random_forest

models:  ## List available models
	uv run ml list-models

# === Testing ===
test:  ## Run all tests (excluding slow and GPU tests)
	uv run pytest tests/ -m "not slow and not gpu"

test-all:  ## Run all tests including slow ones
	uv run pytest tests/

test-cov:  ## Run tests with coverage report
	uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -m "not slow and not gpu"

test-watch:  ## Run tests in watch mode
	uv run pytest-watch -- tests/ -m "not slow and not gpu"

test-gpu:  ## Run GPU-specific tests (requires CUDA)
	uv run pytest tests/ -m gpu

# === Code Quality ===
lint:  ## Run linting with ruff
	uv run ruff check src/ tests/ notebooks/

format:  ## Format code with ruff
	uv run ruff format src/ tests/ notebooks/
	uv run ruff check --fix src/ tests/ notebooks/

format-check:  ## Check if code formatting is correct
	uv run ruff format --check src/ tests/ notebooks/
	uv run ruff check src/ tests/ notebooks/

# === Jupyter ===
jupyter:  ## Start Jupyter Notebook server
	uv run jupyter notebook

lab:  ## Start JupyterLab server
	uv run jupyter lab

notebook: jupyter  ## Alias for jupyter command

# === ML Workflows ===
train:  ## Train a model (usage: make train MODEL=linear_regression)
	uv run ml train $(or $(MODEL),linear_regression)

evaluate:  ## Evaluate a trained model
	uv run ml evaluate $(or $(MODEL),linear_regression)

serve:  ## Start model serving API
	uv run ml serve $(or $(MODEL),linear_regression) --port $(or $(PORT),8000)

experiments:  ## Start MLflow UI for experiment tracking
	uv run mlflow ui --host 0.0.0.0 --port $(or $(PORT),5000)

hyperopt:  ## Run hyperparameter optimization
	uv run ml hyperopt $(or $(MODEL),linear_regression) --trials $(or $(TRIALS),50)

# === Data Management ===
data-check:  ## Validate data integrity and schema
	uv run python -m src.data.validation

data-download:  ## Download sample datasets
	uv run python -m src.data.download

data-preprocess:  ## Run data preprocessing pipeline
	uv run python -m src.data.preprocessing

# === Development Utilities ===
setup-git-hooks:  ## Set up pre-commit hooks
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	find . -type d -name "mlruns" -exec rm -rf {} +
	find . -name "*.ipynb" -exec uv run nbstripout {} +

clean-data:  ## Clean processed data files
	rm -rf data/processed/*
	rm -rf data/interim/*

# === Development Shortcuts ===
dev: dev-install setup-git-hooks test lint  ## Full development setup and validation

ci: test-cov format-check lint  ## Run CI checks

quick-test:  ## Quick test run (fastest tests only)
	uv run pytest tests/test_models.py::TestLinearRegression -v

notebook-clean:  ## Clean all notebook outputs
	find . -name "*.ipynb" -exec uv run nbstripout {} +

# === Docker ===
docker-build:  ## Build Docker image
	docker build -t ml-template .

docker-run:  ## Run Docker container
	docker run -p 8000:8000 ml-template

docker-jupyter:  ## Run Jupyter in Docker
	docker run -p 8888:8888 -v $(PWD):/workspace ml-template jupyter lab --ip=0.0.0.0 --allow-root
