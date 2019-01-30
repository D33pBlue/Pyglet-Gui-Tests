import engine.core as engine
import engine.camera as camera
import engine.texture as tex
import random


class Mushroom(engine.Body):
    def __init__(self,ttex,center):
        super(Mushroom,self).__init__(ttex,center)
        self.add_square(tex.MUSHROOM,(-1,0,0, 1,0,0, 1,1,0, -1,1,0,))
        self.scale_factor = 0.5
        self.rotation[0]=30.0
        self.update_batch()

class Ground(engine.Body):
    def __init__(self,ttex,center):
        super(Ground,self).__init__(ttex,center)
        self.add_square(tex.GRASS_UP,(-1,0,-1, 1,0,-1, 1,0,1, -1,0,1,))
        self.scale_factor = 10.0
        self.update_batch()

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
        self.add_body(self.block)
        for i in range(-10,10):
            for j in range(-10,10):
                self.add_body(Ground(self.ttex,(i*20,-2,j*20)))
        for _ in range(100):
            mushroom = Mushroom(self.ttex,(random.randint(-100,100),-2,random.randint(-100,100)))
            mushroom.rotation[0]=random.uniform(-200.0,200.0)
            self.add_body(mushroom)

    def update(self,dt):
        self.block.center[1]+=0.001
        self.block.update_batch()

if __name__ == '__main__':
    window = engine.setup("Engine test")
    window.set_world(MineWorld())
    window.set_camera(camera.FirstPerson(pos=(0,0,10    )))
    engine.run()
