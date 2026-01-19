# AGENTS.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## 1. Project Overview

This is a Python formatter called `blank-line-after` that automatically
adds blank lines after code blocks to improve readability. The tool is fully
customizable with `--after`, `--not-after`, and `--compound` options to control
which blocks are formatted and how compound statements are spaced.

By default, it formats `if`, `for`, `while`, `with`, and `try` blocks, but can
also handle `def` (functions), `class` (classes), and `match` statements.

The project supports both Python source files (.py) and Jupyter notebooks
(.ipynb).

## 2. Commands

### 2.1. Testing

- Run all tests: `python -m pytest tests/ -v`
- Run specific test files:
  - `python -m pytest tests/test_helper.py -v`
  - `python -m pytest tests/test_main_py.py -v`
  - `python -m pytest tests/test_base_fixer.py -v`
  - `python -m pytest tests/test_main_jupyter.py -v`
  - `python -m pytest tests/test_integration.py -v`
  - `python -m pytest tests/test_end_to_end.py -v`
- Run with coverage:
  `python -m pytest tests/ --cov=blank_line_after --cov-report=term-missing`
- Run tox for multi-environment testing: `tox`

### 2.2. Code Quality

- Type checking: `mypy blank_line_after/`
- Format code: `muff format --config=muff.toml blank_line_after tests`
- Check formatting (without modifying):
  `muff format --diff --config=muff.toml blank_line_after tests`
- Linting: `flake8 .`
- Pre-commit hooks: `pre-commit run -a`

### 2.3. Manual Tool Testing

- Format Python files (default): `blank-line-after file1.py file2.py`
- Format only specific blocks: `blank-line-after --after def,class file.py`
- Add blank lines after docstrings: `blank-line-after --after docstring file.py`
- Format all except specific blocks:
  `blank-line-after --not-after if,for file.py`
- Keep compound statements tight:
  `blank-line-after --compound elif,else,except,finally file.py`
- Format with exclusions:
  `blank-line-after --exclude "tests/|_generated\.py$" src/`
- Format Jupyter notebooks: `blank-line-after-jupyter notebook.ipynb`
- Combine options:
  `blank-line-after --after def,class --compound elif,else file.py`

## 3. Architecture

### 3.1. Core Components

1. **Base Architecture**: Uses inheritance with `BaseFixer` as the base class
   that handles common file processing logic

   - `BaseFixer` (base_fixer.py): Abstract base class for file processing and
     exclusion logic
   - `PythonFileFixer` (main_py.py): Concrete implementation for Python source
     files
   - `JupyterFileFixer` (main_jupyter.py): Concrete implementation for Jupyter
     notebooks

2. **Core Logic**: The actual formatting logic is in `helper.py`:
   - `fix_src()`: Main function that processes Python source code with optional
     `after`, `not_after`, and `compound` parameters
   - `KEYWORD_TO_AST`: Maps block keywords to AST node types
   - `KEYWORD_TO_HEADERS`: Maps compound keywords to their header strings
   - `DEFAULT_BLOCKS`: Default block types (if, for, while, with, try)

3. **Configuration**: File exclusion patterns handled in `config.py` using
   regex matching

4. **Entry Points**: Two CLI commands defined in pyproject.toml:

   - `blank-line-after` → `main_py:main`
   - `blank-line-after-jupyter` → `main_jupyter:main`

### 3.2. Key Design Patterns

- **Template Method Pattern**: `BaseFixer` defines the file processing
  workflow, subclasses implement `fix_one_file()`
- **Strategy Pattern**: Different fixers for Python files vs Jupyter notebooks
- **Single Responsibility**: Each module has a clear focus (config, helpers,
  file processing)

### 3.3. Dependencies

- `click` for CLI interface
- `jupyter-notebook-parser>=0.1.4` for Jupyter notebook processing
- Development dependencies include pytest, mypy, pre-commit, tox

## 4. Configuration

### 4.1. Block Selection

Choose which blocks to format:

1. **`--after`**: Only add blank lines after specific block types
   - Example: `--after if,for` (only if and for blocks)
   - Example: `--after def,class` (only function and class definitions)

2. **`--not-after`**: Add blank lines after all blocks EXCEPT specified ones
   - Example: `--not-after if,for` (all blocks except if and for)
   - Mutually exclusive with `--after`

3. **Default**: `if`, `for`, `while`, `with`, `try` blocks

**Available block types**: `if`, `for`, `while`, `with`, `try`, `def`, `class`,
`match`, `docstring`

### 4.2. Compound Statement Spacing

Control spacing before compound statement headers:

- **`--compound`**: Don't add blank lines before these headers
  - Example: `--compound elif,else` (keep if/elif/else tightly grouped)
  - Example: `--compound except,finally` (keep try/except/finally tight)
  - Default: empty (adds blank lines everywhere for consistency)

**Available compound headers**: `elif`, `else`, `except`, `finally`

### 4.3. File Exclusion

Exclude files/directories via:

1. CLI `--exclude` flag (takes precedence)
2. `pyproject.toml` configuration:
   ```toml
   [tool.blank-line-after]
   exclude = ["tests/", "_generated\.py$", "vendor/", "build/"]
   ```

## 5. Python Coding Style

- Always add type hints where appropriate
- Use "modern" type hints (such as "dict" instead of "typing.Dict")
- Use absolute import instead of relative import
- Code formatted with muff (line length 79, single quotes)
- Strict mypy type checking enabled
- Comprehensive flake8 linting with multiple plugins
