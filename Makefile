.PHONY: install test validate run report

install:
	python -m venv .venv && .venv/bin/pip install -e ".[dev]"

test:
	.venv/bin/pytest -q

validate:
	.venv/bin/glmcompare validate

run:
	.venv/bin/glmcompare run --models sonnet glm --samples 1

report:
	.venv/bin/glmcompare report --run-id latest
