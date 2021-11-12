# -*- coding: utf-8 -*-

import pandas as pd

from pycellid import pycellid_io as ld

import pytest


path = "../muestras_cellid/Position01/out_all"

ld._read_df(path).columns


@pytest.fixture
def df_wout_p():
    return pd.read_table("../muestras_cellid/Position01/out_all")


def test_read_df_c_names(path):
    assert ld._read_df(path).columns

