#!/usr/bin/env python3

import argparse
import pathlib
import re


def pypi_friendly_name(string):
    regex = r'^[a-z][a-z0-9_-]*$'
    if not re.match(regex, string):
        raise argparse.ArgumentTypeError(
            f"pypi will not enjoy that name. The case-sensitive regex to follow is {regex}")
    return string


def python_friendly_name(name):
    return name.replace('-', '_')


def replace_strings(path, list_of_tuples):
    if len(list_of_tuples) < 1:
        raise ValueError('bad len of list')
    contents = path.read_text()
    new_contents = contents
    for tup in list_of_tuples:
        old, new = tup
        new_contents = new_contents.replace(old, new)
    path.write_text(new_contents)


def rename_everything(old_name, new_name):
    old_python_friendly_name = python_friendly_name(old_name)
    new_python_friendly_name = python_friendly_name(new_name)
    old = pathlib.Path(old_name)
    if not old.exists():
        raise ValueError("Old directory {} does not exist.")
    if not old.is_dir():
        raise ValueError("Old directory {} is not a directory.")
    new = pathlib.Path(new_name)
    if new.exists():
        raise ValueError("New directory {} already exists. Try a fresh `git clone`?")
    old.joinpath(f'{old_python_friendly_name}.py').rename(old.joinpath(f'{new_python_friendly_name}.py'))
    old.rename(new_python_friendly_name)
    old_runner = pathlib.Path(f'{old_name}-runner.py')
    for path in [old_runner, pathlib.Path('setup.py')]:
        replace_strings(
            path,
            [(old_python_friendly_name, new_python_friendly_name)])
    old_runner.rename(f'{new_name}-runner.py')
    pathlib.Path(f'{old_name}.png').unlink()
    replace_strings(pathlib.Path('Makefile'), [(old_name, new_name)])
    replace_strings(
        pathlib.Path('README.md'),
        [('![ultracompelling logo](pyplayground.png)', ''),
         (old_name, new_name)])
    for name in ('interactive.py', 'run_tests.py', 'tests/test_cat.py'):
        replace_strings(
            pathlib.Path(name),
            [(old_python_friendly_name, new_python_friendly_name)])
    for path in old.rglob('*'):
        replace_strings(
            path,
            [(old_python_friendly_name, new_python_friendly_name)])


def main():
    parser = argparse.ArgumentParser(
        prog='rename_pyplayground',
        description="""Renames this template from `pyplayground` to --new-name""")
    parser.add_argument(
        '--old-name', type=pypi_friendly_name, default='pyplayground')
    parser.add_argument(
        '--new-name', help='replacement for "pyplayground"', type=pypi_friendly_name)
    args = parser.parse_args()
    if args.new_name is None:
        raise ValueError("missing value for argument --new-name=NEW-NAME")
    rename_everything(args.old_name, args.new_name)
    print('')
    print(r'''Now make a git commit that removes this script and adds the new files and
removes the deleted files.

E.g., try `git add .` followed by `git commit`
''')


if __name__ == '__main__':
    main()
