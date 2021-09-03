#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Created on Sun Nov 15 12:03:09 2020

# @author: jose

"""
Script complemento para cellID.

Requiere librerias python standard `pandas <https://pandas.pydata.org/docs/>`_,
`os <https://docs.python.org/3/library/os.html>`_,
`re <https://docs.python.org/3/library/re.html?highlight=re#module-re>`_
y también `matplotlib <https://matplotlib.org/stable/index.html>`_.

Debe pasarse como parámetro la ruta generada por ``cellID``. 

El programa recorrerá las subcarpetas. Toma de las tablas de salida ``cellID``
(``out_all``, ``out_bf_fl_mapping``) por position. Creará una subcarpeta
``pydata/df`` (opcional).

Salida: único DataFrame con los valores de cada tabla. Agregará las series:

* ``df['ucid']`` identificador de célula por posición. ``int()``. ``Unic Cell ID = ucid``

* ``df['pos']`` identificador de posición de adquisición. ``int()``

* Para los valores de fluorescencia mapeados en ``out_bf_fl_mapping(df_mapp)``
  se crearran tantas series como ``flags`` en ``df_mapp`` multiplicado por
  la cantidad de variables morfológicas ``df['f_tot_x1fp','f_tot_x2fp',..., 'f_tot_xnfp']``
"""

import os
import pandas as pd
import re

# Tables Proccesing
def create_df(file):
    """Delete the delimitations by space of headers.

    :param file: path to the plain text given by *out_all* file (table formater).
    :return: A dataframe.
    """
    try:
        df = pd.read_table(file)
        #Elimino los espacios en los nombres de las columnas ' x.pos '.
        df.columns = df.columns.str.strip()
        #Cambio (. por _) las separaciones x.pos por x_pos
        df.columns = df.columns.str.replace('.', '_')
        return df
    except FileNotFoundError:
        return f'No such file or directory: {file}'


def create_ucid_column(df_table, position):
    """Crea una columna en el dataframe ``(df)`` con número de tracking
    ``df[ucid].loc[0] = 100000000000`` para ``cellID = 0``, ``Position = 1``.

    :param ucid: ``int(numberPosition + cellID)``.

    :param df_table: dataframe creado por ``cellID`` contiene la serie ``df['cellID']``.
    """
    try:
        if position > 0:
            df_table['ucid'] = [position * 100000000000 + cellID for cellID in df_table['cellID']]
            return df_table
        else:
            return f'ingrese una posición válida'
    except:
        f'Input a valid ucid or datafame.'
        

def get_channel(df_mapping, flag):
    """
    :param df_mapping: recibe un DataFrame de mapeo, ``df_mapping``,
                       con series ``['flag']=int()`` y
                       ``['fluor']=str(path_file) ``(ver ``cellID doc``). 
    :return: ``str(chanel)`` correspondiente al ``int(flag)``.
    """
    #La escritura del cellID tiene la siguiente expresión regular
    #De 2 a tres caractes xFP luego  _Position
    chanel = re.compile(r'\w{2,3}_Position')
    # cellID codifica en la columna 'fluor'(ruta_archivo contiene str('chanel'))
    # Filtro el DataFrame  para la coincidencia falg == fluor
    path = df_mapping[df_mapping['flag'] == flag]['fluor'].values[0]
    return chanel.findall(path)[0].split('_')[0].lower()


# def get_serie_channels(df, df_map): funcion eliminada, crea elemento por linea
def make_df(path_file):
    """Crea un dataframe con numero de tracking ``ucid`` y ``position``.

    :param path_file: nombre del archivo de salida ``cellID`` ``out_all``
    :return: un dataframe del archivo pasado conteniendo ``df['ucid']``.
    """
    #Position está codificada en el nombre del path al archivo.
    pos = int(re.findall("\d+", path_file)[0])
    print('leyendo position: ', pos)
    #Leo la tabla de texto plano.
    df = create_df(path_file)
    #Asigno ucid
    df = create_ucid_column(df, pos)
    df['pos'] = [pos for _ in range(len(df))]
    return df


def get_col_chan(df, df_map):
    '''Modifica la entrada df proviniente del pipeline ``pyCell``.
    Separa las series (columnas) morfológicas por canal de fluorecsencia

    :param df: Tabla ``cellID`` contiendo ``df['ucid']``.
    :param df_map: Tabla mapping ``cellID`` (``out_bf_fl_mapping``).
    :return: A dataframe.
             Crea serias morfologicas por canal ``df['f_tot_yfp',...,'f_nuc_bfp',...]``
             Elimina los valores redundandes de ``cellID`` y la serie ``'flag'``.
    '''
    print('Agragando columnas chanles...')
    # Variables de fluorescencia
    fluor  = [f_var for f_var in df.columns if f_var.startswith('f_')]
    # Creo un df con columnas variable_fluor por ucid y t_frame
    # idx = ['ucid', 't_frame'] if 't_frame' in df else idx = ['ucid']
    idx=['ucid', 't_frame']
    df_flag = df.pivot(index =  idx , columns = 'flag', values= fluor)
    # Renombro columnas 
    # Obtengo todos los flag:chanel en mapping
    channels = {flag:get_channel(df_map, flag) for flag in df_map['flag'].unique()}
    # Col_name
    df_flag.columns = [n[0] + '_' + channels[n[1]] for n in df_flag.columns]
    # Lista de variables morfologicas
    morf = [name for name in df.columns if not name.startswith('f_')]
    # Creo un df con las variables morfologicas
    # Elimino las redundancias creadas por cellID, registo un solo flag. 
    df_morf = df[df.flag == 0 ][morf]
    df_morf.set_index(idx, inplace=True)
    # Junto los df_flag y df_morf
    df = pd.merge(df_morf, df_flag, on=idx, how='outer')
    del df['flag']
    # Por congruencia con RCell
    # Indices numéricos. ucid, t_frama pasan a columnas
    df = df.reset_index()
    # Ordeno columnas compatible con marco de datos RCell
    col = ['pos', 't_frame', 'ucid', 'cellID']
    df = pd.concat([df[col],df.drop(col,axis=1)], axis=1)
    return df

def get_outall_files(path):
    '''cambia el working directory.

    :param path: carpeta que contiene las salidas ``cellID``.
    :return: una lista generadora con ``path`` de acceso a
             tablas ``'out'`` de ``cellID``.
    '''
    # Rutas a los archivos out_all, out_bf_fl_mapping de cellID
    for r, d, f in os.walk ( "." ):
        d.sort()
        for name in f:
            if 'out_all' in name:
                p = os.path.join(r, name)
                print(p)
                yield p


def get_mapp_files(path):
    '''cambia el working directory.

    :param path: carpeta que contiene las salidas ``cellID``.
    :return: una lista generadora con path de acceso a tablas
             ``'out'`` de ``cellID``.
    '''
    #Rutas a los archivos out_all, out_bf_fl_mapping de cellID
    for r, d, f in os.walk( "." ):
        d.sort()
        for name in f:
            if 'mapping' in name:
                yield os.path.join(r, name)
                

# Junto el pipeline compact_df
def read_cellidtable(path): #cambio load_df
    '''Falta una descripción.

    :param path: ruta de acceso a las salida ``cellID``.
    :return: Un único ``dataframe`` para las tablas out ``cellID``.
    '''
    #Me posiciono en el directorio a buscar.
    os.chdir(path)
    #creo un DataFrame vacío.
    df = pd.DataFrame()
    #Itero sobre la lista de archivos out.
    for f in get_outall_files(path):
        #Proceso las tablas de a una
        df_i = make_df(f)
        #Creo el DataFrame para mapear canales
        df_i =  get_col_chan(df_i, create_df(get_mapp_files(path).__next__()))
        df = pd.concat([df, df_i], ignore_index=True)
    return df


#Opcional, crear directrio pydata y de guardar tabla
def save_df(df, dir_name = 'pydata'):
    """Crea una carpeda ``/pydata``
    guarda el parámetro ``df`` DataFrame
    
    :param df: A dataframe.
    :param dir_name: A directory. The defauld value is ``pydata``.
    """
    # Mensaje de entrada
    print('\nguardando archivo...')
    # Me fijo si no existe el directorio
    if not os.path.exists(dir_name):
        os.mkdir(dir_name) # si no existe lo creo
    os.chdir(dir_name)
    # Guardo csv.
    csv = 'df.csv'
    df.to_csv(index= False)
    return f'se guardó el archivo {csv} en el diretorio {dir_name}'


# Programa principal y consola
def main(argv):
    try:
        if len(argv) != 2:
            raise SystemExit (f'\nUso adecuado: {sys.argv[0]}'
                                ' ' 'path salida de cellID')
        df = read_cellidtable(argv[1])
        
        guardar = input('¿Decea guardar DataFrame? S/N ')
        if 's' in guardar.lower():
            save_df(df)
        
    except SystemExit as e:
        print(e)
        path = input('\ningrege path de acceso a salida cellID\n')
        
        df = read_cellidtable(path)
        
        guardar = input('¿Decea crear la carpeta pydata y guardar DataFrame? S/N ')
        if 's' in guardar.lower():
            save_df(df)

if __name__ == '__main__':
    import sys
    main(sys.argv)