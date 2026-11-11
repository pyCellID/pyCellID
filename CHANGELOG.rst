PyCellID Changelog
===================


Version (0.2.0)
------------------

- Packaging configuration moved to ``pyproject.toml`` (PEP 621);
  ``setup.py`` and ``requirements/`` removed. Development dependencies
  are now dependency groups (PEP 735): ``pip install -e . --group dev``.
- Supported Python versions: 3.11 to 3.15 (3.8, 3.9 and 3.10 dropped).
- Minimum dependencies: attrs 22.2, matplotlib 3.7, numpy 1.24, pandas 2.0.
- CI rewritten: Python 3.11 to 3.15 matrix without fail-fast, weekly
  scheduled run and manual trigger; style, manifest, coverage and docs
  checked in a separate job. Read the Docs moved to Ubuntu 24.04 and
  Python 3.12 with unpinned documentation dependencies.
- Releases are published to PyPI by GitHub Actions with Trusted
  Publishing (no API tokens); manual runs publish to TestPyPI.
- ``make_df``: avoid ``inplace=True`` in ``set_index`` (deprecated in
  pandas 3.1, to be removed in pandas 4).

Version 0.1.1
-------------

- Fix ``read_df`` with pandas >= 2.0: column-name normalization replaced
  every character with ``_`` (regex ``"."`` matched any character).
- Fix spurious ``ChainedAssignmentError`` warning in ``CellData.__setitem__``
  under pandas copy-on-write.
- Add regression test for column-name normalization.
