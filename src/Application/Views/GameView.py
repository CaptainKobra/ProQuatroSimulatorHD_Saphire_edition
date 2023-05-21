import pygame
from pgu import gui

class GameView:
    class Listener:
        def whoBegin(self, who):
            pass

    def __init__(self, listener:Listener) -> None:
        self.listener = listener
        self.window = gui.App()
        self.mainContainer = gui.Container(width=500, height=500)

        welcome = "Who starts?"
        self.welcomeText = gui.TextArea(value=welcome, width=150, height=20)
        self.mainContainer.add(self.welcomeText, 150, 50)

        self.window.init(widget=self.mainContainer)
        self.window.connect(gui.const.QUIT, self.window.quit)

        self.buttonYou = gui.Button("You")
        self.buttonYou.connect(gui.const.CLICK, self._onButtonYouClick_)
        self.buttonAI = gui.Button("AI")
        self.buttonAI.connect(gui.const.CLICK, self._onButtonAIClick_)
        #self.buttonExit = gui.Button("Exit")
        #self.buttonExit.connect(gui.const.CLICK, self.window.quit)
        self.mainContainer.add(self.buttonYou, 170, 200)
        self.mainContainer.add(self.buttonAI, 220, 230)


    def run(self):
        self.window.run()


    def hide(self):
        self.window.quit()


    def _onButtonYouClick_(self):
        self.listener.whoBegin("you")

    def _onButtonAIClick_(self):
        self.listener.whoBegin("AI")