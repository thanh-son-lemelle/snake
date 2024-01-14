import pygame
from pygame.locals import *
from random import randint
import sys
import json

# Initialisation de Pygame
pygame.init()
# Initialisation de la musique
music = pygame.mixer.music.load("ost.mp3")
pygame.mixer.music.play(-1)

# Paramètres du jeu
windowWidth, windowHeight = 800, 600
playerStep, appleStep = 44, 44
updateCountMax = 60

# Pour les sprites not working
"""right = 0
left = 1
up = 2
down = 3
downleft = 4
downright = 5
upleft = 6
upright = 7"""

# Couleurs
black = (0, 0, 0)

# Initialisation de la fenêtre
window = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Pygame Snake')

# Chargement des images
playerImage = pygame.image.load("img/snake.png").convert_alpha()
# Pour les sprites not working
"""playerHeadImage = playerImage.subsurface(pygame.Rect((16, 0, 16, 16)))
playerHeadImage = pygame.transform.scale(playerHeadImage, (playerStep, playerStep))

playerTailImage = playerImage.subsurface(pygame.Rect((16, 16, 16, 16)))
playerTailImage = pygame.transform.scale(playerTailImage, (playerStep, playerStep))

playerCorImage = playerImage.subsurface(pygame.Rect((32, 32, 16, 16)))
playerCorImage = pygame.transform.scale(playerCorImage, (playerStep, playerStep))

playerBodImage = playerImage.subsurface(pygame.Rect((16, 48, 16, 16)))
playerBodImage = pygame.transform.scale(playerBodImage, (playerStep, playerStep))
"""
playerRectImage = playerImage.subsurface(pygame.Rect((48, 48, 16, 16)))
playerRectImage = pygame.transform.scale(playerRectImage, (playerStep, playerStep))
# Pour les sprites not working
"""playerHead = {
    up : pygame.transform.rotate(playerHeadImage, 90),
    left : pygame.transform.rotate(playerHeadImage, 180),
    down : pygame.transform.rotate(playerHeadImage, 270),
    right : pygame.transform.rotate(playerHeadImage, 0)
}

playerBody = {
    up : pygame.transform.rotate(playerBodImage, 90),
    left : pygame.transform.rotate(playerBodImage, 180),
    down : pygame.transform.rotate(playerBodImage, 270),
    right : pygame.transform.rotate(playerBodImage, 0),

    downleft : pygame.transform.rotate(playerCorImage, 0),
    downright : pygame.transform.rotate(playerCorImage, 90),
    upleft : pygame.transform.rotate(playerCorImage, 270),
    upright : pygame.transform.rotate(playerCorImage, 180),
}

playerTail = {
    up : pygame.transform.rotate(playerTailImage, 90),
    left : pygame.transform.rotate(playerTailImage, 180),
    down : pygame.transform.rotate(playerTailImage, 270),
    right : pygame.transform.rotate(playerTailImage, 0)
}"""

foodImage = pygame.image.load("img/food.png").convert_alpha()
foodImage = pygame.transform.scale(foodImage, (appleStep, appleStep))

menuImage = pygame.image.load("img/menu.png").convert()
menuImage = pygame.transform.scale(menuImage, (windowWidth, windowHeight))

grassImage = pygame.image.load("img/grass.jpg").convert()
grassImage = pygame.transform.scale(grassImage, (windowWidth, windowHeight))

# Initialisation du joueur
def init_player():
    playerX, playerY = [0], [0]
    liPLayerDirection = [0,0,0]
    playerDirection = 0
    playerLength = 3
    updateCount = 0
    score = 0
    gameOver = False
    playerName = ""

    for i in range(1, 2000):
        playerX.append(-100)
        playerY.append(-100)

    playerX[1] = 1 * playerStep
    playerX[2] = 2 * playerStep
    

    return playerX, playerY, playerDirection, liPLayerDirection, playerLength, updateCount, score, gameOver, playerName



# Initialisation de la pomme
foodX = randint(2, 9) * appleStep
foodY = randint(2, 9) * appleStep

# Fonction de collision
def isCollision(x1, y1, x2, y2, size):
    return x2 <= x1 <= x2 + size and y2 <= y1 <= y2 + size

# Fonction d'affichage du score
def display_score(score):
    font = pygame.font.SysFont(None, 25)
    scoreText = font.render("Score: " + str(score), True, (255, 255, 255))
    window.blit(scoreText, (10, 10))

# Fonction de récupération du pseudo
def get_player_name():
    playerName = input("Entrez votre pseudo : ")
    return playerName

def input_name():
    font = pygame.font.SysFont(None, 36)
    textFont = pygame.font.SysFont(None, 25)
    inputBox = pygame.Rect(windowWidth // 2 - 100, windowHeight // 2, 200, 40)
    colorInactive = pygame.Color('lightskyblue3')
    colorActive = pygame.Color('dodgerblue2')
    color = colorInactive
    active = False
    clock = pygame.time.Clock()
    playerName = ""
    name = False

    while name == False:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if inputBox.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = colorActive if active else colorInactive
            if event.type == KEYDOWN:
                if active:
                    if event.key == K_RETURN:
                        if playerName != "":
                            name = True
                            return playerName
                    elif event.key == K_BACKSPACE:
                        playerName = playerName[:-1]
                    else:
                        playerName += event.unicode
        
        window.blit(menuImage, (0, 0))

        txtSurface = font.render(playerName, True, color)
        width = max(200, txtSurface.get_width()+10)
        inputBox.w = width
        window.blit(txtSurface, (inputBox.x+5, inputBox.y+5))
        pygame.draw.rect(window, color, inputBox, 2)
        
        label = textFont.render("Entrez votre pseudo", True, (255, 255, 255))
        window.blit(label, (windowWidth // 2 - label.get_width() // 2, inputBox.y - 30))

        pygame.display.flip()
        clock.tick(30)

# Fonction de sauvegarde du score
def save_score(name, score):
    try:
        # Load existing scores from the file
        with open("scores.json", "r") as file:
             scores = json.load(file)
    except FileNotFoundError:
        scores = []

    newScore = {"name": name, "score": score}
    scores.append(newScore)

    with open("scores.json", "w") as file:
        json.dump(scores, file)

# Fonction d'affichage des 10 meilleurs scores
def display_top10scores():
    try:
        with open("scores.json", "r") as file:
            scores = json.load(file)
    except FileNotFoundError:
        scores = []

    # Trie des scores
    scores.sort(key=lambda x: x['score'], reverse=True)

    font = pygame.font.SysFont(None, 25)
    titleText = font.render("Top 10 Joueurs", True, (255, 255, 255))
    window.blit(titleText, (windowWidth // 2 - 60, 250))

    # Affichage des 10 meilleurs scores
    for i in range(min(10, len(scores))):
        scoreText = font.render(f"{scores[i]['name']} : {scores[i]['score']}", True, (255, 255, 255))
        window.blit(scoreText, (windowWidth // 2 - 60, 280 + i * 20))

    pygame.display.flip()

# Fonction d'affichage du menu
def display_menu(score):
    window.blit(menuImage, (0, 0))
    
    font = pygame.font.SysFont(None, 36)
    titleText = font.render("Snake Game", True, (255, 255, 255))
    window.blit(titleText, (windowWidth // 2 - 80, 100))

    font = pygame.font.SysFont(None, 25)
    scoreText = font.render("Your Score: " + str(score), True, (255, 255, 255))
    window.blit(scoreText, (windowWidth // 2 - 60, 200))

    display_top10scores()
    
    buttonRect = pygame.Rect(windowWidth // 2 - 50, 500, 100, 50)
    pygame.draw.rect(window, (0, 255, 0, 50), buttonRect) 
    # Display the text on the button
    buttonFont = pygame.font.SysFont(None, 25)
    buttonText = buttonFont.render("Rejouer", True, (0, 0, 0))
    window.blit(buttonText, (windowWidth // 2 - 30, 515))

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if buttonRect.collidepoint(mouse_x, mouse_y):
                    
                    gameOver = False
                    return gameOver
        clock.tick(30)


# Boucle principale
running = True
clock = pygame.time.Clock()
playerX, playerY, playerDirection, liPlayerDirection, playerLength, updateCount, score, gameOver, playerName = init_player()

while running:
    # Affichage du menu
    if gameOver:
        if playerName == "":
            playerName = input_name()
            save_score(playerName, score)

        display_menu(score)
        playerX, playerY, playerDirection, liPlayerDirection, playerLength, updateCount, score, gameOver, playerName = init_player()


    else:
        currentDirection = playerDirection
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT and currentDirection != 1:
                    playerDirection = 0
                    currentDirection = playerDirection
                elif event.key == K_LEFT and currentDirection != 0:
                    playerDirection = 1
                    currentDirection = playerDirection
                elif event.key == K_UP and currentDirection != 3:
                    playerDirection = 2
                    currentDirection = playerDirection
                elif event.key == K_DOWN and currentDirection != 2:
                    playerDirection = 3
                    currentDirection = playerDirection
        # Mise à jour du joueur
        updateCount += 10
        if updateCount > updateCountMax:
            for i in range(playerLength - 1, 0, -1):
                playerX[i] = playerX[i - 1]
                playerY[i] = playerY[i - 1]
                liPlayerDirection.insert(0, playerDirection)

            if playerDirection == 0:
                playerX[0] += playerStep
            elif playerDirection == 1:
                playerX[0] -= playerStep
            elif playerDirection == 2:
                playerY[0] -= playerStep
            elif playerDirection == 3:
                playerY[0] += playerStep

            # Vérifier si le serpent sort de l'écran
            if (playerX[0] < 0 or playerX[0] > windowWidth - playerStep or  playerY[0] < 0 or playerY[0] > windowHeight - playerStep):
                gameOver = True

            updateCount = 0

            # #########################################

        # Vérifier si le serpent mange la pomme
        if isCollision(foodX, foodY, playerX[0], playerY[0], 40):
            while True:
                foodX = randint(2, 9) * appleStep
                foodY = randint(2, 9) * appleStep
                # Check if the new food position is not in collision with any part of the snake's body
                if all(foodX != playerX[i] or foodY != playerY[i] for i in range(playerLength)):
                    playerLength += 1
                    score += 1
                    break

        # Vérifier si le serpent entre en collision avec lui-même
        for i in range(2, playerLength):
            if isCollision(playerX[0], playerY[0], playerX[i], playerY[i], 40):
                print("Collision")
                print(playerX[0], playerY[0], playerX[i], playerY[i])
                print(playerX, playerY)
                print(playerLength)
                print(playerDirection)
                print(liPlayerDirection)
                print(currentDirection)
                gameOver = True

        # Affichage
        window.fill(black)
        window.blit(grassImage, (0, 0))
        display_score(score)
        # Pour les sprites not working
        """for i in range(0, playerLength):
            if i == 0:
                window.blit(playerHead[playerDirection], (playerX[i], playerY[i]))
            elif i == playerLength - 1:
                
                print(liPlayerDirection)
                window.blit(playerTail[liPlayerDirection[i]], (playerX[i], playerY[i]))
            else:
                window.blit(playerBody[playerDirection], (playerX[i], playerY[i]))"""
        for i in range(0, playerLength):
            window.blit(playerRectImage, (playerX[i], playerY[i]))


        window.blit(foodImage, (foodX, foodY))
        pygame.display.flip()

        clock.tick(60)

# Quitter Pygame
pygame.quit()