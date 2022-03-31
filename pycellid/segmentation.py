# %%

# !/usr/bin/env python

# -*- coding: utf-8 -*-


# This file is part of the
#   PyCellID Project (
#     https://github.com/pyCellID,
#     https://github.com/darksideoftheshmoo
# ).
# Copyright (c) 2021. Clemente, Jose
# License: MIT
#   Full Text: https://github.com/pyCellID/pyCellID/blob/main/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""
Image segemntatos for PyCellID.

This module provides a suite tools for image segmentation, mask builder for 
cells identifier and measure different features.
"""

# =============================================================================
# IMPORTS
# =============================================================================

import io
import os
from pathlib import Path
import re
import subprocess

from pycellid.io import CHANNEL_REX, POS, SC_NOTATION
import pycellid.io as ld

# %%
# =============================================================================
# GLOBAL PARAMETER
# =============================================================================

# : Tracking/positional file number. Accepts scientific notation.
POSITION_REX = re.compile(fr"({POS})({SC_NOTATION}|\d+)")
# Agrego un grupo más al pos(n) => (pos)(n) ver de cambiar en io.py e importar

# %%
# #############################################################################
# Functions
# #############################################################################


def _make_folder(path, name):
    """Meke folder
    """
    return os.mkdir(os.path.join(path, name))


def _crate_param(param, l):
    """To create .txt with the params
    """
    param = io.StringIO(l) 
    return param


def run_cellid(bf_params, fl_params, output_params, segement_params, mask=True,
 capture_output=True, text=True, *args):
    """Run CellID
    """

    if "shell" in args:
        raise SystemExit("Do not use shell command")
    if mask:
       process = subprocess.run(
            [
                "cell",
                "-b", bf_params,
                "-f", fl_params,
                "-o", output_params,
                "-p", segement_params,
                "-t"
            ],
            capture_output=capture_output,
            text=text,
            *args)
    else:
        process = subprocess.run(
            [
                "cell",
                "-b", bf_params,
                "-f", fl_params,
                "-o", output_params,
                "-p", segement_params,
            ],
            capture_output=capture_output,
            text=text,
            *args)

    return process

def CellID(path, *args):
    """Complete the pipeline
    """
    #Here complete the loop to create the folders.
    
    log = run_cellid(*args)
    return log.stdout

# %%
# #############################################################################
# Pruebas de funciones
# #############################################################################

# Parámetros golbales
b = "/home/jc/Escritorio/cellid_console_test/bf_path_completo_yo.txt"
f = "/home/jc/Escritorio/cellid_console_test/fl_path_completo_yo.txt"
o = "/home/jc/Escritorio/cellid_console_test/samples_cellid/min_samples/out"
p = "/home/jc/Escritorio/cellid_console_test/parameters_yo.txt"

# %%
p = run_cellid(
    bf_params= b,
    fl_params= f,
    output_params= o,
    segement_params= p,
)

# %%
# #############################################################################
# Pruebas cortas
# #############################################################################

p1= subprocess.run([
    "cell",
    "-b", "/home/jc/Escritorio/cellid_console_test/bf_path_completo_yo.txt",
    "-f", "/home/jc/Escritorio/cellid_console_test/fl_path_completo_yo.txt",
    "-o", "/home/jc/Escritorio/cellid_console_test/samples_cellid/min_samples/out",
    "-p", "/home/jc/Escritorio/cellid_console_test/parameters_yo.txt", "-t"
    ], capture_output=True
)
# %%

path = "/home/jc/Escritorio/cellid_console_test/samples_cellid/min_samples"

# Position encoding.
# If the position > 1e20 it may fail
# ('position', 'number')
position = set([POSITION_REX.findall(pos)[0] for pos in os.listdir(path)])
# Crea las carpetas para guardar archivos.
for pos_num in position:
    fold_pos = os.path.join(path, "".join(pos_num))
    os.mkdir(fold_pos)
    p = run_cellid(
        bf_params= b,
        fl_params= f,
        output_params= o,
        segement_params= p,
    )

# %%

CHANNEL_REX.findall(path)[0][0].lower()

# %%
# Necesito escribir un archivo con los parámetros. Voy a usar param = io.StringIO(l)

#param = io.StringIO(l)
positions = set([POSITION_REX.findall(pos)[0] for pos in os.listdir(path)])
channels = set([CHANNEL_REX.findall(str(f))[0][0] for f in Path(path).rglob("*.tif")])

# %%
#with open("bf_path", "w") as bf:
# Creo los parámetros para que se corran en cada archivo.
# Necesito que bf_param tenga repetida la ruta a de bf_pos_n_time para cada chanel

bf_params = io.StringIO()
fl_params = io.StringIO()

for pos in positions:
    for i, ch in enumerate(channels):
        if ch.lower() == "bf":
            pass
        else:
            bf_params.write("some text")
            fl_params.write("some text")

# %%
bf_params.close()
fl_params.close()

# %%
