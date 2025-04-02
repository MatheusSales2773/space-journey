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
    "Sun": {"image": pygame.image.load("assets/sun.png"), "position": (-400, 50)},
    "Mercury": {"image": pygame.image.load("assets/mercury.png"), "position": (500, 325)},
    "Earth": {"image": pygame.image.load("assets/earth.png"), "position": (800, 300)},
}

# SOUNDTRACK
pygame.mixer.init()
pygame.mixer.music.load("assets/audio/soundtrack.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)  

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
titleFont = pygame.font.Font("assets/fonts/Silkscreen-Regular.ttf", 82)
instructionFont = pygame.font.Font("assets/fonts/Silkscreen-Bold.ttf", 30)

# ESTADOS
MENU = "menu"
RUNNING = "running"

IS_MUSIC_PLAYING = True

gameState = MENU

# FUNÇÕES DO JOGO
def showMenu():
    scaled_background = pygame.transform.scale(background, (width, height))
    screen.blit(scaled_background, (0, 0))

    title = titleFont.render("Space Journey", True, WHITE)
    instruction = instructionFont.render("Pressione ESPAÇO para começar", True, WHITE)

    screen.blit(title, (width // 2 - title.get_width() // 2, height // 4 - title.get_height() // 4))
    screen.blit(instruction, (width // 2 - instruction.get_width() // 2, height // 2 + title.get_height()))

def showGame():
    screen.fill(BLACK)

    planet_sizes = {
        "Sun": (800, 800),
        "Mercury": (100, 100),
        "Earth": (150, 150),
    }

    for planet_name, planet in planets.items():
        size = planet_sizes.get(planet_name, (100, 100))  # Default size if not specified
        scaled_planet = pygame.transform.scale(planet["image"], size)
        screen.blit(scaled_planet, planet["position"])

    scaled_ship = pygame.transform.scale(spaceShip, (100, 100))
    screen.blit(scaled_ship, (spaceShip_x, spaceShip_y))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if gameState == MENU:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
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


