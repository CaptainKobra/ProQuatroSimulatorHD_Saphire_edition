import random
from gameView import GameView
from Shape import Shape
from StartWindow import StartWindow
from gameState import gameState

class GameController(GameView.GameViewListener, StartWindow.Listener):
    def __init__(self) -> None:
        self.inTurn = False
        self.AIturn = False
        self.done = False


    def reset(self):
        self.inTurn = False
        self.AIturn = False
        self.done = False
        self.start()


    def init(self):
        self.gameView = GameView()
        self.gameView.setListener(self)
        self.shapes = []
        self.currentShape = None
        self.alreadyTakenShape = [False for i in range(16)]
        self.board = [None for i in range(16)]
        """
        0   1   2   3   \n
        4   5   6   7   \n
        8   9   10  11  \n
        12  13  14  15
        """
        self.currentGameState = gameState(self.board, self.currentShape, self.alreadyTakenShape, self.shapes, self.inTurn)


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


    def selectStarter(self, starter: str):

        """
        Sélectionne le joueur qui commence (l'utilisateur ou l'IA)
        """
        self.init()
        self.createShapes()
        self.gameView.drawSelectSurfaces()

        if(starter == "AI"):
            #Choose randomly a current shape
            self.currentShape = self.shapes[random.randint(0, len(self.shapes) - 1)]
            self.gameView.AIselected(self.shapes.index(self.currentShape))
            self.alreadyTakenShape[self.shapes.index(self.currentShape)] = True

        self.play()

    
    def play(self):
        """
        Boucle de jeu
        """
        while not self.done:
            self.PlayerPlay()
            if self.done: break
            self.AIplay()
            if self.done: break
            self.gameView.refreshAll()
        self.reset()


    def AIplay(self):

        print("AI turn")
        self.currentGameState.generateTree(1)
        print("Tree generated")
        # Select a random child of the root
        if self.currentGameState.winningLeafs != []:
            self.currentGameState = self.currentGameState.winningLeafs[0]
        else:
            self.currentGameState = self.currentGameState.childrens[random.randint(0, len(self.currentGameState.childrens) - 1)]
        # get the position of the current shape on the new board
        self.board = self.currentGameState.board
        currentShapePosition = self.board.index(self.currentShape)
        surface = self.gameView.getSurface(currentShapePosition)
        self.currentShape.draw(surface)
        self.gameView.refresh(currentShapePosition)
        self.alreadyTakenShape = self.curr
        self.currentShape = self.currentGameState.currentShape
        self.alreadyTakenShape = self.currentGameState.alreadyTakenShape
        self.gameView.AIselected(self.shapes.index(self.currentShape))
        self.inTurn = self.currentGameState.inTurn

        if self.quarto(self.board):
            self.gameView.quarto("AI")
            self.done = True
        self.inTurn = False
        print(self.evaluation(self.board, self.inTurn))
        

    # Turn of the player
    def PlayerPlay(self):
        self.inTurn = True
        if(self.currentShape != None):
            self.playerChooseCase()
        if not self.done:
            self.playerChooseShape()
        self.inTurn = False
        self.updateCurrentGameState()

    # Place the shape in the board
    def playerChooseCase(self):
        #print("Please, choose a void case in the game board")
        while(self.inTurn):
            self.gameView.waitEvent()
            if(self.quarto(self.board)):
                #print("QUARTO! You win the game")
                self.gameView.quarto("YOU")
                #self.gameView.end()
                self.done = True
        
        print(self.evaluation(self.board, self.inTurn))

        
        print(self.evaluation(self.board, self.inTurn))


    def select(self, shape):
        """
        Hérité de gameView.Listener -> met à jour self.selected pour le playerChooseShape
        """
        self.currentShape = self.shapes[shape]
        if not self.alreadyTakenShape[shape]:
            self.alreadyTakenShape[shape] = True
            self.selected = True
    

    # Choose a shape for the ia
    def playerChooseShape(self):
        #print("choose a shape")
        self.selected = False
        while not self.selected:
            self.gameView.waitSelectEvent()


    def mouseClick(self, surface, case):
        if(self.board[case] == None):
            self.currentShape.draw(surface)
            self.gameView.refresh(case)
            self.board[case] = self.currentShape
            self.inTurn = False
        else:
            pass
            #print("Choose an other case")
        

    def createShapes(self):
        (width, height) = self.gameView.getSizes()
        num = 1
        for size in ["little", "big"]:
            for color in ["red", "blue"]:
                for shape in ["circle", "rect"]:
                    for filled in [True, False]:
                        s = Shape(num, shape, color, size, filled, width, height)
                        self.shapes.append(s)
                        num += 1
        

    def quarto(self, board):
        quarto = False
        # Check rows
        for i in range(4):
            pieces_in_row =  [board[i*4+j] for j in range(4) if board[i*4+j] is not None]
            if len(pieces_in_row) == 4 and self.has_common_property(pieces_in_row):
                quarto = True
        # Check columns
        for i in range(4):
            pieces_in_col = [board[j*4+i] for j in range(4) if board[j*4+i] is not None]
            if len(pieces_in_col) == 4 and self.has_common_property(pieces_in_col):
                quarto = True
        # Check diagonals
        pieces_in_diag = [board[i] for i in range(0,16,5) if board[i] is not None]
        if len(pieces_in_diag) == 4 and self.has_common_property(pieces_in_diag):
            quarto = True
        pieces_in_diag = [board[i] for i in range(3, 13, 3) if board[i] is not None]
        if len(pieces_in_diag) == 4 and self.has_common_property(pieces_in_diag):
            quarto = True

        return quarto
    

    def has_common_property(self, pieces):
        return self.sameSize(pieces) + self.sameShape(pieces) + self.sameColor(pieces) + self.sameFilled(pieces)


    def sameSize(self, pieces):
        size = pieces[0].getSize()
        for i in range(1,len(pieces)):
            #print(size, "   ", pieces[i].getSize())
            if(pieces[i].getSize() != size):
                return False
        return True
    

    def sameShape(self, pieces):
        shape = pieces[0].getShape()
        for i in range(1,len(pieces)):

            #print(shape, "   ", pieces[i].getShape())
            if(pieces[i].getShape() != shape):
                return 0
        return 1

    

    def sameColor(self, pieces):
        color = pieces[0].getColor()
        for i in range(1,len(pieces)):
            #print(color, "   ", pieces[i].getColor())
            if(pieces[i].getColor() != color):
                return 0
        return 1

    

    def sameFilled(self, pieces):
        filled = pieces[0].getFilled()
        for i in range(1,len(pieces)):
            #print(filled, "   ", pieces[i].getFilled())
            if(pieces[i].getFilled() != filled):
                return 0
        return 1
        

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
        print("score_diag : ",score_diag," score_col : ",score_col," score_row : ",score_row," total : ",score_diag + score_col + score_row)
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
        self.currentGameState.parent = None




    
