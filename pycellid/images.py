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

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def img_name(ucid, t_frame, chanel):
    """This function have a initial ucid ``ucid_in = 100000000000``
    such that try a positional string given by
    ``pos = str(ucid //ucid_in).zfill(2)``.
    For example: ``ucid = int(300000000020)`` numero de traking unico.
    - pos: ``'path : /home/../BF_Position03_time06.tif.out.tif'``
    :param ucid: The unique traking number
    :param t_frame: tag tiempo de la imagen
    :param chanel: Can be one value given by BF, CFP, RFP or YFP.
    :return: A string given by the image's name.
    """
    # ucid inicial
    ucid_in = 100000000000
    # Obtengo str() de position 01, 02, 10, 20, 100
    pos = str(ucid // ucid_in).zfill(2)
    s = str(t_frame + 1).zfill(2)
    name = f"{chanel.upper()}_Position{pos}_time{s}.tif.out.tif"

    return name


def box_img(path, im_name, x_pos, y_pos, dx=(15, 15), dy=(15, 15)):
    """The function ``box_img`` return a array of the intensity values
    (:math:`<= 256`, by pixels). The extended matrix in three bottom
    rows and three right columns with ``0`` values as delimitation. Also,
    ``center`` is the displacement of center ``y``, ``x``
    ``[(start, end),(start, end)]``.
    The ``img`` date is a ``np.array`` where encode rows an columns:
    ``codifica[fila, columna]`` ``y = rows``, ``x = columns``
    :param path: path to the image.
    :param im_name: The image name.
    :param x: x-coordinate where the image begins
    :param y: y-coordinate where the image begins
    :return: A extended array corresponding to a cell.
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
    """Realiza ``n`` selecciones del dataset ``data``, recorre ``path``
    buscando las imagenes correspondientes a ``chanel`` y crea una
    imagen de ``shape(filas, columnas)``.

    Parameters
    ----------
    chanel: str() debe segir en encoding de mapeo de canales
                   ``('BF', 'CFP',...)``
    shape: ``(int(filas)``, ``int(columnas))`` como se
                  ordenan las ``imgs``.
    cent_cel: cuando se movera ``[(Y_m, Y_M),(X_m, X_M)]`` en
                     los ejes coordenados del valor centro aportado
                     por ``data[['x_pos', 'y_pos']]``.
    n: cantidad de cells a representar.
    shape: tupla con la forma de la grilla que representa los recortes
            conteninedo las distintas células.
    criteria: diccionario conteniendo distintos criterios de selección
                para las celulas a mostrar.
    return: La imagen de salida corresponde a ``n``.
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

        # im_size = im.shape

        # seleccion de n filas al azar y sin repo
        data_copy = data.copy()
        data_copy = data_copy[
            (data_copy["ypos"] > 2 * radio)
            & (data_copy["ypos"] < im_size[0] - (2 * radio + 3))
            & (data_copy["xpos"] > 2 * radio)
            & (data_copy["xpos"] < im_size[1] - (2 * radio + 3))
        ]

        if len(criteria) != 0:
            for criterio in criteria.keys():
                data_copy = data_copy[
                    (data_copy[criterio] > criteria[criterio][0])
                    & (data_copy[criterio] < criteria[criterio][1])
                ]

        if data_copy.shape[0] < n:
            raise RuntimeError(
                f"Los criterios especificados no son satisfechos "
                f"por al menos {n} células"
            )

        select = data_copy[["ucid", "t_frame", "xpos", "ypos"]].sample(n)
        # Registra el nombre de cada imagen en la serie 'name'
        select["name"] = select.apply(
            lambda row: img_name(row["ucid"], row["t_frame"], chanel), axis=1
        )

        # Registra un array para cada imagen en la serie 'box_img'
        # Cada imagen tiene dimenciones de 48*53 valores
        y_min = 2 * radio
        y_max = 2 * radio
        x_min = 2 * radio
        x_max = 2 * radio

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


if __name__ == "__main__":
    df = pd.read_csv(".//muestras_cellid//pydata//df.csv")

    criteria = {
        "a_tot": [800.0, 1200.01],
        # "min_axis": [10.,30.],
    }
    array_img(
        df,
        "D://Documents//Universidad//Cursos//famaf software//"
        "proyecto//pyCellID//muestras_cellid",
        criteria=criteria,
    )
