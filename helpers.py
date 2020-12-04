# -*- coding: UTF-8 -*-

# From github.com/villares/villares/file_helpers.py

# 2020-09-25 Added comment with date and URL!
# 2020-11-28 Added sketch_name()
# 2020-12-02 Renamed file_helpers -> helpers, brought in grid() and color.py in
# 2020-12-04 Brought in triangle_area, rect_points, rotate_point, point_in_screen

def adicionar_imagens(selection, imagens=None):
    if imagens is None:
	    imagens = []

    if selection == None:
        print("Seleção cancelada.")
    else:
        dir_path = selection.getAbsolutePath()
        print("Pasta selecionada: " + dir_path)
        for file_name, file_path in lista_imagens(dir_path):
            img = loadImage(file_path)
            img_name = file_name.split('.')[0]
            print("imagem " + img_name + " carregada.")
            imagens.append((img_name, img))
        print('Número de imagens: ' + str(len(imagens)))
    return imagens

def lista_imagens(dir=None):
    """
    Devolve uma a lista de tuplas com os nomes dos arquivos de imagem e os caminhos
    completos para cada uma das images na pasta `dir` ou na pasta /data/ do sketch.
    Requer a função imgext() para decidir quais extensões aceitar.
    """
    from os import listdir
    from os.path import isfile, join
    data_path = dir or sketchPath('data')
    try:
        f_list = [(f, join(data_path, f)) for f in listdir(data_path)
                  if isfile(join(data_path, f)) and imgext(f)]
    except Exception as e:
        print("Erro ({0}): {1}".format(e.errno, e.strerror))
        return []
    return f_list

def imgext(file_name):
    ext = file_name.split('.')[-1]
    # extensões dos formatos de imagem que o Processing aceita!
    valid_ext = ('jpg',
                 'png',
                 'jpeg',
                 'gif',
                 'tif',
                 'tga',
                 )
    return ext.lower() in valid_ext

def sketch_name():
    """Return sketch name."""
    from os import path
    sketch = sketchPath()
    return path.basename(sketch)


def random_hue_saturated(bright=None):
    bright = 255 if bright is None else bright
    with pushStyle():
        colorMode(HSB)
        return color(random(256), 255, bright)
        
def grid(cols, rows, colSize=1, rowSize=1):
    """
    Returns an iterator that provides coordinate tuples. Example:
    # for x, y in grid(10, 10, 12, 12):
    #     rect(x, y, 10, 10)
    """
    rowRange = range(int(rows))
    colRange = range(int(cols))
    for y in rowRange:
        for x in colRange:
            yield (x * colSize, y * rowSize)
            
def memoize(f):
    """Naive memoization."""
    memo = {}
    def memoized_func(*args, **kwargs):
        if args not in memo:
            r = f(*args, **kwargs)
            memo[args] = r
            return r
        return memo[args]
    return memoized_func

def triangle_area(a, b, c):
    area = (a[0] * (b[1] - c[1]) +
            b[0] * (c[1] - a[1]) +
            c[0] * (a[1] - b[1]))
    return area

def rect_points(ox, oy, w, h, mode=CORNER, angle=None):
    if mode == CENTER:
        x, y = ox - w / 2.0, oy - h / 2.0
    else:
        x, y = ox, oy
    points = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    if angle is None:
        return points
    else:
        return [rotate_point((x, y), angle, (ox, oy))
                for x, y in points]

def rotate_point(*args):
    if len(args) == 2:
        (xp, yp), angle = args
        x0, y0 = 0, 0
    if len(args) == 3:
        try:
            (xp, yp), angle, (x0, y0) = args
        except TypeError:
            xp, yp, angle = args
            x0, y0 = 0, 0
    if len(args) == 5:
        xp, yp, angle, x0, y0 = args
    x, y = xp - x0, yp - y0  # translate to origin
    xr = x * cos(angle) - y * sin(angle)
    yr = y * cos(angle) + x * sin(angle)
    return (xr + x0, yr + y0)

def point_in_screen(*args):
    if len(args) == 1:
        x, y = args[0][0], args[0][1]
    else:
        x, y = args[0], args[1]
    return 0 <= screenX(x, y) <= width and 0 <= screenY(x, y) <= height
    
