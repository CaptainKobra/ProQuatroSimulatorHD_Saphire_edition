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
        self.allPossibleChilderen = self.state.getAllPossibleChilderen()


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


    def getActionToObtain(self):
        return self.actionToObtain
    

    def isTerminal(self) -> bool:
        return self.state.isTerminal()
    

    def notFullyExpanded(self):
        if len(self.allPossibleChilderen) == 0:
            return True
        else:
            return False


    def addRandomChild(self):
        if len(self.allPossibleChilderen) > 1:
            index = random.randint(0, len(self.allPossibleChilderen)-1)
        else:
            index = 0
        selectedChild = self.allPossibleChilderen.pop(index)
        childState = copy.deepcopy(self.state)
        self.actionToObtain = childState.createChild(selectedChild)
        child = Node(childState, self)
        self.childeren.append(child)
        #print("enfant ajouté")
        return child


    def getChilderen(self):
        return self.childeren
    

    def getParent(self):
        return self.parent
    

    def getReward(self):
        return self.state.reward()


    def print_Node(self):
        print("Node : ")
        self.state.printBoard()

    
    def whyTerminal(self):
        self.print_Node()
        self.state.whyTerminal()