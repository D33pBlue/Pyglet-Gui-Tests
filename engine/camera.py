import math
from pyglet.window import key


class FirstPerson(object):
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
        # if keys[key.Z]:
        #     self.block.center[0]+=0.1
        #     self.block.update_batch()
        # if keys[key.X]:
        #     self.block.scale_factor+=0.1
        #     self.block.update_batch()


    def mouse_motion(self,dx,dy):
        dx /= 8.0
        dy /= 8.0
        self.rot[0] += dy
        self.rot[1] -= dx
        if self.rot[0]>90: self.rot[0]=90
        elif self.rot[0] < -90: self.rot[0]=-90
