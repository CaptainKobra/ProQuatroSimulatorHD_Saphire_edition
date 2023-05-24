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
        shapes = []
        currentShape = None
        alreadyTakenShape = [False for i in range(16)]
        board = [None for i in range(16)]
        """
        0   1   2   3   \n
        4   5   6   7   \n
        8   9   10  11  \n
        12  13  14  15
        """
        self.currentGameState = gameState(board, currentShape, alreadyTakenShape, shapes, self.inTurn)


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
        self.currentGameState.shapes[case].draw(surface)


    def selectStarter(self, starter: str):

        """
        Sélectionne le joueur qui commence (l'utilisateur ou l'IA)
        """
        self.init()
        self.createShapes()
        self.gameView.drawSelectSurfaces()

        if(starter == "AI"):
            #Choose randomly a current shape
            self.currentGameState.currentShape = self.currentGameState.shapes[0]
            self.gameView.AIselected(self.currentGameState.shapes.index(self.currentGameState.currentShape))
            self.currentGameState.alreadyTakenShape[self.currentGameState.currentShape.num] = True

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
        currentShapeNum = self.currentGameState.currentShape.num
        print("Tree generated")
        # Select a random child of the root
        if len(self.currentGameState.winningLeafs) != 0:
            self.currentGameState = self.currentGameState.winningLeafs[0]
        else:
            foundChildren = False
            for child in self.currentGameState.childrens:
                if not child.haveLoosingChild:
                    print("Child selected")
                    self.currentGameState = child
                    foundChildren = True
                    break
            if not foundChildren:
                print("No non-losing child found")
                self.currentGameState = self.currentGameState.childrens[0]

        # get the position of the current shape on the new board
        currentShapePosition = self.currentGameState.findPositionOnBoard(currentShapeNum)
        print(currentShapeNum)
        print(currentShapePosition)
        self.printBoard(self.currentGameState.board)
        surface = self.gameView.getSurface(currentShapePosition)
        self.currentGameState.shapes[currentShapeNum].draw(surface)
        self.gameView.refresh(currentShapePosition)
        self.gameView.AIselected(currentShapePosition)
        self.currentGameState.inTurn = self.currentGameState.inTurn

        if self.quarto(self.currentGameState.board):
            self.gameView.quarto("AI")
            self.done = True
        self.currentGameState.inTurn = False


    # Turn of the player
    def PlayerPlay(self):
        self.currentGameState.inTurn = True
        if(self.currentGameState.currentShape != None):
            self.playerChooseCase()
        if not self.done:
            self.playerChooseShape()
        self.currentGameState.inTurn = False
        self.updateCurrentGameState()
        self.printBoard(self.currentGameState.board)


    # Place the shape in the board
    def playerChooseCase(self):
        #print("Please, choose a void case in the game board")
        while(self.currentGameState.inTurn):
            self.gameView.waitEvent()
            if(self.quarto(self.currentGameState.board)):
                #print("QUARTO! You win the game")
                self.gameView.quarto("YOU")
                #self.gameView.end()
                self.done = True

    def printBoard(self,board):
        print(self.getNumFromBoard(board,0) + "   " + self.getNumFromBoard(board,1) + "   " + self.getNumFromBoard(board,2) + "   " + self.getNumFromBoard(board,3))
        print(self.getNumFromBoard(board,4) + "   " + self.getNumFromBoard(board,5) + "   " + self.getNumFromBoard(board,6) + "   " + self.getNumFromBoard(board,7))
        print(self.getNumFromBoard(board,8) + "   " + self.getNumFromBoard(board,9) + "   " + self.getNumFromBoard(board,10) + "   " + self.getNumFromBoard(board,11))
        print(self.getNumFromBoard(board,12) + "   " + self.getNumFromBoard(board,13) + "   " + self.getNumFromBoard(board,14) + "   " + self.getNumFromBoard(board,15))


    def getNumFromBoard(self, board, indice):
        if board[indice] == None:
            return "*"
        else:
            return str(board[indice].num)

    def select(self, shape):
        """
        Hérité de gameView.Listener -> met à jour self.selected pour le playerChooseShape
        """
        self.currentGameState.currentShape = self.currentGameState.shapes[shape]
        if not self.currentGameState.alreadyTakenShape[shape]:
            self.currentGameState.alreadyTakenShape[shape] = True
            self.selected = True
    

    # Choose a shape for the ia
    def playerChooseShape(self):
        #print("choose a shape")
        self.selected = False
        while not self.selected:
            self.gameView.waitSelectEvent()


    def mouseClick(self, surface, case):
        if(self.currentGameState.board[case] == None):
            self.currentGameState.currentShape.draw(surface)
            self.gameView.refresh(case)
            self.currentGameState.board[case] = self.currentGameState.currentShape
            self.currentGameState.inTurn = False
        else:
            pass
            #print("Choose another case")
        

    def createShapes(self):
        (width, height) = self.gameView.getSizes()
        num = 0
        for size in ["little", "big"]:
            for color in ["red", "blue"]:
                for shape in ["circle", "rect"]:
                    for filled in [True, False]:
                        s = Shape(num, shape, color, size, filled, width, height)
                        self.currentGameState.shapes.append(s)
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
                return self.connexion(self.currentGameState.board)


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
        self.currentGameState.board = self.currentGameState.board
        self.currentGameState.currentShape = self.currentGameState.currentShape
        self.currentGameState.alreadyTakenShape = self.currentGameState.alreadyTakenShape
        self.currentGameState.inTurn = self.currentGameState.inTurn
        self.currentGameState.parent = None




    
