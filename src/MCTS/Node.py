from MCTS.State import State
import copy
import random
import math

class Node:
    def __init__(self, state:State, parent=None, terminal:bool=False) -> None:
        self.state = state
        self.childeren = []
        self.parent = parent
        self.action = []
        self.N = 0
        self.Q = 0
        self.actionToObtain = None
        self.allPossibleChilderen = self.state.getAllPossibleChilderen()
        self.terminal = terminal
        #print("new node - possible childeren=", self.allPossibleChilderen)


    def printInfoTerminal(self):
        print("self.terminal =", self.terminal)
        print("possible childeren=", self.allPossibleChilderen)
        print("number of childeren =", len(self.childeren))
        self.state.whyTerminal()


    def getN(self):
        return self.N
    

    def getQ(self):
        return self.Q
    

    def addToN(self, val):
        """
        Add val to N
        """
        self.N += val


    def addToQ(self, val):
        """
        Add val to Q
        """
        self.Q += val


    def getState(self):
        return self.state


    def getActionToObtain(self):
        return self.actionToObtain
    

    def isTerminal(self) -> bool:
        return self.state.isTerminal() or self.terminal
    

    def notFullyExpanded(self):
        if len(self.allPossibleChilderen) > 0 or self.state.quasiTerminal():
            return True
        else:
            return False


    def addRandomChild(self):
        if len(self.allPossibleChilderen) > 0:
            index = random.randint(0, len(self.allPossibleChilderen)-1)
            selectedChild = self.allPossibleChilderen.pop(index)
            childState = copy.deepcopy(self.state)
            actionToObtain = childState.createChild(selectedChild)
            if actionToObtain == None:
                print("error : action is none")
            child = Node(childState, self)
        else:
            childState = copy.deepcopy(self.state)
            actionToObtain = childState.createChild(None)
            child = Node(childState, self, terminal=True)
        child.setActionToObtain(actionToObtain)
        self.childeren.append(child)
        return child
    

    def setActionToObtain(self, action):
        self.actionToObtain = action


    def getChilderen(self):
        return self.childeren
    

    def getParent(self):
        return self.parent
    

    def getReward(self):
        return self.state.reward()


    def print_Node(self):
        print("Node : ")
        self.state.printBoard()