# -*- coding: UTF-8 -*-

"""
From https://github.com/villares/villares/blob/main/file_helpers.py

2020-09-25 Added comment with date and URL!
2020-11-28 Added sketch_name()
2020-12-02 Renamed file_helpers -> helpers, brought in grid() and color.py in
2020-12-04 Brought in triangle_area, rect_points, rotate_point, point_in_screen
2021-01_26 Reverted 2020-12-04
2021_03_05 imgext() -> has_img_ext()
2021_06_08 Added lerp_tuple()
2022_06_13 Added save_png_with_src() (for py5 only)
2022_07_14 If on py5 imported mode, save_png_with_src now tries folder+'.py'
2022_07_27 Added datetimestamp() & tweaks to save_png_with_src
2022_08_03 Added get_arduino() based on PyFirmata (for py5 only)
2023_08_15 DONE checked I can't use __file__ inside save_png_with_src
2024-02-01 DONE (re)move things to image_helpers
           TODO fix or delete adicionar_imagens
2024-10-19 Adding save_snapshot_and_code()
"""

try:
    lerp
except NameError:
    from pathlib import Path
    from py5 import lerp
    from py5 import color
    from py5 import color_mode as colorMode
    from py5 import push_style as pushStyle
    from py5 import sketch_path as sketchPath
    
def sketch_name():
    """Return sketch name."""
    from os import path
    sketch = sketchPath()  # will use py5.sketch_path() if in py5
    return path.basename(sketch)

def random_hue_saturated(bright=None):
    bright = 255 if bright is None else bright
    with pushStyle():
        colorMode(HSB)
        return color(random(256), 255, bright)

def hex_color(s):
    """
    This function allows you to create color from a string with hex notation in Python mode.
    
    On "standard" Processing (Java) we can use hexadecimal color notation #AABBCC
    On Python mode one can use this notation between quotes, as a string in fill(),
    stroke() and background(), but, unfortunately, not with color().
    """
    if s.startswith('#'):
        s = s[1:]
    return color(int(s[:2], 16), int(s[2:4], 16), int(s[4:6], 16))

                
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

def lerp_tuple(a, b, t):   
    return tuple(lerp_tuple(ca, cb, t) if isinstance(ca, tuple)
                 else lerp(ca, cb, t)             
                 for ca, cb in zip(a, b))
                                    
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

def datetimestamp(time_prefix='t', time_only=False, date_only=False):
    """
    returns 'YYYY_MM_DDtHH-MM-SS' 
    time_only=True returns 'tHH-MM-SS'
    date_only=True returns 'YYYY_MM_DD' (time_only will override date_only)
    time_prefix keyword argument changes 't' to something else
    """
    from datetime import datetime
    dtnow = str(datetime.now())[:19]
    dts = dtnow.replace('-', '_').replace(' ', time_prefix).replace(':', '-')   
    if time_only:
        return dts[10:]
    elif date_only:
        return dts[:10]
    else:
        return dts

def save_png_with_src(output=None, *args, **kwargs):
    """
    output=None -> folder name used
    datetimestamp=True
    timestamp=False
    """
    import py5
    import PIL.PngImagePlugin
    import glob
    from os.path import basename, join
    import __main__ as m
    src_file = m.__file__
    print(src_file)
    if basename(src_file) == 'run_sketch.py':
        src_path = join(py5.sketch_path(), '*.py')
        src_file = glob.glob(str(src_path))[0]
        #src_file = join(file_path, basename(file_path) + '.py')
    drop_alpha = kwargs.pop('drop_alpha', False)
    kwargs['drop_alpha'] = drop_alpha
    add_ts = kwargs.pop('timestamp', False) 
    add_dts = kwargs.pop('datetimestamp', True) 
    if add_ts:  # timestamp True overrides datetimestamp True
        stamp = datetimestamp(time_prefix='', time_only=True)
    elif add_dts:
        stamp = datetimestamp(time_prefix='v')
    else:
        stamp = None
        
    if output is None and stamp is None:
        output = basename(py5.sketch_path()) + '.png'
    elif output is None:
        output = stamp + '.png'
    else:
        if not output.endswith('.png'):
            output += '.png'
        if stamp:
            output = stamp + '_' + output
    
    with open(src_file) as f:
        src = ''.join(f.read())
        
    other_files = kwargs.pop('files', '').split(',')
    for file_name in other_files:
        if file_name:
             fp = join(py5.sketch_path(), file_name)
             with open(fp) as f:
                 other_src = ''.join(f.read())
             src += '\n# ' + file_name
             src += '\n' + other_src 
    

    metadata = PIL.PngImagePlugin.PngInfo()

    context = kwargs.pop('context', None)
    if context:
        metadata.add_itxt("context", context)   
    metadata.add_itxt("code", src)
    py5.save(output, *args, pnginfo=metadata, **kwargs)
    # read back and print...
    # target_image = PIL.Image.open(output)
    # print(target_image.info['code'])

def save_snapshot_and_code():
    import shutil
    from py5 import sketch_path, Path, save
    path = sketch_path()
    has_image = Path(__file__[:-3]+'.png').is_file()
    number = len(list(path.iterdir())) - has_image
    snap_name = f'{number:03d}'  # 001, 002 ....
    save(path / snap_name / (snap_name + '.png')) 
    shutil.copyfile(__file__, path / snap_name / (snap_name + '.py'))

def get_arduino(port=None):
    """
    This is a PyFirmata 'helper' that tries to connect to
    an Arduino compatible board.
    
    If port is None it tries to connect to the last port
    listed by pyserial's serial.tools.list_ports.comports().
    You can provide a string with the port name or an integer
    index to the port (as listed by pyserial and printed in
    the console if no port is provided)
    
    If successful it returns a pyfirmata Arduino object, but
    before that it starts a pyfirmata.util.Iterator, and adds
    to it analog_read() and digital_read() functions that mimic
    Processing's Firmata library interface (readings are never
    None, and analog pins return a value between 0 and 1023).
    """
    
    from pyfirmata import Arduino, util
    from serial.tools import list_ports
    ports = [comport.device for comport in list_ports.comports()]
    if not ports:
        raise Exception('No board/Arduino port found')
    elif port is None:
        print('\n'.join(f'{i}: {p}' for i, p in enumerate(ports)))
        port = len(ports) - 1
        
    if isinstance(port, str):
        print(f'Trying to connect to port: {port}')
        arduino = Arduino(port)
    else:
        print(f'Trying to connect to port {port}: {ports[port]}')
        arduino = Arduino(ports[port])
        
    util.Iterator(arduino).start()
    for a in range(6):  # A0 A1 A2 A3 A4 A5
        arduino.analog[a].enable_reporting()
    # monkeypatching PyFirmata with Procesing-like methods
    arduino.analog_read = (
        lambda a: round(arduino.analog[a].read() * 1024)
                  if arduino.analog[a].read() is not None
                  else 0
        )
    digital_pin_dict = {d: arduino.get_pin(f'd:{d}:i')
                        for d in range(2, 14)}
    for d in digital_pin_dict.keys():
        digital_pin_dict[d].enable_reporting()
    arduino.digital_read = (
        lambda d: digital_pin_dict[d].read()
                  if digital_pin_dict[d].read() is not None
                  else False
        )
    return arduino
