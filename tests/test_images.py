# -*- coding: utf-8 -*-

import numpy as np
import tifffile as tif

import pycellid


def test_img_name():
    assert (
        pycellid.img_name(ucid=300000000020, t_frame=5, channel="BF")
        == "BF_Position03_time06.tif.out.tif"
    )


def test_box_img():
    radius = np.random.randint(15, 51)
    side = radius * 2 + 1
    imarray = np.random.randint(0, 255, (side, side, 1), "uint8")
    tif.imsave("./tests/imtest.tiff", imarray)
    x_pos = radius + 1
    y_pos = radius + 1
    dx = (radius, radius)
    dy = (radius, radius)
    imresult = pycellid.box_img(
                        "./tests/",
                        "imtest.tiff",
                        x_pos,
                        y_pos,
                        dx,
                        dy
                        )
    centro = imresult[y_pos - 2:y_pos, x_pos - 2:x_pos]
    alto = imresult[:, -3:]
    largo = imresult[-3:, :]
    assert np.sum(centro) + np.sum(alto) + np.sum(largo) == 0
