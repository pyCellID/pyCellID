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

"""Images for PyCellID."""

import re
from pathlib import Path

import matplotlib.pyplot as plt

import numpy as np


def img_name(path, ucid, channel, t_frame=None, fmt=".tif.out.tif"):
    """Construct the image's name according to the output format of CellID.

    The returned string contains the path and name of the image.

    Parameters
    ----------
    ucid : ``int``
                    The unique traking number.
    t_frame : ``int``
                    Time tag of the image.
    channel : ``str``
                    Fluorescence channel of the image. The values allowed
                    are 'BF', 'CFP', 'RFP' or 'YFP'.

    Returns
    -------
    ``str`` :
             Name and image's path according to the output format of CellID.
    """
    base_dir = Path(path)

    # Extract the position from 'ucid'
    pos = re.search(r"\d+(?=\d{11})", str(ucid)).group(0)
    pos = pos.zfill(2)
    # Check if 't_frame' is provided and onstruct the name of the image
    if isinstance(t_frame, np.int64):
        s = str(t_frame + 1).zfill(2)
        name = f"{channel.upper()}_Position{pos}_time{s}{fmt}"
    elif t_frame is None:
        name = f"{channel.upper()}_Position{pos}{fmt}"
    # Join base directory to name
    name = base_dir.joinpath(name)
    return name


def _test_y_pos(im, y_pos, radius):
    if y_pos - radius < 0:
        im = np.concatenate(
            [np.zeros((np.abs(y_pos - radius), im.shape[1])), im], 0
        )
    return im


def _test_x_pos(im, x_pos, radius):
    if x_pos - radius < 0:
        im = np.concatenate(
            [np.zeros((im.shape[0], np.abs(x_pos - radius))), im], 1
        )
    return im


def _mark_center(im, x_pos, y_pos):
    center = np.zeros((2, 2))
    im[y_pos - 1:y_pos + 1, x_pos - 1:x_pos + 1] = center
    return im


def _img_crop(im, x_pos, y_pos, diameter, im_shape):
    y_min = max([y_pos - diameter, 0])
    y_max = min([y_pos + diameter, im_shape[0]])
    x_min = max([x_pos - diameter, 0])
    x_max = min([x_pos + diameter, im_shape[1]])
    im = im[y_min:y_max, x_min:x_max]
    return im


def box_img(im, x_pos, y_pos, radius=90):
    """Create a single image contatinig an individualised cell.

    The resulting image posses a mark in the center of the individualised
    cell and a pair of delimiters in the right and bottm edges.

    Parameters
    ----------
    im : ``numpy.array``
        A full fluorescence microscopy image.
    x_pos : ``int``
        x-coordinate of the center of the cell of interest.
    y_pos : ``int``
        y-coordinate of the center of the cell of interest.
    radius : ``int``
        lenght (in pixels) between the center of the image and each edge.

    Return
    ------
    ``numpy.array`` :
        An array (image) containing an individualised, center-pinned, cell.
    """
    height = width = radius * 2
    im_shape = im.shape
    # Mark the center of the cell
    im = _mark_center(im, x_pos, y_pos)
    # crop the region of the image containing the cell of interest
    im = _img_crop(im, x_pos, y_pos, radius, im_shape)
    iarray = np.zeros((height, width))
    im = _test_y_pos(im, y_pos, radius)
    im = _test_x_pos(im, x_pos, radius)
    iarray[0:im.shape[0], 0:im.shape[1]] = im
    # Adding delimiters
    rule_height = np.zeros((height, 3))
    rule_width = np.zeros((3, (width + 3)))
    iarray = np.concatenate([iarray, rule_height], 1)
    iarray = np.concatenate([iarray, rule_width], 0)
    return iarray


def array_img(data, path, channel="BF", n=16, shape=(4, 4), criteria={}):
    """Create a grid of images containing cells which satisfy given criteria.

    Resulting image has 'n' instances ordered in a grid of shape 'shape'.
    Each instance corresponds to a image centered in a cell satisfying provided
    criteria.

    Parameters
    ----------
    data : ``pandas dataframe``
        Dataframe (output of CellID) containing all the measured parameters
        of each cell.
    path : ``str``
        Path to the directory containing the images asociated to 'data'.
    channel : ``str``
        Fluorescence channel of the image.
        The values allowed are 'BF', 'CFP', 'RFP' or 'YFP'.
    n : ``int``
        Number of instances composing the grid.
    shape : ``tuple``
        Shape (rows, columns) of the final grid of images.
    criteria : ``dict``
        Dictionay containing the criteria of selection of cells.

    Return
    ------
    ``numpy.array`` :
        A grid of 'n' images of cells satisfying given criteria.

    Raises
    ------
    ValueError
        If the number of cells satisfying the selection criteria is less
        than the number of cells to be shown.
    """
    try:
        # Estimate the maximum of the diameters of the cells in data based on
        # their area and assuming round-like cells
        diameter = int(2 * np.round(np.sqrt(data["a_tot"].max() / np.pi)))

        data_copy = data.copy()
        # Checking for extra selection criteria
        if len(criteria) != 0:
            for c in criteria.keys():
                data_copy = data_copy[
                    (criteria[c][0] < data_copy[c])
                    & (data_copy[c] < criteria[c][1])
                ]
        # Checking if the number of cells satisfying the criteria matches the
        # number of cells to be shown
        if data_copy.shape[0] < n:
            message = f"The specified criteria are not satisfied by {n} cells"
            raise ValueError(message)
        select = data_copy[["ucid", "t_frame", "xpos", "ypos"]].sample(n)
        # Registers the name of each image in the series 'name'
        select["name"] = select.apply(
            lambda row: img_name(path, row["ucid"], channel, row["t_frame"]),
            axis=1,
        )
        # Registers the individual image corresponding to each cell in the
        # series 'box_img'
        select["box_img"] = select.apply(
            lambda row: box_img(
                plt.imread(row["name"], format="tif"),
                row["xpos"],
                row["ypos"],
                diameter,
            ),
            axis=1,
        )
        s = (2 * diameter + 3, 2 * diameter + 3)  # Shape of unitary image
        # iarray np.ones, with size for contining all individual images
        iarray = np.ones((s[0] * shape[0], s[1] * shape[1]), dtype=float)

        iloc = 0  # img index
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                xi = s[0] * i
                xf = s[0] * (i + 1)
                yi = s[1] * j
                yf = s[1] * (j + 1)
                iarray[xi:xf, yi:yf] = select["box_img"].iloc[iloc]
                iloc += 1
        return iarray
    except ValueError as e:
        print(e)
        raise