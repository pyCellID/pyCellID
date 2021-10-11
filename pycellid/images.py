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

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def img_name(ucid, t_frame, channel):
    """Contruct te image's name correspondig with CellID output images.
    
    This function have a initial ucid ``ucid_in = 100000000000``
    such that try a positional string given by
    ``pos = str(ucid //ucid_in).zfill(2)``.
    For example: ``ucid = int(300000000020)`` numero de traking
    unico.
    pos: ``'path : /home/../BF_Position03_time06.tif.out.tif'``

    Parameters
    ----------
    ucid : int
        The unique traking number
    t_frame : int
        tag tiempo de la imagen
    channel : int
        Can be one value given by BF, CFP, RFP or YFP.

    Return
    ------
        A string given by the image's name.
    """
    # initial ucid
    ucid_in = 100000000000
    # We obtain a positional string e.g 01, 02, 10, 20, 100
    pos = str(ucid // ucid_in).zfill(2)
    s = str(t_frame + 1).zfill(2)
    name = f"{channel.upper()}_Position{pos}_time{s}.tif.out.tif"
    return name


def box_img(path, im_name, x_pos, y_pos, dx=(15, 15), dy=(15, 15)):
    """Contruct a array of the intensity values (:math:`<= 256`, by pixels).

    The extended matrix in three bottom rows and three right columns
    with ``0`` values as delimitation.
    Also, ``center`` is the displacement of center ``y``, ``x``
    ``[(start, end),(start, end)]``.

    The ``img`` date is a ``np.array`` where encode rows an columns:
    ``codifica[fila, columna]`` ``y = rows``, ``x = columns``

    Parameters
    ----------
    path : str
        path to the image.
    im_name : str
        The image name.
    x : int
        x-coordinate where the image begins
    y : int
        y-coordinate where the image begins.

    Return
    ------
        A extended array corresponding to a cell.
    """
    path_n = Path(path).joinpath(im_name)
    # load image
    im = plt.imread(path_n, format="tif")
    im = im.copy()
    centro = np.zeros((2, 2))
    im[y_pos - 1:y_pos + 1, x_pos - 1:x_pos + 1] = centro
    # Hago un crop de la imagen tomando como margen 20 pixels
    # im = im[abs(y - 20):(y + 25), abs(x - 10):(x + 40)]
    y_min = y_pos - dx[0]
    y_max = y_pos + dx[1]
    x_min = x_pos - dx[0]
    x_max = x_pos + dx[1]
    im = im[y_min:y_max, x_min:x_max]
    # Frame
    alto = np.zeros((im.shape[0], 3))
    largo = np.zeros((3, (im.shape[1] + 3)))
    # Recuadro
    im = np.concatenate([im, alto], 1)
    im = np.concatenate([im, largo], 0)
    return im


def array_img(data, path, chanel="BF", n=16, shape=(4, 4), criteria={}):
    """Make ``n`` selections on dataset ``data`` in the ``path``.

    walk the ``path`` looking for the images
    corresponding to ``chanel`` and create an
    image of ``shape(row, columns)``.

    Parameters
    ----------
    chanel : str
        str() debe segir en encoding de mapeo
        de canales ``('BF', 'CFP',...)``
    shape : int
        ``(int(filas)``, ``int(columnas))`` como
        se ordenan las ``imgs``.
    cent_cel : int
        cuando se movera ``[(Y_m, Y_M),(X_m, X_M)]``
        en los ejes coordenados del valor centro
        aportado por ``data[['x_pos', 'y_pos']]``.
    n : int
        cantidad de cells a representar.
    shape : tuple
        tupla con la forma de la grilla que representa
        los recortes conteninedo las distintas células.
    criteria : dict
        diccionario conteniendo distintos criterios
        de selección para las celulas a mostrar.

    Return
    ------
        La imagen de salida corresponde a ``n``.
    """
    # Selecciono ucid al azar para las n celulas
    # select = np.random.choice(data['ucid'], 91 ,replace = False)
    # Calculo las dimensiones de la imagen unitaria en base al area de la
    # célula, suponiéndola esférica (con una proyección circular cuyo area es
    # df['a_tot'])
    try:
        radio = int(np.round(np.sqrt(data["a_tot"].max() / np.pi)))
        # Leo las dimensiones de una imagen típica
        image_name = list(Path(path).glob("*.tif.out.tif"))[0]
        image_name = str(image_name).split("\\")[-1]
        filename = Path(path).joinpath(image_name)
        im = plt.imread(filename, format="tif")
        im_size = im.shape
        del image_name, filename
        # seleccion de n filas al azar y sin repo
        data_copy = data.copy()
        data_copy = data_copy[
            (data_copy["ypos"] > 2 * radio)
            & (data_copy["ypos"] < im_size[0] - (2 * radio + 3))
            & (data_copy["xpos"] > 2 * radio)
            & (data_copy["xpos"] < im_size[1] - (2 * radio + 3))
        ]
        if len(criteria) != 0:
            for c in criteria.keys():
                data_copy = data_copy[
                    (criteria[c][0] < data_copy[c] < criteria[c][1])
                ]
        if data_copy.shape[0] < n:
            raise RuntimeError(
                f"The specified criteria are not satisfied by {n} cells"
            )
        select = data_copy[["ucid", "t_frame", "xpos", "ypos"]].sample(n)
        # Registra el nombre de cada imagen en la serie 'name'
        select["name"] = select.apply(
            lambda row: img_name(row["ucid"], row["t_frame"], chanel), axis=1
        )
        # Registra un array para cada imagen en la serie 'box_img'
        # Cada imagen tiene dimenciones de 48*53 valores
        y_min = y_max = x_min = x_max = 2 * radio
        select["box_img"] = select.apply(
            lambda row: box_img(
                path,
                row["name"],
                row["xpos"],
                row["ypos"],
                (y_min, y_max),
                (x_min, x_max),
            ),
            axis=1,
        )
        s = (4 * radio + 3, 4 * radio + 3)  # Shape of unitary image
        # iarray np.ones, con dimencion para contenr todas las imgs
        iarray = np.ones((s[0] * shape[0], s[1] * shape[1]), dtype=float)
        # Para las filas i y columnas j de iarray
        # se remplazan las img de c/celula seleccionada
        iloc = 0  # img index
        for i in range(0, shape[0]):
            for j in range(0, shape[1]):
                xi = s[0] * i
                xf = s[0] * (i + 1)
                yi = s[1] * j
                yf = s[1] * (j + 1)
                iarray[xi:xf, yi:yf] = select["box_img"].iloc[iloc]
                iloc += 1
        plt.imshow(iarray, cmap="gist_gray")
        plt.show()
        # return iarray
    except RuntimeError as e:
        print(e)
