import os

from pycellid.core import CellData

#import pytest as pt

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)
file_path = os.path.join(base, 'samples_cellid')

def test_cell_data():
    df = CellData(file_path)
    df.path
    assert '_df' in vars(df)
