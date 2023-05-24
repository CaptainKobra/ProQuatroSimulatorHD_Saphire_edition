from Players.Player import Player

from gameView import GameView
from Shape import Shape

import random


class AIPlayer(Player, GameView.GameViewListener):
    def __init__(self, gameView:GameView, currentShape:Shape, shapes:list, alreadyTakenShape:list, board:list, playerID:str, done:bool) -> None:
        super().__init__(gameView, currentShape, shapes, alreadyTakenShape, board, playerID, done)


    def begin(self):
        index = random.randint(0, len(self.shapes) - 1)
        self.currentShape = self.shapes[index]
        self.gameView.AIselected(index, self)
        self.alreadyTakenShape[index] = True
        self.gameState.selectShape(index)


    def play(self):
        return super().play()
    

    def draw(self, surface, case:int):
        """
        Dessine la forme d'index "case" dans la surface "surface"
        """
        self.shapes[case].draw(surface)