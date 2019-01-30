# import pyglet,math
# from pyglet.gl import *
# from pyglet.window import key
import engine.core as engine
import engine.camera as camera
import engine.texture as tex


class Block(engine.Body):
    def __init__(self,ttex,center):
        super(Block,self).__init__(ttex,center)
        x,y,z = 0,0,-1
        X,Y,Z = x+1,y+1,z+1
        self.add_square(tex.GRASS_SIDE,(X,y,z, x,y,z, x,Y,z, X,Y,z,))
        self.add_square(tex.GRASS_SIDE,(x,y,Z, X,y,Z, X,Y,Z, x,Y,Z,))
        self.add_square(tex.GRASS_SIDE,(x,y,z, x,y,Z, x,Y,Z, x,Y,z,))
        self.add_square(tex.GRASS_SIDE,(X,y,Z, X,y,z, X,Y,z, X,Y,Z,))
        self.add_square(tex.GRASS_UP,(x,Y,z, X,Y,z, X,Y,Z, x,Y,Z,))
        self.add_square(tex.GRASS_DOWN,(x,y,z, X,y,z, X,y,Z, x,y,Z,))
        self.update_batch()


class MineWorld(engine.World):
    def __init__(self):
        super(MineWorld, self).__init__()
        self.ttex = tex.load()
        self.block = Block(self.ttex,(0,0,0))
        for i in range(-10,10):
            for j in range(-10,10):
                self.add_body(Block(self.ttex,(i,-2,j)))
        self.add_body(self.block)

    def update(self,dt):
        self.block.center[1]+=0.001
        self.block.update_batch()

if __name__ == '__main__':
    # window = Window(width=800, height=600, caption='Pyglet test', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    # window.set_exclusive_mouse(True)
    # setup()
    window = engine.setup("Engine test")
    window.set_world(MineWorld())
    window.set_camera(camera.FirstPerson())
    engine.run()
