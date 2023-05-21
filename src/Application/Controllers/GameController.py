from Views.GameView import GameView

class GameController(GameView.Listener):
    def __init__(self) -> None:
        self.gameView = GameView(self)


    def run(self):
        self.gameView.run()

    def whoBegin(self, who:str):
        if who == "you":
            print("you")
        elif who == "AI":
            print("AI")