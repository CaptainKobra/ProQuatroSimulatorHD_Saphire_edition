from MCTS.Node import Node
from MCTS.State import State
import time
import math
import copy

class UCT:
    def __init__(self, maxTime) -> None:
        self.maxTime = maxTime
        self.action = {}
        self.N = {}
        self.Q = {}
        self.Cp = 2
        self.fullyExtended = False


    def search(self, currentState):
        #print("search")
        startTime = time.time()
        root = Node(currentState)
        currentNode = root
        self.fullyExtended = False
        while (time.time() - startTime) < self.maxTime:
            node = self.treePolicy(currentNode)
            reward = self.defaultPolicy(node.getState())
            self.backup(node, reward)
        if self.fullyExtended:
            print("fully extended")
        best = self.bestChild(root, 0)
        return best.getActionToObtain()
    

    def treePolicy(self, node:Node):
        #print("treePolicy")
        while not node.isTerminal():
            if node.notFullyExpanded():
                return self.expand(node)
            else:
                self.fullyExtended = True
                node = self.bestChild(node, self.Cp)
        return node
    

    def expand(self, node:Node):
        #print("expand")
        child, action = node.addRandomChild()
        child.setActionToObtain(action)
        return child
    

    def bestChild(self, node:Node, c) -> Node:
        #print("bestChild")
        valMax = -10000000
        bestChild = None
        for child in node.getChilderen():
            Qc = child.getQ()
            Nc = child.getN()
            Nn = child.getN()
            val = Qc/Nc +  c*math.sqrt(2*math.log(Nn) / Nc)
            if val > valMax:
                valMax = val
                bestChild = child
        if bestChild == None:
            print(node.getChilderen())
            print("bestChild is None")
        return bestChild
    

    def defaultPolicy(self, state:State):
        #print("defaultPolicy")
        s = copy.deepcopy(state)
        i = 0
        while not s.isTerminal():
            state = s.randomAction()
            i+=1
            if i > 20:
                exit(0)
        return s.reward()
    

    def backup(self, node:Node, reward):
        #print("backup")
        while node != None:
            node.addToN(1)
            node.addToQ(reward)
            reward = -reward
            node = node.getParent()

        