NAME		= call_me_maybe
GOINFRE		?= C:\Users\laflu\Desktop
TARGET =  src
export UV_PROJECT_ENVIRONMENT	?= $(GOINFRE)\$(NAME)\venv
export UV_CACHE_DIR		?= $(GOINFRE)\uv-cache
export UV_LINK_MODE		?= copy
export HF_HOME			?= $(GOINFRE)\huggingface

VENV		= $(UV_PROJECT_ENVIRONMENT)
LINT_TOOLS	= --with flake8 --with mypy
EXCLUDES	= llm_sdk,.venv,.git,__pycache__

all: install run

install:
	@mkdir -p $(dir $(VENV)) $(UV_CACHE_DIR) $(HF_HOME)
	@if [ -d .venv ] && [ ! -L .venv ]; then rm -rf .venv; fi
	uv sync
	@ln -sfn $(VENV) .venv

run:
	uv run python -m $(TARGET)

debug:
	uv run python -m pdb -m $(TARGET)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

fclean: clean
	rm -rf $(VENV) .venv

re: fclean install

lint:
	uv run $(LINT_TOOLS) flake8 . --exclude=$(EXCLUDES)
	uv run $(LINT_TOOLS) mypy . --exclude '(llm_sdk|\.venv)' \
		--warn-return-any --warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run $(LINT_TOOLS) flake8 . --exclude=$(EXCLUDES)
	uv run $(LINT_TOOLS) mypy . --exclude '(llm_sdk|\.venv)' \
		--strict --ignore-missing-imports

.PHONY: all install run debug clean fclean re lint lint-strict