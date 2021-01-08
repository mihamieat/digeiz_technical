# --------------------------------License Notice----------------------------------
# Python Project Boilerplate - A boilerplate project for python packages
#
# Written in 2018 by Mickaël 'lastmikoi' FALCK <lastmikoi@lastmikoi.net>
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.
# --------------------------------License Notice----------------------------------

"""Setuptools-backed setup module."""

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="digeiz_test",
    version="0.1",
    author="Francesco Perna",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frank2410/digeiz_test",
    python_requires=">=3.6",
    package_dir={"digeiz_test": "digeiz_api"},
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=requirements,
)
