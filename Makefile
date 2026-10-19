NAME = call_me_maybe
SOURCE =
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/myp


all: install run

install:
	uv sync

run:
	uv run python -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:

lint-strict:
	$(FLAKE8) .
	$(MYPY) . --stric

.PHONY: install run dev debug clean lint lint-strict