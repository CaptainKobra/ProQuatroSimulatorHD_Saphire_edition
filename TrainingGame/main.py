from gameController import GameController

numberOfGames = 1000

if __name__ == '__main__':

    for i in range(numberOfGames):
        mainController = GameController()
        mainController.createShapes()
        print("Game number: ", i+1)
        mainController.play()

