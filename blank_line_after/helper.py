from __future__ import annotations

import ast
import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

# Mapping of keywords to AST node types
KEYWORD_TO_AST = {
    'if': (ast.If,),
    'for': (ast.For,),
    'while': (ast.While,),
    'with': (ast.With,),
    'try': (ast.Try,),
    'def': (ast.FunctionDef, ast.AsyncFunctionDef),
    'class': (ast.ClassDef,),
    'match': (ast.Match,) if hasattr(ast, 'Match') else (),
    'docstring': (),  # Special case: handled separately
}

# Mapping of keywords to compound headers
KEYWORD_TO_HEADERS = {
    'elif': 'elif ',
    'else': 'else:',
    'except': 'except',
    'finally': 'finally:',
}

DEFAULT_BLOCKS = ('if', 'for', 'while', 'with', 'try', 'docstring', 'def', 'class', 'match')


def fix_src(
    source_code: str,
    after: tuple[str, ...] | None = None,
    not_after: tuple[str, ...] | None = None,
    compound: tuple[str, ...] = (),
) -> str:
    """Add blank lines after specified blocks."""
    try:
        tree = ast.parse(source=source_code)
    except SyntaxError:
        # Ignore syntax errors (e.g., Jupyter cells with ipython magics)
        return source_code

    # Determine which blocks to process
    if after:
        block_keywords = after
    elif not_after:
        # All blocks except the ones listed
        all_blocks = set(KEYWORD_TO_AST.keys())
        block_keywords = tuple(all_blocks - set(not_after))
    else:
        block_keywords = DEFAULT_BLOCKS

    # Determine which compound headers to exclude
    excluded_headers = tuple(
        KEYWORD_TO_HEADERS[kw] for kw in compound if kw in KEYWORD_TO_HEADERS
    )

    # Find all block statements that need blank lines after them
    blocks_to_fix = _collect_blocks_to_fix(tree, block_keywords)

    if not blocks_to_fix:
        return source_code

    # Split source into lines and add blank lines
    lines = source_code.splitlines(keepends=True)
    return _add_blank_lines(lines, blocks_to_fix, excluded_headers)


def _get_docstring_end_lines(tree: ast.Module) -> set[int]:
    """Get line numbers where docstrings end."""
    docstring_ends = set()

    def _is_docstring(node: ast.stmt, body: list[ast.stmt]) -> bool:
        """Check if node is a docstring (first statement that's a string)."""
        return (
            body
            and body[0] is node
            and isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        )

    # Module-level docstring
    if _is_docstring(tree.body[0], tree.body) if tree.body else False:
        if hasattr(tree.body[0], 'end_lineno') and tree.body[0].end_lineno:
            docstring_ends.add(tree.body[0].end_lineno)

    # Function and class docstrings
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef):
            if node.body and _is_docstring(node.body[0], node.body):
                if (
                    hasattr(node.body[0], 'end_lineno')
                    and node.body[0].end_lineno
                ):
                    docstring_ends.add(node.body[0].end_lineno)

    return docstring_ends


def _collect_blocks_to_fix(
    tree: ast.Module, block_keywords: tuple[str, ...]
) -> set[int]:
    """Collect line numbers where blank lines should be added after blocks."""
    blocks_to_fix = set()

    # Handle docstrings separately
    if 'docstring' in block_keywords:
        blocks_to_fix.update(_get_docstring_end_lines(tree))

    # Build block_types from keywords (excluding docstring)
    block_types = []
    for keyword in block_keywords:
        if keyword in KEYWORD_TO_AST and keyword != 'docstring':
            block_types.extend(KEYWORD_TO_AST[keyword])

    if not block_types:
        return blocks_to_fix

    block_types = tuple(block_types)

    for node in ast.walk(tree):
        if isinstance(node, block_types):
            # Handle if/elif/else chains specially
            if isinstance(node, ast.If):
                # Add blank line after the if/elif body
                if (
                    node.body
                    and hasattr(node.body[-1], 'end_lineno')
                    and node.body[-1].end_lineno is not None
                ):
                    blocks_to_fix.add(node.body[-1].end_lineno)
                # Add blank line after else clause (if it's not another if/elif)
                if (
                    hasattr(node, 'orelse')
                    and node.orelse
                    and not isinstance(node.orelse[0], ast.If)
                ):
                    if (
                        hasattr(node.orelse[-1], 'end_lineno')
                        and node.orelse[-1].end_lineno is not None
                    ):
                        blocks_to_fix.add(node.orelse[-1].end_lineno)
            # Handle compound statements (for-else, while-else) specially
            elif (
                isinstance(node, ast.For | ast.While)
                and hasattr(node, 'orelse')
                and node.orelse
            ):
                # Add blank line after main body
                if (
                    node.body
                    and hasattr(node.body[-1], 'end_lineno')
                    and node.body[-1].end_lineno is not None
                ):
                    blocks_to_fix.add(node.body[-1].end_lineno)
                # Add blank line after else clause
                if (
                    hasattr(node.orelse[-1], 'end_lineno')
                    and node.orelse[-1].end_lineno is not None
                ):
                    blocks_to_fix.add(node.orelse[-1].end_lineno)
            # For other blocks, add blank line after entire construct
            elif hasattr(node, 'end_lineno') and node.end_lineno is not None:
                blocks_to_fix.add(node.end_lineno)

    return blocks_to_fix


def _add_blank_lines(
    lines: list[str],
    blocks_to_fix: set[int],
    excluded_headers: tuple[str, ...] = (),
) -> str:
    """Add blank lines after specified line numbers."""
    result = []

    for i, line in enumerate(lines):
        result.append(line)
        current_line_num = i + 1

        if current_line_num in blocks_to_fix:  # noqa: SIM102
            # Check if next line exists and is not already blank
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Do not insert a blank line before excluded compound headers
                if (
                    next_line
                    and not next_line.startswith(('#', '"""', "'''"))
                    and not next_line.startswith(excluded_headers)
                ):
                    result.append('\n')

    return ''.join(result)


def should_exclude_file(file_path: Path, exclude_pattern: str) -> bool:
    """Check if a file should be excluded based on the regex pattern."""
    if not exclude_pattern:
        return False

    try:
        exclude_regex = re.compile(exclude_pattern)
        return bool(exclude_regex.search(file_path.as_posix()))
    except re.error:
        # Invalid regex pattern, don't exclude anything
        return False
