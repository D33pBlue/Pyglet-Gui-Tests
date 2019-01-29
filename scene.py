import pyglet,math
from pyglet.gl import *
from pyglet.window import key

TICKS_PER_SEC = 60


class Player:
    def __init__(self,pos=(0,0,0),rot=(0,0)):
        self.pos = list(pos)
        self.rot = list(rot)

    def update(self,dt,keys):
        s = dt*10
        rotY = -self.rot[1]/180*math.pi
        dx,dz = s*math.sin(rotY),s*math.cos(rotY)
        if keys[key.W]: self.pos[0]+=dx; self.pos[2]-=dz
        if keys[key.S]: self.pos[0]-=dx; self.pos[2]+=dz
        if keys[key.A]: self.pos[0]-=dz; self.pos[2]-=dx
        if keys[key.D]: self.pos[0]+=dz; self.pos[2]+=dx
        if keys[key.SPACE]: self.pos[1]+=s

    def mouse_motion(self,dx,dy):
        dx /= 8.0
        dy /= 8.0
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90: self.rot[0]=90
        elif self.rot[0] < -90: self.rot[0]=-90
        # m = 0.15
        # x, y = self.rot
        # x, y = x + dx * m, y + dy * m
        # y = max(-90, min(90, y))
        # self.rot[0] = x
        # self.rot[1] = y

# GRASS_SIDE = ('t2f',(0.12,0.62, 0.25,0.62, 0.25,0.75, 0.12,0.75,))
# GRASS_UP = ('t2f',(0.25,0.62, 0.38,0.62, 0.38,0.75, 0.25,0.75,))
# SAND = ('t2f',(0,0, 0.13,0, 0.13,0.13, 0,0.13,))
GRASS_SIDE = ('t2f',(0.375,0.625, 0.5,0.625, 0.5,0.75, 0.375,0.75,))
GRASS_UP = ('t2f',(0.5,0.625, 0.625,0.625, 0.625,0.75, 0.5,0.75,))
SAND = ('t2f',(0,0, 0.13,0, 0.13,0.13, 0,0.13,))

class Model:
    def __init__(self):
        self.batch = pyglet.graphics.Batch()
        x,y,z = 0,0,-1
        X,Y,Z = x+1,y+1,z+1
        tex_coords = ('t2f',(0,0, 1,0, 1,1, 0,1,))
        self.ttex = self.get_tex("resources/tex.png")
        self.batch.add(4,GL_QUADS,self.ttex,('v3f',(X,y,z, x,y,z, x,Y,z, X,Y,z,)),GRASS_SIDE)
        self.batch.add(4,GL_QUADS,self.ttex,('v3f',(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z,)),GRASS_SIDE)
        self.batch.add(4,GL_QUADS,self.ttex,('v3f',(x,y,z, x,y,Z, x,Y,Z, x,Y,z,)),GRASS_SIDE)
        self.batch.add(4,GL_QUADS,self.ttex,('v3f',(X,y,Z, X,y,z, X,Y,z, X,Y,Z,)),GRASS_SIDE)
        self.batch.add(4,GL_QUADS,self.ttex,('v3f',(x,Y,z, X,Y,z, X,Y,Z, x,Y,Z,)),GRASS_UP)



    def draw(self):
        self.batch.draw()

    def get_tex(self,tfile):
        tex = pyglet.image.load(tfile).texture
        return pyglet.graphics.TextureGroup(tex)

class Window(pyglet.window.Window):

    def set3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)#
        glLoadIdentity()#
        gluPerspective(65.0, width / float(height), 0.1, 60.0)#
        glMatrixMode(GL_MODELVIEW)#
        glLoadIdentity()#
        # y,x = self.player.rot
        # glRotatef(-x, 0, 1, 0)
        # glRotatef(-y, math.cos(math.radians(-x)), 0, math.sin(math.radians(-x)))


    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.set_minimum_size(800,600)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        # pyglet.clock.schedule(self.update)
         # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)

        self.model = Model()
        self.player = Player((0,0,2.5),(0,6))


    def push(self,pos,rot):
        glPushMatrix()
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0],-pos[1],-pos[2])
        print rot

    def on_draw(self):
        self.clear()
        self.set3d()
        self.push(self.player.pos,self.player.rot)
        self.model.draw()
        glPopMatrix()

    def update(self,dt):
        self.player.update(dt,self.keys)

    def setLock(self,state): self.lock=state; self.set_exclusive_mouse(state)
    lock = True; mouse_lock=property(lambda self:self.lock,setLock)

    def on_key_press(self,KEY,MOD):
        if KEY==key.ESCAPE:
            self.close()
        elif KEY==key.E:
            self.mouse_lock = not self.mouse_lock

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock:
            self.player.mouse_motion(dx,dy)


def setup_fog():
    """ Configure the OpenGL fog properties.

    """
    # Enable fog. Fog "blends a fog color with each rasterized pixel fragment's
    # post-texturing color."
    glEnable(GL_FOG)
    # Set the fog color.
    glFogfv(GL_FOG_COLOR, (GLfloat * 4)(0.5, 0.69, 1.0, 1))
    # Say we have no preference between rendering speed and quality.
    glHint(GL_FOG_HINT, GL_DONT_CARE)
    # Specify the equation used to compute the blending factor.
    glFogi(GL_FOG_MODE, GL_LINEAR)
    # How close and far away fog starts and ends. The closer the start and end,
    # the denser the fog in the fog range.
    glFogf(GL_FOG_START, 20.0)
    glFogf(GL_FOG_END, 60.0)


def setup():
    """ Basic OpenGL configuration.

    """
    # Set the color of "clear", i.e. the sky, in rgba.
    glClearColor(0.5, 0.69, 1.0, 1)
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
    setup_fog()

if __name__ == '__main__':
    window = Window(width=800, height=600, caption='Pyglet test', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()
