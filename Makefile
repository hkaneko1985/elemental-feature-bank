PYTHON ?= python

.PHONY: validate
validate:
	$(PYTHON) scripts/validate_repository_snapshot.py --repo-root .

.PHONY: help
help:
	@echo "make validate  Run the public repository snapshot checks"
