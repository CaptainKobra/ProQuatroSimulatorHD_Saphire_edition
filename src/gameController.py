import random
from gameView import GameView
from Shape import Shape
from StartWindow import StartWindow

class GameController(GameView.GameViewListener, StartWindow.Listener):
    def __init__(self) -> None:
        self.inTurn = False
        self.AIturn = False

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
        if(starter == "AI"):
            self.AIturn = True
        self.init()
        self.createShapes()
        self.gameView.drawSelectSurfaces()
        self.play()

    
    def play(self):
        """
        Boucle de jeu
        """
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
                self.gameView.quarto("YOU")
                self.gameView.end()
                self.start()
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
            self.gameView.AIselected(choice)
        else:
            print("choose a shape")
            self.selected = False
            while not self.selected:
                self.gameView.waitSelectEvent()
                

    def select(self, shape):
        self.currentShape = self.shapes[shape]
        if not self.alreadyTakenShape[shape]:
            self.alreadyTakenShape[shape] = True
            self.selected = True


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
            self.gameView.quarto("AI")
            self.gameView.end()
            self.start()
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
    