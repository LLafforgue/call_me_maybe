NAME		= call_me_maybe

# --- Stockage dans le goinfre (le home 42 est limite en quota) ---------------
# Surchargeable : make install GOINFRE=/goinfre/autre_login
GOINFRE		?= /goinfre/llafforg

export UV_PROJECT_ENVIRONMENT	?= $(GOINFRE)/$(NAME)/venv
export UV_CACHE_DIR		?= $(GOINFRE)/uv-cache
export UV_LINK_MODE		?= copy
export HF_HOME			?= $(GOINFRE)/huggingface

VENV		= $(UV_PROJECT_ENVIRONMENT)
LINT_TOOLS	= --with flake8 --with mypy
EXCLUDES	= llm_sdk,.venv,.git,__pycache__

all: install run

# Cree le venv dans le goinfre et laisse un lien .venv dans le projet
# (pour que uv / les IDE le retrouvent sans rien configurer).
install:
	@mkdir -p $(dir $(VENV)) $(UV_CACHE_DIR) $(HF_HOME)
	@if [ -d .venv ] && [ ! -L .venv ]; then rm -rf .venv; fi
	uv sync
	@ln -sfn $(VENV) .venv

run:
	uv run python -m src

debug:
	uv run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache

# Supprime aussi le venv du goinfre (le cache uv et le modele HF sont conserves)
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