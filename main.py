# SPACE JOURNEY 
# UNIVERSIDADE CATÓLICA DE BRASÍLIA x SECRETARIA DE CIÊNCIA, TECNOLOGIA E INOVAÇÃO DO DISTRITO FEDERAL
# Developed and designed by: Matheus Sales, Matheus Lopes, Maria Fernanda, Pablo Dias e Raul.
# (c) Copyright 2025

import sys
import pygame

pygame.init()

# CONFIGURAÇÕES DA TELA DO JOGO
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

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimento da nave
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        spaceShip_x -= spaceShip_speed
    if teclas[pygame.K_RIGHT]:
        spaceShip_x += spaceShip_speed
    if teclas[pygame.K_UP]:
        spaceShip_y -= spaceShip_speed
    if teclas[pygame.K_DOWN]:
        spaceShip_y += spaceShip_speed

    # Atualiza tela
    screen.blit(background, (0, 0))

    # Desenha planetas
    for planet in planets.values():
        screen.blit(planet["image"], planet["position"])

    # Desenha nave
    screen.blit(spaceShip, (spaceShip_x, spaceShip_y))

    # Atualiza janela
    pygame.display.flip()

    # Controla FPS
    clock.tick(60)


