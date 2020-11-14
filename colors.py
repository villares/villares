

def random_hue_saturated(bright=None):
    bright = 255 if bright is None else bright
    with pushStyle():
        colorMode(HSB)
        return color(random(256), 255, bright)
