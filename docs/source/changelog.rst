.. .. include:: ..\..\CHANGELOG

PyCell Changelog
=========================

introduction:
-------------

The following changes are compatible with the initial version of the repository, they are changes to the characteristic structure of the project, however minimal they may be. (Bug fixes or new versions will also be recorded for learning purposes).

- Only a summary of these will be made for the final version of the project.

Introducción:
-------------

Los siguientes cambios son compatibles con versión inicial del repositorio, son los cambios de la estructura característica del proyectp, por más minimas que puedan resultar (las correcciones de errores o las nuevas versiones también serán registradas a modo de aprendizaje).

- Para la versión final del proyecto solo se hará un resumen de éstas.

0.0.1
-------

``__init__.py``
~~~~~~~~~~~~~~~~


.. code-block:: python
    
    # @author: jose
    # @author: Juan David Ferreira
    
    # Modulo de importación de tablas PyCell
    import pycell.load_data as ld
    from pycell.load_data import read_cellidtable
    
    class PyCell(object):
        """Base class for PyCell objects."""
        
        def __init__(self, app=None):
            if app is not None:
                self.init_app(app)

Build Docs
--------------

.. code-block:: none

    (venv) $> pip freeze > requirements.txt
    (venv) $> pip install sphinx sphinx-rtd-theme
    (venv) $> mkdir docs
    (venv) $> cd docs
    (venv) $> sphinx-quickstart
    (venv) D:\Documents\posgrado\FaMAF\DiSCSI 2021\pycell\pycell\docs>sphinx-quickstart
    Bienvenido a la utilidad de inicio rápido de Sphinx 4.1.2.
    
    Ingrese los valores para las siguientes configuraciones (solo presione Entrar para
    aceptar un valor predeterminado, si se da uno entre paréntesis).
    
    Ruta raíz seleccionada: .
    
    Tiene dos opciones para colocar el directorio de compilación para la salida de Sphinx.
    
    O usas un directorio "_build" dentro de la ruta raíz, o separas
    directorios "fuente" y "compilación" dentro de la ruta raíz.
    > Separar directorios fuente y compilado (y/n) [n]: y
    
    El nombre del proyecto aparecerá en varios lugares en la documentación construida.
    
    > Nombre de proyecto: PyCellID
    > Autor(es): Ferreira, Juan David
    > Liberación del proyecto []: 0.0.1
    
    Si los documentos deben escribirse en un idioma que no sea inglés,
    puede seleccionar un idioma aquí por su código de idioma. Sphinx entonces
    traducir el texto que genera a ese idioma.
    
    Para obtener una lista de códigos compatibles, vea
    https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
    > Lenguaje del proyecto [en]: 
    
    Creando archivo D:\Documents\posgrado\FaMAF\DiSCSI 2021\pycell\pycell\docs\source\conf.py.
    Creando archivo D:\Documents\posgrado\FaMAF\DiSCSI 2021\pycell\pycell\docs\source\index.rst.
    Creando archivo D:\Documents\posgrado\FaMAF\DiSCSI 2021\pycell\pycell\docs\Makefile.
    Creando archivo D:\Documents\posgrado\FaMAF\DiSCSI 2021\pycell\pycell\docs\make.bat.
    
    Terminado: se ha creado una estructura de directorio inicial.
    
    Ahora debe completar su archivo maestro D:\paht\to\the\pycell\docs\source\index.rst y crear otros archivos fuente de documentación. Use el archivo Makefile para compilar los documentos, así ejecute el comando:
        make builder
    donde "builder" es uno de los constructores compatibles, por ejemplo, html, latex o linkcheck.

include into ``docs\source\conf.py`` the followings code

.. code-block:: python
    
    import sphinx_rtd_theme

    extensions = [
        sphinx_rtd_theme,
    ]

Change ``'alabaste'`` by ``'sphinx_rtd_theme'`` in the ``html_theme`` value.

.. code-block:: python

    # html_theme = 'alabaster'
    html_theme = 'sphinx_rtd_theme'

Path setup
--------------------------------------------------------------

If extensions (or modules to document with autodoc) are in another directory,
add these directories to sys.path here. If the directory is relative to the
documentation root, use os.path.abspath to make it absolute, like shown here.

.. code-block:: python
    
    import os
    import sys
    sys.path.insert(0, os.path.abspath('../../'))

.. code-block:: python
    
    import sphinx_rtd_theme

    extensions = [
        'sphinx_rtd_theme',
        'sphinx.ext.autodoc',
        'sphinx.ext.intersphinx',
        'sphinx.ext.todo',
        'sphinx.ext.mathjax',
        'sphinx.ext.autosummary', # solamente si se la quiere usar
        'sphinx.ext.viewcode',
    ]

.. code-block:: none

    (venv) $> sphinx-apidoc -o source/modules ..

