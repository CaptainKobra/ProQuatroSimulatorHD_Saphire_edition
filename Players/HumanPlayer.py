from Players.Player import Player

from gameView import GameView
from Shape import Shape

class HumanPlayer(Player, GameView.GameViewListener):
    def __init__(self, gameView:GameView, currentShape:Shape, shapes:list, alreadyTakenShape:list, board:list, playerID:str, done:bool) -> None:
        super().__init__(gameView, currentShape, shapes, alreadyTakenShape, board, playerID, done)
        self.inTurn = False


    def play(self):
        self.currentShape = self.gameState.getPreviousSelectedShape()
        self.inTurn = True
        if(self.currentShape != None):
            self.playerChooseCase()
        if not self.done:
            self.playerChooseShape()
        super().play()
    

    def playerChooseCase(self):
        """
        Place the shape in the board
        """
        while(self.inTurn):
            self.gameView.waitEvent(self)
            if(self.gameState.quarto()):
                self.done = True


    def select(self, shape):
        """
        Hérité de gameView.Listener -> met à jour self.selected pour le playerChooseShape
        """
        self.currentShape = self.shapes[shape]
        if not self.alreadyTakenShape[shape]:
            self.alreadyTakenShape[shape] = True
            self.selected = True
            self.gameState.selectShape(shape)
    

    # Choose a shape for the ia
    def playerChooseShape(self):
        self.selected = False
        while not self.selected:
            self.gameView.waitSelectEvent(self)


    def mouseClick(self, surface, case):
        if(self.board[case] == None):
            self.currentShape.draw(surface)
            self.gameView.refresh(case)
            self.board[case] = self.currentShape
            self.inTurn = False
            self.gameState.selectPos(case)