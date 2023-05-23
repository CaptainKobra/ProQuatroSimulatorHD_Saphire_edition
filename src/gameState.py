class gameState:

    def __init__(self, board, currentShape, alreadyTakenShape, shapes, inTurn, parent = None, childrens = []) -> None:
        self.parent = parent
        self.childrens = childrens
        self.board = board
        self.currentShape = currentShape
        self.inTurn = inTurn
        self.haveLoosingChild = None
        self.alreadyTakenShape = alreadyTakenShape
        self.shapes = shapes
        self.loosingLeafs = []
        self.winningLeafs = []


    def generateTree(self ,depth, force = False):
        """
        Generate the tree of possibilities for the current game state util a given depth
        The parameter force is used to force the generation of the tree even if a win or a lose is found
        to avoid the case where there are no other options than loosing
        """
        if depth >= 0:
            if self.childrens == []:
                boards =[]
                for i in range(16):
                    if self.board[i] is None:
                        newBoard = self.board.copy()
                        newBoard[i] = self.currentShape
                        boards.append(newBoard)

                index = self.shapes.index(self.currentShape)
                newAlreadyTakenShape = self.alreadyTakenShape.copy()
                newAlreadyTakenShape[index] = True

                for board in boards:
                    if self.quarto(board):
                        if self.inTurn:
                            # get the indices of the current shape in shapes
                            index = self.shapes.index(self.currentShape)
                            newAlreadyTakenShape = self.alreadyTakenShape.copy()
                            newAlreadyTakenShape[index] = True
                            newInTurn = not self.inTurn
                            newGameState = gameState(board, newAlreadyTakenShape, self.shapes, newInTurn, self)
                            newGameState.haveLoosingChild = "win"
                            self.winningLeafs.append(newGameState)
                            boards.remove(board)
                            # Break because if we find a win we don't need to check the other boards
                            # since we will always choose the winning one if we can reach the parent node
                            break

                        else:
                            # get the indices of the current shape in shapes
                            index = self.shapes.index(self.currentShape)
                            newAlreadyTakenShape = self.alreadyTakenShape.copy()
                            newAlreadyTakenShape[index] = True
                            newInTurn = not self.inTurn
                            newGameState = gameState(board, newAlreadyTakenShape, self.shapes, newInTurn, self)
                            self.haveLoosingChild = True
                            self.loosingLeafs.append(newGameState)
                            boards.remove(board)
                            if not force:
                                self.haveLoosingChild = "lose"
                                break
                                
                for board in boards:
                    for shapeIndice in newAlreadyTakenShape:
                        if not shapeIndice:
                            # get the indices of the current shape in shapes
                            index = self.shapes.index(self.currentShape)
                            newAlreadyTakenShape = self.alreadyTakenShape.copy()
                            newAlreadyTakenShape[index] = True
                            newInTurn = not self.inTurn
                            newCurrentShape = self.shapes[shapeIndice]
                            newGameState = gameState(board, newCurrentShape, newAlreadyTakenShape, self.shapes, newInTurn, self)
                            self.childrens.append(newGameState)
                            newGameState.generateTree(depth-1)

            else:
                for child in self.childrens:
                    child.generateTree(depth-1)
        
    
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




    
    

    
