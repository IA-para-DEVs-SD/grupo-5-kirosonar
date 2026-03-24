.PHONY: help dev dev-down dev-logs dev-build dev-rebuild lint format test test-watch test-coverage clean

help:
	@echo "ERP Gráficas Expressas - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev              - Start development environment"
	@echo "  make dev-down         - Stop development environment"
	@echo "  make dev-logs         - View development logs"
	@echo "  make dev-build        - Build Docker images"
	@echo "  make dev-rebuild      - Rebuild and restart everything"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             - Run ESLint"
	@echo "  make format           - Format code with Prettier"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run tests"
	@echo "  make test-watch       - Run tests in watch mode"
	@echo "  make test-coverage    - Run tests with coverage"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Remove build artifacts and node_modules"

dev:
	npm run dev

dev-down:
	npm run dev:down

dev-logs:
	npm run dev:logs

dev-build:
	npm run dev:build

dev-rebuild:
	npm run dev:rebuild

lint:
	npm run lint

format:
	npm run format

test:
	npm test

test-watch:
	npm test:watch

test-coverage:
	npm test:coverage

clean:
	npm run clean
	docker-compose down -v
