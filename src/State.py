from Shape import Shape
import random
import copy

class State:
    def __init__(self, shapes:list=None, previousSelectedShape:Shape=None, turnLeft:int=None) -> None:
        self.endQuarto = False
        self.board = [None for i in range(16)]
        """
        0   4   8   12  \n
        1   5   9   13  \n
        2   6   10  14  \n
        3   7   11  15
        """
        self.availablePos = [i for i in range(16)]
        self.availableShapes = copy.deepcopy(shapes)
        self.previousSelectedShape = previousSelectedShape
        self.turnLeft = turnLeft
    

    def decrementTurnLeft(self):
        if self.turnLeft != None:
            self.turnLeft -= 1


    def getTurnLeft(self) -> int:
        return self.turnLeft


    def getBoard(self):
        return self.board


    def getMaxNumberOfChildren(self):
        """
        Return the maximum number of children for this state
        """
        return len(self.availablePos) * len(self.availableShapes)
    

    def getAllPossibleChildren(self) -> list:
        """
        Return the list of all possible children for this state
        """
        allPossibleChildren = []
        for pos in self.availablePos:
            for s in self.availableShapes:
                allPossibleChildren.append((pos, s.getNum()))
        return allPossibleChildren


    def createChild(self, child:tuple):
        """
        Update the state to obtain a child of the previous state
        """
        if child == None:
            if self.quasiTerminal():
                pos = self.availablePos.pop()
                self.previousSelectedShape = None
        else:
            pos = child[0]
            self.availablePos.remove(child[0])
            self.board[pos] = self.previousSelectedShape
            for i, s in enumerate(self.availableShapes):
                if child[1] == s.getNum():
                    self.previousSelectedShape = self.availableShapes.pop(i)
                    break
        return pos, self.previousSelectedShape


    def randomPlaceShapeOnBoard(self) -> int:
        """
        Place the previous selected shape on the board in an random selected available position
        """
        if len(self.availablePos) > 0:
            pos = random.choice(self.availablePos)
            self.availablePos.remove(pos)
            self.board[pos] = self.previousSelectedShape
        else:
            pos = None
        return pos


    def randomSelectShape(self) -> Shape:
        """
        Select randomly a niew current shape among the availables shape
        """
        if len(self.availableShapes) > 0:
            self.previousSelectedShape = random.choice(self.availableShapes)
            self.availableShapes.remove(self.previousSelectedShape)
        else:
            self.previousSelectedShape = None
        return self.previousSelectedShape


    def isTerminal(self) -> bool:
        """
        Return True if the state is Terminal, False otherwise
        """
        if self.quarto():
            self.endQuarto = True
            terminal = True
        else:
            if len(self.availablePos) == 0:
                terminal = True
            else:
                terminal = False
        return terminal
    

    def reward(self):
        """
        Return the reward associated to the state
        """
        if self.endQuarto:
            return 1
        else:
            return 0
        

    def randomAction(self):
        """
        Make a random action
        """
        self.randomPlaceShapeOnBoard()
        self.randomSelectShape()


    def selectShape(self, s:int):
        """
        Select the shape s
        """
        for i in range(len(self.availableShapes)):
            num = self.availableShapes[i].getNum()
            if s == num:
                self.previousSelectedShape = self.availableShapes[i]
                self.availableShapes.pop(i)
                break


    def selectPos(self, pos:int):
        """
        Place the previous selected shape at position pos on the board
        """
        self.board[pos] = self.previousSelectedShape
        self.availablePos.remove(pos)


    def getPreviousSelectedShape(self) -> Shape:
        """
        Return the previous selected shape (= current shape for the gameState)
        """
        return self.previousSelectedShape
    

    def quasiTerminal(self) -> bool:
        """
        Return true if the state is quasi terminal, False otherwise
        """
        return len(self.availablePos) == 1 and len(self.availableShapes) == 0


    def quarto(self) -> bool:
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
            if(pieces[i].getSize() != size):
                return False
        return True
    

    def sameShape(self, pieces):
        shape = pieces[0].getShape()
        for i in range(1,4):
            if(pieces[i].getShape() != shape):
                return False
        return True
    

    def sameColor(self, pieces):
        color = pieces[0].getColor()
        for i in range(1,4):
            if(pieces[i].getColor() != color):
                return False
        return True
    

    def sameFilled(self, pieces):
        filled = pieces[0].getFilled()
        for i in range(1,4):
            if(pieces[i].getFilled() != filled):
                return False
        return True