# -*- coding: utf-8 -*-
# %%
from pathlib import Path

import pandas as pd

import pycellid.io as ld

import pytest
#%%

path = '../muestras_cellid/Position01/out_all'

ld._read_df(path).columns
#%%
@pytest.fixture
def df_wout_p():
    return pd.read_table('../muestras_cellid/Position01/out_all')


def test_read_df_c_names(path):
    
    assert ld._read_df(path).columns

# %%
pycellid.p_io.merge_id_table('../muestras_cellid')

# %%
df = pycellid.io.merge_id_tables('../muestras_cellid', v=True)

# %%

