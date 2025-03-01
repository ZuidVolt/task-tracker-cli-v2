PYTHON_FILES := main.py models.py

.PHONY: format ruff-check mypy-strict basedpyright-check check radon radon-mi vultures

# main check (Enforced before commit)

format:
	ruff format --preview --line-length 120 .

ruff-check:
	ruff check --fix --unsafe-fixes $(PYTHON_FILES)

mypy-check:
	mypy $(PYTHON_FILES)

basedpyright-check:
	basedpyright $(PYTHON_FILES)

check: format ruff-check mypy-check basedpyright-check

# Additional analysis checks (not Enforced)

radon: # cyclomatic complexity
	radon cc -a -nc -s $(PYTHON_FILES)

radon-mi: # maintainability index
	radon mi -s $(PYTHON_FILES)

vulture: # unused code
	vulture $(PYTHON_FILES) --min-confidence 80 --sort-by-size