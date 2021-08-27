#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   Pyedra Project (https://github.com/darksideoftheshmoo/pycell/).
# Copyright (c) 2021, Author1, Author2, Author3, Author4, Author5
# License: MIT
#   Full Text: https://github.com/darksideoftheshmoo/pycell/blob/master/LICENSE

# =====================================================================
# DOCS
# =====================================================================

"""This file is for distribute and install PyCell"""

# ======================================================================
# IMPORTS
# ======================================================================

import os
import pathlib

""" preguntar ¿para qué sirve ez_setup.py? y ¿cómo se usa? 

import ez_setup

ez_setup.use_setuptools() """

from setuptools import setup  # noqa

# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))


REQUIREMENTS = ["pandas>=1.3.2", "attrs", "matplotlib>=3.4.3"]

with open(PATH / "pycell" / "__init__.py") as fp:
    for line in fp.readlines():
        if line.startswith("__version__ = "):
            VERSION = line.split("=", 1)[-1].replace('"', "").strip()
            break


with open("README.md") as fp:
    LONG_DESCRIPTION = fp.read()


# =============================================================================
# FUNCTIONS
# =============================================================================

setup(
    name="PyCell",
    version=VERSION,
    description="An extension that analyze Cell-ID single-cell cytometry data using Python language.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="https://github.com/darksideoftheshmoo/pycell",
    py_modules=["ez_setup"],
    packages=["pycellid"],
    license="The MIT License",
    install_requires=REQUIREMENTS,
    keywords=["pycell", "key2", "key3"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        'Intended Audience :: Developers',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)