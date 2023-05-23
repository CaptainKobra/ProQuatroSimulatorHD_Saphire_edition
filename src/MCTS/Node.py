from MCTS.State import State
import copy
import random
import math

class Node:
    def __init__(self, state:State, parent=None) -> None:
        self.state = state
        self.childeren = []
        self.parent = parent
        self.action = []
        self.N = 0
        self.Q = 0
        self.actionToObtain = None


    def getN(self):
        return self.N
    

    def getQ(self):
        return self.Q
    

    def addToN(self, val):
        self.N += val


    def addToQ(self, val):
        self.Q += val


    def getState(self):
        return self.state
    

    def setActionToObtain(self, action):
        self.actionToObtain = action


    def getActionToObtain(self):
        return self.actionToObtain
    

    def isTerminal(self) -> bool:
        return self.state.isTerminal()
    

    def notFullyExpanded(self):
        if len(self.childeren) < 256:
            return True
        else:
            return False


    def addRandomChild(self):
        copyState = copy.deepcopy(self.state)
        pos = copyState.randomPlaceShapeOnBoard()
        selectedShape = copyState.randomSelectShape()
        action = (pos, selectedShape)
        child = Node(copyState, self)
        self.childeren.append(child)
        return child, action

        """"
        action = self.selectAction()
        i = math.floor(action/16)
        j = action%16
        copyState = copy.deepcopy(self.state)
        while not copyState.placeShapeOnBoard(i, j):
            action = self.selectAction()
            i = math.floor(action/16)
            j = action%16
        child = Node(copyState, self)
        self.action.append(action)
        self.childeren.append(child)
        return child, action
        """
    """
    def selectAction(self):
        action = random.randint(0,255)
        while True:
            try:
                self.action.index(action)
            except:
                break
            else:
                action = random.randint(0,255)
        return action
    """


    def getChilderen(self):
        return self.childeren
    

    def getParent(self):
        return self.parent


    def print_Node(self):
        print("Node : ")
        self.state.printBoard()