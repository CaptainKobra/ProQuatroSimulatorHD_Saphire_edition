from gameView import GameView
from Shape import Shape

from State import State

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


    def eraseSelectionCase(self):
        self.gameView.eraseSelectionCase()


    def play(self):
        # state of game
        if self.gameState.quarto():
            self.gameView.quarto(self.playerID)
            self.done = True
        elif self.gameState.isTerminal():
            self.equal()

    def equal(self):
        self.gameView.equal()
        self.done = True


    def isDone(self) -> bool:
        return self.done