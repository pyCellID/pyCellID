Get Started
===========

The package `PyCellID <https://semantic-ui.com/>`_ está diseñado para navegar un path y rastrear tablas con
data y metadata(mapping) para retornar un único objeto Dataframe.

.. code-block::

    padre/
        hijo01/
            data.ext
            mapping.ext
        hijo03/
            data.ext
            mapping.ext
        hijo03/
            data.ext
            mapping.ext

Requiere librerias python standard:

Este proyecto comienza como soporte al software Cell-ID
Gordon, Colman‐Lerner et al. 2007
publicación original DOI: 10.1038/nmeth1008
`software <https://sourceforge.net/projects/cell-id/>`_.
Orientado, pero no limitando, a las salidas prodcidas por cell-ID:

- ``input``: la ruta generada por ``cellID``.

En el futuro se integrará el código en C de Cell-ID para dar una
rutina acabada y completa.

El programa recorrerá las subcarpetas. Toma de las tablas de salida ``cellID``
(``out_all``, ``out_bf_fl_mapping``) por position. Creará una subcarpeta
``pydata/df`` (opcional).

Salida: único DataFrame con los valores de cada tabla. Agregará las series:

* ``df['ucid']`` identificador de célula por posición. ``int()``.
    ``Unic Cell ID = ucid``

* ``df['pos']`` identificador de posición de adquisición. ``int()``

* Para los valores de fluorescencia mapeados en ``out_bf_fl_mapping(df_mapp)``
  se crearran tantas series como ``flags`` en ``df_mapp`` multiplicado por la
  cantidad de variables morfológicas
  ``df['f_tot_x1fp','f_tot_x2fp',..., 'f_tot_xnfp']``



Dependecies for this project.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- `attrs <https://www.attrs.org/en/stable/>`_ For build the backend.
- `numpy <https://numpy.org/>`_ for numerical computing management.
- `pandas <https://pandas.pydata.org/docs/>`_ for panel and dashboard management.
- `matplotlib <https://matplotlib.org/stable/index.html>`_ for plots management.



Installation
------------

PyCellID can be installed using ``pip`` from `PyPI
<http://pypi.python.org/pypi/PyCellID>`_. Using `virtualenv <http://www.virtualenv.org/en/latest/>`_ is recommended -- for no specific reason other than it being good practice.
Installing is simple:

.. code-block:: none

    (venv) $> pip install pycellid

For development, clone the `Github Repository <https://github.com/https://github.com/pyCellID/pyCellID>`_ instead and use:

.. code-block:: none

    (venv) $> python setup.py .


Getting started
---------------

To get started, the first step is to import and load the extension

.. code-block:: python
    
    from pycell import PyCellID

    # do something with app...

After loading, new templates are available to derive from in your application.

To get started, go ahead by reading :doc:`basic-usage`.

Sample Application
------------------

If you want to have a look at a small sample application, try `browsing it on
github <https://github.com/darksideoftheshmoo/sample_app>`_.


Resources
----------------
