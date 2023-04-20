import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)

width = 100
height = 100

# Créer une liste pour stocker les zones rectangulaires de chaque case
cases = []
for x in range(0, 5):
    for y in range(0, 5):
        rect = pygame.Rect(x * width, y * height, width, height)
        cases.append(rect)

# Créer une liste pour stocker les surfaces des formes
shape_surfaces = [pygame.Surface((width, height), pygame.SRCALPHA) for _ in cases]

# Dessinez les lignes comme avant
for x in range(0, 5):
    pygame.draw.line(screen, white, (x * width, 0), (x * width, 400), 10)
    pygame.draw.line(screen, white, (0, x * height), (400, x * height), 10)

pygame.display.flip()  # Rafraîchit l'écran

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Demander la forme, la couleur, la taille et la nature (pleine ou creuse) à l'utilisateur
            shape = None
            while shape not in ['0', '1']:
                shape = input("Entrez la forme (0 pour cercle, 1 pour carré) : ")
            color = None
            while color not in ['0', '1']:
                color = input("Entrez la couleur (0 pour rouge, 1 pour bleu) : ")
            size = None
            while size not in ['0', '1']:
                size = input("Entrez la taille (0 pour petit, 1 pour grand) : ")
            filled = None
            while filled not in ['0', '1']:
                filled = input("Entrez la nature de la pièce (0 pour creuse, 1 pour pleine) : ")

            # Convertir la couleur, la taille et la nature en arguments utilisables pour dessiner une forme
            if color == '0':
                shape_color = red
            else:
                shape_color = blue
            if size == '0':
                shape_size = min(width, height) // 6
            else:
                shape_size = min(width, height) // 3
            if filled == '0':
                shape_width = 5
            else:
                shape_width = 0

            # Vérifiez si la souris est dans une case
            for i, rect in enumerate(cases):
                if rect.collidepoint(event.pos):
                    # La souris est dans cette case
                    if not shape_surfaces[i].get_at((0, 0))[3]:
                        # Si une forme n'est pas déjà affichée, dessinez-en une
                        if shape == '0':
                            pygame.draw.circle(shape_surfaces[i], shape_color, (width//2, height//2), shape_size, width=shape_width)
                        else:
                            pygame.draw.rect(shape_surfaces[i], shape_color, pygame.Rect((width - 2 * shape_size) / 2, (height - 2 * shape_size) / 2, 2 * shape_size, 2 * shape_size), width=shape_width)

                        screen.blit(shape_surfaces[i], rect)
                    else:
                        # Sinon, supprimez la forme
                        shape_surfaces[i].fill((0, 0, 0, 0)) # Remplissez la surface avec la couleur transparente (alpha=0)
                        screen.blit(shape_surfaces[i], rect)
            pygame.display.flip()  # Rafraîchit l'écran
