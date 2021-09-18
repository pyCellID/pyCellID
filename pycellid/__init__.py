#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Created on Thursday Aug 26 10:24:27 2021

# @author: Jose Antonio Clemente
# @author: Juan David Ferreira


#Modulo de importación de tablas PyCell
import pycellid.pycellid_io as ld
from pycellid_io import read_cellidtable

class PyCell(object):
    """Base class for PyCell objects."""
    
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
