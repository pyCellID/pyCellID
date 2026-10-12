PyCellID Changelog
===================

Version 0.1.1
-------------

- Fix ``read_df`` with pandas >= 2.0: column-name normalization replaced
  every character with ``_`` (regex ``"."`` matched any character).
- Fix spurious ``ChainedAssignmentError`` warning in ``CellData.__setitem__``
  under pandas copy-on-write.
- Add regression test for column-name normalization.
