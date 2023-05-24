from Players.AIPlayer import AIPlayer

from gameView import GameView
from Shape import Shape

from MCTS.State import State
from MCTS.UCT import UCT

class MCTSAIPlayer(AIPlayer):
    def __init__(self, gameView:GameView, currentShape:Shape, shapes:list, alreadyTakenShape:list, board:list, playerID:str, done:bool) -> None:
        super().__init__(gameView, currentShape, shapes, alreadyTakenShape, board, playerID, done)


    def begin(self):
        super().begin()


    def play(self):
        print("MCTS play")
        mcts_tree = UCT(1)
        position, shape = mcts_tree.search(self.gameState)
        self.gameState.selectPos(pos=position)

        surface = self.gameView.getSurface(position)
        self.currentShape.draw(surface)
        self.gameView.refresh(position)
        self.board[position] = self.currentShape

        self.currentShape = shape
        index = self.currentShape.getNum()
        self.gameView.AIselected(index)
        self.gameState.selectShape(shape)
        self.alreadyTakenShape[index] = True
        
        #super().play()
        
