class gameState:

    def __init__(self, board, currentShape, alreadyTakenShape, shapes, inTurn, parent = None, childrens = []) -> None:
        self.parent = parent
        self.childrens = childrens
        self.board = board
        self.currentShape = currentShape
        self.inTurn = inTurn
        self.haveDescisivChild = False
        self.alreadyTakenShape = alreadyTakenShape
        self.shapes = shapes
        self.descisivLeafs = []



    def generateTree(self ,depth):
        """
        Generate the tree of possibilities for the current game state util a given depth
        """
        self.childrens = []
        self.haveLoosingChild = False
        self.loosingLeafs = []
        self.winningLeafs = []
        if depth >= 0:
            self.alreadyTakenShape[self.currentShape.num] = True
            boards =[]
            for i in range(16):
                if self.board[i] is None:
                    newBoard = self.board.copy()
                    newBoard[i] = self.currentShape
                    boards.append(newBoard)

            for board in boards:
                winFind = False
                for shapeIndice in range(len(self.alreadyTakenShape)-1):
                    if not self.alreadyTakenShape[shapeIndice]:
                        newCurrentShape = self.shapes[shapeIndice]
                        newAlreadyTakenShape = self.alreadyTakenShape.copy()
                        newAlreadyTakenShape[shapeIndice] = True
                        newInTurn = not self.inTurn
                        newGameState = gameState(board, newCurrentShape, newAlreadyTakenShape, self.shapes, newInTurn, self)

                        if self.quarto(board):
                            self.descisivLeafs.append(newGameState)
                            self.haveDescisivChild = True
                            if not self.inTurn:
                                # Stop if there is an immediate win 
                                winFind = True
                                break
                        else:
                            newGameState.generateTree(depth-1)
                            self.childrens.append(newGameState)
                if winFind:
                    break

                            

    def findPositionOnBoard(self, shapeNum):
        """
        Find the position of the piece on the board
        """
        for i in range(16):
            if self.board[i] != None:
                if self.board[i].num == shapeNum:
                    return i
        print("Piece not found on board")
        return None
        


    def quarto(self,board):
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




    
    

    
