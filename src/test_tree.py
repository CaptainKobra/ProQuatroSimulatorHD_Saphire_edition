from Shape import Shape
from tree.MinMaxTree import MinMaxTree
import time

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
    start = time.time()
    tree = MinMaxTree(shapes=shapes)
    tree.buildTree(True)
    h = tree.getHRoot()
    end = time.time()
    total_time = end-start
    print("h de root = ", h)
    print("temps nécessaire (en s) : ", total_time)