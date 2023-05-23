from tree.State import State
from tree.Node import Node

class MinMaxTree:
    def __init__(self, shapes) -> None:
        self.rootState = State(shapes)
        self.root = Node(state=self.rootState)



    def buildTree(self, win:bool):
        """
        win = True  si l'IA place sa pièce au tour impair
        win = False si l'IA place sa pièce au tour pair
        """
        self.root.createChilderen(win, 0)
        print("FIN de l'arbre")
        self.root.computeHfromChilderen()


    
    def getHRoot(self):
        return self.root.getH()
    
