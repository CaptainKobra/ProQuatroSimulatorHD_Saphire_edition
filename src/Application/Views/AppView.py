import pygame
from pgu import gui

class AppView:
    class Listener:
        def newGame(self):
            pass

    def __init__(self, listener:Listener) -> None:
        self.listener = listener
        self.window = gui.Desktop()
        self.window.connect(gui.const.QUIT, self.window.quit)
        self.table = gui.Table(width=400,height=400)
        self.window.init(self.table)

        welcome = "Welcome in the quarto game simulator!"
        self.welcomeLabel = gui.Label(value=welcome)

        self.table.tr()
        self.table.td(self.welcomeLabel)

        self.buttonStart = gui.Button("Start a new game")
        self.buttonStart.connect(gui.const.CLICK, self._start_)
        self.buttonExit = gui.Button("Exit")
        self.buttonExit.connect(gui.const.CLICK, self.window.quit)

        self.table.tr()
        self.table.td(self.buttonStart)
        self.table.tr()
        self.table.td(self.buttonExit)


    def run(self):
        self.window.run()


    def _start_(self):
        """
        Launch the game
        """
        self.listener.newGame()
