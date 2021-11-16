# !/usr/bin/env python
# -*- coding: utf-8 -*-

# =============================================================================
# DOCS
# =============================================================================

"""Merge and analyze the tables of characteristics calculated cell by cell
and quickly find the images."""

# =============================================================================
# IMPORTS
# =============================================================================

from pathlib import Path

import attr

import matplotlib.pyplot as plt

from pycellid import images
from pycellid.io import merge_id_tables


# make tempdir _cache see librery tempdir
# PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__))) / "_cache"


@attr.s(repr=False)
class Data(object):
    """Collapse the data in the path.


    Merge the tables into a single dataset, create a unique
    cell-ID, and inspect related images

    Parameters
    ----------
    path:
        global path from output ``cellID`` tables.

    Return
    ------
        A dataframe ``cellID``.

    * to use:

    >>> from pycellid.celldata import Data
    >>> df = Data(
        path = '../my_experiment'
    )

    Other Parameters
    ----------------
    name_data:
        srt() name to finde each table data.
    name_meta_data:
        srt() name to finde tables metadata/mapping_tags
    verbose:
        bool, True to print in realtime pipeline

    """

    path = attr.ib(validator=attr.validators.instance_of(str))

    name_data = attr.ib(
        validator=attr.validators.instance_of(str), default="out_all"
    )

    name_meta_data = attr.ib(
        validator=attr.validators.instance_of(str), default="*mapping"
    )


    @path.validator
    def _check_path(self, attribute, value):
        if not Path(value).exists():
            raise FileNotFoundError(f"Path < {value} > not exist")

    @property
    def df(self):
        if "_df" not in vars(self):
            self._df = merge_id_tables(
                path=self.path,
                n_data=self.name_data,
                n_mdata=self.name_meta_data
            )
        return self._df.copy()

    def __getattr__(self, a):
        return getattr(self.df, a)

    def __getitem__(self, k):
        """x[k] <=> x.__getitem__(k)."""
        return self.df.__getitem__(k)

    def __iter__(self):
        """iter(x) <=> x.__iter__()."""
        return iter(self.df)

    def __len__(self):
        """len(x) <=> x.__len__()."""
        return len(self.df)

    def __repr__(self):
        """repr(x) <=> x.__repr__()."""
        return f"DataTables({repr(self.df)})"

    def __repr_html__(self):
        return self.df._repr_html_()

    def __setitem__(self, key, values):
        self._df[key] = values

    def show(
        self,
        data,
        ch="BF",
        n=16,
        criteria={},
        figsize=(3, 3),
        dpi=200,
        cmap="gray",
        *args,
        **kwargs,
    ):
        """Show values in df"""
        arr = images.array_img(
            data,
            path=self.path,
            channel=ch,
            n=n,
            criteria=criteria,
        )

        fig = plt.figure(figsize=figsize, dpi=dpi, *args, *kwargs)
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(arr, cmap=cmap, *args, **kwargs)
        ax.axis("off")

        plt.show()
        # plt.xticks(X+0.38, ["A","B","C","D"])


# %%
