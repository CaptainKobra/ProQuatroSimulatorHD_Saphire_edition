from Views.AppView import AppView
from Controllers.GameController import GameController

class AppController(AppView.Listener):
    def __init__(self) -> None:
        self.appView = AppView(self)
        self.gameController = None


    def run(self):
        self.appView.run()


    def newGame(self):
        self.appView.hide()
        #self.gameController = GameController()
        #self.gameController.run()