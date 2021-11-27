Prueba de funciones
===================

imagen de prueba

.. code-block:: python
    
    im_name = 'BF_Position03_time06.tif.out.tif'
    path = os.path.join(path_c, im_name)
    #path = '../muestras_cellid'


Posicion estanca para reproducibilidad

.. code-block:: python
    
    x_pos = 182
    y_pos = 465
    ym = 22
    yM = 42
    xm = 21
    xM = 41

Pruebas para buscar centro

.. code-block:: python
    
    c = [(ym, yM),(xm, xM)]
    c[0][0]

Cargo array correspondiente a una imagen

.. code-block:: python
    
    im = box_img(path_c, im_name, x_pos=x_pos, y_pos=y_pos, dx=(3, 30), dy=(0,0))
    #Veo la pinta de la imagen
    plt.imshow(im, cmap="gist_gray")

hasta acá es un crop

.. code-block:: python
    
    i_complet = plt.imread(path, format= 'tif')
    plt.imshow(i_complet[424:444, 20:40], cmap='gist_gray')

Pruebo sumar las matrices numericas para entender si se registran cambios

.. code-block:: python
    
    #im2 = im + im
    #plt.imshow(im2, cmap="gist_gray")

Creo plantillas, matriz de unos (``0`` está recesvado a las separaciones entre ``imgs``)

.. code-block:: python
    
    plantilla_5 = np.ones((480//2, 510//2), dtype=float)
    plantilla_10 = np.ones((480, 510), dtype=float)
    plantilla_20 = np.ones((480*2, 510*2), dtype=float)
    
    s = dimension unidad de img
    s = im.shape
    
    for i in range(0,5):
        # i=representa filas de la imagen final
            for j in range (0,5):
                # j=representa columnas de la imagen final
                # reemplazo cada celda de unos con la imagen individual
                # para la fila i y columna j
                plantilla_5[s[0]*i:s[0]*(i+1), s[1]*j:s[1]*(j+1)] = im
    
    
    plt.imshow(plantilla_5, cmap="gist_gray")
    plantilla_10[0:48, 0:51] = im #i = 0
    plantilla_10[48:96, 51:102] = im #i = 1
    
    my_list = [im for _ in range(12)]
    my_array = np.array(my_list)
    
    r=np.stack(my_array, axis=1)
    blok = np.block(my_list)
    blok2 = np.block(my_list)
    blok3 = np.block(my_list)
    blok4 = np.concatenate((blok, blok2, blok3), axis=0)
    plt.imshow(blok4, cmap="gist_gray")
    
    np.reshape(my_array, (612*576), order = 'C')
    
    my_array.shape = (4*51, 3*48)
    plt.imshow(my_array, cmap="gist_gray")



Selección random de imagenes

Filtro :math:`440 < area < 445` (:math:`91` valores).

.. code-block:: python
    
    data = df[(df['a_tot'] > 440) & (df['a_tot'] < 445)]
    select = np.random.choice(data.index, 5,replace = False)
    
    df.iloc[select[4]]['ucid']#,'ucid','t_frame']]


selecciono :math:`10` filas al azar y sin repetición

.. code-block:: python
    
    select = df[['ucid','t_frame','xpos', 'ypos']].sample(10)
    
    select['name'] = select.apply(
        lambda row : get_img_name(row['ucid'], row['t_frame'], 'bf'),
        axis=1
        )
        
    select['box_img'] =select.apply(
        lambda row : box_img(path, row['name'], row['xpos'], row['ypos']),
        axis = 1
        )
    
    get_img_name(select['ucid'].iloc[5], select['t_frame'].iloc[5], 'bf')
    
    get_img_name(100000000404, 1, 'bf')
    
    array_img(df, path_c)

    
imagen de prueba

.. code-block:: python
    
    im_name = 'BF_Position02_time07.tif.out.tif'
    path = os.path.join(path_c, im_name)
    path = '../muestras_cellid/BF_Position02_time07.tif.out.tif'

Pocision estanca para reproducibilidad

.. code-block:: python
    
    x_pos = 1376
    y_pos = 135

Cargo array correspondiente a una imagen

.. code-block:: python
    
    im = box_img(path_c, im_name, x_pos, y_pos, [(0, 0),(0, 3)])

Veo la pinta de la imagen

.. code-block:: python
    
    plt.imshow(im, cmap="gist_gray")
    im = plt.imread(path)
    plt.imshow(im, cmap="gist_gray")
    plt.axes('off')
    plt.show()
    
    centro = np.zeros((3,3))
    
    im[9:12, 9:12] = centro