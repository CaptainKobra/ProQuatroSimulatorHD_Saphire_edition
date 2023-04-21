import pygame

class GameView:

    class GameViewListener:
        def mouseClick(self, surface, case):
            pass

    def __init__(self) -> None:
        self.listener = None
        pygame.init()
        self.screen = pygame.display.set_mode((400, 400))

        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        self.colors = {"black":black, "white":white, "red":red, "blu":blue}

        self.width = 100
        self.height = 100

        # Créer une liste pour stocker les zones rectangulaires de chaque case
        self.cases = []
        for x in range(0, 4):
            for y in range(0, 4):
                rect = pygame.Rect(x * self.width, y * self.height, self.width, self.height)
                self.cases.append(rect)

        # Créer une liste pour stocker les surfaces des formes
        self.shape_surfaces = [pygame.Surface((self.width, self.height), pygame.SRCALPHA) for _ in self.cases]

        # Dessinez les lignes comme avant
        for x in range(0, 5):
            pygame.draw.line(self.screen, white, (x * self.width, 0), (x * self.width, 400), 10)
            pygame.draw.line(self.screen, white, (0, x * self.height), (400, x * self.height), 10)

        pygame.display.flip()  # Rafraîchit l'écran


    def setListener(self, l:GameViewListener):
        self.listener = l


    def getSizes(self):
        return (self.width, self.height)
    

    def getSurface(self, i):
        return self.shape_surfaces[i]


    def waitEvent(self):
        pygame.event.clear()
        event = pygame.event.wait(1000000)
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, rect in enumerate(self.cases):
                if rect.collidepoint(event.pos):
                    # La souris est dans cette case
                    if not self.shape_surfaces[i].get_at((0, 0))[3]:
                        self.listener.mouseClick(self.shape_surfaces[i], i)
                        self.screen.blit(self.shape_surfaces[i], rect)
                        pygame.display.flip()  # Rafraîchit l'écran
                        break


    def end(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    
    def refresh(self, case):
        pygame.event.clear()
        self.screen.blit(self.shape_surfaces[case], self.cases[case])
        pygame.display.flip()


    def refreshAll(self):
        pygame.event.clear()
        for i in range(16):
            self.screen.blit(self.shape_surfaces[i], self.cases[i])
        pygame.display.flip()