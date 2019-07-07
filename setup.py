# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('pyplayground/pyplayground.py').read(),
    re.M
    ).group(1)


with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "cmdline-pyplayground",
    packages = ["pyplayground"],
    entry_points = {
        "console_scripts": ['pyplayground = pyplayground.pyplayground:main']
        },
    version = version,
    description = "Python command line application pyplayground.",
    long_description = long_descr
    # TODO: author = "Learning To Code",
    )
