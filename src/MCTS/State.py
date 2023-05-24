from Shape import Shape
import random
import copy

class State:
    def __init__(self, shapes:list=None, previousSelectedShape=None) -> None:
        self.endQuarto = False
        self.board = [None for i in range(16)]
        """
        0   1   2   3   \n
        4   5   6   7   \n
        8   9   10  11  \n
        12  13  14  15
        """
        self.availablePos = [i for i in range(16)]
        self.availableShapes = copy.deepcopy(shapes)
        #self.shapes = self.listToDict(self.availableShapes)
        #print(self.shapes)
        #print(self.availableShapes)
        #self.alreadyTakenShapes = [False for i in range(16)]
        self.previousSelectedShape = previousSelectedShape
    

    def getMaxNumberOfChilderen(self):
        return len(self.availablePos) * len(self.availableShapes)
    

    def getAllPossibleChilderen(self) -> list:
        allPossibleChilderen = []
        for pos in self.availablePos:
            for s in self.availableShapes:
                allPossibleChilderen.append((pos, s.getNum()))
        return allPossibleChilderen


    def createChild(self, child:tuple):
        if child == None:
            if not self.quasiTerminal():
                print("error in createChild")
                exit()
            else:
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
        if len(self.availablePos) > 0:
            pos = random.choice(self.availablePos)
            self.availablePos.remove(pos)
            self.board[pos] = self.previousSelectedShape
        else:
            pos = None
            #print(self.availablePos)
        return pos


    def randomSelectShape(self) -> Shape:
        if len(self.availableShapes) > 0:
            self.previousSelectedShape = random.choice(self.availableShapes)
            self.availableShapes.remove(self.previousSelectedShape)
        else:
            self.previousSelectedShape = None
        return self.previousSelectedShape
    

    def whyTerminal(self):
        if self.endQuarto:
            print("quarto")
        print("available pos = ", self.availablePos)
        sh = []
        for s in self.availableShapes:
            sh.append(s.getNum())
        print("available shapes = ", sh)


    def isTerminal(self) -> bool:
        if self.quarto():
            self.endQuarto = True
            terminal = True
        else:
            if len(self.availablePos) == 0:
                terminal = True
                #print(self.terminal)
            else:
                terminal = False
        return terminal
    

    def reward(self):
        if self.endQuarto:
            return 1
        else:
            return 0
        

    def randomAction(self):
        self.randomPlaceShapeOnBoard()
        self.randomSelectShape()


    def selectShape(self, s:int):
        #print("select Shape:", s)
        #print(self.shapes)
        #self.previousSelectedShape = self.shapes[s]
        for i in range(len(self.availableShapes)):
            #print(i, end=" ")
            num = self.availableShapes[i].getNum()
            if s == num:
                self.previousSelectedShape = self.availableShapes[i]
                self.availableShapes.pop(i)
                break
        #print(" s:", s)
        #print(self.availableShapes)


    def selectPos(self, pos:int):
        #print("select pos", pos)
        self.board[pos] = self.previousSelectedShape
        self.availablePos.remove(pos)
        #print(pos)
        #print(self.availablePos)


    def getPreviousSelectedShape(self):
        return self.previousSelectedShape
    

    def quasiTerminal(self):
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
        ## Write the winner at the end of the file
        #if(quarto):
        #    self.file.write(str(self.inTurn) + "\n")
        
        #if quarto : self.printBoard()
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
    


    def printBoard(self):
        print("BOARD:")
        for i, case in enumerate(self.board):
            print("case ", i, ":", end=" ")
            if case == None:
                print("None")
            else:
                case.print()


    def listToDict(self, liste:list):
        dico = {}
        for i in range(len(liste)):
            dico[i] = liste[i]
        return dico
