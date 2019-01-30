import pyglet,math
from pyglet.gl import *
from pyglet.window import key

TICKS_PER_SEC = 60

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


    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.set_minimum_size(800,600)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        # pyglet.clock.schedule(self.update)
         # This call schedules the `update()` method to be called
        # TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / TICKS_PER_SEC)
        self.world = None
        self.camera = None

    def set_camera(self,camera):
        self.camera = camera

    def set_world(self,world):
        self.world = world

    def push(self,pos,rot):
        glPushMatrix()
        glRotatef(-rot[0],1,0,0)
        glRotatef(-rot[1],0,1,0)
        glTranslatef(-pos[0],-pos[1],-pos[2])

    def on_draw(self):
        if self.camera!=None and self.world!=None:
            self.clear()
            self.set3d()
            self.push(self.camera.pos,self.camera.rot)
            self.world.draw()
            glPopMatrix()

    def update(self,dt):
        if self.world!=None:
            self.world.update(dt)
        if self.camera!=None:
            self.camera.update(dt,self.keys)

    def setLock(self,state): self.lock=state; self.set_exclusive_mouse(state)
    lock = True; mouse_lock=property(lambda self:self.lock,setLock)

    def on_key_press(self,KEY,MOD):
        if KEY==key.ESCAPE:
            self.close()
        elif KEY==key.E:
            self.mouse_lock = not self.mouse_lock

    def on_mouse_motion(self,x,y,dx,dy):
        if self.mouse_lock and self.camera!=None:
            self.camera.mouse_motion(dx,dy)
