import os
import random

import matplotlib

import pandas as pd

from pycellid.core import CellData, CellsPloter

import pytest


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)
file_path = os.path.join(base, 'samples_cellid')


def test_get_dataframe():
    df = CellData.from_csv(file_path)
    df_test = df.get_dataframe()
    assert isinstance(df_test, pd.DataFrame)


def test_repr(create_test_object_minimum):
    #df_repr = 
    repr_result = (
        '   pos  t_frame  cellID  f_local2_bg_rfp  f_local2_bg_tfp\n'
        '0    1        0       0         241.2194         12523.05\n'
        '1    1        1       0         240.1235         12138.30\n'
        '2    1        2       0         242.0784         11993.09'
        )
    assert repr(create_test_object_minimum) == repr_result


def test_repr_html(create_test_object_minimum):
    df_repr = create_test_object_minimum._repr_html_()
    df_repr = df_repr.split("\n", 1)[1]
    repr_result = (
        '<style scoped>\n'
        '    .dataframe tbody tr th:only-of-type {\n'
        '        vertical-align: middle;\n'
        '    }\n'
        '\n'
        '    .dataframe tbody tr th {\n'
        '        vertical-align: top;\n'
        '    }\n'
        '\n'
        '    .dataframe thead th {\n'
        '        text-align: right;\n'
        '    }\n'
        '</style>\n'
        '<table border="1" class="dataframe">\n'
        '  <thead>\n'
        '    <tr style="text-align: right;">\n'
        '      <th></th>\n'
        '      <th>pos</th>\n'
        '      <th>t_frame</th>\n'
        '      <th>cellID</th>\n'
        '      <th>f_local2_bg_rfp</th>\n'
        '      <th>f_local2_bg_tfp</th>\n'
        '    </tr>\n'
        '  </thead>\n'
        '  <tbody>\n'
        '    <tr>\n'
        '      <th>0</th>\n'
        '      <td>1</td>\n'
        '      <td>0</td>\n'
        '      <td>0</td>\n'
        '      <td>241.2194</td>\n'
        '      <td>12523.05</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>1</th>\n'
        '      <td>1</td>\n'
        '      <td>1</td>\n'
        '      <td>0</td>\n'
        '      <td>240.1235</td>\n'
        '      <td>12138.30</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>2</th>\n'
        '      <td>1</td>\n'
        '      <td>2</td>\n'
        '      <td>0</td>\n'
        '      <td>242.0784</td>\n'
        '      <td>11993.09</td>\n'
        '    </tr>\n'
        '  </tbody>\n'
        '</table>\n'
        '</div>PyCellID.core.CellData - 3 rows x 5 columns'
        '</div>PyCellID.core.CellData - 3 rows x 5 columns</div>'
        )
    assert df_repr == repr_result


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
    channel = random.choice(['BF', 'CFP', 'RFP', 'YFP'])
    ucids = list(df['ucid'])
    ucid = random.choice(ucids)
    t_frames = list(df[df['ucid'] == ucid]['t_frame'])
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
    with pytest.warns(UserWarning, match=message):
        df = CellData.from_csv(file_path)
        pp = CellsPloter(df)

        ucids = df['ucid'].unique()
        ucid = random.choice(ucids)

        channel = random.choice(['BF', 'CFP', 'RFP', 'YFP'])

        tframe_complete = set(range(13))
        tframe_sample = set(df[df['ucid'] == ucid]['t_frame'].unique())

        empty_tframe = tframe_complete - tframe_sample
        while not empty_tframe:
            ucid = random.choice(ucids)
            tframe_sample = set(df[df['ucid'] == ucid]['t_frame'].unique())
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
