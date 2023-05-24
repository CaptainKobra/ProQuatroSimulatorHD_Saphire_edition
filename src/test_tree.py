from Shape import Shape
import time
from MCTS.UCT_fromRef import UCT
from MCTS.State import State
import random

if __name__=='__main__':
    def createShapes():
        shapes = []
        num = 1
        for size in ["little", "big"]:
            for color in ["red", "blue"]:
                for shape in ["circle", "rect"]:
                    for filled in [True, False]:
                        s = Shape(num, shape, color, size, filled, 100, 100)
                        shapes.append(s)
                        num += 1
        return shapes


    shapes = createShapes()
    maxTime = 1.0
    tree = UCT(maxTime)
    s = random.choice(shapes)
    shapes.remove(s)
    initialState = State(shapes, s)
    action = tree.search(initialState)
    print(action)