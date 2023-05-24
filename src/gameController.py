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
        self.turnsLeft = 16


    def reset(self):
        self.inTurn = False
        self.AIturn = False
        self.done = False
        self.turnsLeft = 16
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
        """
        Ai turn where it temporise until turn 11 and then calculate the full tree and play the bests moves
        """
        if self.turnsLeft > 5: # play saflly
            print("AI turn")
            self.currentGameState.generateTree(1)
            currentShapeNum = self.currentGameState.currentShape.num
            print("Tree generated")
            # Select a random child of the root
            if len(self.currentGameState.descisivLeafs) != 0:
                self.currentGameState = self.currentGameState.descisivLeafs[0]
            else:
                self.currentGameState = self.bestChildToTemporise(self.currentGameState.childrens)
        else: #go minmax
            print("AI turn")
            self.currentGameState.generateTree(self.turnsLeft)
            currentShapeNum = self.currentGameState.currentShape.num
            print("Tree generated")
            # Analyse l'arbre qui va jusqu'a la fin de la partie
            self.currentGameState = self.minmax(self.currentGameState)

        # Refresh the gameView
        currentShapePosition = self.currentGameState.findPositionOnBoard(currentShapeNum)
        self.printBoard(self.currentGameState.board)
        surface = self.gameView.getSurface(currentShapePosition)
        self.currentGameState.shapes[currentShapeNum].draw(surface)
        self.gameView.refresh(currentShapePosition)
        self.gameView.AIselected(currentShapePosition)
        self.currentGameState.inTurn = self.currentGameState.inTurn

        # Check if the game is over
        if self.quarto(self.currentGameState.board):
            self.gameView.quarto("AI")
            self.done = True
        self.currentGameState.inTurn = False


    def bestChildToTemporise(self, childrens):
        """
        Retourne le meilleur enfant de la liste d'enfants "childrens"
        """
        bestChild = childrens[0]
        bestChildvalue = self.connexion(bestChild.board)
        bestChildFound = False
        for child in childrens:
            if self.connexion(child.board) > bestChildvalue and (not child.haveDescisivChild):
                bestChild = child
                bestChildvalue = self.connexion(child.board)
                bestChildFound = True
        if not bestChildFound:
            for child in childrens:
                if self.connexion(child.board) > bestChildvalue:
                    bestChild = child
                    bestChildvalue = self.connexion(child.board)

        return bestChild

    def minmax(self, gameState):
        for child in gameState.childrens:
            self.generateMinMaxValues(child)
        bestChild = gameState.childrens[0]
        bestChildvalue = gameState.childrens[0].MinMaxValue
        for child in gameState.childrens:
            if child.MinMaxValue > bestChildvalue:
                bestChild = child
                bestChildvalue = child.MinMaxValue
        return bestChild

    def generateMinMaxValues(self, gameState):
        if gameState.childrens == []:
            if not gameState.haveDescisivChild:
                return 0
            elif gameState.inTurn:
                return 1
            else:
                return -1
        else:
            for child in gameState.childrens:
                gameState.MinMaxValue += self.generateMinMaxValues(child)
            
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
        

    def evaluation(self,board):
        if self.quarto(board):
            return 1000000
        else:
            return( -1 * self.connexion(self.currentGameState.board))


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
        return -(score_diag + score_col + score_row)


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




    
