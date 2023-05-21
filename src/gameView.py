import pygame
from pygame.locals import *
from pgu import text

class GameView:

    class GameViewListener:
        def mouseClick(self, surface, case):
            pass
        def draw(self, surface, case):
            pass
        def select(self, shape):
            pass

    def __init__(self) -> None:
        self.listener = None
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))

        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        self.colors = {"black":black, "white":white, "red":red, "blue":blue}

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

        # Cases pour les pièces disponibles
        self.selectCases = []
        for x in range(8):
            for y in range(2):
                rect = pygame.Rect(x * self.width, y * self.height + 450, self.width, self.height)
                self.selectCases.append(rect)

        # Surfaces pour les pièces disponibles
        self.selectShape_surfaces = [pygame.Surface((self.width, self.height), pygame.SRCALPHA) for _ in self.selectCases]

        # Case et Surface pour la pièce choisie par l'IA
        self.selectedShapeCase = pygame.Rect(550, 60, self.width, self.height)
        self.selectedSahpeSurface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Textes
        font = pygame.font.SysFont("default", 30)
        text.write(self.screen,font,(450,30),white,"The piece the AI has selected for you:")
        text.write(self.screen, font, (10, 430), white, "Available pieces:")
        
        pygame.display.flip()  # Rafraîchit l'écran


    def setListener(self, l:GameViewListener):
        self.listener = l


    def quarto(self, winner:str):
        """
        Affiche le vainqueur
        """
        print("in quarto")
        font = pygame.font.SysFont("default", 80)
        text.writec(self.screen, font, self.colors['white'], "QUARTO! The winner is: "+winner, border=5)
        pygame.display.flip()


    def getSizes(self):
        return (self.width, self.height)
    

    def getSurface(self, i):
        return self.shape_surfaces[i]


    def waitEvent(self):
        """
        Attend que l'utilisateur choisisse une case où placer la pièce
        """
        pygame.event.clear()
        event = pygame.event.wait(1000000)
        #self.app.event(event)
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
                        self.erase(self.selectedSahpeSurface, self.selectedShapeCase)
                        break


    def waitSelectEvent(self):
        """
        Attend que l'utilisateur sélectionne une pièce
        """
        #pygame.event.clear()
        event = pygame.event.wait(1000000)
        if event.type == pygame.QUIT:
            pygame.quit()
            #quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("mousebuttondown")
            for i, rect in enumerate(self.selectCases):
                if rect.collidepoint(event.pos):
                    # La souris est dans cette case
                    self.listener.select(i)
                    self.erase(self.selectShape_surfaces[i], rect)
                    pygame.display.flip()  # Rafraîchit l'écran
                    break


    def erase(self, surface, rect):
        """
        Efface une pièce (la recouvre d'un rectangel noir, en fait)
        """
        pygame.draw.rect(surface, self.colors['black'], pygame.Rect(0, 0, 100, 100))
        self.screen.blit(surface, rect)
        pygame.display.flip()


    def AIselected(self, i:int):
        """
        Dessine la pièce choisie par l'IA dans l'espace prévu
        """
        self.listener.draw(self.selectedSahpeSurface, i)
        self.screen.blit(self.selectedSahpeSurface, self.selectedShapeCase)
        self.erase(self.selectShape_surfaces[i], self.selectCases[i])


    def drawSelectSurfaces(self):
        """
        Dessine toutes les pièces disponibles (appelé une seule fois, avant le début de la partie)
        """
        for i, rect in enumerate(self.selectCases):
            self.listener.draw(self.selectShape_surfaces[i], i)
            self.screen.blit(self.selectShape_surfaces[i], rect)
        pygame.display.flip()


    def end(self):
        """
        Fin de la partie. Attend que l'utilisateur ferme l'application.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

    
    def refresh(self, case):
        """
        Refresh une case 
        """
        pygame.event.clear()
        self.screen.blit(self.shape_surfaces[case], self.cases[case])
        pygame.display.flip()


    def refreshAll(self):
        """
        Refresh toutes les cases
        """
        pygame.event.clear()
        for i in range(16):
            self.screen.blit(self.shape_surfaces[i], self.cases[i])
        pygame.display.flip()



