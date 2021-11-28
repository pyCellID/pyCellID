import os

from pycellid.core import CellData

import pytest

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)
file_path = os.path.join(base, 'samples_cellid')

def test_cell_data():
    df = CellData(file_path)
    df['pos']
    assert '_df' in vars(df)


def test_celldata_filenotfounderror():
    with pytest.raises(FileNotFoundError):
        df = CellData(file_path)
        df = pd.read_csv(file)
        n = 16
        criteria = {"a_tot": [800.0, 700.00]}
        iarray = pycellid.array_img(
            df,
            os.path.join(base, "muestras_cellid"),
            n=n,
            criteria=criteria,
        )
        print(iarray.shape)