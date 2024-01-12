import pygame
from pygame.locals import *
from random import randint

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
windowWidth, windowHeight = 800, 600
playerStep, appleStep = 44, 44
playerLength = 3
updateCountMax = 2

# Couleurs
black = (0, 0, 0)

# Initialisation de la fenêtre
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Pygame Snake')

# Chargement des images
playerImage = pygame.image.load("img/idle_animation/idle00.png").convert()
foodImage = pygame.image.load("img/food/bootle.png").convert()

# Initialisation du joueur
playerX, playerY = [0], [0]
playerDirection = 0
updateCount = 0

for i in range(1, 2000):
    playerX.append(-100)
    playerY.append(-100)

playerX[1] = 1 * playerStep
playerX[2] = 2 * playerStep

# Initialisation de la pomme
foodX = randint(2, 9) * appleStep
foodY = randint(2, 9) * appleStep

# Fonction de collision
def isCollision(x1, y1, x2, y2, size):
    return x2 <= x1 <= x2 + size and y2 <= y1 <= y2 + size

# Boucle principale
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[K_RIGHT] and playerDirection != 1:
        playerDirection = 0
    if keys[K_LEFT] and playerDirection != 0:
        playerDirection = 1
    if keys[K_UP] and playerDirection != 3:
        playerDirection = 2
    if keys[K_DOWN] and playerDirection != 2:
        playerDirection = 3

    # Mise à jour du joueur
    updateCount += 1
    if updateCount > updateCountMax:
        for i in range(playerLength - 1, 0, -1):
            playerX[i] = playerX[i - 1]
            playerY[i] = playerY[i - 1]

        if playerDirection == 0:
            playerX[0] += playerStep
        elif playerDirection == 1:
            playerX[0] -= playerStep
        elif playerDirection == 2:
            playerY[0] -= playerStep
        elif playerDirection == 3:
            playerY[0] += playerStep

        updateCount = 0

    # Vérifier si le serpent mange la pomme
    if isCollision(foodX, foodY, playerX[0], playerY[0], 40):
        foodX = randint(2, 9) * appleStep
        foodY = randint(2, 9) * appleStep
        playerLength += 1

    # Vérifier si le serpent entre en collision avec lui-même
    for i in range(2, playerLength):
        if isCollision(playerX[0], playerY[0], playerX[i], playerY[i], 40):
            print("Vous avez perdu ! Collision : ")
            print("x[0] (" + str(playerX[0]) + "," + str(playerY[0]) + ")")
            print("x[" + str(i) + "] (" + str(playerX[i]) + "," + str(playerY[i]) + ")")
            running = False

    # Affichage
    window.fill(black)
    for i in range(0, playerLength):
        window.blit(playerImage, (playerX[i], playerY[i]))

    window.blit(foodImage, (foodX, foodY))
    pygame.display.flip()

    clock.tick(25)

# Quitter Pygame
pygame.quit()