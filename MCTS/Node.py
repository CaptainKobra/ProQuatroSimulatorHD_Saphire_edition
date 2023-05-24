from State import State
import copy
import random

class Node:
    def __init__(self, state:State, parent=None, terminal:bool=False) -> None:
        self.state = state
        self.children = []
        self.parent = parent
        self.action = []
        self.N = 0
        self.Q = 0
        self.actionToObtain = None
        self.allPossibleChildren = self.state.getAllPossibleChildren()
        self.terminal = terminal


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
        if len(self.allPossibleChildren) > 0 or self.state.quasiTerminal():
            return True
        else:
            return False


    def addRandomChild(self):
        if len(self.allPossibleChildren) > 0:
            index = random.randint(0, len(self.allPossibleChildren)-1)
            selectedChild = self.allPossibleChildren.pop(index)
            childState = copy.deepcopy(self.state)
            actionToObtain = childState.createChild(selectedChild)
            child = Node(childState, self)
        else:
            childState = copy.deepcopy(self.state)
            actionToObtain = childState.createChild(None)
            child = Node(childState, self, terminal=True)
        child.setActionToObtain(actionToObtain)
        self.children.append(child)
        return child
    

    def setActionToObtain(self, action):
        self.actionToObtain = action


    def getChildren(self):
        return self.children
    

    def getParent(self):
        return self.parent
    

    def getReward(self):
        return self.state.reward()