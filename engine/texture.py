import os
import pyglet


dir_path = os.path.dirname(os.path.realpath(__file__))
TEXTURE = dir_path+"/tex.png"

GRASS_SIDE = ('t2f',(0.375,0.625, 0.5,0.625, 0.5,0.75, 0.375,0.75,))
GRASS_UP = ('t2f',(0.5,0.625, 0.622,0.625, 0.622,0.745, 0.5,0.745,))
GRASS_DOWN = ('t2f',(0.375,0.5, 0.5,0.5, 0.5,0.625, 0.375,0.625,))
SAND = ('t2f',(0,0, 0.13,0, 0.13,0.13, 0,0.13,))
MUSHROOM = ('t2f',(0.375,0.375, 0.5,0.375, 0.5,0.45, 0.375,0.45,))

def load(tfile=TEXTURE):
    tex = pyglet.image.load(tfile).texture
    return pyglet.graphics.TextureGroup(tex)
