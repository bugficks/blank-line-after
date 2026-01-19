# This file is inspired by
# https://github.com/asottile/add-trailing-comma/blob/6be6dfc05176bddfc05176bddfc5a9c4bf0fd4941850f0fb41/add_trailing_comma/_main.py

import sys
from pathlib import Path

# Add the parent directory to the path to allow relative imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import click

from blank_line_after import __version__, helper
from blank_line_after.base_fixer import BaseFixer


class PythonFileFixer(BaseFixer):
    """Fixer for Python source files."""

    def __init__(
            self,
            path: str,
            exclude_pattern: str = r'\.git|\.tox|\.pytest_cache',
            after: tuple[str, ...] | None = None,
            not_after: tuple[str, ...] | None = None,
            compound: tuple[str, ...] = (),
    ) -> None:
        super().__init__(path=path, exclude_pattern=exclude_pattern)
        self.after = after
        self.not_after = not_after
        self.compound = compound

    def fix_one_file(self, filename: str) -> int:
        """Fix formatting in a single Python file."""
        if filename == '-':
            source_bytes = sys.stdin.buffer.read()
        else:
            file_path = Path(filename)
            if not file_path.is_file():
                msg = f'{filename} is not a file (skipping)'
                print(msg, file=sys.stderr)
                return 0

            source_bytes = Path(filename).read_bytes()

        try:
            source_text_orig = source_text = source_bytes.decode()
        except UnicodeDecodeError:
            msg = f'{filename} is non-utf-8 (not supported)'
            print(msg, file=sys.stderr)
            return 1

        source_text = helper.fix_src(
            source_text,
            after=self.after,
            not_after=self.not_after,
            compound=self.compound,
        )

        if filename == '-':
            print(source_text, end='')
        elif source_text != source_text_orig:
            print(f'Rewriting {filename}', file=sys.stderr)
            Path(filename).write_bytes(source_text.encode())

        return source_text != source_text_orig


@click.command()
@click.version_option(version=__version__)
@click.argument('paths', nargs=-1, type=click.Path())
@click.option(
    '--exclude',
    type=str,
    default=r'\.git|\.tox|\.pytest_cache',
    help='Regex pattern to exclude files/directories',
)
@click.option(
    '--after',
    type=str,
    help='Comma-separated list of block types to add blank lines after '
    '(e.g., if,for,while,with,try,def,class,match,docstring)',
)
@click.option(
    '--not-after',
    type=str,
    help='Add blank lines after all blocks EXCEPT these '
    '(e.g., if,for - adds after everything except if and for)',
)
@click.option(
    '--compound',
    type=str,
    default='',
    help=(
        'Comma-separated list of compound headers to NOT add blank lines '
        'before (e.g., elif,else,except,finally). '
        'Default: empty (consistent spacing)'
    ),
)
def main(
        paths: tuple[str, ...],
        exclude: str,
        after: str | None,
        not_after: str | None,
        compound: str,
) -> None:
    """Add blank lines after blocks in Python files."""
    # Validate mutual exclusivity
    if after and not_after:
        msg = '--after and --not-after are mutually exclusive'
        raise click.BadParameter(msg)

    # Parse comma-separated values
    after_tuple = tuple(after.split(',')) if after else None
    not_after_tuple = tuple(not_after.split(',')) if not_after else None
    compound_tuple = tuple(compound.split(',')) if compound else ()

    ret = 0
    for path in paths:
        fixer = PythonFileFixer(
            path=path,
            exclude_pattern=exclude,
            after=after_tuple,
            not_after=not_after_tuple,
            compound=compound_tuple,
        )
        ret |= fixer.fix_one_directory_or_one_file()

    if ret != 0:
        raise SystemExit(ret)


if __name__ == '__main__':
    raise SystemExit(main())
