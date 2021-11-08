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

"""This file is for distribute and install PyCellID"""

# ======================================================================
# IMPORTS
# ======================================================================

import os
import pathlib

from setuptools import setup  # noqa

# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))


REQUIREMENTS = ["pandas>=1.3.2", "matplotlib>=3.4.3"]

with open(PATH / "pycellid" / "__init__.py") as fp:
    for line in fp.readlines():
        if line.startswith("__version__ = "):
            VERSION = line.split("=", 1)[-1].replace('"', "").strip()
            break


with open("README.md") as fp:
    LONG_DESCRIPTION = fp.read()


# =============================================================================
# FUNCTIONS
# =============================================================================

short_description = "An extension that analyze Cell-ID single-cell."

setup(
    name="pycellid",
    version=VERSION,
    description=short_description,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Clemente, José",
    author_email="",
    url="https://github.com/pyCellID/pyCellID",
    packages=["pycellid"],
    license="The MIT License",
    install_requires=REQUIREMENTS,
    keywords=["pycellid", "key2", "key3"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
