# -*- coding: utf-8 -*-

import os
import random
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import pycellid

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)


def get_array_img(doc, n, criteria):
    file = os.path.join(base, "samples_cellid", "pydata", doc)
    df = pd.read_csv(file)
    iarray = pycellid.array_img(
        df,
        os.path.join(base, "samples_cellid"),
        n=n,
        criteria=criteria,
    )

    return iarray


def get_size(shape, criteria):
    diameter = int(2 * np.round(np.sqrt(criteria["a_tot"][0] / np.pi)))
    unitary_size = 2 * diameter + 3
    total_size = unitary_size * shape[0]
    return total_size


@pytest.mark.parametrize(
    "ucid, channel, t_frame, expected",
    [
        (100000000020, "BF", np.int64(0), "BF_Position01_time01.tif.out.tif"),
        (
            100000000020,
            "CFP",
            np.int64(1),
            "CFP_Position01_time02.tif.out.tif",
        ),
        (
            200000000020,
            "RFP",
            np.int64(2),
            "RFP_Position02_time03.tif.out.tif",
        ),
        (
            200000000020,
            "YFP",
            np.int64(3),
            "YFP_Position02_time04.tif.out.tif",
        ),
        (300000000020, "BF", np.int64(4), "BF_Position03_time05.tif.out.tif"),
        (300000000020, "BF", np.int64(5), "BF_Position03_time06.tif.out.tif"),
        (200000000020, "BF", np.int64(6), "BF_Position02_time07.tif.out.tif"),
        (200000000020, "BF", np.int64(7), "BF_Position02_time08.tif.out.tif"),
        (100000000020, "BF", np.int64(8), "BF_Position01_time09.tif.out.tif"),
        (100000000020, "BF", np.int64(9), "BF_Position01_time10.tif.out.tif"),
        (300000000020, "BF", np.int64(10), "BF_Position03_time11.tif.out.tif"),
        (300000000020, "BF", np.int64(11), "BF_Position03_time12.tif.out.tif"),
        (300000000020, "BF", np.int64(12), "BF_Position03_time13.tif.out.tif"),
        (300000000020, "BF", None, "BF_Position03.tif.out.tif"),
    ],
)
def test_img_name(ucid, channel, t_frame, expected):
    base_dir = Path("./mypath")
    assert pycellid.img_name(
        path=base_dir, ucid=ucid, channel=channel, t_frame=t_frame
    ) == base_dir.joinpath(expected)


def test_box_img():
    radius = np.random.randint(15, 51)
    side = radius * 2 + 1
    imarray = np.random.randint(0, 255, (side, side), "uint8")

    x_pos = radius + 1
    y_pos = radius + 1
    imresult = pycellid.box_img(imarray, x_pos, y_pos, radius)
    centro = imresult[y_pos - 2 : y_pos, x_pos - 2 : x_pos]  # noqa
    alto = imresult[:, -3:]
    largo = imresult[-3:, :]
    assert np.sum(centro) + np.sum(alto) + np.sum(largo) == 0


def test_array_img():
    iarray = get_array_img("df.csv", 16, {"a_tot": [800.0, 1200.01]})
    total_size = get_size((4, 4), {"a_tot": [800.0, 1200.01]})
    assert iarray.shape >= (total_size, total_size)


def test_array_img_2():
    ypos_lim = random.uniform(50.0, 60.0)
    iarray = get_array_img(
        "df.csv", 12, {"a_tot": [800.0, 1200.01], "ypos": [0.0, ypos_lim]}
    )
    total_size = get_size(
        (4, 3), {"a_tot": [800.0, 1200.01], "ypos": [0.0, ypos_lim]}
    )
    assert iarray.shape >= (total_size, total_size)


def test_array_img_3():
    xpos_lim = random.uniform(50.0, 60.0)
    iarray = get_array_img(
        "df.csv", 12, {"a_tot": [800.0, 1200.01], "xpos": [0.0, xpos_lim]}
    )
    total_size = get_size(
        (4, 3), {"a_tot": [800.0, 1200.01], "xpos": [0.0, xpos_lim]}
    )
    assert iarray.shape >= (total_size, total_size)


def test_array_img_warning_1():
    message = "The specified criteria is not satisfied by any cell"
    with pytest.warns(UserWarning, match=message):
        file = os.path.join(base, "samples_cellid", "pydata", "df.csv")
        df = pd.read_csv(file)
        n = random.randint(16, 100)
        lim = random.uniform(100.0, 1000.0)
        criteria = {"a_tot": [lim, lim]}
        iarray = pycellid.array_img(
            df,
            os.path.join(base, "samples_cellid"),
            n=n,
            criteria=criteria,
        )
        print(iarray.shape)


def test_array_img_warning_2():
    n = random.randint(16, 100)
    message = f"The specified criteria are not satisfied by {n} cells"
    with pytest.warns(UserWarning, match=message):
        file = os.path.join(base, "samples_cellid", "pydata", "df.csv")
        df = pd.read_csv(file)
        criteria = {"a_tot": [700.0, 702.00]}
        iarray = pycellid.array_img(
            df,
            os.path.join(base, "samples_cellid"),
            n=n,
            criteria=criteria,
        )
        print(iarray.shape)
