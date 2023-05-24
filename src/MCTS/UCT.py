from MCTS.Node import Node
from MCTS.State import State
import time
import math
import copy
import random

class UCT:
    def __init__(self, maxTime:float) -> None:
        self.maxTime = maxTime
        self.action = {}
        self.N = {}
        self.Q = {}
        self.Cp = 1/math.sqrt(2) # TODO à ajuster, éventuellement de manière dynamique selon l'étape du jeu
        self.fullyExtended = False
        self.error = False
        self.currentNode = None


    def search(self, currentState):
        #print("search")
        startTime = time.time()
        root = Node(currentState)
        self.fullyExtended = False
        it = 0
        while (time.time() - startTime) < self.maxTime:
            it +=1
            node = self.treePolicy(root)
            self.defaultPolicy(node)
        best = self.bestChild(root, 0)
        return best.getActionToObtain()
    

    def treePolicy(self, node:Node):
        #print("treePolicy")
        if node.isTerminal() and not self.error:
            self.error = True
            print("probleme in treePolicy -> node terminal")
            node.printInfoTerminal()
        while not node.isTerminal():
            if node.notFullyExpanded():
                return self.expand(node)
            else:
                self.fullyExtended = True
                node = self.bestChild(node, self.Cp)
        return node
    

    def expand(self, node:Node):
        #print("expand")
        child = node.addRandomChild()
        return child
    

    def bestChild(self, node:Node, c) -> Node:
        #print("bestChild")
        valMax = None
        bestChild = None
        for child in node.getChildren():
            Qc = child.getQ()
            Nc = child.getN()
            Nn = child.getN()
            val = Qc/Nc +  c*math.sqrt(2*math.log(Nn) / Nc)
            if valMax == None or val > valMax:
                valMax = val
                bestChild = child
        if bestChild == None:
            print("c =", c)
            print("is terminal ?", node.isTerminal())
            node.printInfoTerminal()
            print(node.getChildren())
            print("bestChild is None")
            exit()
        return bestChild
    

    def defaultPolicy(self, node:Node):
        while not node.isTerminal():
            if not node.notFullyExpanded():
                break
            node = node.addRandomChild()
        reward = node.getReward()
        self.backup(node, reward)
    

    def backup(self, node:Node, reward):
        #print("backup")
        while node != None:
            node.addToN(1)
            node.addToQ(reward)
            reward = -reward
            node = node.getParent()

        