# Change Log

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- Added
  - **`--after` option**: Specify exactly which block types to add blank lines
    after (e.g., `--after if,for` or `--after def,class`)
  - **`--not-after` option**: Add blank lines after all blocks EXCEPT the
    specified ones (e.g., `--not-after if,for`)
  - **`--compound` option**: Control spacing before compound statement headers
    (e.g., `--compound elif,else,except,finally,case`)
  - Support for `def` (function definitions) and `class` (class definitions)
    blocks
  - Support for `match` statements (Python 3.10+) with blank lines after each
    `case` block by default. Use `--compound case` to keep case blocks tightly
    grouped.
  - Support for `docstring` (module/function/class docstrings)
  - Support for `async for` and `async with` statements (automatically included
    with `for` and `with` keywords)
- Changed
  - **BREAKING**: Default behavior now adds blank lines after each branch in
    compound statements (if/elif/else, try/except/finally) for consistent
    spacing. Use `--compound elif,else,except,finally` to restore the previous
    tight grouping behavior.
  - `--after` and `--not-after` are mutually exclusive options
  - `--compound` defaults to empty (consistent spacing) instead of excluding
    compound headers

## [0.1.5] - 2025-10-25

- Changed
  - Updated linter and auto formatter configs. No actual functionality changes
- Full diff
  - https://github.com/jsh9/blank-line-after/compare/0.1.4...0.1.5

## [0.1.4] - 2025-09-03

- Changed
  - Formatter no longer inserts a blank line before the second part of compound
    blocks (`else/elif/except/finally`). This avoids awkward spacing like a
    blank line before `else:` and keeps compound statements visually tight.
- Added
  - `--version` flag for both CLIs (`blank-line-after` and
    `blank-line-after-jupyter`) to print the tool version.
- Full diff
  - https://github.com/jsh9/blank-line-after/compare/0.1.3...0.1.4

## [0.1.3] - 2025-09-02

- Fixed
  - Exclude functionality now works correctly for single files in pre-commit
    hooks
- Added
  - Tests for single file exclusion scenarios
- Full diff
  - https://github.com/jsh9/blank-line-after/compare/0.1.2...0.1.3

## [0.1.2] - 2025-09-01

- Added
  - A config option `--exclude` to exclude certain directories/files
- Removed
  - An unnecessary config option `--exit-zero-even-if-changed`
- Full diff
  - https://github.com/jsh9/blank-line-after/compare/0.1.1...0.1.2

## [0.1.1] - 2025-08-27

- Changed
  - Refactor code & add test cases
- Fixed
  - File path for Windows
- Full diff
  - https://github.com/jsh9/blank-line-after/compare/0.1.0...0.1.1

## [0.1.0] - 2025-08-27

- Added
  - Initial release of blank-line-after formatter
  - Core functionality to add blank lines after code blocks (if, for, while,
    with, try/except, etc.)
  - Support for Python (.py) files
  - Support for Jupyter notebooks (.ipynb)
  - Command-line interface for processing files and directories
  - Pre-commit hook integration
  - Comprehensive test suite with test data for various scenarios
  - Configuration support via pyproject.toml and tox.ini
  - Development dependencies and tooling setup
- Full diff
  - N/A
