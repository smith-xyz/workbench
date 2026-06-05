# Makefile for Rust Web Service Template

# Variables
BINARY_NAME := web-service-template
DOCKER_IMAGE := $(BINARY_NAME)
DOCKER_TAG := latest
PORT := 3000

# Default target
.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Development targets
.PHONY: run
run: ## Run the application in development mode
	@echo "Starting web service on port $(PORT)..."
	RUST_LOG=info cargo run

.PHONY: dev
dev: ## Run with auto-reload (requires cargo-watch)
	@echo "Starting development server with auto-reload..."
	@if ! command -v cargo-watch >/dev/null 2>&1; then \
		echo "Installing cargo-watch..."; \
		cargo install cargo-watch; \
	fi
	RUST_LOG=debug cargo watch -x run

.PHONY: build
build: ## Build the application
	@echo "Building application..."
	cargo build

.PHONY: build-release
build-release: ## Build optimized release binary
	@echo "Building release binary..."
	cargo build --release

# Testing targets
.PHONY: test
test: ## Run tests
	@echo "Running tests..."
	cargo test

.PHONY: test-verbose
test-verbose: ## Run tests with verbose output
	@echo "Running tests with verbose output..."
	cargo test -- --nocapture

# Code quality targets
.PHONY: fmt
fmt: ## Format code
	@echo "Formatting code..."
	cargo fmt

.PHONY: fmt-check
fmt-check: ## Check code formatting
	@echo "Checking code formatting..."
	cargo fmt -- --check

.PHONY: lint
lint: ## Run linter (clippy)
	@echo "Running linter..."
	cargo clippy -- -D warnings

.PHONY: check
check: fmt-check lint test ## Run all checks (format, lint, test)

# Dependency management
.PHONY: deps
deps: ## Install dependencies
	@echo "Installing dependencies..."
	cargo fetch

.PHONY: deps-update
deps-update: ## Update dependencies
	@echo "Updating dependencies..."
	cargo update

# Docker targets
.PHONY: docker-build
docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

.PHONY: docker-run
docker-run: ## Run Docker container
	@echo "Running Docker container on port $(PORT)..."
	docker run -p $(PORT):$(PORT) $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: docker-shell
docker-shell: ## Run shell in Docker container
	@echo "Starting shell in Docker container..."
	docker run -it --rm $(DOCKER_IMAGE):$(DOCKER_TAG) /bin/bash

# Utility targets
.PHONY: clean
clean: ## Clean build artifacts
	@echo "Cleaning build artifacts..."
	cargo clean

.PHONY: install
install: ## Install binary to system
	@echo "Installing binary..."
	cargo install --path .

.PHONY: uninstall
uninstall: ## Uninstall binary from system
	@echo "Uninstalling binary..."
	cargo uninstall $(BINARY_NAME)

# Health check
.PHONY: health
health: ## Check if service is running
	@echo "Checking service health..."
	@curl -f http://localhost:$(PORT)/health || echo "Service is not running"

# Development utilities
.PHONY: logs
logs: ## Show application logs (if running via systemd or similar)
	@echo "Showing logs..."
	journalctl -u $(BINARY_NAME) -f

.PHONY: bench
bench: ## Run benchmarks
	@echo "Running benchmarks..."
	cargo bench

# CI/CD targets
.PHONY: ci
ci: deps check ## Run CI pipeline
	@echo "CI pipeline completed successfully"

.PHONY: pre-commit
pre-commit: fmt lint test ## Run pre-commit checks
	@echo "Pre-commit checks completed"

# Documentation
.PHONY: docs
docs: ## Generate documentation
	@echo "Generating documentation..."
	cargo doc --open

.PHONY: docs-deps
docs-deps: ## Generate documentation with dependencies
	@echo "Generating documentation with dependencies..."
	cargo doc --document-private-items --open

# Security
.PHONY: audit
audit: ## Run security audit
	@echo "Running security audit..."
	@if ! command -v cargo-audit >/dev/null 2>&1; then \
		echo "Installing cargo-audit..."; \
		cargo install cargo-audit; \
	fi
	cargo audit

# Performance
.PHONY: profile
profile: ## Run with profiling
	@echo "Running with profiling..."
	RUST_LOG=info cargo run --release

# Environment setup
.PHONY: setup
setup: ## Set up development environment
	@echo "Setting up development environment..."
	@rustup component add rustfmt clippy
	@cargo install cargo-watch cargo-audit
	@echo "Development environment ready!"

# Production deployment helper
.PHONY: deploy-prep
deploy-prep: build-release test ## Prepare for deployment
	@echo "Deployment preparation completed"
	@echo "Binary location: target/release/$(BINARY_NAME)"
	@echo "Binary size: $$(ls -lh target/release/$(BINARY_NAME) | awk '{print $$5}')" 