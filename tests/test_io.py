# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random

import numpy as np

import pandas as pd

import pycellid.io as ld

import pytest as pt

# =============================================================================
# Parameter & fixtures
# =============================================================================


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)


# =============================================================================
# Test read, parse: Folders, File names
# =============================================================================


@pt.mark.xfail(raises=FileNotFoundError)
def test_make_df_file_path_fails(invalid_f_name_fail):
    ld.make_df(invalid_f_name_fail)


@pt.mark.xfail(raises=FileNotFoundError)
def test_make_df_file_pos_fails(invalid_pos_fail):
    ld.make_df(invalid_pos_fail)


def test_make_df_file():
    file = os.path.join(
        base, "samples_cellid", "pydata", "Position2e2+2", "out_all"
    )
    df = ld.make_df(file)
    assert df["pos"].unique() == 202


def test_merge_tables_fnd():
    f = np.random.choice(["P", "p", "Pos", "Position", "Posicion"])
    n = np.random.randint(5, 200)
    fnd = os.path.join(base, "samples_cellid", f"{f}{n}")
    with pt.raises(StopIteration):
        ld.merge_tables(fnd)


def test_merge_tables_fnd_file():
    n = np.random.randint(1, 4)
    folder = os.path.join(base, "samples_cellid", f"P{n}")
    data_table = random.choice(
        ["out", "out_alll", "Pos", "tablas", "datos.txt"]
    )
    m_data = random.choice(["map", "mapeo", "m", "seguimiento"])
    with pt.raises(StopIteration):
        ld.merge_tables(path=folder, n_data=data_table, n_mdata=m_data)


def test_read_mapping_file(create_mapping_file):
    df1 = ld.read_df(create_mapping_file)
    df2 = pd.DataFrame(
        {
            "flag": [0, 1, 2, 3],
            "fluor": ["BF_Pos02", "YFP_Pos02", "CFP_Pos02", "RFP_Pos02"],
        }
    )
    assert np.array_equal(df1.values, df2.values)


def test_read_out_all_file(create_out_all_file):
    rs = np.random.RandomState(np.random.MT19937(np.random.SeedSequence(1234)))
    df1 = ld.read_df(create_out_all_file)
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

    df_out_all = ld.read_df(create_out_all_file)
    df_mapp = ld.read_df(create_mapping_file)

    df = ld._make_cols_chan(df_out_all, df_mapp)

    for name in df.columns:
        if name.startswith("f_"):
            assert name in var_ch


def test_make_df_ucid(rand_make_df):
    ucid = rand_make_df.ucid
    pos = rand_make_df.pos
    cellid = rand_make_df.cellID
    assert np.array_equal(ucid, pos * 100000000000 + cellid)


# =============================================================================
# test data integrity
# =============================================================================


def test_make_df_values():
    p_out_all = os.path.join(base, "samples_cellid", "Position01", "out_all")
    df1 = ld.make_df(p_out_all)
    df1 = df1.drop(["ucid", "pos"], axis=1)
    df2 = pd.read_table(p_out_all)
    assert np.array_equal(df1.values, df2.values)


@pt.mark.parametrize(
    "string,expected",
    [
        ("BF_Position01_time01.tif.out.tif", "bf"),
        ("bF_Position01_t01.tif.out.tif", "bf"),
        ("bf_Position01_tiemp01.tif.out.tif", "bf"),
        ("dsf/BF_Position01_time01.tif.out.tif", "bf"),
        ("d34sf/BF_Position01_time01.tif.out.tif", "bf"),
        ("dsf/BF-Position01_time01.tif.out.tif", "bf"),
        ("d34sf/BF-Position01_time01.tif.out.tif", "bf"),
        ("RFP_Position01_time01.tif.out.tif", "rfp"),
        ("RFP_Position01_time01.tif.out.tif", "rfp"),
        ("RFp_Position01_time01.tif.out.tif", "rfp"),
        ("dsf/RfP_Position01_time01.tif.out.tif", "rfp"),
        ("d34sf/rFp_Position01_time01.tif.out.tif", "rfp"),
        ("dsf/YfP-Position01_time01.tif.out.tif", "yfp"),
        ("d34sf/YFP-Position01_time01.tif.out.tif", "yfp"),
    ],
)
def test_channels_rex(string, expected):
    assert ld.CHANNEL_REX.findall(string)[0][0].lower() == expected


@pt.mark.parametrize(
    "string,expected",
    [
        ("BF_Position1_t01.tif.out.tif", ["1"]),
        ("bF_Position01_time10.tif.out.tif", ["01"]),
        ("bf_P00001_time010.tif.out.tif", ["00001"]),
        ("dsf/position1e3_time01.tif.out.tif", ["1e3"]),
        ("d34sf/_Pos23e2+1.tif.out.tif", ["23e2+1"]),
        ("dsf/BF-Position23+12_time01.tif.out.tif", ["23"]),
        ("d34sf/BF-P01_time01.tif.out.tif", ["01"]),
        ("RFP_p01_time01.tif.out.tif", ["01"]),
        ("RFP/Pdasasfaf$sasd01_time01.tif.out.tif", []),
    ],
)
def test_position_rex(string, expected):
    assert ld.POSITION_REX.findall(string) == expected


# =============================================================================
# test: transpose tables and add fluorescence values
# =============================================================================


def test_make_cols_cahnnels(create_out_all_file_min, create_mapping_file_min):
    """
    Variables starting with f_ (f_vacuole) are disaggregated by channel
    f_vacuole_yfp f_vacuole_tfp f_vacuole_rfp f_vacuole_tfp f_vacuole_bf
    """
    df_out_all = ld.read_df(create_out_all_file_min)
    df_mapp = ld.read_df(create_mapping_file_min)

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


def test_merge_tables():
    # these are synthetic values ​​for test
    path = os.path.join(base, "samples_cellid", "pydata", "test")
    synthetic = ld.merge_tables(path=path).copy()

    ch_crtl = [
        "f_tot_yfp",
        "f_tot_cfp",
        "f_tot_tfp",
        "f_local_bg_yfp",
        "f_local_bg_cfp",
        "f_local_bg_tfp",
        "f_nucl_yfp",
        "f_nucl_cfp",
        "f_nucl_tfp",
    ]

    ucid_crtl = {
        1100000000001,
        1100000000002,
        2200000000001,
        2200000000002,
        3300000000001,
        3300000000002,
    }

    ch_var = []

    for name in synthetic.columns:
        assert "." not in name
        assert " " not in name[0]
        assert " " not in name[-1]
        if name.startswith("f_"):
            ch_var.append(name)

    assert ch_var == ch_crtl
    assert set(synthetic["pos"]) == {11, 22, 33}
    assert set(synthetic["ucid"]) == ucid_crtl


# =============================================================================
# To build controls
# =============================================================================

# %%

# Synthetic data for control.
# Simulation: acquisition of 3 fluorescent channels, 4 time-lapse in 3
# positions and measurement of 2 cells per image.
# Minimum tree of files (metadata and measurements) returned by CellID.

# rs = np.random.RandomState(np.random.MT19937(np.random.SeedSequence(1234)))

# folder_test = os.path.join(base, "samples_cellid", "pydata", "test")
# folder = ["Pos0011", "Position02e1+2", "p33"]
# ch = ["YFP", "CFP", "TFP"]
# m = []
# oa = []
# for f in folder:
#     path = os.path.join(folder_test, f)
#     os.mkdir(path)

#     img = [os.path.join(folder_test, f'{c}_{f}_time{t}.tif')
#            for c in ch for t in range(1,5)]

#     img_bf = [os.path.join(folder_test, f'BF_{f}_time{t}.tif')
#               for t in range(1,5)]

#     meta_data = pd.DataFrame(
#         {
#             'fluor' : img,
#             'flag' :  np.repeat(np.linspace(0, 2, 3, dtype=int), 4),
#             't.frame' : np.repeat(np.linspace(0, 2, 3, dtype=int), 4),
#             'bright' : img_bf * 3,
#             'bf.as.fl' : np.zeros(12, dtype=int),
#         }
#     )
#     meta_data.to_csv(
#         path_or_buf= os.path.join(folder_test, f, "out_bf_fl_mapping"),
#         sep="\t",
#         index=False,
#     )
#     m.append(meta_data)

#     df_crl = pd.DataFrame(
#         {
#           'cellID ' : np.repeat(np.linspace(1, 2, 2, dtype=int), 12),
#           't.frame' : list(np.repeat(np.linspace(0, 3, 4, dtype=int), 3))*2,
#           ' flag ' : [0,1,2] * 8,
#           ' f.tot ' : rs.rand(24),
#           ' f.local.bg ': rs.rand(24)*256,
#           ' f.nucl ': rs.rand(24)*256,
#         }
#     )
#     df_crl.to_csv(
#         path_or_buf= os.path.join(folder_test, f, "out_all"),
#         sep="\t",
#         index=False,
#     )
#     oa.append(df_crl)
