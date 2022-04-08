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
from regex import cache_all

# %%
# =============================================================================
# GLOBAL PARAMETER
# =============================================================================

# : Tracking/positional file number. Accepts scientific notation.
POSITION_REX = re.compile(fr"({POS})({SC_NOTATION}|\d+)")
# Agrego un grupo más al pos(n) => (pos)(n) ver de cambiar en io.py e importar

# %%
# =============================================================================
# Functions
# =============================================================================

def _make_folder(path, name):
    """Meke folder
    """
    folder = Path(path) / name
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def _crate_param(params, l, buffer = False):
    """To create strams with the params
    """
    if not buffer:
    #    with open(path, 'w') as params:
            params.write(l)
    else:
        params = io.StringIO(l) 
    return params


def run_cellid(bf_params, fl_params, output_params, segement_params, mask=True,
 capture_output=True, text=True, *args):
    """Run CellID
    """

    # if "shell" in args:
        # raise SystemExit("Do not use shell command")
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
    # New

    # for positions in path:
    #     creo una carpeta por posición
    #     creo los archivos de parámetros
    #     Corro Cellid
    #     ¿registro cada salida para hacer un log?
    # Retorno un log

    # End New
    log = run_cellid(*args)
    return log.stdout

# %%
# =============================================================================
# Pruebas de funciones
# =============================================================================
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
# =============================================================================
# Pruebas cortas
# =============================================================================
# Globals
# Path to minimal experiment
path_min = "/home/jc/Escritorio/cellid_console_test/samples_cellid/min_samples"
# Path observable, minimo para poder contar los archivos creados
path = "/home/jc/Escritorio/cellid_console_test/samples_cellid/min_min_samples"

# %%
p1= subprocess.run([
    "cell",
    "-b", "/home/jc/Escritorio/cellid_console_test/bf_path_completo_yo.txt",
    "-f", "/home/jc/Escritorio/cellid_console_test/fl_path_completo_yo.txt",
    "-o", "/home/jc/Escritorio/cellid_console_test/samples_cellid/min_samples/out",
    "-p", "/home/jc/Escritorio/cellid_console_test/parameters_yo.txt",
    "-t"
    ], capture_output=True
)

# Que quede un archivin con los parámetros que se usaron al correr el paquete 
# Gracias Hele y Nico!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11111
# Peeeeeeeerrrroo que sea opcional para quien tenga ganas de usar más memoria.
# %%
p = Path(path).rglob('*.tif')
channels = set([CHANNEL_REX.findall(str(f))[0][0] for f in p])

# files = []
# channels = set()
# positions = set()
# for file in Path(path).glob('*.tif'):
#     channels.add(CHANNEL_REX.findall(str(file))[0][0])
#     positions.add(POSITION_REX.findall(str(file))[0])
#     files.append(file)

# %%
# positions = set([POSITION_REX.findall(pos)[0] for pos in os.listdir(path)])
# La ventaja de pathlib es que estoy mirando solo las extenciones .tif

positions = set([POSITION_REX.findall(str(f))[0] for f in Path(path).glob("*.tif")])

for pos in positions:
    # Construt the output folder
    folder = Path(path) / ''.join(pos)
    folder.mkdir(parents=True, exist_ok=True)
    # Data path
    bf_params = io.StringIO()
    fl_params = io.StringIO()

    for img_path in Path(path).glob("*.tif"):
        # [('Position', '01')] POSITION_REX
        pos_path = POSITION_REX.findall(str(img_path))[0][1]
        fl_channel = CHANNEL_REX.findall(str(img_path))[0][0]

        if pos[1] == pos_path and not "BF" in fl_channel:
            # Built bf_path
            new_path = img_path.name.replace(fl_channel, 'BF',)
            base = os.path.dirname(img_path)
            file_path = os.path.join(base, new_path)
            # Build memory data
            bf_params.writelines([file_path, '\n'])
            fl_params.writelines([str(img_path), '\n'])

#            if save_params:
            # Pathlib open/close
            bf = folder / "bf_params.txt"
            bf.write_text(bf_params.getvalue())

            fl = folder / "fl_params.txt"
            fl.write_text(fl_params.getvalue())

    out = os.path.join(folder, "out")

    p1= subprocess.run([
        "cell",
        "-b", str(bf),
        "-f", str(fl),
        "-o", out,
        "-p", "/home/jc/Escritorio/cellid_console_test/parameters_yo.txt",
        #"-t"
        ], capture_output=True
    )

    bf_params.close()
    fl_params.close()

# p1.returncode == 1 todo corrió sin acusar error. Manejo de errores.
# p1.stdout ver para el retorno del proceso
