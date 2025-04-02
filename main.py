# SPACE JOURNEY 
# UNIVERSIDADE CATÓLICA DE BRASÍLIA x SECRETARIA DE CIÊNCIA, TECNOLOGIA E INOVAÇÃO DO DISTRITO FEDERAL
# Developed and designed by: Matheus Sales, Matheus Lopes, Maria Fernanda, Pablo Dias e Raul.
# (c) Copyright 2025

import sys
import pygame

pygame.init()

# CONFIGURAÇÕES DA screen DO JOGO
width, height = 1080, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("UCB's Space Journey")

# IMAGENS
background = pygame.image.load("assets/background.png")
spaceShip = pygame.image.load("assets/spaceship.png")
planets = {
    "Earth": {"image": pygame.image.load("assets/earth.png"), "position": (100, 100)},
}

spaceShip_x, spaceShip_y = 50, 50
spaceShip_speed = 5

# CONFIGURAÇÃO FPS
clock = pygame.time.Clock()

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 50)

pygame.font.get_fonts()

# FONTES
titleFont = pygame.font.SysFont('C:\Windows\Fonts\Arial.ttf', 50)
descriptionFont = pygame.font.SysFont('terminal', 30)

# ESTADOS
MENU = "menu"
RUNNING = "running"

gameState = MENU

# FUNÇÕES DO JOGO
def showMenu():
    scaled_background = pygame.transform.scale(background, (width, height))
    screen.blit(scaled_background, (0, 0))

    title = titleFont.render("Space Journey", True, WHITE)
    instruction = descriptionFont.render("Pressione ENTER para começar", True, WHITE)

    screen.blit(title, (width // 2 - title.get_width() // 2, height // 2 - title.get_height() // 2))
    screen.blit(instruction, (width // 2 - instruction.get_width() // 2, height // 2 + title.get_height()))

def showGame():
    scaled_background = pygame.transform.scale(background, (width, height))
    screen.blit(scaled_background, (0, 0))

    for planet in planets.values():
        screen.blit(planet["image"], planet["position"])

    screen.blit(spaceShip, (spaceShip_x, spaceShip_y))

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gameState == MENU:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    gameState = RUNNING  

    # CONDICIONAL PARA O MENU E O JOGO
    if gameState == MENU:
        showMenu()

    elif gameState == RUNNING:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceShip_x -= spaceShip_speed
        if keys[pygame.K_RIGHT]:
            spaceShip_x += spaceShip_speed
        if keys[pygame.K_UP]:
            spaceShip_y -= spaceShip_speed
        if keys[pygame.K_DOWN]:
            spaceShip_y += spaceShip_speed

        showGame()

    # ATUALIZAÇÃO DA TELA
    pygame.display.flip()
    clock.tick(60)


