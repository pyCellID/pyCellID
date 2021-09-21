#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Created on Sun Nov 15 12:03:09 2020

# @author: Clemente Jose Antonio

"""
Este pipeline está diseñado para navegar un path y rastrear tablas con
data y metadata(mapping) para retornar un único objeto Dataframe.::

    padre/
        hijo01/
            data.ext
            mapping.ext
        hijo03/
            data.ext
            mapping.ext
        hijo03/
            data.ext
            mapping.ext

Requiere librerias python standard:
`os <https://docs.python.org/3/library/os.html>`_,
`re <https://docs.python.org/3/library/re.html?highlight=re#module-re>`_
`pandas <https://pandas.pydata.org/docs/>`_,
`matplotlib <https://matplotlib.org/stable/index.html>`_.

Este proyecto comienza como soporte al software Cell-ID
Gordon, Colman‐Lerner et al. 2007
publicación original DOI: 10.1038/nmeth1008
`software <https://sourceforge.net/projects/cell-id/>`_.
Orientado, pero no limitando, a las salidas prodcidas por cell-ID:

- ``input``: la ruta generada por ``cellID``.

En el futuro se integrará el código en C de Cell-ID para dar una
rutina acabada y completa.

El programa recorrerá las subcarpetas. Toma de las tablas de salida ``cellID``
(``out_all``, ``out_bf_fl_mapping``) por position. Creará una subcarpeta
``pydata/df`` (opcional).

Salida: único DataFrame con los valores de cada tabla. Agregará las series:

* ``df['ucid']`` identificador de célula por posición. ``int()``.
    ``Unic Cell ID = ucid``

* ``df['pos']`` identificador de posición de adquisición. ``int()``

* Para los valores de fluorescencia mapeados en ``out_bf_fl_mapping(df_mapp)``
  se crearran tantas series como ``flags`` en ``df_mapp`` multiplicado por la
  cantidad de variables morfológicas
  ``df['f_tot_x1fp','f_tot_x2fp',..., 'f_tot_xnfp']``
"""

import os
import re

import pandas as pd


def _read_df(path_file):
    """Crea una dataframe para el path.
    Elimina las delimitaciones por espacio de headers.

    :param path_file: ruta al texto plano (formato tabla).
    :return: A dataframe.
    """
    try:
        df = pd.read_table(path_file)
        # Elimino los espacios en los nombres de las columnas ' x.pos '.
        df.columns = df.columns.str.strip()
        # Cambio (. por _) las separaciones x.pos por x_pos
        df.columns = df.columns.str.replace(".", "_", regex=True)
        return df
    except FileNotFoundError:
        return f"No such file or directory: {path_file}"


def _create_ucid(df, pos):
    """ucid = unique cell identifier
    Crea una columna en el dataframe ``(df)`` con número de tracking
    ``df[ucid].loc[0] = 100000000000`` ``para ``cellID = 0``, ``Position = 1``.

    :param ucid: ``int(numberPosition + cellID)``.

    :param df: dataframe creado por ``cellID`` contiene la
               serie ``df['cellID']``.
    """
    try:
        if pos > 0:
            calc = pos * 100000000000
            df["ucid"] = [calc + cellid for cellid in df["cellID"]]
            return df
        else:
            return f"ingrese nueva una posición. '{pos}'' no es válida"
    except ValueError:
        # * No sé si es ValueError. Lo puse para que deje de joder
        # * flake8 después lo cambio
        return f"ingrese nueva una posición. '{pos}'' no es válida"


def _decod_chanel(df_mapping, flag):
    """Decodifica el flag, alojado en df_mapping. convirtiendolo
    en un nombre adecuado para su lectura.

    :param df_mapping: recibe un DataFrame de mapeo, ``df_mapping``,
                       con series ``['flag']=int()`` y
                       ``['fluor']=str(path_file) ``(ver ``cellID doc``).
    :return: ``str(chanel)`` correspondiente al ``int(flag)``.
    """
    # La escritura del cellID tiene la siguiente expresión regular
    # De 2 a tres caractes xFP luego  _Position
    chanel = re.compile(r"\w{2,3}_Position")
    # cellID codifica en la columna 'fluor'(ruta_archivo contiene
    # str('chanel'))
    # Filtro el DataFrame  para la coincidencia falg == fluor
    path = df_mapping[df_mapping["flag"] == flag]["fluor"].values[0]
    return chanel.findall(path)[0].split("_")[0].lower()


def _make_cols_chan(df, df_map, v=False):
    """Modifica la entrada df proviniente del pipeline ``pyCell``.
    Separa las series (columnas) morfológicas por canal de fluorecsencia.
    Elimina los valores redundandes de ``cellID`` y la serie ``'flag'``.

    :param df: Tabla ``cellID`` contiendo ``df['ucid']``.
    :param df_map: Tabla mapping ``cellID`` (``out_bf_fl_mapping``).
    :return: Crea serias morfologicas por canal
             ``df['f_tot_yfp',...,'f_nuc_bfp',...]``.
    """
    if v:
        print("Agragando columnas chanles ...")

    # Variables de fluorescencia
    fluor = [f_var for f_var in df.columns if f_var.startswith("f_")]
    # Creo un df con columnas variable_fluor por ucid y t_frame
    # idx = ['ucid', 't_frame'] if 't_frame' in df else idx = ['ucid']
    idx = ["ucid", "t_frame"]
    df_flag = df.pivot(index=idx, columns="flag", values=fluor)

    # Renombro columnas
    # Obtengo todos los flag:chanel en mapping
    df_m = df_map["flag"]
    chanels = {flag: _decod_chanel(df_map, flag) for flag in df_m.unique()}
    # Col_name
    df_flag.columns = [n[0] + "_" + chanels[n[1]] for n in df_flag.columns]

    # Lista de variables morfologicas
    morf = [name for name in df.columns if not name.startswith("f_")]

    # Creo un df con las variables morfologicas
    # Elimino las redundancias creadas por cellID, registo un solo flag.
    df_morf = df[df.flag == 0][morf]

    df_morf.set_index(idx, inplace=True)
    # Junto los df_flag y df_morf
    df = pd.merge(df_morf, df_flag, on=idx, how="outer")
    del df["flag"]
    # Por congruencia con RCell
    # Indices numéricos. ucid, t_frama pasan a columnas
    df = df.reset_index()
    # Ordeno columnas compatible con marco de datos RCell
    col = ["pos"] + idx[::-1] + ["cellID"]
    df = pd.concat([df[col], df.drop(col, axis=1)], axis=1)
    return df


def make_df(path_file, v=False):
    """Crea un dataframe con numero de tracking ``ucid`` y ``position``.

    :param path_file: nombre del archivo de salida ``cellID`` ``out_all``
    :return: un dataframe del archivo pasado conteniendo ``df['ucid']``.
    """
    # Position está codificada en el nombre del path al archivo.
    pos = int(re.findall("\\d+", path_file)[0])
    if v:
        print("leyendo position: ", pos)
    # Leo la tabla de texto plano.
    df = _read_df(path_file)
    # Asigno ucid
    df = _create_ucid(df, pos)
    df["pos"] = [pos for _ in range(len(df))]
    return df


def _parse_path(find_f, path=False):
    """Parsea la ruta pasada y devuele de a una las
    ubicaciones a los archivos ``find_f``, si ``path=False``
    la búsqueda se realiza en el ``path`` actual.

    :param path: str(path_to_parse).
    :param find_f: str(searched_file).
    :return: srt(path_to_find_f)
    """
    if path:
        os.chdir(path)
    # Rutas a los archivos out_all, out_bf_fl_mapping de cellID
    for r, d, f in os.walk("."):
        d.sort()
        for name in f:
            if find_f in name:
                yield os.path.join(r, name)


def cellidtable(path, n_data="out_all", n_mdata="mapping", v=False):
    """Concatenate the tables in the path with the pandas method.
    Transforms the identifying index of each cell from each data
    table into a temporal index UCID (Unique Cell Identifier)
    Disaggregate the columns of morphological measurements into
    columns by fluorescence channel. It uses the mapping present
    in the metadata file (mapping).

    :param path: global path from output ``cellID`` tables.
    :param n_data: srt() name to finde each table data
    :param n_mdata: srt() name to finde tables metadata/mapping_tags
    :param verbose: bool, True to print in realtime pipeline
    :return: dataframe ``cellID``.

    Example
    -------
    >>> import pycellid_io as ld

    >>> df = ld.cellidtable(path, n_data='out_all', n_mdata='mapping', v=False)

    """
    # Me posiciono en el directorio a buscar.
    os.chdir(path)
    # creo un DataFrame vacío.
    df = pd.DataFrame()
    # Itero sobre la lista tablas (data).
    for data_table in _parse_path(find_f=n_data):
        # Proceso las tablas de a una
        df_i = make_df(data_table, v=v)
        # Modifica el iesimo_df, crea columnas por fluorescencia
        df_i = _make_cols_chan(
            df_i, _read_df(_parse_path(find_f=n_mdata).__next__()), v=v
        )
        df = pd.concat([df, df_i], ignore_index=True)
    return df


def save_df(df, dir_name="pydata"):
    """Crea una carpeda ``/pydata``
    guarda el parámetro ``df`` DataFrame"""
    # Me fijo si no existe el directorio
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)  # si no existe lo creo
    os.chdir(dir_name)
    # guardo csv
    df.to_csv("df.csv", index=False)
    return f"Se guardó el archivo {df}"


def main(argv):
    try:
        if len(argv) != 2:
            raise SystemExit(
                f"\nUso adecuado: {sys.argv[0]}" " " "path salida de cellID"
            )
        df = cellidtable(argv[1])

        guardar = input("¿Decea guardar DataFrame? S/N ")
        if "s" in guardar.lower():
            save_df(df)

    except SystemExit as e:
        print(e)
        path = input("\ningrege path de acceso a salida cellID\n")

        df = cellidtable(path)

        p = "¿Decea crear la carpeta pydata y guardar DataFrame? S/N "
        guardar = input(p)
        if "s" in guardar.lower():
            save_df(df)


if __name__ == "__main__":
    import sys

    main(sys.argv)
