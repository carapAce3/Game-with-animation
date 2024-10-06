from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, OrthographicLens, TextureStage


config = '''
win-size 1920 1080
show-frame-rate-meter 1
'''
loadPrcFileData("", config)

keys = {
    "left": False,
    "right": False,
}

def animation(key_name, key_state, model, walking):
    keys[key_name] = key_state
    if walking:
        model.find('**/+SequenceNode').node().loop(True, 0,9)
    else:
        model.find('**/+SequenceNode').node().loop(True, 10,19)
    
    if key_name == "right":
        model.setTexScale(TextureStage.getDefault(),1,1)
    elif key_name == "left":
        model.setTexScale(TextureStage.getDefault(),-1,1)

class Game(ShowBase):
    def __init__(self):
        super().__init__()

        self.model = self.loader.loadModel("animations/Jack.egg")
        self.model.setScale(0.3)
        self.model.reparentTo(self.render)

        self.model.find('**/+SequenceNode').node().loop(True, 10,19)

        n = OrthographicLens()
        n.setFilmSize(1920,1080)
        n.setNearFar(-50, 50)
        self.cam.node().setLens(n)




        self.accept("arrow_left", animation, ["left", True, self.model, True])
        self.accept("arrow_left-up", animation, ["left", False, self.model, False])
        self.accept("arrow_right", animation, ["right", True, self.model, True])
        self.accept("arrow_right-up", animation, ["right", False, self.model, False])

        self.taskMgr.add(self.move_jack, "move-jack")

        self.x = 0
        self.speed = 200

    def move_jack(self, task):
        dt = globalClock.getDt()

        if keys["left"]:
            self.x -= self.speed * dt
        if keys["right"]:
            self.x += self.speed * dt

        self.model.setPos(self.x, 0, 0)

        return task.cont

game = Game()
game.run()