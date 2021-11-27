import io
import os

import numpy as np

import pandas as pd

import pycellid
import pycellid.io as ld


import pytest as pt


# =============================================================================
# Parameter & fixtures
# =============================================================================


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)


@pt.fixture
def invalid_f_name_fail():
    folder_n = ["osition", "p/osition", "Pos2e2+"]
    file = ["out_all", "bf_vcellid", "fl_vcellid", "out_bf_fl_mapping"]
    f = np.random.choice(file)
    n = np.random.randint(1, 3)
    f_ph = os.path.join(base, "samples_cellid", f"{folder_n}{n}", f"{f}")
    return f_ph


@pt.fixture
def invalid_pos_fail():
    l_pos = ["osition", "Posicion", "1e10", "osition01", "p", "P", "p2345"]
    pos = np.random.choice(l_pos)
    ph = os.path.join(base, "samples_cellid", f"{pos}", "out_all")
    return ph


@pt.fixture
def rand_make_df():
    """Choise a random table from the folder mustras_cellid"""
    p = np.random.randint(1, 4)
    path = os.path.join(base, "samples_cellid", f"Position0{p}", "out_all")
    df = ld.make_df(path)
    return df


@pt.fixture
def create_mapping_file():
    df = pd.DataFrame(
        {
            "flag": [0, 1, 2, 3],
            "fluor": ["BF_Pos02", "YFP_Pos02", "CFP_Pos02", "RFP_Pos02"],
        }
    ).to_csv(sep="\t", index=False)
    return io.StringIO(df)


@pt.fixture(scope="session")
def create_mapping_file_min():
    df = pd.DataFrame(
        {
            "flag": [0, 1],
            "fluor": ["BF_Pos02", "YFP_Pos02"],
        }
    ).to_csv(sep="\t", index=False)
    return io.StringIO(df)


@pt.fixture
def create_out_all_file():
    rs = np.random.RandomState(np.random.MT19937(np.random.SeedSequence(1234)))
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


@pt.fixture(scope="session")
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


@pt.fixture(scope="session")
def read_mapp_file():
    return pd.read_table(create_mapping_file)


@pt.fixture(scope="session")
def read_out_all_file(create_out_all_file):
    return pd.read_table(create_out_all_file)
