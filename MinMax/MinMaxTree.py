import copy
from State import State


class Tree:
    def __init__(self, state:State, inTurn:bool, parent=None) -> None:
        self.rootState = state
        self.children = []
        self.winningLeafs = []
        self.hasWinLeaf = False
        self.parent = None
        self.inTurn = inTurn
        self.actionToObtain = None
        self.parent = None
        self.MinMaxValue = 0


    def getInTurn(self):
        return self.inTurn


    def getWinningLeafs(self) -> list:
        return self.winningLeafs
    

    def getChildren(self) -> list:
        return self.children
    

    def getAction(self) -> tuple:
        return self.actionToObtain
    

    def haveDescisivChild(self) -> bool:
        return self.hasWinLeaf
    

    def getBoard(self):
        return self.rootState.getBoard()
    

    def getMinMaxValue(self):
        return self.MinMaxValue
    

    def setMinMaxValue(self, val):
        self.MinMaxValue = val


    def setActionToObtain(self, action):
        self.actionToObtain = action


    def generateTree(self, depth):
        if depth > 0:
            if not self.rootState.quasiTerminal():
                possiblechildren = self.rootState.getAllPossibleChildren()

                for c in possiblechildren:
                    childState = copy.deepcopy(self.rootState)
                    action = childState.createChild(c)
                    child = Tree(childState, not self.inTurn, self)
                    child.setActionToObtain(action)

                    if childState.quarto():
                        self.winningLeafs.append(child)
                        self.hasWinLeaf = True
                        if not self.inTurn:
                            break
                    else:
                        child.generateTree(depth-1)
                        self.children.append(child)
            else:
                childState = copy.deepcopy(self.rootState)
                action= childState.createChild(None)
                child = Tree(childState, not self.inTurn, self)
                child.setActionToObtain(action)
                if childState.quarto():
                    self.winningLeafs.append(child)
                    self.hasWinLeaf = True
                else:
                    self.children.append(child)