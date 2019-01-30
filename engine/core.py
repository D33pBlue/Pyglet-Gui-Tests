import math
import pyglet
from pyglet.gl import *
import window


def run():
    pyglet.app.run()

def setup(title,skyColor=(0.5, 0.69, 1.0, 1),fog=True,fogStart=10.0,fogEnd=30.0,ticks=60,
        screen_w=800,screen_h=600,screen_resizable=True,mouse_cap=True):
    """
    Basic configurations and window creation
    """
    window.TICKS_PER_SEC = ticks
    win = window.Window(width=screen_w, height=screen_h, caption=title, resizable=screen_resizable)
    win.set_exclusive_mouse(mouse_cap)
    # Set the color of "clear", i.e. the sky, in rgba.
    glClearColor(*skyColor)
    # Enable culling (not rendering) of back-facing facets -- facets that aren't
    # visible to you.
    # glEnable(GL_CULL_FACE)
    # Set the texture minification/magnification function to GL_NEAREST (nearest
    # in Manhattan distance) to the specified texture coordinates. GL_NEAREST
    # "is generally faster than GL_LINEAR, but it can produce textured images
    # with sharper edges because the transition between texture elements is not
    # as smooth."
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if fog:
        # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
        # post-texturing color."
        glEnable(GL_FOG)
        # Set the fog color.
        glFogfv(GL_FOG_COLOR, (GLfloat * 4) (*skyColor))
        # Say we have no preference between rendering speed and quality.
        glHint(GL_FOG_HINT, GL_DONT_CARE)
        # Specify the equation used to compute the blending factor.
        glFogi(GL_FOG_MODE, GL_LINEAR)
        # How close and far away fog starts and ends. The closer the start and end,
        # the denser the fog in the fog range.
        glFogf(GL_FOG_START, fogStart)
        glFogf(GL_FOG_END, fogEnd)
    return win



class World(object):
    def __init__(self):
        self.bodies = dict()

    def add_body(self,body,idb=0):
        while idb in self.bodies.keys():
            idb += 1
        self.bodies[idb] = body
        return idb

    def update(self,dt):
        pass

    def remove_body(self,idb):
        del self.bodies[idb]

    def draw(self):
        for k in self.bodies.keys():
            self.bodies[k].draw()


class Body(object):
    def __init__(self,tileset,center=(0,0,0),scale_factor=1.0):
        self.center = list(center)
        self.rotation = [0,0]
        self.scale_factor = scale_factor
        self.tileset = tileset
        self.shapes = []
        self.batch = pyglet.graphics.Batch()

    def add_square(self,texture,vertices):
        self.shapes.append((4,
            GL_QUADS,
            self.tileset,
            vertices,
            texture
            ))

    def update_batch(self):
        self.batch = pyglet.graphics.Batch()
        # 180:pi=tot:x
        radRot = [self.rotation[0]*math.pi/180.0,self.rotation[1]*math.pi/180.0]
        for x in self.shapes:
            n,t,tiles,vrts,tx = x
            vertices = list(vrts)
            for i in range(len(vrts)):
                vertices[i] *= self.scale_factor
            for i in range(n):
                vertices[i*3] += self.center[0]
                vertices[i*3+1] += self.center[1]
                vertices[i*3+2] += self.center[2]
                # apply rotations
                if radRot[0]!=0 or radRot[1]!=0:
                    lx,ly,lz = vertices[i*3]-self.center[0],vertices[i*3+1]-self.center[1],vertices[i*3+2]-self.center[2]
                    dx = math.cos(radRot[0])*lx-lx+math.cos(radRot[1])*lx-lx
                    dz = -math.sin(radRot[0])*lx
                    dy = math.sin(radRot[1])*lx
                    vertices[i*3] += dx
                    vertices[i*3+1] += dy
                    vertices[i*3+2] += dz
            self.batch.add(n,t,tiles,('v3f',tuple(vertices)),tx)

    def draw(self):
        self.batch.draw()
