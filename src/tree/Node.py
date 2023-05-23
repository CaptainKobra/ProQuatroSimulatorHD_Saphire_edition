from tree.State import State
import copy

class Node:
    def __init__(self, state:State, parent=None) -> None:
        self.state = state
        self.childeren = []
        self.parent = parent
        self.h = 0


    def setH(self, h):
        self.h = h
        

    def getH(self):
        return self.h
    

    def createChilderen(self, win:bool, counter:int):
        print(counter)
        counter+=1
        for i in range(16):
            for j in range(16):
                copyState = copy.deepcopy(self.state)
                s = State(state=copyState)
                if s.placeShapeOnBoard(i, j):
                    child = Node(s, self)
                    #child.print_Node()
                    if not s.quarto():
                        child.createChilderen(not win, counter)
                    else:
                        #print("quarto")
                        if win:
                            self.h = 100
                        else:
                            self.h = -100
                    self.childeren.append(child)
        #print("node avec ", len(self.childeren), " enfants")



    #def addChild(self, child):
    #    self.childeren.append(child)


    def computeHfromChilderen(self):
        for child in self.childeren:
            child.computeHfromChilderen()
            self.h += child.getH()


    def print_Node(self):
        print("Node : ")
        self.state.printBoard()