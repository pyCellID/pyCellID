# -*- coding: utf-8 -*-

#Modulo de importación de tablas PyCell
#import io.load_data as ld
#from io.load_data import read_cellidtable
#import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os


#%%

def get_img_name(ucid, t_frame, chanel):
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

def array_img(data, path, chanel='BF', n=25, shape=(5,5),\
              cent_cel=[(20, 20),(20, 20)]):
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
        
    #seleccion de n filas al azar y sin repo
    select = data[['ucid','t_frame','xpos', 'ypos']].sample(n)
    #Registra el nombre de cada imagen en la serie 'name'
    select['name'] = select.apply(
        lambda row : get_img_name(row['ucid'], row['t_frame'], chanel),\
        axis=1
        )
    
    #Registra un array para cada imagen en la serie 'box_img'
      #Cada imagen tiene dimenciones de 48*53 valores
    Y_m = cent_cel[0][0]
    Y_M = cent_cel[0][1]
    X_m = cent_cel[1][0]
    X_M = cent_cel[0][1]
    
    #box_img(path, im_name, x_pos, y_pos, dx=(15, 15), dy=(15, 15))
    select['box_img'] =select.apply(
        lambda row : box_img(path, row['name'], row['xpos'], row['ypos'],\
        dx=(Y_m, Y_M),dy=(X_m, X_M)), axis = 1
        )
    
    #iarray np.ones, con dimencion para contener todas las imgs
    iarray = np.ones((48*shape[0], 53*shape[1]), dtype=float)
     
    #Para las filas i y columnas j de iarray
     #se remplazan las img de c/celula seleccionada
        
    s = (48, 53) #Shape of unitary image
    iloc = 0 #img index
    for i in range(0,shape[0]):
        for j in range (0,shape[1]):
            try:
                iarray[s[0]*i:s[0]*(i+1), s[1]*j:s[1]*(j+1)] =\
                    select['box_img'].iloc[iloc]
            except:
                print(select.iloc[iloc], select['box_img'].iloc[iloc].shape)
                pass
            iloc +=1
    
    plt.imshow(iarray, cmap="gist_gray")
    return iarray
