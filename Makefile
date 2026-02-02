.PHONY: test test-cov clean install

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

test-specific:
	pytest tests/test_generators.py::TestCreditCardGenerator -v

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	python bot.py

all: install test run