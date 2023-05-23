from Shape import Shape

class State:
    def __init__(self, shapes=None, state=None) -> None:
        if state == None:
            self.board = [None for i in range(16)]
            """
            0   1   2   3   \n
            4   5   6   7   \n
            8   9   10  11  \n
            12  13  14  15
            """

            self.shapes = shapes
            self.alreadyTakenShapes = [False for i in range(16)]
        else:
            self.board, self.shapes, self.alreadyTakenShapes = state.getState()


    def getState(self):
        return self.board, self.shapes, self.alreadyTakenShapes
    

    def placeShapeOnBoard(self, shape:int, pos:int) -> bool:
        if not self.alreadyTakenShapes[shape] and self.board[pos] == None:
            self.alreadyTakenShapes[shape] = True
            self.board[pos] = self.shapes[shape]
            return True
        return False


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
        for i, case in enumerate(self.board):
            print("case ", i, ":", end=" ")
            if case == None:
                print("None")
            else:
                case.print()