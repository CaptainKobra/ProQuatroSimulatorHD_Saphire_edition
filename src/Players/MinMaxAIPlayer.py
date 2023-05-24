from Players.AIPlayer import AIPlayer

from gameView import GameView
from Shape import Shape

from State import State
from MinMax.MinMaxTree import Tree


class MinMaxAIPlayer(AIPlayer):
    def __init__(self, gameView:GameView, currentShape:Shape, shapes:list, alreadyTakenShape:list, board:list, playerID:str, done:bool) -> None:
        super().__init__(gameView, currentShape, shapes, alreadyTakenShape, board, playerID, done)


    def begin(self):
        super().begin()


    def play(self):
        #print("start turn of", self.playerID)
        #print("AD currentShape=", self.gameState.getPresiousSelectedShape().getNum())
        self.currentShape = self.gameState.getPreviousSelectedShape()
        if(self.currentShape != None):
            
            #AI turn where it temporise until turn 11 and then calculate the full tree and play the bests moves
            if self.gameState.getTurnLeft() > 5:
                child = self.temporisePlay()
            else:
                # minmax
                child = self.minmax()

            # update state and board
            position, shape = child.getAction()
            self.gameState.selectPos(pos=position)
            super().eraseSelectionCase()
            surface = self.gameView.getSurface(position)
            self.currentShape.draw(surface)
            self.gameView.refresh(position)
            self.board[position] = self.currentShape
            self.currentShape = shape
            if self.currentShape == None:
                super().equal()
                return
            index = self.currentShape.getNum()
            self.gameView.AIselected(index, self)
            self.gameState.selectShape(index)
            self.alreadyTakenShape[index] = True

            super().play()
        else:
            self.currentShape = super().begin()


        #print("end turn of", self.playerID)

        #print("AF currentShape=", self.gameState.getPresiousSelectedShape().getNum())
    

    def temporisePlay(self):

        tree = Tree(self.gameState, True)
        tree.generateTree(1)
        self.currentShape = self.gameState.getPreviousSelectedShape()
        #print("Tree generated")
        descisivLeafs = tree.getWinningLeafs()
        if len(descisivLeafs) > 0:
            child = descisivLeafs[0]
        else:
            child = self.bestChildToTemporise(tree.getChildren())

        return child


    def bestChildToTemporise(self, children:list):
        #Retourne le meilleur enfant de la liste d'enfants "childrens"
        bestChild = children[0]
        bestChildvalue = self.connexion(bestChild.getBoard())
        bestChildFound = False
        for child in children:
            if self.connexion(child.getBoard()) > bestChildvalue and (not child.haveDescisivChild()):
                bestChild = child
                bestChildvalue = self.connexion(child.getBoard())
                bestChildFound = True
        if not bestChildFound:
            for child in children:
                if self.connexion(child.getBoard()) > bestChildvalue:
                    bestChild = child
                    bestChildvalue = self.connexion(child.getBoard())
        return bestChild
    


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
        #print("score_diag : ",score_diag," score_col : ",score_col," score_row : ",score_row," total : ",score_diag + score_col + score_row)
        return -(score_diag + score_col + score_row)
    


    def common_properties_count(self, shapes:list):
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
    

    def minmax(self) -> Tree:
        tree = Tree(self.gameState, True)
        tree.generateTree(self.gameState.getTurnLeft())
        #print("Tree generated")

        descisivLeafs = tree.getWinningLeafs()
        if len(descisivLeafs) > 0:
            bestChild = descisivLeafs[0]
        else:
            children = tree.getChildren()
            for child in children:
                self.generateMinMaxValues(child)
            bestChild = children[0]
            bestChildvalue = children[0].getMinMaxValue()
            for child in children:
                if child.getMinMaxValue() > bestChildvalue:
                    bestChild = child
                    bestChildvalue = child.getMinMaxValue()
        return bestChild


    def generateMinMaxValues(self, tree:Tree):
        children = tree.getChildren()
        if len(children) > 0:
            for child in children:
                tree.addToMinMaxValue(self.generateMinMaxValues(child))         
            return 0
        else:
            if not tree.haveDescisivChild():
                return 0
            elif tree.getInTurn():
                return 1
            else:
                return -1