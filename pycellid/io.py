# !/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the
#   PyCellID Project (
#     https://github.com/pyCellID,
#     https://github.com/darksideoftheshmoo
# ).
# Copyright (c) 2021, Clemente Jose
# License: MIT
#   Full Text: https://github.com/pyCellID/pyCellID/blob/main/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""in-out implementations for pyCellID."""

# =============================================================================
# IMPORTS
# =============================================================================

import re
from pathlib import Path

import pandas as pd

# =============================================================================
# FUNCTIONS
# =============================================================================


# Processing of tables
def _read_df(path_file):
    """Read a df in the path and remove the delimitations by space headers.

    Parameters
    ----------
    path_file: ``str``
        String containing the path files.

    Return
    ------
        A dataframe.
    """
    df = pd.read_table(path_file)
    # Remove spaces in headers ' x.pos ' produced from cellid
    df.columns = df.columns.str.strip()
    # Change name delimiter "."" to "_"
    df.columns = df.columns.str.replace(".", "_", regex=True)
    return df


def _create_ucid(df, pos):
    """Match the data with the numbered position from the microscopy image.

    CellID param: cellID = cell identifier into df ``df['ucid']``
    Positional series pycellid ucid = unique cell identifier

    Parameters
    ----------
    df:
        dataframe from ``cellID`` whith serie ``df['cellID']``.
    pos:
        ``int(positional image number)``.

    Return
    ------
        Same df with the ``ucid`` series.

    """
    if not isinstance(pos, int):
        raise TypeError(f"{pos} must be integer")
    calc = pos * 100000000000
    df["ucid"] = [calc + cellid for cellid in df["cellID"]]
    return df


def _decod_chanel(df_mapping, flag):
    """Join the fluorescence reference and numeric ``flag`` in a string.

    Parameters
    ----------
    df_mapping:
        Table with metadata. Must contain column e.g.
        ``['flag']=int()`` ``['fluor']=str('xFP_Position')``
    flag:
        A numeric reference.

    Return
    ------
        ``str(channel)`` from ``int(flag)``.
    """
    # Two or three characters for fluorescent proteins and _Position
    # xFP_Position
    channel = re.compile(r"([\w][f|F][\w]{,1})([_|\D][p|P][\D]*)")
    # re.compile(r"\w{2,3}_Position")
    # CellID encodes in column 'fluor'(path_file whit str('channel'))

    path = df_mapping[df_mapping["flag"] == flag]["fluor"].values[0]

    if not path:
        raise ValueError(f"{flag} is not encoding in {df_mapping}")

    else:
        return channel.findall(path)[0][0].lower()
    # channel.findall(path)[0].split("_")[0].lower()


def _make_cols_chan(df, df_map):
    """Dataframe df will be restructured.

    Split morphological series by fluorescence channels.
    Remove ``flag`` serie and redundant values ​​from CellID.

    Parameters
    ----------
    df:
        Data Table ``cellID.out.all``.
    df_map:
        Mapping Table ``cellID`` (``out_bf_fl_mapping``).

    Return
    ------
        Create morphological series per channel.
             ``df['f_tot_yfp',...,'f_nuc_bfp',...]``.
    """
    # Fluorescence variables
    fluor = [f_var for f_var in df.columns if f_var.startswith("f_")]
    # Save the series with fluorescence values ​​in df_flag
    # idx = ['ucid', 't_frame'] if 't_frame' in df else idx = ['ucid']
    df_flag = df.pivot(index=["ucid", "t_frame"], columns="flag", values=fluor)

    # Rename columns. Get all the flags:chanel in mapping
    chanels = {fg: _decod_chanel(df_map, fg) for fg in df_map["flag"].unique()}

    df_flag.columns = [f"{n[0]}_{chanels[n[1]]}" for n in df_flag.columns]

    # List of morphological variables
    morf = [name for name in df.columns if not name.startswith("f_")]

    # Remove redundant values ​​from CellID.
    df_morf = df[df.flag == 0][morf]
    df_morf.set_index(["ucid", "t_frame"], inplace=True)
    # Merge df_flag y df_morf
    df = pd.merge(df_morf, df_flag, on=["ucid", "t_frame"], how="outer")

    df = df.reset_index()
    # Relevant features
    col = ["pos", "t_frame", "ucid", "cellID"]

    df = pd.concat([df[col], df.drop(col, axis=1)], axis=1)
    return df


def make_df(path_file):
    """Make a dataframe with number tracking ``ucid`` and ``position``.

    Parameters
    ----------
    path_file:
        path to data table, CellID's ``outall``.

    Return
    ------
        A dataframe with ``df['ucid']`` unique cell identifier.
    """
    # Position encoding.
    try:
        pos = int(re.search(r"([p|P][\D]*)(\d+)", str(path_file), flags=0)[2])
    except TypeError as err:
        print(f"{err = }\nPath < {path_file} > does not encode valid position")
        pos = None
    if pos:
        try:
            df = _read_df(path_file)
            df = _create_ucid(df, pos)
            df["pos"] = [pos for _ in range(len(df))]
            return df
        except (FileNotFoundError, TypeError) as err:
            print(f"{err = }\n {path_file}")


# To find tables
def _parse_path(path, find_f):
    """Construct a generator list with the path file.

    Parameters
    ----------
    path : str
        path to folder root to find.
    find_f : str
        str(searched_file).

    Return
    ------
        srt(path_to_find_f).
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"Path < {path} > not exist")
    else:
        return (f for f in Path(path).rglob(find_f))


# Final pipeline
def merge_id_tables(path, n_data="out_all", n_mdata="*mapping", v=False):
    """Concatenate the tables in the path with the pandas method.

    Transforms the identifying index of each cell from each data
    table into a temporal index UCID (Unique Cell Identifier)
    Disaggregate the columns of morphological measurements into
    columns by fluorescence channel. It uses the mapping present
    in the metadata file (mapping).

    Parameters
    ----------
    path:
        global path from output ``cellID`` tables.
    n_data:
        srt() name to finde each table data.
    n_mdata:
        srt() name to finde tables metadata/mapping_tags
    verbose:
        bool, True to print in realtime pipeline

    Return
    ------
        A dataframe ``cellID``.

    * to use:

    >>> import pycellid_io as ld
    >>> df=ld.cellid_table(
        path = '../my_experiment',
        n_data ='out_all',
        n_mdata ='mapping',
        v=False
    )
    """
    # Initial tables
    data_tables = _parse_path(path=path, find_f=n_data)
    file_mapping = _parse_path(path=path, find_f=n_mdata)
    table = next(data_tables)

    if v:
        print(f"Reading : \n{table}")
    df = make_df(table)
    df = _make_cols_chan(df, pd.read_table(next(file_mapping)))

    for data_table in data_tables:
        if v:
            print(f"Reading : \n{data_table}")
        df_i = make_df(data_table)
        df_i = _make_cols_chan(df_i, pd.read_table(next(file_mapping)))
        df = pd.concat([df, df_i], ignore_index=True)
    return df


# To complete the experimet tables
def merge_pdata_csv(df, data_path, cl_mrg="pos", sep=",", *args):
    """Add the content in the ``data_path`` table to the ``DataFrame``.

    There must be a matching of values and header of the
    ``col_merge`` in both frames. Use the pandas merge method.

    Parameters
    ----------
    df:
        DataFrame to be modified.
    data_path:
        str() path to csv table to be added.
    col_merge:
        str() name of header must be coincidence.
    sep:
        separator or tab.
    *args:
        see pandas.read_csv() for extend function.

    Return
    ------
        new DataFrame containing aggregate series.
    """
    add_d = pd.read_csv(data_path, *args)

    df = pd.merge(df, right=add_d, how="left", left_on=cl_mrg, right_on=cl_mrg)

    return df