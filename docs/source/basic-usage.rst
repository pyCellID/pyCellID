Get Started
===========

The package `PyCellID <https://semantic-ui.com/>`_ está diseñado para navegar un path y rastrear tablas con
data y metadata(mapping) para retornar un único objeto Dataframe.::

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
`os <https://docs.python.org/3/library/os.html>`_,
`re <https://docs.python.org/3/library/re.html?highlight=re#module-re>`_
`pandas <https://pandas.pydata.org/docs/>`_,
`matplotlib <https://matplotlib.org/stable/index.html>`_.

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



To get started, the first step is to import and load the extension

.. code-block:: python
    
    from pycell import PyCellID

    # do something with app...

After loading, new templates are available to derive from in your application.

Installation
------------

PyCellID can be installed using ``pip`` from `PyPI
<http://pypi.python.org/pypi/PyCellID>`_. Using `virtualenv <http://www.virtualenv.org/en/latest/>`_ is recommended -- for no specific reason other than it being good practice. Installing is simple::

   pip install pycell

For development, clone the `official github repository <https://github.com/darksideoftheshmoo/pycell>`_ instead and use::

   python setup.py develop

Getting started
---------------

To get started, go ahead by reading :doc:`basic-usage`.

Sample Application
------------------

If you want to have a look at a small sample application, try `browsing it on
github <https://github.com/darksideoftheshmoo/sample_app>`_.


Examples
~~~~~~~~



Resources
----------------
