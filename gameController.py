from gameView import GameView
from Shape import Shape
from StartWindow import StartWindow
from State import State

from Players.HumanPlayer import HumanPlayer
from Players.MCTSAIPlayer import MCTSAIPlayer
from Players.MinMaxAIPlayer import MinMaxAIPlayer


class GameController(GameView.GameViewListener, StartWindow.Listener):
    def __init__(self) -> None:
        self.done = False


    def reset(self):
        """
        Reset the game
        """
        self.done = False
        self.start()


    def init(self):
        """
        Game initialization
        """
        self.gameView = GameView()
        self.shapes = []
        self.currentShape = None
        self.createShapes()
        self.alreadyTakenShape = [False for i in range(16)]
        self.board = [None for i in range(16)]
        """
        0   4   8   12  \n
        1   5   9   13  \n
        2   6   10  14  \n
        3   7   11  15
        """
        self.gameState = None
        self.gameView.drawSelectSurfaces(self)


    def createShapes(self):
        """
        Shpes initialization
        """
        (width, height) = self.gameView.getSizes()
        num = 0
        for size in ["little", "big"]:
            for color in ["red", "blue"]:
                for shape in ["circle", "rect"]:
                    for filled in [True, False]:
                        s = Shape(num, shape, color, size, filled, width, height)
                        self.shapes.append(s)
                        num += 1


    def start(self):
        """
        Appelle la fenêtre de départ
        """
        sw = StartWindow()
        sw.setListener(self)
        sw.run()


    def draw(self, surface, case:int):
        """
        Dessine la forme d'index "case" dans la surface "surface"
        """
        self.shapes[case].draw(surface)


    def selectPlayers(self, player1:str, player2:str):
        """
        Player initialization
        """
        self.init()

        if player1 == "human":
            self.player1 = HumanPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "player_1", self.done)
        elif player1 == "MCTS":
            self.player1 = MCTSAIPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "MCTS_1", self.done)
        elif player1 == "MinMax":
            self.player1 = MinMaxAIPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "MinMax_1", self.done)

        if player2 == "human":
            self.player2 = HumanPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "player_2", self.done)
        elif player2 == "MCTS":
            self.player2 = MCTSAIPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "MCTS_2", self.done)
        elif player2 == "MinMax":
            self.player2 = MinMaxAIPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "MinMax_2", self.done)

        self.gameState = State(shapes=self.shapes, previousSelectedShape=self.currentShape, turnLeft=16)
        self.player1.setGameState(self.gameState)
        self.player2.setGameState(self.gameState)

        self.play()

    
    def play(self):
        """
        Boucle de jeu
        """
        while True:
            self.player1.play()
            self.gameState.decrementTurnLeft()
            if self.player1.isDone(): break
            self.player2.play()
            self.gameState.decrementTurnLeft()
            if self.player2.isDone(): break
            self.gameView.refreshAll()
        self.reset()