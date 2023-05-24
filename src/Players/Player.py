from gameView import GameView
from Shape import Shape

from MCTS.State import State

class Player:
    def __init__(self, gameView:GameView, currentShape:Shape, shapes:list, alreadyTakenShape:list, board:list, playerID:str, done:bool) -> None:
        self.gameView = gameView
        self.currentShape = currentShape
        self.shapes = shapes
        self.alreadyTakenShape = alreadyTakenShape
        self.board = board
        self.playerID = playerID
        self.gameState = None
        self.done = done

    
    def setGameState(self, state:State):
        self.gameState = state


    def play(self):
        # etat du jeu
        self.gameState.printBoard()
        if self.gameState.quarto():
            self.gameView.quarto(self.playerID)
            self.done = True