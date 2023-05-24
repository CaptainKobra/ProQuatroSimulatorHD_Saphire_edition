import random
from gameView import GameView
from Shape import Shape
from StartWindow import StartWindow
from gameState import gameState

from MCTS.UCT import UCT
from MCTS.State import State

from Players.HumanPlayer import HumanPlayer
from Players.MCTSAIPlayer import MCTSAIPlayer


class GameController(GameView.GameViewListener, StartWindow.Listener):
    def __init__(self) -> None:
        self.inTurn = False
        self.player1Turn = True
        self.done = False


    def reset(self):
        self.inTurn = False
        self.done = False
        self.start()


    def init(self):
        self.gameView = GameView()
        self.shapes = []
        self.currentShape = None
        self.createShapes()
        self.alreadyTakenShape = [False for i in range(16)]
        self.board = [None for i in range(16)]
        """
        0   1   2   3   \n
        4   5   6   7   \n
        8   9   10  11  \n
        12  13  14  15
        """
        #self.currentGameState = gameState(self.board, self.currentShape, self.alreadyTakenShape, self.shapes, self.inTurn)
        self.gameState = None
        self.gameView.drawSelectSurfaces(self)


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
        self.init()

        if player1 == "human":
            self.player1 = HumanPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "player_1", self.done)
        elif player1 == "MCTS":
            self.player1 = MCTSAIPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "MCTS_1", self.done)
        elif player1 == "MinMax":
            # TODO
            pass

        if player2 == "human":
            self.player2 = HumanPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "player_2", self.done)
        elif player2 == "MCTS":
            self.player2 = MCTSAIPlayer(self.gameView, self.currentShape, self.shapes, self.alreadyTakenShape, self.board, "MCTS_2", self.done)
        elif player2 == "MinMax":
            # TODO
            pass

        self.gameState = State(shapes=self.shapes, previousSelectedShape=self.currentShape)
        self.player1.setGameState(self.gameState)
        self.player2.setGameState(self.gameState)

        self.play()

    
    def play(self):
        """
        Boucle de jeu
        """
        while True:
            self.player1.play()
            #print("ctrl current shape=", self.gameState.getPresiousSelectedShape().getNum())
            if self.player1.isDone(): break
            self.player2.play()
            #print("ctrl current shape=", self.gameState.getPresiousSelectedShape().getNum())
            if self.player2.isDone(): break
            self.gameView.refreshAll()
        self.reset()
        

    def createShapes(self):
        (width, height) = self.gameView.getSizes()
        num = 0
        for size in ["little", "big"]:
            for color in ["red", "blue"]:
                for shape in ["circle", "rect"]:
                    for filled in [True, False]:
                        s = Shape(num, shape, color, size, filled, width, height)
                        self.shapes.append(s)
                        num += 1
        


"""
    def evaluation(self,board,playerTurn):
        if self.quarto(board):
            if playerTurn:
               return 10000
            else:
                return -10000
        else:
            if playerTurn:
                return self.connexion(board)
            else:
                return self.connexion(self.board)


    def connexion(self,board):
        score = 0
        score_row = 0
        score_col = 0
        score_diag = 0
        # Check rows
        for i in range(4):
            pieces = self.get_line(board,i)  
            score_row += (10**len(pieces))*self.common_properties_count(pieces)

        # Check columns
        for i in range(4):
            pieces = self.get_column(board,i)  
            score_col += (10**len(pieces))*self.common_properties_count(pieces)

        # Check diagonals
        pieces = self.get_diag_1(board)
        score_diag += (10**len(pieces))*self.common_properties_count(pieces)
        pieces = self.get_diag_2(board)
        score_diag += (10**len(pieces))*self.common_properties_count(pieces)
        #print("score_diag : ",score_diag," score_col : ",score_col," score_row : ",score_row," total : ",score_diag + score_col + score_row)
        return score_diag + score_col + score_row




    def common_properties_count(self, shapes):
        if len(shapes) == 0:
            return 0
        
        color_in_common = 1
        filled_in_common = 1
        shape_in_common = 1
        size_in_common = 1
        first_color = shapes[0].color
        first_filled = shapes[0].filled
        first_shape = shapes[0].shape
        first_size = shapes[0].size
        
        for shape in shapes:
            if shape.getColor() != first_color:
                color_in_common = 0
            if shape.getFilled() != first_filled:
                filled_in_common = 0
            if shape.getShape() != first_shape:
                shape_in_common = 0
            if shape.getSize() != first_size:
                size_in_common = 0
            
        return color_in_common + filled_in_common + shape_in_common + size_in_common
    
    def get_line(self,board,nb_line):
        line = []
        for i in range(4):
            if board[i+nb_line*4] is not None:
                line.append(board[i+nb_line*4])
        return line
    
    def get_column(self,board,nb_column):
        column = []
        for i in range(4):
            if board[i*4+nb_column] is not None:
                column.append(board[i*4+nb_column])
        return column
    
    def get_diag_1(self,board):
        diag = []
        for i in range(4):
            if board[i*5] is not None:
                diag.append(board[i*5])
        return diag

    def get_diag_2(self,board):
        diag = []
        for i in range(4):
            if board[i*3+3] is not None:
                diag.append(board[i*3+3])
        return diag    
    
    def updateCurrentGameState(self):
        self.currentGameState.board = self.board
        self.currentGameState.currentShape = self.currentShape
        self.currentGameState.alreadyTakenShape = self.alreadyTakenShape
        self.currentGameState.inTurn = self.inTurn
        self.currentGameState.childrens = []
        self.currentGameState.parent = None
        self.currentGameState.winningLeafs = []
        self.currentGameState.losingLeafs = []

"""
