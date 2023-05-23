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


    def getState(self):
        return self.state
    

    def isTerminal(self) -> bool:
        return self.state.isTerminal()
    

    def notFullyExpanded(self):
        if len(self.childeren < 256):
            return True
        else:
            return False


    def addRandomChild(self):
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


    def getChilderen(self):
        return self.childeren
    

    def getParent(self):
        return self.parent


    def print_Node(self):
        print("Node : ")
        self.state.printBoard()