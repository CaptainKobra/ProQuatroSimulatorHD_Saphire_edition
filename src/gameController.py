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
            self.AIturn = True
        while True:
            self.chooseShape()
            self.inTurn = True
            if(not self.AIturn):
                self.AIChooseCase()
                self.AIturn = True
            else:
                print("Please, choose a void case in the game board")
                while(self.inTurn):
                    self.gameView.waitEvent()
                self.AIturn = False
            self.gameView.refreshAll()


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


    def chooseShape(self) -> Shape:
        if(self.AIturn):
            random.seed(None)
            choice = random.randint(0, 15)
            while (self.alreadyTakenShape[choice]):
                choice = random.randint(0, 15)
            self.alreadyTakenShape[choice] = True
            self.currentShape = self.shapes[choice]
            print("The AI has chosen for you the form:")
            self.currentShape.print()
        else:
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
        


    def quarto(self):
        # Check rows
        for i in range(4):
            pieces_in_row =  [self.board[i*4+j] for j in range(4) if self.board[i*4+j] is not None]
            if len(pieces_in_row) == 4 and self.has_common_property(pieces_in_row):
                return True
        # Check columns
        for i in range(4):
            pieces_in_col = [self.board[j*4+i] for j in range(4) if self.board[j*4+i] is not None]
            if len(pieces_in_col) == 4 and self.has_common_property(pieces_in_col):
                return True
        # Check diagonals
        pieces_in_diag = [self.board[i] for i in range(0,16,5) if self.board[i] is not None]
        if len(pieces_in_diag) == 4 and self.has_common_property(pieces_in_diag):
            return True
        pieces_in_diag = [self.board[i] for i in range(3, 13, 3) if self.board[i] is not None]
        if len(pieces_in_diag) == 4 and self.has_common_property(pieces_in_diag):
            return True
        return False
    
    def has_common_property(self, pieces):
        if(self.sameSize(pieces)):
            return True
        if(self.sameShape(pieces)):
            return True
        if(self.sameColor(pieces)):
            return True
        if(self.sameFilled(pieces)):
            return 
        return False
        
    def sameSize(self, pieces):
        size = pieces[0].getSize()
        for i in range(1,4):
            #print(size, "   ", pieces[i].getSize())
            if(pieces[i].getSize() != size):
                return False
        return 
    
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
    