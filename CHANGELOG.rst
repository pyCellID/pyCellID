PyCell Changelog
=========================

Primera semana
--------------------

introduction:
~~~~~~~~~~~~~~~~~~~~

The following changes are compatible with the initial version of the repository,
they are changes to the characteristic structure of the project, however minimal
they may be. (Bug fixes or new versions will also be recorded for learning purposes).

- Only a summary of these will be made for the final version of the project.


Introducción:
~~~~~~~~~~~~~~~~~

Los siguientes cambios son compatibles con versión inicial del repositorio,
son los cambios de la estructura característica del proyectp, por más mínima
que puedan resultar (las correcciones de errores o las nuevas versiones también
serán registradas a modo de aprendizaje).

- Para la versión final del proyecto solo se hará un resumen de éstas.


Clonar el repositorio del proyecto
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Luago de hacer un fork del proyector original

.. code-block:: none

    (venv) $>git clone https://github.com/juniors90/pycell.git




.. code-block:: none

    (venv) $>git remote -v
    origin  https://github.com/juniors90/pycell.git (fetch)
    origin  https://github.com/juniors90/pycell.git (push)
    
    (venv) $>git remote -h
    usage: git remote [-v | --verbose]
       ...
       or: git remote rename <old> <new>
       ...

    (venv) $>git remote rename origin fork
    
    (venv) $>git remote -v
    fork    https://github.com/juniors90/pycell.git (fetch)
    fork    https://github.com/juniors90/pycell.git (push)
    
    (venv) $>git remote add origin https://github.com/darksideoftheshmoo/pycell.git
    
    (venv) $>git remote -v
    fork    https://github.com/juniors90/pycell.git (fetch)
    fork    https://github.com/juniors90/pycell.git (push)
    origin  https://github.com/darksideoftheshmoo/pycell.git (fetch)
    origin  https://github.com/darksideoftheshmoo/pycell.git (push)
    
    (venv) $> git checkout -b juniors90
    Switched to a new branch 'juniors90'
    
    (venv) $> git add -A
    
    (venv) $> git commit -m "a message"
    
    (venv) $> git push fork juniors90


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

Contruir la documentación Docs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    (venv) $> pip freeze > requirements.txt
    (venv) $> pip install sphinx sphinx-rtd-theme
    (venv) $> mkdir docs
    (venv) $> cd docs
    (venv) $> sphinx-quickstart
    (venv) $\docs>sphinx-quickstart
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
    
    Creando archivo $\docs\source\conf.py.
    Creando archivo $\docs\source\index.rst.
    Creando archivo $\docs\Makefile.
    Creando archivo $\docs\make.bat.
    
    Terminado: se ha creado una estructura de directorio inicial.
    
    Ahora debe completar su archivo maestro D:\paht\to\the\pycell\docs\source\index.rst
    y crear otros archivos fuente de documentación. Use el archivo Makefile para compilar
    los documentos, así ejecute el comando:
        make builder
    donde "builder" es uno de los constructores compatibles, por ejemplo, html, latex o linkcheck.

incluir esto en ``docs\source\conf.py``:

.. code-block:: python
    
    import sphinx_rtd_theme

    extensions = [
        sphinx_rtd_theme,
    ]

Change ``'alabaste'`` by ``'sphinx_rtd_theme'`` in the ``html_theme`` value.

.. code-block:: python

    # html_theme = 'alabaster'
    html_theme = 'sphinx_rtd_theme'

- Path setup


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

    (venv) $> sphinx-apidoc -f -o source/modules ../pycellid/


Construir el repositorio de la organización
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Los comandos que ofrece GitHub al crear el repositorio.

.. code-block:: none
    
    echo "# pyCellID" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin https://github.com/pyCellID/pyCellID.git
    git push -u origin main




.. code-block:: python

    # Tables Proccesing
    def create_df(file):
        """Delete the delimitations by space of headers.
        
        :param file: path to the plain text given by *out_all* file (table formater).
        :return: A dataframe.
        """
        try:
            df = pd.read_table(file)
            # Elimino los espacios en los nombres de las columnas ' x.pos '.
            df.columns = df.columns.str.strip()
            # Cambio (. por _) las separaciones x.pos por x_pos
            df.columns = df.columns.str.replace('.', '_')
            return df
        except FileNotFoundError:
            return f'No such file or directory: {file}'


.. code-block:: python

    def get_ucid(df, pos):
    """Crea una columna en el dataframe ``(df)`` con número de tracking
    ``df[ucid].loc[0] = 100000000000`` para ``cellID = 0``, ``Position = 1``.

    :param ucid: ``int(numberPosition + cellID)``.

    :param df: dataframe creado por ``cellID`` contiene la serie ``df['cellID']``.
    """
    df['ucid'] = [pos * 100000000000 + cellID for cellID in df['cellID']]
    return df

.. code-block:: python

    def create_ucid_column(df, position):
        """Crea una columna en el dataframe ``(df)`` con número de tracking
        ``df[ucid].loc[0] = 100000000000`` para ``cellID = 0``, ``Position = 1``.
        
        :param ucid: ``int(numberPosition + cellID)``.
        :param df: dataframe creado por ``cellID`` contiene la serie ``df['cellID']``.
        """
        df['ucid'] = [position * 100000000000 + cellID for cellID in df['cellID']]
        return df


.. code-block:: python

    def get_col_chan(df, df_map):
        """Modifica la entrada df proviniente del pipeline ``pyCell``. 
        Separa las series (columnas) morfológicas por canal de fluorecsencia.
        Elimina los valores redundandes de ``cellID`` y la serie ``'flag'``.
        :param df: Tabla ``cellID`` contiendo ``df['ucid']``.
        :param df_map: Tabla mapping ``cellID`` (``out_bf_fl_mapping``).
        :return: Crea series morfologicas por canal ``df['f_tot_yfp',...,'f_nuc_bfp',...]``.
        """
        #Mensaje
        print('Agragando columnas chanles ...')
        #Variables de fluorescencia
        fluor  = [f_var for f_var in df.columns if f_var.startswith('f_')]
        #Creo un df con columnas variable_fluor por ucid y t_frame
        #idx = ['ucid', 't_frame'] if 't_frame' in df else idx = ['ucid']
        df_flag = df.pivot(index = ['ucid', 't_frame'] ,columns = 'flag', values= fluor)
        #Renombro columnas 
        #Obtengo todos los flag:chanel en mapping
        chanels = {flag:get_chanel(df_map, flag) for flag in df_map['flag'].unique()}
        #Col_name
        df_flag.columns = [n[0] + '_' + chanels[n[1]] for n in df_flag.columns]
        #Lista de variables morfologicas
        morf = [name for name in df.columns if not name.startswith('f_')]
        
        #Creo un df con las variables morfologicas
        #Elimino las redundancias creadas por cellID, registo un solo flag. 
        df_morf = df[df.flag == 0 ][morf]
        df_morf.set_index(['ucid', 't_frame'], inplace=True)
        #Junto los df_flag y df_morf
        df = pd.merge(df_morf, df_flag, on=['ucid', 't_frame'], how='outer')
        del df['flag']
        #Por congruencia con RCell
        #Indices numéricos. ucid, t_frama pasan a columnas
        df = df.reset_index()
        #Ordeno columnas compatible con marco de datos RCell
        col = ['pos', 't_frame', 'ucid', 'cellID']
        df = pd.concat([df[col],df.drop(col,axis=1)], axis=1)
        return df

la función ``get_col_chan(df, df_map)`` está bien pero hace demasiadas cosas a la vez.
Es sólo mí opinión. Pero si funciona dejemoslo ahí.


.. code-block:: python

    def create_morphological_series_by_channel(df, df_map):
        """Modifica la entrada df proviniente del pipeline ``pyCell``. 
        Separa las series (columnas) morfológicas por canal de fluorecsencia.
        Elimina los valores redundandes de ``cellID`` y la serie ``'flag'``.
        :param df: Tabla ``cellID`` contiendo ``df['ucid']``.
        :param df_map: Tabla mapping ``cellID`` (``out_bf_fl_mapping``).
        :return: Crea serias morfologicas por canal ``df['f_tot_yfp',...,'f_nuc_bfp',...]``.
        """
        #Variables de fluorescencia
        fluor  = [f_var for f_var in df.columns if f_var.startswith('f_')]
        idx = ['ucid', 't_frame']
        #Creo un df con columnas variable_fluor por ucid y t_frame
        #idx = ['ucid', 't_frame'] if 't_frame' in df else idx = ['ucid']
        df_flag = df.pivot(index = idx,
                           columns = 'flag',
                           values= fluor)
        #Renombro columnas 
        #Obtengo todos los flag:chanel en mapping
        chanels = {flag:get_chanel(df_map, flag) for flag in df_map['flag'].unique()}
        #Col_name
        df_flag.columns = [n[0] + '_' + chanels[n[1]] for n in df_flag.columns]
        #Lista de variables morfologicas
        morf = [name for name in df.columns if not name.startswith('f_')]
        
        #Creo un df con las variables morfologicas
        #Elimino las redundancias creadas por cellID, registo un solo flag. 
        df_morf = df[df.flag == 0 ][morf]
        df_morf.set_index(idx, inplace=True)
        #Junto los df_flag y df_morf
        df = pd.merge(df_morf, df_flag, on=idx, how='outer')
        del df['flag']
        #Por congruencia con RCell
        #Indices numéricos. ucid, t_frama pasan a columnas
        df = df.reset_index()
        #Ordeno columnas compatible con marco de datos RCell
        col = ['pos', 't_frame', 'ucid', 'cellID']
        df = pd.concat([df[col], df.drop(col, axis=1)], axis=1)
        return df




Could not add webhook for pyCellID. Make sure you have the correct GitHub permissions.
Your primary email address is not verified. Please verify it here.
The project pyCellID doesn't have a valid webhook set up, commits won't trigger new builds for this project. See the project integrations for more information.