import os

from numpy import ndarray

from pycellid.core import CellData

import pytest

import random

import pandas as pd


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base = os.path.dirname(ROOT_DIR)
file_path = os.path.join(base, 'samples_cellid')

def test_cell_data():
    df = CellData(file_path)
    df['pos']
    assert '_df' in vars(df)


def test_celldata__check_path(fake_filepath):
    with pytest.raises(FileNotFoundError):
        df = CellData(fake_filepath)

# def test_celldata__check_input():
#     with pytest.raises(ValueError):
#         n =random.randint(1,100)
#         wrong_types = [int, float, bool]
#         wrong_type = random.choice(wrong_types)
#         wrong_input = wrong_type(n)
#         df = CellData(wrong_input)

def test_to_pandas():
    df = CellData(file_path)
    df_test = df.to_pandas()
    assert isinstance(df_test, pd.DataFrame)

def test_repr():
    df = CellData(file_path)
    df_repr = repr(df)
    repr_result = (
        '       pos  t_frame  cellID  f_local2_bg_rfp  f_local2_bg_tfp  f_local2_bg_yfp\n'
        '0        1        0       0         241.2194         12523.05         310.0760\n'
        '1        1        1       0         240.1235         12138.30         317.3976\n'
        '3        1        3       0         437.9252         11549.44         331.3429\n'
        '23642   22        1       2              NaN              NaN              NaN\n'
        '23643   22        2       2              NaN              NaN              NaN\n'
        '23644   22        3       2              NaN              NaN              NaN\n'
        '\nPyCellID.CellData - 23645 rows x 125 columns'
        )
    assert df_repr == repr_result

def test_repr_html():
    path = os.path.join(file_path,'pydata','test','p33')
    df = CellData(path)
    df_repr = df._repr_html_()
    df_repr = df_repr.split("\n",1)[1]
    repr_result = (
        '<style scoped>\n'
        '    .dataframe tbody tr th:only-of-type {\n'
        '        vertical-align: middle;\n'
        '    }\n\n'
        '    .dataframe tbody tr th {\n'
        '        vertical-align: top;\n'
        '    }\n\n'
        '    .dataframe thead th {\n'
        '        text-align: right;\n'
        '    }\n</style>\n'
        '<table border="1" class="dataframe">\n'
        '  <thead>\n'
        '    <tr style="text-align: right;">\n'
        '      <th></th>\n'
        '      <th>pos</th>\n'
        '      <th>t_frame</th>\n'
        '      <th>ucid</th>\n'
        '      <th>cellID</th>\n'
        '      <th>flag</th>\n'
        '      <th>f_tot_yfp</th>\n'
        '      <th>f_tot_cfp</th>\n'
        '      <th>f_tot_tfp</th>\n'
        '      <th>f_local_bg_yfp</th>\n'
        '      <th>f_local_bg_cfp</th>\n'
        '      <th>f_local_bg_tfp</th>\n'
        '      <th>f_nucl_yfp</th>\n'
        '      <th>f_nucl_cfp</th>\n'
        '      <th>f_nucl_tfp</th>\n'
        '    </tr>\n'
        '  </thead>\n'
        '  <tbody>\n'
        '    <tr>\n'
        '      <th>0</th>\n'
        '      <td>33</td>\n'
        '      <td>0</td>\n'
        '      <td>3300000000001</td>\n'
        '      <td>1</td>\n'
        '      <td>0</td>\n'
        '      <td>0.758827</td>\n'
        '      <td>0.960994</td>\n'
        '      <td>0.591346</td>\n'
        '      <td>20.737175</td>\n'
        '      <td>11.085219</td>\n'
        '      <td>206.121792</td>\n'
        '      <td>8.963806</td>\n'
        '      <td>215.053249</td>\n'
        '      <td>236.667868</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>1</th>\n'
        '      <td>33</td>\n'
        '      <td>1</td>\n'
        '      <td>3300000000001</td>\n'
        '      <td>1</td>\n'
        '      <td>0</td>\n'
        '      <td>0.479292</td>\n'
        '      <td>0.433191</td>\n'
        '      <td>0.437516</td>\n'
        '      <td>155.610060</td>\n'
        '      <td>112.850706</td>\n'
        '      <td>219.102953</td>\n'
        '      <td>58.695248</td>\n'
        '      <td>41.416067</td>\n'
        '      <td>96.080660</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>2</th>\n'
        '      <td>33</td>\n'
        '      <td>2</td>\n'
        '      <td>3300000000001</td>\n'
        '      <td>1</td>\n'
        '      <td>0</td>\n'
        '      <td>0.234152</td>\n'
        '      <td>0.184732</td>\n'
        '      <td>0.565839</td>\n'
        '      <td>47.583935</td>\n'
        '      <td>191.166193</td>\n'
        '      <td>111.228651</td>\n'
        '      <td>180.840876</td>\n'
        '      <td>33.133101</td>\n'
        '      <td>179.600264</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>3</th>\n'
        '      <td>33</td>\n'
        '      <td>3</td>\n'
        '      <td>3300000000001</td>\n'
        '      <td>1</td>\n'
        '      <td>0</td>\n'
        '      <td>0.873194</td>\n'
        '      <td>0.502716</td>\n'
        '      <td>0.990881</td>\n'
        '      <td>194.359682</td>\n'
        '      <td>138.757162</td>\n'
        '      <td>255.124366</td>\n'
        '      <td>84.813714</td>\n'
        '      <td>87.602774</td>\n'
        '      <td>244.533928</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>4</th>\n'
        '      <td>33</td>\n'
        '      <td>0</td>\n'
        '      <td>3300000000002</td>\n'
        '      <td>2</td>\n'
        '      <td>0</td>\n'
        '      <td>0.620329</td>\n'
        '      <td>0.711842</td>\n'
        '      <td>0.070788</td>\n'
        '      <td>148.485845</td>\n'
        '      <td>117.239603</td>\n'
        '      <td>79.894820</td>\n'
        '      <td>54.015287</td>\n'
        '      <td>90.811131</td>\n'
        '      <td>50.020915</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>5</th>\n'
        '      <td>33</td>\n'
        '      <td>1</td>\n'
        '      <td>3300000000002</td>\n'
        '      <td>2</td>\n'
        '      <td>0</td>\n'
        '      <td>0.570126</td>\n'
        '      <td>0.539031</td>\n'
        '      <td>0.562518</td>\n'
        '      <td>100.458392</td>\n'
        '      <td>255.952273</td>\n'
        '      <td>45.961396</td>\n'
        '      <td>230.943431</td>\n'
        '      <td>119.606424</td>\n'
        '      <td>174.165830</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>6</th>\n'
        '      <td>33</td>\n'
        '      <td>2</td>\n'
        '      <td>3300000000002</td>\n'
        '      <td>2</td>\n'
        '      <td>0</td>\n'
        '      <td>0.190640</td>\n'
        '      <td>0.194078</td>\n'
        '      <td>0.047514</td>\n'
        '      <td>154.626810</td>\n'
        '      <td>248.402509</td>\n'
        '      <td>25.159397</td>\n'
        '      <td>228.457480</td>\n'
        '      <td>215.485929</td>\n'
        '      <td>44.179661</td>\n'
        '    </tr>\n'
        '    <tr>\n'
        '      <th>7</th>\n'
        '      <td>33</td>\n'
        '      <td>3</td>\n'
        '      <td>3300000000002</td>\n'
        '      <td>2</td>\n'
        '      <td>0</td>\n'
        '      <td>0.640290</td>\n'
        '      <td>0.518797</td>\n'
        '      <td>0.370817</td>\n'
        '      <td>208.592933</td>\n'
        '      <td>185.558721</td>\n'
        '      <td>130.628655</td>\n'
        '      <td>123.776959</td>\n'
        '      <td>236.150055</td>\n'
        '      <td>134.515515</td>\n'
        '    </tr>\n'
        '  </tbody>\n'
        '</table>\n'
        '</div>PyCellID.core.CellData - 8 rows x 14 columns</div>'
        )
    assert df_repr == repr_result