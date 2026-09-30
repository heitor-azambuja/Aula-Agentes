.PHONY: install test lint check run

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest

lint:
	python -m ruff check .

check: lint test

run:
	python run.py
