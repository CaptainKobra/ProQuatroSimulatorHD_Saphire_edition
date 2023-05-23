from MCTS.Node import Node
from MCTS.State import State
import time
import math
import copy

class UCT:
    def __init__(self, maxTime) -> None:
        self.maxTime = maxTime
        self.tree = []
        self.action = {}
        self.N = {}
        self.Q = {}
        self.Cp = 2


    def search(self, currentState):
        startTime = time.time()
        root = Node(currentState)
        self.tree.append(root)
        while (time.time() - startTime) < self.maxTime:
            node = self.treePolicy(root)
            self.tree.append(node)
            reward = self.defaultPolicy(node.getState())
            self.backup(node, reward)
        best = self.bestChild(root, 0)
        return self.action[best]
    

    def treePolicy(self, node:Node):
        while not node.isTerminal():
            if node.notFullyExpanded():
                return self.expand(node)
            else:
                node = self.bestChild(node, self.Cp)
        return node
    

    def expand(self, node:Node):
        child, action = node.addRandomChild()
        self.action[child] = action
        return child
    

    def bestChild(self, node:Node, c):
        valMax = -10000000
        bestChild = None
        for child in node.getChilderen():
            val = self.Q[child]/self.N[child] +  c*math.sqrt(2*math.log(self.N[node]) / self.N[child])
            if val > valMax:
                valMax = val
                bestChild = child
        return bestChild
    

    def defaultPolicy(self, state:State):
        s = copy.deepcopy(state)
        while not s.isTerminal():
            state = s.randomAction()
        return s.reward()
    

    def backup(self, node:Node, reward):
        while node != None:
            self.N[node] += 1
            self.Q[node] += reward
            reward = -reward
            node = node.getParent()

        