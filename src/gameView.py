import pygame
from pygame.locals import *
from pgu import gui
from MyApp import MyApp

from AppController import AppController

class GameView(MyApp.Listener):

    class GameViewListener:
        def mouseClick(self, surface, case):
            pass

    def __init__(self) -> None:
        self.listener = None
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), SWSURFACE)

        self.app = MyApp()
        self.app.setListener(self)
        self.container = gui.Container(align=-1,valign=-1)
        ctr = AppController()
        self.container.add(ctr,0,0)
        self.app.init(self.container)

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
        self.app.event(event)
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
        self.app.paint()
        pygame.display.flip()


    def welcome(self):
        self.app.send(200)
        self.done = False
        while not self.done:
            for event in pygame.event.get():
                self.app.event(event)
            self.app.paint()
            pygame.display.flip()

    
    def selectStarter(self, starter: str):
        self.starter = starter
        self.done = True

    
    def getStarter(self):
        print(self.starter)
        return self.starter



