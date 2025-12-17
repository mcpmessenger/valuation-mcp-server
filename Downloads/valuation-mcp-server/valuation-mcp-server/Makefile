.PHONY: help install test run build deploy clean lint format

help:
	@echo "Valuation MCP Server - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make install       - Install dependencies"
	@echo "  make run          - Run the server locally"
	@echo "  make test         - Run unit tests"
	@echo "  make lint         - Run code linting"
	@echo "  make format       - Format code with black"
	@echo ""
	@echo "Docker & Deployment:"
	@echo "  make build        - Build Docker image"
	@echo "  make deploy       - Deploy to GCP Cloud Run"
	@echo "  make clean        - Clean up Docker images and cache"

install:
	pip install -r requirements.txt

run:
	python src/main.py

test:
	pytest tests/ -v

lint:
	pylint src/ tests/ || true

format:
	black src/ tests/ || true

build:
	docker build -t valuation-mcp-server:latest .

deploy:
	chmod +x deploy-gcp.sh
	./deploy-gcp.sh

clean:
	docker system prune -a --force
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/
