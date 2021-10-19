# -*- coding: utf-8 -*-
from pathlib import Path

import numpy as np

import pandas as pd

import pycellid

import pytest


@pytest.mark.parametrize(
    "ucid, channel, t_frame, expected",
    [
        (
            100000000020,
            "BF",
            np.int64(0),
            "BF_Position01_time01.tif.out.tif"
            ),
        (
            100000000020,
            "CFP",
            np.int64(1),
            "CFP_Position01_time02.tif.out.tif"
            ),
        (
            200000000020,
            "RFP",
            np.int64(2),
            "RFP_Position02_time03.tif.out.tif"
            ),
        (
            200000000020,
            "YFP",
            np.int64(3),
            "YFP_Position02_time04.tif.out.tif"
            ),
        (
            300000000020,
            "BF",
            np.int64(4),
            "BF_Position03_time05.tif.out.tif"
            ),
        (
            300000000020,
            "BF",
            np.int64(5),
            "BF_Position03_time06.tif.out.tif"
            ),
        (
            200000000020,
            "BF",
            np.int64(6),
            "BF_Position02_time07.tif.out.tif"
            ),
        (
            200000000020,
            "BF",
            np.int64(7),
            "BF_Position02_time08.tif.out.tif"
            ),
        (
            100000000020,
            "BF",
            np.int64(8),
            "BF_Position01_time09.tif.out.tif"
            ),
        (
            100000000020,
            "BF",
            np.int64(9),
            "BF_Position01_time10.tif.out.tif"
            ),
        (
            300000000020,
            "BF",
            np.int64(10),
            "BF_Position03_time11.tif.out.tif"
            ),
        (
            300000000020,
            "BF",
            np.int64(11),
            "BF_Position03_time12.tif.out.tif"
            ),
        (
            300000000020,
            "BF",
            np.int64(12),
            "BF_Position03_time13.tif.out.tif"
            ),
        (
            300000000020,
            "BF",
            None,
            "BF_Position03.tif.out.tif"
            ),
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
    dx = (radius, radius)
    dy = (radius, radius)
    imresult = pycellid.box_img(imarray, x_pos, y_pos, dx, dy)
    centro = imresult[y_pos - 2:y_pos, x_pos - 2:x_pos]
    alto = imresult[:, -3:]
    largo = imresult[-3:, :]
    assert np.sum(centro) + np.sum(alto) + np.sum(largo) == 0


def test_array_img():
    df = pd.read_csv(".//muestras_cellid//pydata//df.csv")
    n = 16
    shape = (4, 4)
    criteria = {"a_tot": [800.0, 1200.01]}
    iarray = pycellid.array_img(
        df,
        "D://Documents//Universidad//Cursos//famaf software//"
        "proyecto//pyCellID//muestras_cellid",
        n=n,
        shape=shape,
        criteria=criteria,
    )

    diameter = int(2 * np.round(np.sqrt(criteria["a_tot"][0] / np.pi)))
    unitary_size = 2 * diameter + 3
    total_size = unitary_size * shape[0]

    assert iarray.shape >= (total_size, total_size)


def test_array_img_2():
    df = pd.read_csv(".//muestras_cellid//pydata//df.csv")
    n = 12
    shape = (4, 3)
    criteria = {"a_tot": [800.0, 1200.01], "ypos": [0.0, 50.0]}
    iarray = pycellid.array_img(
        df,
        "D://Documents//Universidad//Cursos//famaf software//"
        "proyecto//pyCellID//muestras_cellid",
        n=n,
        shape=shape,
        criteria=criteria,
    )
    diameter = int(2 * np.round(np.sqrt(criteria["a_tot"][0] / np.pi)))
    unitary_size = 2 * diameter + 3
    total_size = unitary_size * shape[0]

    assert iarray.shape >= (total_size, total_size)


def test_array_img_3():
    df = pd.read_csv(".//muestras_cellid//pydata//df.csv")
    n = 12
    shape = (4, 3)
    criteria = {"a_tot": [800.0, 1200.01], "xpos": [0.0, 50.0]}
    iarray = pycellid.array_img(
        df,
        "D://Documents//Universidad//Cursos//famaf software//"
        "proyecto//pyCellID//muestras_cellid",
        n=n,
        shape=shape,
        criteria=criteria,
    )
    diameter = int(2 * np.round(np.sqrt(criteria["a_tot"][0] / np.pi)))
    unitary_size = 2 * diameter + 3
    total_size = unitary_size * shape[0]

    assert iarray.shape >= (total_size, total_size)


def test_array_img_valueerror():
    with pytest.raises(ValueError):
        df = pd.read_csv(".//muestras_cellid//pydata//df.csv")
        n = 16
        shape = (4, 4)
        criteria = {"a_tot": [800.0, 700.00]}
        iarray = pycellid.array_img(
            df,
            "D://Documents//Universidad//Cursos//famaf software//"
            "proyecto//pyCellID//muestras_cellid",
            n=n,
            shape=shape,
            criteria=criteria,
        )
        print(iarray.shape)
