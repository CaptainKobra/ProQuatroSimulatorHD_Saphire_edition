from Players.AIPlayer import AIPlayer

from gameView import GameView
from Shape import Shape

from MCTS.State import State
from MinMax.MinMaxTree import Tree

import random


class MinMaxAIPlayer(AIPlayer):
    def __init__(self, gameView:GameView, currentShape:Shape, shapes:list, alreadyTakenShape:list, board:list, playerID:str, done:bool) -> None:
        super().__init__(gameView, currentShape, shapes, alreadyTakenShape, board, playerID, done)


    def begin(self):
        super().begin()


    def play(self):
        #print("start turn of", self.playerID)
        #print("AD currentShape=", self.gameState.getPresiousSelectedShape().getNum())
        self.currentShape = self.gameState.getPreviousSelectedShape()
        if(self.currentShape != None):
            tree = Tree(self.gameState, True)
            tree.generateTree(2)
            winningLeafs = tree.getWinningLeafs()
            if len(winningLeafs) != 0:
                child = random.choice(winningLeafs)
            else:
                foundChildren = False
                for c in tree.getChilderen():
                    if not c.haveLoosingChild():
                        print("Child selected")
                        child = c
                        foundChildren = True
                        break
                if not foundChildren:
                    print("No non-losing child found")
                    child = random.choice(tree.getChilderen())

            position, shape = child.getAction()
            self.gameState.selectPos(pos=position)

            super().eraseSelectionCase()

            surface = self.gameView.getSurface(position)
            self.currentShape.draw(surface)
            self.gameView.refresh(position)
            self.board[position] = self.currentShape

            self.currentShape = shape
            if self.currentShape == None:
                super().equal()
                return
            index = self.currentShape.getNum()
            self.gameView.AIselected(index, self)
            self.gameState.selectShape(index)
            self.alreadyTakenShape[index] = True

        else:
            self.currentShape = super().begin()


        #print("end turn of", self.playerID)

        #print("AF currentShape=", self.gameState.getPresiousSelectedShape().getNum())