# Makefile generated with pymakefile
help:
	@grep -E '^[A-Za-z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "[36m%-30s[0m %s\n", $$1, $$2}'

lint:  ## lint fix
	black .
	isort . --profile black
	flake8 .

lint-check: ## lint check
	black . --check
	isort . --check-only --profile black
	flake8 .
