import random
from gameView import GameView
from Shape import Shape

class GameController(GameView.GameViewListener):
    def __init__(self) -> None:
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
        self.inTurn = False
        self.AIturn = False

    def play(self):

        print("Who starts? AI or You?")
        starter = str(input("(Enter me if you want start, AI otherwise) "))
        while(starter != "AI" and starter != "me"):
            starter = str(input("Please, enter a right answer. (me if you want start, AI otherwise) "))

        if(starter == "AI"):
            self.AIplay()

        while True:
            self.PlayerPlay()
            self.AIplay()
            self.gameView.refreshAll()


    def AIplay(self):
        if(self.currentShape != None):
            self.AIChooseCase()

        # Choose a shape for the player
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
        if(self.quarto()):
            print("QUARTO! AI win the game")
            self.gameView.end()
        self.inTurn = False

    # Choose a shape for the player
    def AIChooseshape(self):
        random.seed(None)
        choice = random.randint(0, 15)
        while (self.alreadyTakenShape[choice]):
            choice = random.randint(0, 15)
        self.alreadyTakenShape[choice] = True
        self.currentShape = self.shapes[choice]
        print("The AI has chosen for you the form:")
        self.currentShape.print()

    # Turn of the player
    def PlayerPlay(self):
        self.inTurn = True
        if(self.currentShape != None):
            self.playerChooseCase()
        self.playerChooseShape()
        self.inTurn = False

    # Place the shape in the board
    def playerChooseCase(self):
        print("Please, choose a void case in the game board")
        while(self.inTurn):
            self.gameView.waitEvent()

    # Choose a shape for the ia
    def playerChooseShape(self):
        print("Available shapes:")
        for i in range(len(self.shapes)):
            if(not self.alreadyTakenShape[i]):
                self.shapes[i].print()
        choice = int(input("Please, enter the number of the form that you choose: "))
        while (choice < 0 or choice > 17):
            choice = int(input("Please, enter a right number: "))
        while (self.alreadyTakenShape[choice-1]):
            choice = int(input("Please, enter a right number: "))
        self.alreadyTakenShape[choice-1] = True
        self.currentShape = self.shapes[choice-1]

    def mouseClick(self, surface, case):
        if(self.board[case] == None):
            self.currentShape.draw(surface)
            self.gameView.refresh(case)
            self.board[case] = self.currentShape
            if(self.quarto()):
                print("QUARTO! You win the game")
                self.gameView.end()
            self.inTurn = False
        else:
            print("Choose an other case")
        

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


    def quarto(self):
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
        ## Write the winner at the end of the file
        #if(quarto):
        #    self.file.write(str(self.inTurn) + "\n")

        return quarto
    

    def has_common_property(self, pieces):
        if(self.sameSize(pieces)):
            return True
        if(self.sameShape(pieces)):
            return True
        if(self.sameColor(pieces)):
            return True
        if(self.sameFilled(pieces)):
            return True
        return False


    def sameSize(self, pieces):
        size = pieces[0].getSize()
        for i in range(1,4):
            #print(size, "   ", pieces[i].getSize())
            if(pieces[i].getSize() != size):
                return False
        return True
    

    def sameShape(self, pieces):
        shape = pieces[0].getShape()
        for i in range(1,4):
            #print(shape, "   ", pieces[i].getShape())
            if(pieces[i].getShape() != shape):
                return False
        return True
    

    def sameColor(self, pieces):
        color = pieces[0].getColor()
        for i in range(1,4):
            #print(color, "   ", pieces[i].getColor())
            if(pieces[i].getColor() != color):
                return False
        return True
    

    def sameFilled(self, pieces):
        filled = pieces[0].getFilled()
        for i in range(1,4):
            #print(filled, "   ", pieces[i].getFilled())
            if(pieces[i].getFilled() != filled):
                return False
        return True
    
    # Write the current state of the game in a csv file
    def writeGameStateInCSV(self):
        # Write the state of the board
        for case in self.board:
            if case == None:
                self.file.write("0,")
            else:
                self.file.write(case.num + ",")
        # Write the one who is playing
        if self.inTurn:
            self.file.write("A,") 