# !/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import io

import numpy as np
from numpy.random import RandomState, SeedSequence

import pandas as pd
# from pandas.testing import assert_extension_array_equal
# from pandas._testing import assert_frame_equal
# from pandas._testing import assert_index_equal

import pytest

# import re

# import tempfile

import pycellid.io as ld


# =============================================================================
# Parameter & fixtures
# =============================================================================


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)


@pytest.fixture
def invalid_f_name_fail():
    file = ["out_all", "bf_vcellid", "fl_vcellid", "out_bf_fl_mapping"]
    f = np.random.choice(file)
    n = np.random.randint(5, 200)
    f_ph = os.path.join(base, "muestras_cellid", f"Position{n}", f"{f}")
    return f_ph


@pytest.fixture
def invalid_pos_fail():
    l_pos = ["osition", "Posicion", "01", "osition01", "p", "P"]
    pos = np.random.choice(l_pos)
    ph = os.path.join(base, "muestras_cellid", f"{pos}", "out_all")
    return ph


@pytest.fixture
def rand_make_df():
    """Choise a random table from the folder mustras_cellid"""
    p = np.random.randint(1, 4)
    path = os.path.join(base, "muestras_cellid", f"Position0{p}", "out_all")
    df = ld.make_df(path)
    return df


@pytest.fixture
def create_mapping_file():
    df = pd.DataFrame(
        {
            "flag": [0, 1, 2, 3],
            "fluor": ["BF_Pos02", "YFP_Pos02", "CFP_Pos02", "RFP_Pos02"],
        }
    ).to_csv(sep="\t", index=False)
    return io.StringIO(df)


@pytest.fixture(scope="session")
def create_mapping_file_min():
    df = pd.DataFrame(
        {
            "flag": [0, 1],
            "fluor": ["BF_Pos02", "YFP_Pos02"],
        }
    ).to_csv(sep="\t", index=False)
    return io.StringIO(df)


@pytest.fixture
def create_out_all_file():
    rs = RandomState(np.random.MT19937(SeedSequence(1234)))
    df = pd.DataFrame(
        {
            "area": np.linspace(200, 1000, 300, dtype=int),
            "f_nuc": np.linspace(50, 500, 300, dtype=int),
            "f_tot": np.linspace(50, 500, 300, dtype=int),
            "f_vac": np.linspace(50, 500, 300, dtype=int),
            "flag": rs.randint(0, 4, 300, dtype=int),
            "cellID": np.linspace(100, 400, 300, endpoint=True, dtype=int),
            "ucid": np.linspace(100, 400, 300, endpoint=True, dtype=int)
            + 100000000000,
            "t_frame": rs.randint(1, 13, 300, dtype=int),
            "pos": np.ones(300, dtype=int),
        }
    ).to_csv(sep="\t", index=False)
    return io.StringIO(df)


@pytest.fixture(scope="session")
def create_out_all_file_min():
    df = pd.DataFrame(
        {
            "area": np.linspace(200, 1000, 10, dtype=int),
            "f_nuc": np.linspace(50, 500, 10, dtype=int),
            "f_tot": np.linspace(50, 500, 10, dtype=int),
            "f_vac": np.linspace(50, 500, 10, dtype=int),
            "flag": [0 if i % 2 == 0 else 1 for i in range(1, 11)],
            "cellID": np.linspace(100, 400, 10, endpoint=True, dtype=int),
            "ucid": np.linspace(100, 400, 10, endpoint=True, dtype=int)
            + 100000000000,
            "t_frame": [i for i in range(1, 11)],
            "pos": np.ones(10, dtype=int),
        }
    ).to_csv(sep="\t", index=False)
    return io.StringIO(df)


@pytest.fixture(scope="session")
def read_mapp_file():
    return pd.read_table(create_mapping_file)


@pytest.fixture(scope="session")
def read_out_all_file(create_out_all_file):
    return pd.read_table(create_out_all_file)


# =============================================================================
# Test read, parse: Folders, File names
# =============================================================================


@pytest.mark.xfail(raises=FileNotFoundError)
def test_make_df_file_path_fails():
    ld.make_df(invalid_f_name_fail)


@pytest.mark.xfail(raises=TypeError)
def test_make_df_file_pos_fails():
    ld.make_df(invalid_pos_fail)


def test_merge_id_tables_FND():
    f = np.random.choice(["P", "p", "Pos", "Position", "Posicion"])
    n = np.random.randint(5, 200)
    FND = os.path.join(base, "muestras_cellid", f"{f}{n}")
    with pytest.raises(FileNotFoundError):
        ld.merge_id_tables(FND)


def test_merge_id_tables_FND_file():
    n = np.random.randint(1, 4)
    folder = os.path.join(base, "muestras_cellid", f"P{n}")
    data_table = np.random.choice(
        ["out", "out_alll", "Pos", "tablas", "datos.txt"]
    )
    m_data = np.random.choice(["map", "mapeo", "m", "seguimiento"])
    with pytest.raises(FileNotFoundError):
        ld.merge_id_tables(path=folder, n_data=data_table, n_mdata=m_data)


def test_read_mapping_file(create_mapping_file):
    df1 = ld._read_df(create_mapping_file)
    df2 = pd.DataFrame(
        {
            "flag": [0, 1, 2, 3],
            "fluor": ["BF_Pos02", "YFP_Pos02", "CFP_Pos02", "RFP_Pos02"],
        }
    )
    assert np.array_equal(df1.values, df2.values)


def test_read_out_all_file(create_out_all_file):
    rs = RandomState(np.random.MT19937(SeedSequence(1234)))
    df1 = ld._read_df(create_out_all_file)
    df2 = pd.DataFrame(
        {
            "area": np.linspace(200, 1000, 300, dtype=int),
            "f_nuc": np.linspace(50, 500, 300, dtype=int),
            "f_tot": np.linspace(50, 500, 300, dtype=int),
            "f_vac": np.linspace(50, 500, 300, dtype=int),
            "flag": rs.randint(0, 4, 300, dtype=int),
            "cellID": np.linspace(100, 400, 300, endpoint=True, dtype=int),
            "ucid": np.linspace(100, 400, 300, endpoint=True, dtype=int)
            + 100000000000,
            "t_frame": rs.randint(1, 13, 300, dtype=int),
            "pos": np.ones(300, dtype=int),
        }
    )
    assert np.array_equal(df1.values, df2.values)


# =============================================================================
# test crated values: col_names, UCID
# =============================================================================


def test_make_df_c_names(rand_make_df):
    for name in rand_make_df.columns:
        assert "." not in name
        assert " " not in name[0]
        assert " " not in name[-1]


def test_fluor_col(create_out_all_file, create_mapping_file):
    ch = ["BF", "YFP", "CFP", "RFP"]
    var = ["f_nuc", "f_tot", "f_vac"]
    var_ch = [f"{v}_{c.lower()}" for v in var for c in ch]

    df_out_all = ld._read_df(create_out_all_file)
    df_mapp = ld._read_df(create_mapping_file)

    df = ld._make_cols_chan(df_out_all, df_mapp)

    for name in df.columns:
        if name.startswith("f_"):
            assert name in var_ch


#            var_ch = var_ch.remove(name)


def test_make_df_ucid(rand_make_df):
    ucid = rand_make_df.ucid
    pos = rand_make_df.pos
    cellID = rand_make_df.cellID
    assert np.array_equal(ucid, pos * 100000000000 + cellID)


# =============================================================================
# test data integrity
# =============================================================================


def test_make_df_values():
    p_out_all = os.path.join(base, "muestras_cellid", "Position01", "out_all")
    df1 = ld.make_df(p_out_all)
    df1 = df1.drop(["ucid", "pos"], axis=1)
    df2 = pd.read_table(p_out_all)
    assert np.array_equal(df1.values, df2.values)


# =============================================================================
# test: transpose tables and add fluorescence values
# =============================================================================


def test_make_cols_cahnnels(create_out_all_file_min, create_mapping_file_min):
    """
    Variables starting with f_ (f_vacuole) are disaggregated by channel
    f_vacuole_yfp f_vacuole_tfp f_vacuole_rfp f_vacuole_tfp f_vacuole_bf
    """
    df_out_all = ld._read_df(create_out_all_file_min)
    df_mapp = ld._read_df(create_mapping_file_min)

    df_pycellid = ld._make_cols_chan(df_out_all, df_mapp)

    par = [np.nan if i % 2 == 0 else i * 50 for i in range(1, 11)]
    impar = [i * 50 if i % 2 == 0 else np.nan for i in range(1, 11)]

    df = pd.DataFrame(
        {
            "area": np.linspace(200, 1000, 10, dtype=int),
            "f_nuc_bf": par,
            "f_nuc_yfp": impar,
            "f_tot_bf": par,
            "f_tot_yfp": impar,
            "f_vac_bf": par,
            "f_vac_yfp": impar,
            "flag": [0 if i % 2 == 0 else 1 for i in range(1, 11)],
            "cellID": np.linspace(100, 400, 10, endpoint=True, dtype=int),
            "ucid": np.linspace(100, 400, 10, endpoint=True, dtype=int)
            + 100000000000,
            "t_frame": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "pos": np.ones(10, dtype=int),
        }
    )
    assert len(df_pycellid.columns) == len(df.columns)


# =============================================================================
# test merge table
# =============================================================================


# def foo():
#     ld._make_cols_chan(ld.make_df(out_all), mapping)
#     pass


# =============================================================================
# ToDo
# =============================================================================

# def test_make_df_values():
#    df1 = ld.make_df(p_out_all)
#    df1 = df1.drop(["ucid", "pos"], axis=1)
#    df2 = pd.read_table(p_out_all)
#       assert np.array_equal(df1.values, df2.values)


# def test_make_df_values2(tmpdir):
#    data_in = 'out_all'
#    f_path = f'{tmpdir}/test.txt'
#    df = ld.make_df(f_path)
#
#    with open(f_path) as file_out:
#        data_out = file_out.read()

#    assert df == data_out


# @pytest.fixture(scope="session")
# def out_all_mapping_file(tmp_path_factory):
#     folder = tmp_path_factory.mktemp("Pos01")
#     #.join("out_all.txt")
#     out_all = pd.DataFrame(
#         {
#             'area': np.linspace(200, 1000, 300),
#             'f_nuc': np.linspace(50, 500, 300),
#             'f_tot': np.linspace(50, 500, 300),
#             'flag': np.random.randint(0,4, 300, dtype=int),
#             'cellID': np.linspace(100, 400, 300, endpoint=True, dtype=int),
#             'ucid': np.linspace(100,400, 300, endpoint=True) + 100000000000,
#             't_frame': np.random.randint(1,13,300),
#             'pos': np.ones(300,dtype=int)
#         }
#     ).to_csv(os.path.join(f'{folder}', 'out_all'))

#     mapping_file = pd.DataFrame(
#         {
#             'flag': [0,1,2,3],
#             'fluor': ['BF_Pos02', 'YFP_Pos02', 'CFP_Pos02', 'RFP_Pos02']
#         }
#     ).to_csv(os.path.join(f'{folder}', 'mapping_file'))

#     return folder


# CONTENT = "content"


# def test_create_file(tmp_path):
#     d = tmp_path / "sub"
#     d.mkdir()
#     p = d / "hello.txt"
#     p.write_text(CONTENT)
#     assert p.read_text() == CONTENT
#     assert len(list(tmp_path.iterdir())) == 1
#     assert 0


# def test_pivot(path=out_all_mapping_file):
#     df = ld.merge_id_tables(path,
#         n_data='out_all_file',
#         n_mdata='mapping_file'
#         )
#     fluor_var = ['f_nuc', 'f_tot']
#     ch = ['bf', 'cfp', 'yfp', 'rfp', 'tfp']
#     var = [f'{f}_{c}' for c in ch for f in fluor_var]

#     assert var in df.columns
