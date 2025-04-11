help: ## Show help
	# From https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

up: ## Start the application
	docker compose up --build --remove-orphans --force-recreate -d

down: ## Stop the application
	docker compose down --volumes

build: ## Build the application
	docker compose build --no-cache

logs: ## Show logs
	docker compose logs -f 

clean: ## Clean the application
	docker compose down --volumes --remove-orphans --rmi all

test: ## Run tests
	docker compose run --rm api poetry run pytest

lint: ## Run linter
	docker compose run --rm api poetry run ruff check --show-fixes .

format: ## Run formatter
	docker compose run --rm api poetry run ruff format --check --diff .


local.process: up ## Run full process locally
	sleep 10
	poetry run typer importer.run run fetch 10 --api-url http://localhost:8000
	poetry run typer importer.run run process --num-processes 2 --api-url http://localhost:8000
	poetry run typer exporter.run run --api-url http://localhost:8000

