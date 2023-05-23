import random
from gameView import GameView
from Shape import Shape
from StartWindow import StartWindow

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
            self.AIplay()
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

    """
    def AIplay(self):
        if(self.currentShape != None):
            self.AIChooseCase()

        # Choose a shape for the player
        if not self.done:
            self.AIChooseshape()

    # The ia place a shape in the board
    def AIChooseCase(self):
        choice = random.randint(0, 15)
        while(self.board[choice] != None):
            choice = random.randint(0, 15)
        surface = self.gameView.getSurface(choice)
        self.currentShape.draw(surface)
        self.board[choice] = self.currentShape
        self.gameView.refresh(choice)
        if(self.quarto(self.board)):
            #print("QUARTO! AI win the game")
            self.gameView.quarto("AI")
            #self.gameView.end()
            self.done = True
        self.inTurn = False
        print(self.evaluation(self.board, self.inTurn))


    # Choose a shape for the player
    def AIChooseshape(self):
        random.seed(None)
        choice = random.randint(0, 15)
        while (self.alreadyTakenShape[choice]):
            choice = random.randint(0, 15)
        self.alreadyTakenShape[choice] = True
        self.currentShape = self.shapes[choice]
        #print("The AI has chosen for you the form:")
        #self.currentShape.print()
        self.gameView.AIselected(choice)
    """

    def AIplay(self):
        if self.currentShape is not None:
            self.AIChooseCase()

        # Choose a shape for the player
        if not self.done:
            self.AIChooseshape()

    # The AI places a shape on the board
    def AIChooseCase(self):
        best_score = float("-inf")
        best_choice = None

        for choice in range(16):
            if self.board[choice] is None:
                self.board[choice] = self.currentShape
                score = self.minimax(self.board, False, 3, True) 
                self.board[choice] = None

                if score > best_score:
                    best_score = score
                    best_choice = choice

        surface = self.gameView.getSurface(best_choice)
        self.currentShape.draw(surface)
        self.board[best_choice] = self.currentShape
        self.gameView.refresh(best_choice)

        if self.quarto(self.board):
            self.gameView.quarto("AI")
            self.done = True

        self.inTurn = False

    def minimax(self, board, is_maximizing, depth, playerTurn):
        if self.quarto(board):
            return 10000
        elif self.is_board_full(board):
            return 0
        elif depth == 0:
            return self.evaluation(board, is_maximizing)

        if is_maximizing:
            best_score = float("-inf")

            for choice in range(16):
                if board[choice] is None:
                    board[choice] = self.currentShape
                    score = self.minimax(board, False, depth - 1, not playerTurn)  # Pour le joueur non-maximisant
                    board[choice] = None
                    best_score = max(best_score, score)

            return best_score
        else:
            best_score = float("inf")

            for choice in range(16):
                if board[choice] is None:
                    board[choice] = self.get_next_shape()
                    score = self.minimax(board, True, depth - 1, not playerTurn)  # Pour le joueur maximisant
                    board[choice] = None
                    best_score = min(best_score, score)

            return best_score


        # Choose a shape for the player
    # Choose a shape for the player
    def AIChooseshape(self):
        best_score = float("-inf")
        best_choice = None

        for choice in range(16):
            if not self.alreadyTakenShape[choice]:
                self.alreadyTakenShape[choice] = True
                self.currentShape = self.shapes[choice]
                score = self.minimax(self.board, True, 3, True)
                self.alreadyTakenShape[choice] = False

                if score > best_score:
                    best_score = score
                    best_choice = choice

        self.alreadyTakenShape[best_choice] = True
        self.currentShape = self.shapes[best_choice]
        self.gameView.AIselected(best_choice)

    # Turn of the player
    def PlayerPlay(self):
        self.inTurn = True
        if(self.currentShape != None):
            self.playerChooseCase()
        if not self.done:
            self.playerChooseShape()
        self.inTurn = False

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




    def select(self, shape):
        """
        Hérité de gameView.Listener -> met à jour self.selected pour le playerChooseShape
        """
        self.currentShape = self.shapes[shape]
        if not self.alreadyTakenShape[shape]:
            self.alreadyTakenShape[shape] = True
            self.selected = True
    

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
            pieces_in_row =  [self.board[i*4+j] for j in range(4) if self.board[i*4+j] is not None]
            if len(pieces_in_row) == 4 and self.has_common_property(pieces_in_row):
                quarto = True
        # Check columns
        for i in range(4):
            pieces_in_col = [self.board[j*4+i] for j in range(4) if self.board[j*4+i] is not None]
            if len(pieces_in_col) == 4 and self.has_common_property(pieces_in_col):
                quarto = True
        # Check diagonals
        pieces_in_diag = [self.board[i] for i in range(0,16,5) if self.board[i] is not None]
        if len(pieces_in_diag) == 4 and self.has_common_property(pieces_in_diag):
            quarto = True
        pieces_in_diag = [self.board[i] for i in range(3, 13, 3) if self.board[i] is not None]
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
                return 1000
            else:
                return -1000
        else:
            if playerTurn:
                return self.connexion(board)  # Score positif pour le joueur maximisant
            else:
                return -1*self.connexion(board)  # Score négatif pour le joueur non-maximisant


    def connexion(self,board):
        score = 0

        # Check rows
        for i in range(4):
            pieces = self.get_line(board,i)  
            score += (10**len(pieces))*self.common_properties_count(pieces)

        # Check columns
        for i in range(4):
            pieces = self.get_column(board,i)  
            score += (10**len(pieces))*self.common_properties_count(pieces)

        # Check diagonals
        pieces = self.get_diag_1(board)
        score += (10**len(pieces))*self.common_properties_count(pieces)
        pieces = self.get_diag_2(board)
        score += (10**len(pieces))*self.common_properties_count(pieces)
        return score

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
    
    def is_board_full(self,board):
        for i in range(16):
            if board[i] is None:
                return False
        return True 
    
    def get_next_shape(self):
        for shape in self.shapes:
            if not self.alreadyTakenShape[shape.num]:
                return shape
        return None
