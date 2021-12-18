# -*- coding: utf-8 -*-

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
    author="Mihamina Rakotovazaha",
    description="DiGeiz technical test delivery pakage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mihamieat/digeiz_technical",
    python_requires=">=3.6",
    package_dir={"app": "test"},
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=requirements,
)
