# -*- coding: utf-8 -*-

#Modulo de importación de tablas PyCell
# import load_data as ld
# from load_data import read_cellidtable
#import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import glob
from bokeh.plotting import figure, output_file, show



#%%

def img_name(ucid, t_frame, chanel):
    """This function have a initial ucid ``ucid_in = 100000000000``
    such that try a positional string given by ``pos = str(ucid //ucid_in).zfill(2)``.
    For example: ``ucid = int(300000000020)`` numero de traking unico.
    - pos: ``'path : /home/../BF_Position03_time06.tif.out.tif'``
    
    :param ucid: The unique traking number
    :param t_frame: tag tiempo de la imagen
    :param chanel: Can be one value given by BF, CFP, RFP or YFP.
    :return: A string given by the image's name.
    """
    #ucid inicial
    ucid_in = 100000000000 
    #Obtengo str() de position 01, 02, 10, 20, 100
    pos = str(ucid //ucid_in).zfill(2)
    
    return f'{chanel.upper()}_Position{pos}_time{str(t_frame+1).zfill(2)}.tif.out.tif'
    
def box_img(path, im_name, x_pos, y_pos, dx=(15, 15), dy=(15, 15)):
    """The function ``box_img`` return a array of the intensity values
    (:math:`\leq 256`, by pixels). The extended matrix in three bottom
    rows and three right columns with ``0`` values as delimitation. Also,
    ``center`` is the displacement of center ``y``, ``x``
    ``[(start, end),(start, end)]``.

    The ``img`` date is a ``np.array`` where encode rows an columns:
    ``codifica[fila, columna]`` ``y = rows``, ``x = columns``
    
    :param path: path to the image.
    :param im_name: The image name.
    :param x: x-coordinate where the image begins
    :param y: y-coordinate where the image begins
    
    :return: A extended array corresponding to a cell.
    """
    path_n = os.path.join(path, im_name)
    
    # Y_min = y_pos - dy[0]
    # Y_max = y_pos + dy[1]
    # X_min = x_pos - dx[0]
    # X_max = x_pos + dx[1]
    
    # load image
    im = plt.imread(path_n, format= 'tif') # [Y_min : Y_max, X_min : X_max]
    
    im = im.copy()
    centro = np.zeros((2,2))
    im[y_pos-1:y_pos+1, x_pos-1:x_pos+1] = centro
    
    # Hago un crop de la imagen tomando como margen 20 pixels
    # im = im[abs(y - 20):(y + 25), abs(x - 10):(x + 40)]
    Y_min = y_pos - dx[0]
    Y_max = y_pos + dx[1]
    X_min = x_pos - dx[0]
    X_max = x_pos + dx[1]
    
    im = im[Y_min : Y_max, X_min : X_max]
        
    # Frame
    alto = np.zeros((im.shape[0], 3))
    largo = np.zeros((3, (im.shape[1] + 3)))
    # Recuadro
    im = np.concatenate([im, alto], 1)
    im = np.concatenate([im, largo], 0)
    
    return im

def array_img(data, path, chanel='BF', n=16, shape=(4,4)):
    """Realiza ``n`` selecciones del dataset ``data``, recorre ``path``
    buscando las imagenes correspondientes a ``chanel`` y crea una
    imagen de ``shape(filas, columnas)``.
    
    :param chanel: str() debe segir en encoding de mapeo de canales
                   ``('BF', 'CFP',...)``
    :param shape: ``(int(filas)``, ``int(columnas))`` como se
                  ordenan las ``imgs``.
    :param cent_cel: cuando se movera ``[(Y_m, Y_M),(X_m, X_M)]`` en
                     los ejes coordenados del valor centro aportado
                     por ``data[['x_pos', 'y_pos']]``.
    :param n: cantidad de cells a representar .
    :return: La imagen de salida corresponde a ``n``.     
    """
    #Selecciono ucid al azar para las n celulas
    #select = np.random.choice(data['ucid'], 91 ,replace = False)
    
    # Calculo las dimensiones de la imagen unitaria en base al area de la
    # célula, suponiéndola esférica (con una proyección circular cuyo area es 
    # df['a_tot'])
    
    radio = int(np.round(np.sqrt(data['a_tot'].max()/np.pi)))
    
    # Leo las dimensiones de una imagen típica
    
    image_name = glob.glob("*.tif.out.tif")[0]
    filename = os.path.join(path, image_name)
    im = plt.imread(filename, format= 'tif') # [Y_min : Y_max, X_min : X_max]
    
    im_size = im.shape
    
    del image_name, filename
    
    # im_size = im.shape
    
    #seleccion de n filas al azar y sin repo
    data_copy = data.copy()
    data_copy = data_copy[(data_copy['ypos'] > 2*radio) & 
                          (data_copy['ypos'] < im_size[0] - (2*radio+3)) & 
                          (data_copy['xpos'] > 2*radio) & 
                          (data_copy['xpos'] < im_size[1] - (2*radio+3))]
    
    select = data_copy[['ucid','t_frame','xpos', 'ypos']].sample(n)
    #Registra el nombre de cada imagen en la serie 'name'
    select['name'] = select.apply(
        lambda row : img_name(row['ucid'], row['t_frame'], chanel),\
        axis=1
        )
    
    #Registra un array para cada imagen en la serie 'box_img'
      #Cada imagen tiene dimenciones de 48*53 valores
    Y_m = 2*radio#cent_cel[0][0]
    Y_M = 2*radio#cent_cel[0][1]
    X_m = 2*radio#cent_cel[1][0]
    X_M = 2*radio#cent_cel[0][1]
    
    select['box_img'] =select.apply(
        lambda row : box_img(path, row['name'], row['xpos'], row['ypos'],\
        (Y_m, Y_M),(X_m, X_M)), axis = 1
        )
    
        
    s = (4*radio+3, 4*radio+3) #Shape of unitary image    
    
    #iarray np.ones, con dimencion para contenr todas las imgs
    iarray = np.ones((s[0]*shape[0], s[1]*shape[1]), dtype=float)
     
    #Para las filas i y columnas j de iarray
     #se remplazan las img de c/celula seleccionada
        
    
    iloc = 0 #img index
    for i in range(0,shape[0]):
        for j in range (0,shape[1]):
            try:
                iarray[s[0]*i:s[0]*(i+1), s[1]*j:s[1]*(j+1)] = select['box_img'].iloc[iloc]
                print(select.iloc[iloc], select['box_img'].iloc[iloc].shape)
            except:
                print(select.iloc[iloc], select['box_img'].iloc[iloc].shape)
                pass
            iloc +=1
    
    plt.imshow(iarray, cmap="gist_gray")
    return iarray


def array_img_alt(data, path, chanel='BF', n=16, shape=(4,4), 
                  extra_parameters = []):
    """Realiza ``n`` selecciones del dataset ``data``, recorre ``path``
    buscando las imagenes correspondientes a ``chanel`` y crea una
    imagen de ``shape(filas, columnas)``. Muestra metadatos de cada una de las 
    imagenes representadas.
    
    :param chanel: str() debe segir en encoding de mapeo de canales
                   ``('BF', 'CFP',...)``
    :param shape: ``(int(filas)``, ``int(columnas))`` como se
                  ordenan las ``imgs``.
    :param cent_cel: cuando se movera ``[(Y_m, Y_M),(X_m, X_M)]`` en
                     los ejes coordenados del valor centro aportado
                     por ``data[['x_pos', 'y_pos']]``.
    :param n: cantidad de cells a representar .
    extra_parameters: debe ser una lista con parametros a mostrar de las 
    células. Por defecto se informan 'name', 'ucid', 't_frame', 'xpos' y 'ypos' 
    :return: La imagen de salida corresponde a ``n``.     
    """
    #Selecciono ucid al azar para las n celulas
    #select = np.random.choice(data['ucid'], 91 ,replace = False)
    
    
    
    # output_file("pycellId.html")
    
    # Calculo las dimensiones de la imagen unitaria en base al area de la
    # célula, suponiéndola esférica (con una proyección circular cuyo area es 
    # df['a_tot'])
    
    radio = int(np.round(np.sqrt(data['a_tot'].max()/np.pi)))
    
    # Leo las dimensiones de una imagen típica
    
    image_name = glob.glob("*.tif.out.tif")[0]
    filename = os.path.join(path, image_name)
    im = plt.imread(filename, format= 'tif') # [Y_min : Y_max, X_min : X_max]
    
    im_size = im.shape
    
    del image_name, filename
    
    # Seleccion de n filas al azar y sin repo
    # Descarto aquellas celulas que se encuentran cerca del borde de la imagen
    
    data_copy = data.copy()
    data_copy = data_copy[(data_copy['ypos'] > 2*radio) & 
                          (data_copy['ypos'] < im_size[0] - (2*radio+3)) & 
                          (data_copy['xpos'] > 2*radio) & 
                          (data_copy['xpos'] < im_size[1] - (2*radio+3))]
    
    parameters = ['ucid','t_frame','xpos', 'ypos'] + extra_parameters
    
    select = data_copy[parameters].sample(n)
    #Registra el nombre de cada imagen en la serie 'name'
    select['name'] = select.apply(
        lambda row : img_name(int(row['ucid']), int(row['t_frame']), chanel),\
        axis=1
        )
    
    # Defino las dimensiones de las imagenes unitarias en función del radio
    # estimado de la célula de mayor area.
    Y_m = 2*radio
    Y_M = 2*radio
    X_m = 2*radio
    X_M = 2*radio
    
    select['box_img'] =select.apply(
        lambda row : box_img(path, row['name'], row['xpos'], row['ypos'],\
        (Y_m, Y_M),(X_m, X_M)), axis = 1
        )
    
    s = (4*radio+3, 4*radio+3) #Shape of unitary image    
    
    # Ancho de las imagenes
    dw = [s[0]] * n
     
    # construyo listas con las coordenadas de los puntos inferior izquierdo de 
    # cada imagen unitaria
    x = [s[0] * i for i in range(shape[0]) for j in range(shape[1])]
    y = [s[1] * j for i in range(shape[0]) for j in range(shape[1])]
    
    # A partir del dataframe select construyo un diccionario que sirve como 
    # entrada para el método image del paquete bokeh
    
    select_dict = select.to_dict(orient="list")
    select_dict['x'] = x
    select_dict['y'] = y
    select_dict['dh'] = dw.copy()
    select_dict['dw'] = dw
    
    # Defino los parámetros que se mostraran en el tooltip sobre cada imagen
    
    tooltips = [
    ("name", "@name"),
    ("ucid", "@ucid"),
    ("(x,y)", "(@xpos, @ypos)"),
    ("t frame", "@t_frame"),]
    
    extra_tootlips = [(str(param), "@"+str(param)) for param in extra_parameters]
    
    tooltips = tooltips + extra_tootlips
    
    p = figure(x_range=(0, shape[0]*s[0]), y_range=(0, shape[1]*s[1]), 
               tools='hover,wheel_zoom', tooltips=tooltips)
    p.image(source=select_dict, image='box_img', x='x', y='y', dw='dw', 
            dh='dh', palette="Greys256")
    
    show(p)
    
    
if __name__ == '__main__':
    df = pd.read_csv('.//pydata//df.csv')
    # array_img(df, "D://Documents//Universidad//Cursos//Curso FAMAF Diseño de software para cómputo científico//proyecto//pyCellID//muestras_cellid")
    
    array_img_alt(df, "D://Documents//Universidad//Cursos//Curso FAMAF Diseño de software para cómputo científico//proyecto//pyCellID//muestras_cellid",
                   extra_parameters = ['a_tot','perim', 'maj_axis', 'min_axis'])
