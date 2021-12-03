import os
import random
import re

import matplotlib

import numpy as np
from numpy.testing import assert_allclose

import pandas as pd

from pycellid.core import CellData, CellsPloter

import pytest as pt


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)
file_path = os.path.join(base, "samples_cellid")


@pt.mark.xfail(raises=FileNotFoundError)
def test__check_path(invalid_pos_fail, create_test_object_minimum):
    valid_df = create_test_object_minimum
    CellData(path=invalid_pos_fail, df=valid_df)


def test_get_dataframe():
    df = CellData.from_csv(file_path)
    df_test = df.get_dataframe()
    assert isinstance(df_test, pd.DataFrame)


def test_repr(create_test_object_minimum):
    num = re.compile(r"-?\d+\.?\d*")
    df_repr = repr(create_test_object_minimum)
    parts = df_repr.split("\n")
    expected = [
        "   pos  t_frame  cellID  f_local2_bg_rfp  f_local2_bg_tfp",
        "0    1        0       0         241.2194         12523.05",
        "1    1        1       0         240.1235         12138.30",
        "2    1        2       0         242.0784         11993.09",
    ]
    assert len(parts) == len(expected)

    for i, val in enumerate(parts[1:]):
        n_parts = np.array([n for n in num.findall(val)][1:], dtype=float)
        n_spect = np.array(
            [n for n in num.findall(expected[i + 1])][1:], dtype=float
        )

        assert_allclose(n_parts, n_spect, rtol=1e-3, verbose=True)


def test_repr_html(create_test_object_minimum):
    num_rex = re.compile(r"\\-?\d+\.?\d*")
    idx_html_rex = re.compile(r"<th>\d+</th>")

    expected = (
        '<div class="PyCellID.core.CellData" id=140120093808240>'
        '<div class="PyCellID.core.CellData" id=140121229801216><div>\n'
        "<style scoped>\n"
        "    .dataframe tbody tr th:only-of-type {\n"
        "        vertical-align: middle;\n"
        "    }\n\n"
        ""
        "    .dataframe tbody tr th {\n"
        "        vertical-align: top;\n"
        "    }\n\n"
        ""
        "    .dataframe thead th {\n"
        "        text-align: right;\n"
        "    }\n"
        "</style>\n"
        '<table border="1" class="dataframe">\n'
        "  <thead>\n"
        '    <tr style="text-align: right;">\n'
        "      <th></th>\n"
        "      <th>pos</th>\n"
        "      <th>t_frame</th>\n"
        "      <th>cellID</th>\n"
        "      <th>f_local2_bg_rfp</th>\n"
        "      <th>f_local2_bg_tfp</th>\n"
        "    </tr>\n"
        "  </thead>\n"
        "  <tbody>\n"
        "    <tr>\n"
        "      <th>0</th>\n"
        "      <td>1</td>\n"
        "      <td>0</td>\n"
        "      <td>0</td>\n"
        "      <td>241.2194</td>\n"
        "      <td>12523.05</td>\n"
        "    </tr>\n"
        "    <tr>\n"
        "      <th>1</th>\n"
        "      <td>1</td>\n"
        "      <td>1</td>\n"
        "      <td>0</td>\n"
        "      <td>240.1235</td>\n"
        "      <td>12138.30</td>\n"
        "    </tr>\n"
        "    <tr>\n"
        "      <th>2</th>\n"
        "      <td>1</td>\n"
        "      <td>2</td>\n"
        "      <td>0</td>\n"
        "      <td>242.0784</td>\n"
        "      <td>11993.09</td>\n"
        "    </tr>\n"
        "  </tbody>\n"
        "</table>\n"
        "</div>PyCellID.core.CellData - 3 rows x 5 columns"
        "</div>PyCellID.core.CellData - 3 rows x 5 columns</div>"
    )

    repr_test = create_test_object_minimum._repr_html_()

    parts = idx_html_rex.split(repr_test)
    spect_part = idx_html_rex.split(expected)

    head = num_rex.split(parts[0])[0].split(" ")
    headers = [
        "<th>pos</th>\n",
        "<th>t_frame</th>\n",
        "<th>cellID</th>\n",
        "<th>f_local2_bg_rfp</th>\n",
        "<th>f_local2_bg_tfp</th>\n",
    ]

    assert len(parts) == len(spect_part)

    for h in headers:
        assert h in head

    for i, body in enumerate(parts[1:2]):
        test = num_rex.split(body)[0].split(" ")[1:]
        spect_repr = num_rex.split(spect_part[i + 1])[0].split(" ")[1:]
        assert set(test) == set(spect_repr)


def test_celldata_slicing():
    df = CellData.from_csv(file_path)
    cols = list(df.columns)
    df_test = df[random.choice(cols)]
    assert isinstance(df_test, CellData)


def test_cellsploter_cells_image():
    df = CellData.from_csv(file_path)
    pp = CellsPloter(df)
    pp_ax = pp.cells_image()
    assertiony = isinstance(pp_ax.get_yaxis(), matplotlib.axis.YAxis)
    assertionx = isinstance(pp_ax.get_xaxis(), matplotlib.axis.XAxis)
    assert assertiony & assertionx


def test_cellsploter_cimage():
    df = CellData.from_csv(file_path)
    pp = CellsPloter(df)
    channel = random.choice(["BF", "CFP", "RFP", "YFP"])
    ucids = list(df["ucid"])
    ucid = random.choice(ucids)
    t_frames = list(df[df["ucid"] == ucid]["t_frame"])
    t_frame = random.choice(t_frames)
    dict_cimage = {
        "channel": channel,
        "ucid": ucid,
        "t_frame": t_frame,
    }
    pp_ax = pp.cimage(dict_cimage)
    assertiony = isinstance(pp_ax.get_yaxis(), matplotlib.axis.YAxis)
    assertionx = isinstance(pp_ax.get_xaxis(), matplotlib.axis.XAxis)
    assert assertiony & assertionx


def test_cellsploter_cimage_2(valid_picture):
    df = CellData.from_csv(file_path)
    pp = CellsPloter(df)
    pp_ax = pp.cimage(valid_picture)
    assertiony = isinstance(pp_ax.get_yaxis(), matplotlib.axis.YAxis)
    assertionx = isinstance(pp_ax.get_xaxis(), matplotlib.axis.XAxis)
    assert assertiony & assertionx


def test_cellsploter_cimage_warning():
    message = "not match ucid and t_frame. See picture!"
    with pt.warns(UserWarning, match=message):
        df = CellData.from_csv(file_path)
        pp = CellsPloter(df)

        ucids = df["ucid"].unique()
        ucid = random.choice(ucids)

        channel = random.choice(["BF", "CFP", "RFP", "YFP"])

        tframe_complete = set(range(13))
        tframe_sample = set(df[df["ucid"] == ucid]["t_frame"].unique())

        empty_tframe = tframe_complete - tframe_sample
        while not empty_tframe:
            ucid = random.choice(ucids)
            tframe_sample = set(df[df["ucid"] == ucid]["t_frame"].unique())
            empty_tframe = tframe_complete - tframe_sample
        t_frame = random.choice(list(empty_tframe))

        dict_cimage = {
            "channel": channel,
            "ucid": ucid,
            "t_frame": t_frame,
        }
        pp_ax = pp.cimage(dict_cimage)
        pp_ax


def test_cellploter_call():
    df = CellData.from_csv(file_path)
    pp = CellsPloter(df)
    pp_ax = pp()
    assertiony = isinstance(pp_ax.get_yaxis(), matplotlib.axis.YAxis)
    assertionx = isinstance(pp_ax.get_xaxis(), matplotlib.axis.XAxis)
    assert assertiony & assertionx


def test_celldata_gt(create_test_object_minimum):
    assertion = (create_test_object_minimum > -1).all(axis=None)
    assert assertion


def test_celldata_ge(create_test_object_minimum):
    assertion = (create_test_object_minimum >= -1).all(axis=None)
    assert assertion


def test_celldata_lt(create_test_object_minimum):
    assertion = (create_test_object_minimum < 1e15).all(axis=None)
    assert assertion


def test_celldata_le(create_test_object_minimum):
    assertion = (create_test_object_minimum <= 1e15).all(axis=None)
    assert assertion


def test_check_path(fake_filepath):
    with pt.raises(FileNotFoundError):
        file = os.path.join(base, "samples_cellid", "pydata", "df.csv")
        df = pd.read_csv(file)
        cell_test = CellData(path=fake_filepath, df=df)
        cell_test.plot()


def test_call_plot(fake_filepath):
    df = CellData.from_csv(file_path)
    df_ax = df.plot()
    assertiony = isinstance(df_ax.get_yaxis(), matplotlib.axis.YAxis)
    assertionx = isinstance(df_ax.get_xaxis(), matplotlib.axis.XAxis)
    assert assertiony & assertionx


def test_invalid_plot_method(create_test_object_minimum):
    with pt.raises(AttributeError):
        pp = CellsPloter(create_test_object_minimum)
        pp("something")


def test_not_callable(create_test_object_minimum):
    with pt.raises(AttributeError):
        pp = CellsPloter(create_test_object_minimum)
        pp(create_test_object_minimum)


def test_repr_html_2(create_test_object_minimum):
    num_rex = re.compile(r"\\-?\d+\.?\d*")
    idx_html_rex = re.compile(r"<th>\d+</th>")

    expected = (
        '<div class="PyCellID.core.CellData" id=140120093808240>'
        '<div class="PyCellID.core.CellData" id=140121229801216><div>\n'
        "<style scoped>\n"
        "    .dataframe tbody tr th:only-of-type {\n"
        "        vertical-align: middle;\n"
        "    }\n\n"
        ""
        "    .dataframe tbody tr th {\n"
        "        vertical-align: top;\n"
        "    }\n\n"
        ""
        "    .dataframe thead th {\n"
        "        text-align: right;\n"
        "    }\n"
        "</style>\n"
        '<table border="1" class="dataframe">\n'
        "  <thead>\n"
        '    <tr style="text-align: right;">\n'
        "      <th></th>\n"
        "      <th>pos</th>\n"
        "      <th>t_frame</th>\n"
        "      <th>cellID</th>\n"
        "      <th>f_local2_bg_rfp</th>\n"
        "      <th>f_local2_bg_tfp</th>\n"
        "    </tr>\n"
        "  </thead>\n"
        "  <tbody>\n"
        "    <tr>\n"
        "      <th>0</th>\n"
        "      <td>1</td>\n"
        "      <td>0</td>\n"
        "      <td>0</td>\n"
        "      <td>241.2194</td>\n"
        "      <td>12523.05</td>\n"
        "    </tr>\n"
        "    <tr>\n"
        "      <th>1</th>\n"
        "      <td>1</td>\n"
        "      <td>1</td>\n"
        "      <td>0</td>\n"
        "      <td>240.1235</td>\n"
        "      <td>12138.30</td>\n"
        "    </tr>\n"
        "    <tr>\n"
        "      <th>2</th>\n"
        "      <td>1</td>\n"
        "      <td>2</td>\n"
        "      <td>0</td>\n"
        "      <td>242.0784</td>\n"
        "      <td>11993.09</td>\n"
        "    </tr>\n"
        "  </tbody>\n"
        "</table>\n"
        "</div>PyCellID.core.CellData - 3 rows x 5 columns"
        "</div>PyCellID.core.CellData - 3 rows x 5 columns</div>"
    )
    obj_test = create_test_object_minimum
    repr_test = obj_test._df._repr_html_()

    parts = idx_html_rex.split(repr_test)
    spect_part = idx_html_rex.split(expected)

    head = num_rex.split(parts[0])[0].split(" ")
    headers = [
        "<th>pos</th>\n",
        "<th>t_frame</th>\n",
        "<th>cellID</th>\n",
        "<th>f_local2_bg_rfp</th>\n",
        "<th>f_local2_bg_tfp</th>\n",
    ]

    assert len(parts) == len(spect_part)

    for h in headers:
        assert h in head

    for i, body in enumerate(parts[1:2]):
        test = num_rex.split(body)[0].split(" ")[1:]
        spect_repr = num_rex.split(spect_part[i + 1])[0].split(" ")[1:]
        assert set(test) == set(spect_repr)
