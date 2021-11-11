# !/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# DOCS
# =============================================================================

"""in-out implementations for pyCellID."""

# =============================================================================
# IMPORTS
# =============================================================================

import attr

import pandas as pd

from pycellid.io import merge_id_tables


# Necesito crear un tempdir _cache ver librery tempdir
# PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__))) / "_cache"


@attr.s
class Data(object):
    """The Class for data object by images"""
    path = attr.ib()
    model = attr.ib(validator=attr.validators.instance_of(str), init=False)
    model_df = attr.ib(
        validator=attr.validators.instance_of(pd.DataFrame), init=False
    )

    @property
    def df(self):
        if "_df" not in vars(self):
            self._df = merge_id_tables(self.path)
        return self._df.copy()

    def __getattr__(self, a):
        return getattr(self.df, a)

    def __getitem__(self, slice):
        """x[k] <=> x.__getitem__(k)."""
        return self.df.__getitem__(slice)

    def __iter__(self):
        """iter(x) <=> x.__iter__()."""
        return iter(self.df)

    def __len__(self):
        """len(x) <=> x.__len__()."""
        return len(self.df)

    def __repr__(self):
        """repr(x) <=> x.__repr__()."""
        return f"DataTables({repr(self.df)})"

    # def __setattr__(self, name, value)-> None:
    #     return self._df.__setattr__(name, value)

    def _repr_html_(self):
        return self.df._repr_html_()
