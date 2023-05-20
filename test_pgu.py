import pygame
from pgu import gui


class myApp:
    def __init__(self) -> None:
        self.myApp = gui.App()
        self.container = gui.Container(width=400, height=400)
        self.text = gui.TextArea(value="Who starts?")

        self.buttonMe = gui.Button("Me")
        self.buttonMe.connect(gui.CLICK, self.onButtonMeClick)

        self.buttonAI = gui.Button("AI")
        self.buttonAI.connect(gui.const.CLICK, self.onButtonAIClick)

        self.container.add(self.text, 10, 10)
        self.container.add(self.buttonMe, 50, 50)
        self.container.add(self.buttonAI, 50, 70)

        self.myApp.init(widget=self.container)
        self.myApp.connect(gui.const.QUIT, self.myApp.quit)


    def run(self):
        self.myApp.run()


    def onButtonMeClick(self):
        self.text2 = gui.TextArea("You starts!")
        self.container.add(self.text2, 10, 100)
        self.buttonMe.disconnect(gui.const.CLICK)
        self.buttonAI.disconnect(gui.const.CLICK)

    def onButtonAIClick(self):
        self.text2 = gui.TextArea("AI starts!")
        self.container.add(self.text2, 10, 100)
        self.buttonMe.disconnect(gui.const.CLICK)
        self.buttonAI.disconnect(gui.const.CLICK)



if __name__ == '__main__':
    app = myApp()
    app.run()

 