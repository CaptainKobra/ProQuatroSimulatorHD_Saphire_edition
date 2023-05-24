import copy
from MCTS.State import State


class Tree:
    def __init__(self, state:State, inTurn:bool, parent=None) -> None:
        self.rootState = state
        self.childeren = []
        self.loosingLeafs = []
        self.winningLeafs = []
        self.hasLoosingChild = False
        self.parent = None
        self.inTurn = inTurn
        self.actionToObtain = None
        self.parent = None


    def getWinningLeafs(self) -> list:
        return self.winningLeafs
    

    def getChilderen(self) -> list:
        return self.childeren
    

    def getAction(self) -> tuple:
        return self.actionToObtain
    
    def haveLoosingChild(self) -> bool:
        return self.hasLoosingChild


    def generateTree(self, depth):
        if depth > 0:
            if not self.rootState.quasiTerminal():
                possibleChilderen = self.rootState.getAllPossibleChilderen()

                for c in possibleChilderen:
                    childState = copy.deepcopy(self.rootState)
                    self.actionToObtain = childState.createChild(c)
                    child = Tree(childState, not self.inTurn, self)

                    if childState.quarto():
                        if not self.inTurn:
                            self.winningLeafs.append(child)
                            break
                        else:
                            self.haveLoosingChild = True
                            self.loosingLeafs.append(child)
                            break
                    else:
                        child.generateTree(depth-1)
                        self.childeren.append(child)
            else:
                childState = copy.deepcopy(self.rootState)
                self.actionToObtain = childState.createChild(None)
                child = Tree(childState, not self.inTurn, self)
                if childState.quarto():
                    if not self.inTurn:
                        self.winningLeafs.append(child)
                    else:
                        self.haveLoosingChild = True
                        self.loosingLeafs.append(child)
                else:
                    self.childeren.append(child)