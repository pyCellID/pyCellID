# !/usr/bin/env python

# -*- coding: utf-8 -*-

# This file is part of the
#   PyCellID Project (
#     https://github.com/pyCellID,
#     https://github.com/darksideoftheshmoo
# ).
# Copyright (c) 2021. Clemente, Jose
# License: MIT
#   Full Text: https://github.com/pyCellID/pyCellID/blob/main/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""Merge and analyze tables of characteristics of cells and find images."""

# =============================================================================
# IMPORTS
# =============================================================================
import warnings
from pathlib import Path

import attr

import matplotlib.pyplot as plt

import pandas as pd

from pycellid import images as img
from pycellid.io import merge_tables


# =============================================================================
# CellData Class
# =============================================================================


def _check_path(self, attribute, value):
    if not Path(value).exists():
        raise FileNotFoundError(f"Path < {value} > not exist")


@attr.s(cmp=False, repr=False)
class CellData(object):
    """Collapse your data into a single data frame.

    Recursively inspect the path, create a unique identifier per cell,
    and inspect related images.

    Parameters
    ----------
    path:
        global path from output ``cellID`` tables.

    Return
    ------
        A dataframe ``cellID``.

    * to use:

    >>> from pycellid.core import CellData
    >>> df = CellData(
        path = '../my_experiment'
    )

    Other Parameters
    ----------------
    name_data:
        srt() file name to finde each table data.
    name_meta_data:
        srt() file name to finde tables metadata or mapping_tags
    verbose:
        bool, True to print in realtime pipeline

    """

    _path = attr.ib(validator=_check_path)
    _df = attr.ib()

    @classmethod
    def from_csv(cls, path, **kwargs):
        """Build a data frame from the tables contained in path.

        A CellData class will be instantiated.
        """
        return cls(path=path, df=merge_tables(path, **kwargs))

    @property
    def plot(self):
        """Represent set of ``cells_image`` or numerical data.

        For ``cimage`` method you must specify an identifier id={}.
        """
        return CellsPloter(self)

    def __eq__(self, other):
        """
        Call to perform equality comparison.

        x == a <=> x.__eq(a) => bool.
        """
        return self._df == other

    def __ne__(self, other):
        """Call to perform inequality comparison.

        x != a <=> x.__ne(a) => bool.
        """
        return not self == other

    def __lt__(self, other):
        """Call for comparison less than.

        x < a <=> x.__lt(a) => bool.
        """
        return self._df < other

    def __le__(self, other):
        """Call to compare less than or equal to.

        x <= a <=> x.__lt(a) => bool.
        """
        return self._df <= other

    def __gt__(self, other):
        """Call for comparison, greater than.

        x > a <=> x.__lt(a) => bool.
        """
        return self._df > other

    def __ge__(self, other):
        """Call for comparison, greater than or equal to.

        x >= a <=> x.__lt(a) => bool.
        """
        return self._df >= other

    def __lshift__(self, other):
        """Return a shifted left by b.

        operator.__lshift__(a, b).
        """
        return self._df.__lshift__(other)

    def __rshift__(self, other):
        """Return a shifted right by b.}.

        operator.__rshift__(a, b).
        """
        return self._df.__rshift__(other)

    def __getitem__(self, slices):
        """Return the value of x at index k.

        x[k] <=> x.__getitem__(k).
        """
        sliced = self._df.__getitem__(slices)
        return CellData(path=self._path, df=sliced)

    def __getattr__(self, a):
        """getattr(x, y) <==> x.__getattr__(y) <==> getattr(x, y)."""
        return self._df.__getattr__(a)

    def __setitem__(self, idx, values):
        """Call to implement assignment to self[key]."""
        return self._df.__setitem__(idx, values)

    def __iter__(self):
        """Call when an iterator is required for a container.

        iter(x) <=> x.__iter__().
        """
        return iter(self._df)

    def __len__(self):
        """Call to implement the built-in function len().

        len(x) <=> x.__len__().
        """
        return len(self._df)

    def __repr__(self):
        """Print a representation of your object."""
        return repr(self._df)

    def _repr_html_(self):
        """Print a rich HTML version of your object."""
        ad_id = id(self)

        if isinstance(self._df, pd.DataFrame) or \
           isinstance(self._df, self.__class__):
            with pd.option_context("display.show_dimensions", False):
                df_html = self._df._repr_html_()

            rows = f"{self._df.shape[0]} rows"
            columns = f"{self._df.shape[1]} columns"

            footer = f"PyCellID.core.CellData - {rows} x {columns}"

            parts = [
                f'<div class="PyCellID.core.CellData" id={ad_id}>',
                df_html,
                footer,
                "</div>",
            ]

            html = "".join(parts)
            return html
        else:
            self._df.__repr__()

    def get_dataframe(self):
        """To return a copy of the internal _df."""
        return self._df.copy()


# =============================================================================
# CellsPloter Class
# =============================================================================


@attr.s(repr=False)
class CellsPloter:
    """
    Accessor to plotter class.

    Create a representation of each cell within a grid, inspect an entire
    image or create a snippet of a single cell.
    We provide a wrapper of the same pandas methods for plotting.

    Returns
    -------
    axes to plot

    Attributes
    ----------
    cells_image:
        Matrix of cells
    cimage:
        single cell representation.
    """

    cells = attr.ib()

    def __call__(self, kind="cells_image", **kwargs):
        """
        When the instance is “called” as a function.

        ``plot() <==> plot.__call__()``.
        """
        if kind.startswith("_"):
            raise AttributeError(f"Invalid plot method '{kind}'")

        method = getattr(self, kind, None)

        if not callable(method):
            raise AttributeError(f"Invalid plot method '{kind}'")

        if method is None:
            method = getattr(self.cells._df.plot, kind)

        return method(**kwargs)

    def __getattr__(self, a):
        """
        Is called when the default attribute access fails (AttributeError).

        getattr(x, y) <==> x.__getattr__(y) <==> getattr(x, y).
        """
        return getattr(self.cells._df.plot, a)

    def __repr__(self):
        """
        Compute the “official” string representation of an object.

        repr(x) <=> x.__repr__().
        """
        return f"CellsPloter(cells={hex(id(self.cells))})"

    def cells_image(self, array_img_kws=None, imshow_kws=None, ax=None):
        """Display a random selection of cells on a square grid.

        By default it represents a 4 X 4 matrix chosen at random.

        Returns
        -------
        ax to plot or figure.

        Other Parameters
        ----------------
        array_img_kws : dict.
            Set the pycellid.images.img_array parameters.
            n : number of cells.
            channles : "TFP" or another that you have encoded.

        imshow_kws : dict
            If you use matplotlib set equal to plt.imshow.

        ax:
            Use your axes to plot.
        """
        data_c = self.cells

        ax = plt.gca() if ax is None else ax

        imshow_kws = {} if imshow_kws is None else imshow_kws
        array_img_kws = {} if array_img_kws is None else array_img_kws

        imshow_kws.setdefault("cmap", "Greys")

        arr_c = img.array_img(data=data_c, path=data_c._path, **array_img_kws)

        ax.imshow(arr_c, **imshow_kws)
        ax.axis("off")
        return ax

    def cimage(self, identifier, box_img_kws=None, imshow_kws=None, ax=None):
        """Show a sigle cell or complete image.
        ``Identifier`` param is required. Reference a valid image or position.
        By default, an image with a size of (1392 X 1040)px will be rendered.
        Use the arguments of box_img_kws to choose as you like.
        Parameters
        ----------
        idtfer : path or dict.
                 path to an image file
                 ``dict = { "channel":str, "UCID":int, t_frame":int }``
        Returns
        -------
        ax to plot or figure.
        Other Parameters
        ----------------
        box_img_kws : dict.
            Set the pycellid.images.box_img parameters.
            ``im`` : numpy.array.
                 A full fluorescence microscopy image.
            ``x_pos`` : int.
                    x-coordinate of the center of the cell of interest.
            ``y_pos`` : int.
                    x-coordinate of the center of the cell of interest.
            ``radius`` : int.
                     lenght (in px) between the center of the image and
                     each edge. Default = 90.
            ``mark_center`` : bool
                          mark a black point. Default = False.
        imshow_kws : dict
                     If you use matplotlib set equal to plt.imshow.
        ax:
            Use your axes to plot.
        """
        data_c = self.cells

        ax = plt.gca() if ax is None else ax

        imshow_kws = {} if imshow_kws is None else imshow_kws
        box_img_kws = {} if box_img_kws is None else box_img_kws

        imshow_kws.setdefault("cmap", "Greys")

        if isinstance(identifier, dict):
            ucid = identifier["ucid"]
            t_frame = identifier["t_frame"]
            try:
                [[x, y]] = data_c[
                    (data_c.ucid == ucid) & (data_c.t_frame == t_frame)
                ][["xpos", "ypos"]].values.tolist()
                r = 90
            except ValueError:
                x, y, r = int(1392 / 2), int(1040 / 2), int(1040 / 2)
                message = "not match ucid and t_frame. See picture!"
                warnings.warn(message)

            identifier = img.img_name(data_c._path, **identifier)

        else:
            x, y, r = int(1392 / 2), int(1040 / 2), int(1040 / 2)

        box_img_kws.setdefault("x_pos", x)
        box_img_kws.setdefault("y_pos", y)
        box_img_kws.setdefault("radius", r)

        arr = plt.imread(identifier)
        arr_c = img.box_img(im=arr, **box_img_kws)

        ax.imshow(arr_c, **imshow_kws)
        ax.axis("off")
        return ax
