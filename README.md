# Fork Notice

This fork enhances the original `blank-line-after-blocks` tool. It introduces
command-line options (`--after`, `--not-after`, `--compound`) for granular
control over block formatting and extends support to `def`, `class`, `match`
statements, and docstrings.

**Breaking Changes:**

- The default behavior now adds blank lines after `docstring`, `def`, `class`,
  and `match` blocks, in addition to the original `if`, `for`, `while`, `with`,
  and `try` blocks.
- The default behavior for compound statements (like `if/elif/else`) has
  changed to add blank lines between each part for consistent spacing.

To restore the original behavior, use the following command:

```bash
blank-line-after --not-after docstring,def,class,match --compound elif,else,except,finally <files>
```

______________________________________________________________________

# blank-line-after

A Python formatter to automatically add blank lines after code blocks to
improve readability. Fully customizable with `--after`, `--not-after`, and
`--compound` options.

<!--TOC-->

______________________________________________________________________

**Table of Contents**

- [blank-line-after](#blank-line-after)
  - [1. Installation](#1-installation)
  - [2. Usage](#2-usage)
    - [2.1. Command Line](#21-command-line)
    - [2.2. Customization Options](#22-customization-options)
    - [2.3. Pre-commit Hook](#23-pre-commit-hook)
    - [2.4. Configuration File](#24-configuration-file)
  - [3. What it does](#3-what-it-does)
  - [4. Examples](#4-examples)
    - [4.1. Default behavior](#41-default-behavior)
    - [4.2. Custom block types with --after](#42-custom-block-types-with---after)
    - [4.3. Exclude specific blocks with --not-after](#43-exclude-specific-blocks-with---not-after)
    - [4.4. Control compound statement spacing with --compound](#44-control-compound-statement-spacing-with---compound)
    - [4.5. Add blank lines after docstrings with --after docstring](#45-add-blank-lines-after-docstrings-with---after-docstring)
    - [4.6. Match/case statements (Python 3.10+)](#46-matchcase-statements-python-310)
    - [4.7. Async statements](#47-async-statements)

______________________________________________________________________

<!--TOC-->

## 1. Installation

```bash
pip install blank-line-after
```

## 2. Usage

### 2.1. Command Line

```bash
# Format Python files (default: adds blank lines after if/for/while/with/try)
blank-line-after file1.py file2.py

# Format Jupyter notebooks
blank-line-after-jupyter notebook1.ipynb notebook2.ipynb

# Format with exclude patterns (regex - use | for multiple patterns)
blank-line-after --exclude "tests/|_generated\.py$" src/
```

### 2.2. Customization Options

Control which blocks get blank lines and how compound statements are formatted:

```bash
# Only add blank lines after specific block types
blank-line-after --after if,for file.py
blank-line-after --after def,class file.py

# Add blank lines after ALL blocks EXCEPT specified ones
blank-line-after --not-after if,for file.py

# Control compound statement spacing (default: consistent spacing everywhere)
# Use --compound to keep certain compound statements tight
blank-line-after --compound elif,else file.py
blank-line-after --compound except,finally file.py

# Combine options (--after/--not-after are mutually exclusive)
blank-line-after --after def,class --compound elif,else file.py
```

**Available block types for `--after`/`--not-after`:**

- `if`, `for`, `while`, `with`, `try` (default blocks, includes `async for` and `async with`)
- `def` (functions, includes `async def`), `class` (classes)
- `match` (Python 3.10+ match statements)
- `docstring` (module/function/class docstrings)

**Available compound headers for `--compound`:**

- `elif`, `else`, `except`, `finally`, `case`

### 2.3. Pre-commit Hook

Add this to your `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/jsh9/blank-line-after
    rev: <LATEST_TAG>
    hooks:
      - id: blank-line-after
      - id: blank-line-after-jupyter
```

You can also pass customization options to pre-commit hooks:

```yaml
repos:
  - repo: https://github.com/jsh9/blank-line-after
    rev: <LATEST_TAG>
    hooks:
      - id: blank-line-after
        args: ["--after", "def,class", "--compound", "elif,else"]
      - id: blank-line-after
        args: ["--exclude", r"tests/|_generated\.py$"]
      - id: blank-line-after-jupyter
        args: ["--exclude", "notebooks/generated/"]
```

### 2.4. Configuration File

You can also configure exclude patterns in `pyproject.toml`:

```toml
[tool.blank-line-after]
exclude = [
    "tests/",            # Exclude all files in tests directory
    "_generated\.py$",   # Exclude files ending with _generated.py
    "vendor/",           # Exclude all files in vendor directory
    "build/",            # Exclude build directory
]
```

**Note**: CLI `--exclude` options take precedence over configuration file
settings.

## 3. What it does

By default, this tool adds one blank line after the end of `if`, `for`,
`while`, `with`, and `try` blocks to improve code readability.

**Key features:**

- **Customizable**: Use `--after` to specify exactly which blocks to format
- **Flexible**: Use `--not-after` to format all blocks except specific ones
- **Consistent spacing**: By default, adds blank lines after each branch in
  compound statements (if/elif/else, try/except/finally) for consistency
- **Compact mode**: Use `--compound` to keep compound statements tightly
  grouped

The tool supports these block types:

- Control flow: `if`, `for`, `while`, `with`, `try`
- Definitions: `def` (functions), `class` (classes)
- Pattern matching: `match` (Python 3.10+)
- Documentation: `docstring` (module/function/class docstrings)

## 4. Examples

### 4.1. Default behavior

Default adds blank lines after `if`, `for`, `while`, `with`, `try` blocks with
consistent spacing (blank lines after each branch):

```diff
  if a == 'a':
      depth += 1
+
  elif b == 'b':
      depth -= 1
+
  else:
      depth = 0
+
  j = 1
```

```diff
  for item in items:
      process(item)
+
  final_step()
```

```diff
  try:
      risky()
+
  except ValueError:
      handle()
+
  finally:
      cleanup()
+
  done()
```

### 4.2. Custom block types with --after

Only add blank lines after specific block types:

```bash
blank-line-after --after def,class file.py
```

```diff
  if x > 5:
      print("hello")
  def my_func():
      return 42
+
  class MyClass:
      pass
+
  print("world")
```

### 4.3. Exclude specific blocks with --not-after

Add blank lines after ALL blocks EXCEPT the specified ones:

```bash
blank-line-after --not-after if,for file.py
```

```diff
  if x > 5:
      print("hello")
  def my_func():
      return 42
+
  for i in range(10):
      print(i)
  while True:
      break
+
  print("world")
```

### 4.4. Control compound statement spacing with --compound

Keep compound statements tightly grouped:

```bash
blank-line-after --compound elif,else file.py
```

```diff
  if a == 'a':
      depth += 1
  elif b == 'b':
      depth -= 1
  else:
      depth = 0
+
  j = 1
```

```bash
blank-line-after --compound except,finally file.py
```

```diff
  try:
      risky()
  except ValueError:
      handle()
  finally:
      cleanup()
+
  done()
```

### 4.5. Add blank lines after docstrings with --after docstring

```bash
blank-line-after --after docstring file.py
```

```diff
  def my_func():
      """Function docstring."""
+
      return 42

  class MyClass:
      """Class docstring."""
+
      def method(self):
          pass
```

### 4.6. Match/case statements (Python 3.10+)

Default behavior adds blank lines after each `case` block:

```diff
  match status:
      case 200:
          success()
+
      case 404:
          not_found()
+
      case _:
          default()
+
  done()
```

Keep `case` blocks tightly grouped with `--compound case`:

```bash
blank-line-after --compound case file.py
```

```diff
  match status:
      case 200:
          success()
      case 404:
          not_found()
      case _:
          default()
+
  done()
```

### 4.7. Async statements

Async variants of `for` and `with` are automatically supported:

```diff
  async def process_items():
      async for item in async_iterator:
          await handle(item)
+
      async with aiofiles.open("file.txt") as f:
          content = await f.read()
+
      done()
```
