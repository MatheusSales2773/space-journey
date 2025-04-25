import pygame
import sys
import math
import random

# Inicializa o pygame
pygame.init()

# Tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("MACACOS ME MORDAM")

# Imagens
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (64, 64))

bullet_img = pygame.image.load("assets/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (16, 32))

enemy_img = pygame.image.load("assets/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (64, 64))

explosion_img = pygame.image.load("assets/explosion.png")
explosion_img = pygame.transform.scale(explosion_img, (64, 64))

# Jogador
player_x = 370
player_y = 480
player_vel = 5

# Tiro
bullet_x = 0
bullet_y = player_y
bullet_vel = 10
bullet_state = "ready"

def atirar(x, y):
    tela.blit(bullet_img, (x + player_img.get_width() // 2 - bullet_img.get_width() // 2, y))

# Inimigos
num_inimigos = 6
enemy_x = []
enemy_y = []
enemy_vel_y = 5

for i in range(num_inimigos):
    enemy_x.append(random.randint(0, LARGURA - 64))
    enemy_y.append(random.randint(-600, -64))

# Colisão
def houve_colisao(enemy_x, enemy_y, bullet_x, bullet_y):
    distancia = math.sqrt((enemy_x - bullet_x)**2 + (enemy_y - bullet_y)**2)
    return distancia < 27

# Progresso
destino_x = 800
progress = 0
distancia = destino_x - progress

# Fonte
tela_inicio = True
tela_selecao_fase = False
fase_selecionada = 1
fonte = pygame.font.Font(None, 36)

# Explosao
explosao_state = "ready"
explosao_x = 0
explosao_y = 0
explosao_start_time = 0

def mostrar_explosao():
    if explosao_state == "explode":
        tela.blit(explosion_img, (explosao_x, explosao_y))

def mostrar_distancia():
    texto = fonte.render(f"Distância: {distancia}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

# Game Over
game_over_state = False

def mostrar_game_over():
    texto1 = fonte.render("TOMOU GAP, BY OTTON", True, (255, 0, 0))
    texto2 = fonte.render("Pressione qualquer tecla para reiniciar", True, (255, 255, 255))
    texto3 = fonte.render("Ou ESC para voltar ao menu", True, (255, 255, 255))

    texto1_rect = texto1.get_rect(center=(LARGURA // 2, ALTURA // 2 - 40))
    texto2_rect = texto2.get_rect(center=(LARGURA // 2, ALTURA // 2))
    texto3_rect = texto3.get_rect(center=(LARGURA // 2, ALTURA // 2 + 40))

    tela.blit(texto1, texto1_rect)
    tela.blit(texto2, texto2_rect)
    tela.blit(texto3, texto3_rect)

def reiniciar_jogo():
    global player_x, bullet_x, bullet_y, bullet_state, progress, explosao_state
    global enemy_x, enemy_y, distancia, explosao_x, explosao_y, game_over_state
    global explosao_start_time, enemy_vel_y, destino_x

    player_x = 370
    bullet_x = 0
    bullet_y = player_y
    bullet_state = "ready"
    progress = 0
    distancia = destino_x - progress
    explosao_state = "ready"
    explosao_x = 0
    explosao_y = 0
    game_over_state = False
    explosao_start_time = 0

    if fase_selecionada == 1:
        enemy_vel_y = 3
        destino_x = 600
    elif fase_selecionada == 2:
        enemy_vel_y = 5
        destino_x = 800
    elif fase_selecionada == 3:
        enemy_vel_y = 7
        destino_x = 1000
    elif fase_selecionada == 4:
        enemy_vel_y = 10
        destino_x = 1500

    for i in range(num_inimigos):
        enemy_x[i] = random.randint(0, LARGURA - 64)
        enemy_y[i] = random.randint(-600, -64)

# Clock
clock = pygame.time.Clock()

# Loop do jogo
while True:
    tela.fill((0, 0, 0))  # Limpa a tela

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if tela_inicio:
                # Impedir qualquer tecla de iniciar antes da seleção de fase
                tela_inicio = False
                tela_selecao_fase = True
                game_over_state = False  # Resetar o estado de Game Over
            elif tela_selecao_fase:
                if evento.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    fase_selecionada = int(evento.unicode)
                    tela_selecao_fase = False
                    reiniciar_jogo()
                    game_over_state = False  # Resetar o estado de Game Over
            elif game_over_state:
                if evento.key == pygame.K_ESCAPE:
                    # Volta para o menu de seleção de fase
                    tela_inicio = False
                    tela_selecao_fase = True
                    game_over_state = False  # Resetar o estado de Game Over
                else:
                    reiniciar_jogo()

            elif evento.key == pygame.K_SPACE and bullet_state == "ready" and not game_over_state:
                bullet_x = player_x
                bullet_y = player_y
                bullet_state = "fire"

    if tela_inicio:
        titulo = fonte.render("SPACE DEFENDERS", True, (255, 255, 255))
        sub = fonte.render("Pressione qualquer tecla para iniciar", True, (200, 200, 200))
        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 200)))
        tela.blit(sub, sub.get_rect(center=(LARGURA // 2, 260)))

    elif tela_selecao_fase:
        titulo = fonte.render("SELECIONE A FASE", True, (255, 255, 255))
        fase1 = fonte.render("1 - Lua (Fácil)", True, (255, 255, 255))
        fase2 = fonte.render("2 - Marte (Média)", True, (255, 255, 255))
        fase3 = fonte.render("3 - Vênus (Difícil)", True, (255, 255, 255))
        fase4 = fonte.render("4 - Júpiter (Insano)", True, (255, 255, 255))

        tela.blit(titulo, titulo.get_rect(center=(LARGURA // 2, 150)))
        tela.blit(fase1, fase1.get_rect(center=(LARGURA // 2, 250)))
        tela.blit(fase2, fase2.get_rect(center=(LARGURA // 2, 300)))
        tela.blit(fase3, fase3.get_rect(center=(LARGURA // 2, 350)))
        tela.blit(fase4, fase4.get_rect(center=(LARGURA // 2, 400)))

    elif not game_over_state:  # Apenas processar o jogo se não for Game Over
        teclas = pygame.key.get_pressed()
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and player_x > 0:
            player_x -= player_vel
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and player_x < LARGURA - 64:
            player_x += player_vel
        if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and player_y > 0:
            player_y -= player_vel
        if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and player_y < ALTURA - 64:
            player_y += player_vel

        if progress < destino_x:
            progress += 1
            distancia = destino_x - progress

        for i in range(num_inimigos):
            enemy_y[i] += enemy_vel_y

            if enemy_y[i] > ALTURA:
                enemy_y[i] = random.randint(-600, -64)
                enemy_x[i] = random.randint(0, LARGURA - 64)

            if houve_colisao(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
                bullet_y = player_y
                bullet_state = "ready"
                enemy_y[i] = random.randint(-600, -64)
                enemy_x[i] = random.randint(0, LARGURA - 64)

            if houve_colisao(enemy_x[i], enemy_y[i], player_x, player_y):
                explosao_state = "explode"
                explosao_x = player_x
                explosao_y = player_y
                explosao_start_time = pygame.time.get_ticks()
                game_over_state = True

            tela.blit(enemy_img, (enemy_x[i], enemy_y[i]))

        pygame.draw.rect(tela, (0, 255, 0), (LARGURA * 0.35, 20, (progress * (LARGURA * 0.55)) / destino_x, 10))

        if bullet_state == "fire":
            atirar(bullet_x, bullet_y)
            bullet_y -= bullet_vel
            if bullet_y <= 0:
                bullet_y = player_y
                bullet_state = "ready"

        mostrar_distancia()
        mostrar_explosao()

        if explosao_state == "ready":
            tela.blit(player_img, (player_x, player_y))

    if explosao_state == "explode":
        if pygame.time.get_ticks() - explosao_start_time > 4000:
            game_over_state = True

    if game_over_state:
        mostrar_game_over()

    pygame.display.flip()
    clock.tick(60)
