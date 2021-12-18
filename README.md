![logo](https://raw.githubusercontent.com/pyCellID/pyCellID/clementejose/docs/logo/PycellID_logo.jpg)

# PyCellID

[![Build status](https://github.com/pyCellID/pyCellID/actions/workflows/CI.yml/badge.svg)](https://github.com/pyCellID/pyCellID/actions)
[![codecov](https://codecov.io/gh/pyCellID/pyCellID/branch/main/graph/badge.svg?token=SXFRA6KCLV)](https://codecov.io/gh/pyCellID/pyCellID)
[![Documentation Status](https://readthedocs.org/projects/pycellid/badge/?version=latest)](https://pycellid.readthedocs.io/en/latest/?badge=latest)
[![issues](https://img.shields.io/github/issues/pyCellID/pyCellID)](https://img.shields.io/github/issues/pyCellID/pyCellID)
[![license](https://img.shields.io/github/license/pyCellID/pyCellID)](https://github.com/pyCellID/pyCellID/blob/main/LICENSE)
[![forks](https://img.shields.io/github/forks/pyCellID/pyCellID)](https://github.com/pyCellID/pyCellID/)
[![stars](https://img.shields.io/github/stars/pyCellID/pyCellID)](https://github.com/pyCellID/pyCellID/)

Functions to analyze Cell-ID single-cell cytometry data using python language.

## Motivation

Microscopy-based cytometry provides a powerful means to study cells with high throughput. Single cell measurements can reveal information hidden in the population. Some commercial software packages, as well as some open source projects, provide tools for working with microscopy images. However, either they do not fit the problem posed by cell-to-cell analysis, or they do not deliver a complete pipeline. 

Here, we present a set of tools that facilitate inspection and analysis of fluorescence microscopy images based on their segmentation data. 

We hope to integrate tools for image segmentation in future releases. In that way we would be able to contribute to completing the routine from data sampling to already analyzed samples.

## Requirements

Python 3.8+

## Dependecies for this project.

- [attrs(>=21.1.0)](https://www.attrs.org/en/stable/) for building the backend.
- [matplotlib(>=3.4.0)](https://matplotlib.org/) for plots management
- [pandas(>=1.3.0)](https://pandas.pydata.org/) for panel and dashboard management.
- [numpy(>=1.21.0)](https://numpy.org/) for numerical management.

## Installation


PyCellID can be installed using ``pip`` from [PyPI](http://pypi.python.org/pypi/pycellid). Using [virtualenv](http://www.virtualenv.org/en/latest/) is recommended -- for no specific reason other than it being good practice. Installing is simple:

```cmd
    $> pip install pycellid
```
   

For development, clone the [official github repository](https://github.com/pyCellID/pyCellID) instead and use:

```cmd
    $> python setup.py .
```

## Contact

You can contact us via [email](clemente.jac@gmail.com).

## Issues

Please submit bug reports, suggestions for improvements and patches via
the [issue tracker](https://github.com/pyCellID/pyCellID/issues).

## Links

- [Documentation](https://pycellid.readthedocs.io)
- [Example Application](https://github.com/pyCellID/pyCellID/blob/main/docs/source/notes/examples.ipynb)
- [PyPI Releases](https://pypi.org/project/PyCellID/)
- [Changelog](https://github.com/pyCellID/pyCellID/blob/main/CHANGELOG.rst)


## Credits

We propose using the open source software Cell-ID for the image segmentation task. We plan to integrate it into our code in the future.

The cellID developers ([1](https://www.nature.com/articles/nmeth1008))([2](http://dx.doi.org/10.1002/0471142727.mb1418s100)).

Original source can be found at sourceforge ([link](https://sourceforge.net/projects/cell-id/)) and in the original publication ([link](https://www.nature.com/articles/nmeth1008#supplementary-information)).

You can also visit the official repository [ACL's Yeast Systems Biology Lab](https://github.com/darksideoftheshmoo/cellID-linux) 
for further details.

We have got inspiration from [rcell and rcell2](https://github.com/darksideoftheshmoo/rcell2).


## License

This project is licensed under the MIT License (see the
[LICENSE](https://github.com/pyCellID/pyCellID/blob/main/LICENSE) file for details).
