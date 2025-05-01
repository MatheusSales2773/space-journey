import pygame
import math
import random
from core.state_manager import State
from screens.gameplay import GameplayState

class LevelSelectionState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        # Configuração dos planetas
        self.planets = [
            {"name": "Mercúrio", "image": "assets/images/mercury.png", "distance": 77_000_000, "speed": 300_000},
            {"name": "Vênus", "image": "assets/images/earth.png", "distance": 41_000_000, "speed": 250_000}, # mudar imagem
            {"name": "Terra", "image": "assets/images/earth.png"},
            {"name": "Marte", "image": "assets/images/earth.png", "distance": 78_000_000, "speed": 350_000}, # mudar imagem
            {"name": "Júpiter", "image": "assets/images/earth.png", "distance": 628_000_000, "speed": 500_000}, # mudar imagem
            {"name": "Saturno", "image": "assets/images/earth.png", "distance": 1_275_000_000, "speed": 600_000}, # mudar imagem
            {"name": "Urano", "image": "assets/images/earth.png", "distance": 2_721_000_000, "speed": 700_000}, # mudar imagem
            {"name": "Netuno", "image": "assets/images/earth.png", "distance": 4_351_000_000, "speed": 800_000}, # mudar imagem
        ]
        self.current_index = 0  # Índice do planeta selecionado
        self.font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 50) 

        # Carregar imagens dos planetas
        self.planet_images = [
            pygame.transform.smoothscale(
                pygame.image.load(planet["image"]).convert_alpha(), (500, 500)  
            )
            for planet in self.planets
        ]
        
        # Obter o tamanho da tela para as estrelas
        width, height = pygame.display.get_surface().get_size()
        
        # Criar estrelas no fundo
        self.stars = [
            {
                "x": random.randint(0, width),  # Posição horizontal
                "y": random.randint(0, height),  # Posição vertical
                "radius": random.randint(1, 3),  # Tamanho da estrela
                "brightness": random.randint(50, 255),  # Brilho inicial (50 a 255)
                "blink_speed": random.uniform(0.5, 2.0),  # Velocidade de piscada (0.5 a 2 segundos)
            }
            for _ in range(114)  # Número de estrelas
        ]
        
        # Animação das letras e planetas
        self.animation_time = 0  # Tempo acumulado para a animação
        self.text_scale = 1.0  # Escala inicial do texto
        self.brightness_time = 0  # Tempo acumulado para o brilho
        self.brightness_scale = 1.0  # Escala inicial do brilho
        
        # Estados dos símbolos de navegação - ao se pressionados, mudam de cor
        self.left_arrow_active = False  # Estado do símbolo "<"
        self.right_arrow_active = False  # Estado do símbolo ">"

        # Estados dos símbolos de navegação
        self.left_arrow_active = False
        self.right_arrow_active = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # Navegar para o planeta anterior
                    self.current_index = (self.current_index - 1) % len(self.planets)
                    self.left_arrow_active = True  # Ativar o estado do símbolo "<"
                elif event.key == pygame.K_RIGHT:  # Navegar para o próximo planeta
                    self.current_index = (self.current_index + 1) % len(self.planets)
                    self.right_arrow_active = True  # Ativar o estado do símbolo ">"
                elif event.key == pygame.K_RETURN:  # Confirmar seleção
                    selected_planet = self.planets[self.current_index]
                    self.manager.set_state(GameplayState(self.manager, selected_planet["name"], selected_planet["distance"], selected_planet["speed"]))
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:  # Soltar a tecla "<"
                    self.left_arrow_active = False
                elif event.key == pygame.K_RIGHT:  # Soltar a tecla ">"
                    self.right_arrow_active = False
                    
    def update(self, dt):
        # Atualizar o tempo acumulado para a animação
        self.animation_time += dt
        self.text_scale = 1.0 + 0.1 * math.sin(self.animation_time * 5)

        # Atualizar o brilho dos planetas com pulsação suave
        self.brightness_time += dt
        self.brightness_scale = 1.0 + 0.01 * math.sin(self.brightness_time * 1.5)  # Suavizado
        
        # Atualizar o brilho das estrelas
        for star in self.stars:
            star["brightness"] = 128 + 127 * math.sin(pygame.time.get_ticks() * 0.001 * star["blink_speed"])

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fundo preto
        
        width, height = screen.get_size()

        # Desenhar estrelas de fundo
        for star in self.stars:
            brightness = max(0, min(255, int(star["brightness"])))  # Garantir que o brilho esteja entre 0 e 255
            color = (brightness, brightness, brightness)  # Cor da estrela (escala de cinza)
            pygame.draw.circle(screen, color, (star["x"], star["y"]), star["radius"])

        # Calcular os índices do planeta anterior e seguinte
        previous_index = (self.current_index - 1) % len(self.planets)
        next_index = (self.current_index + 1) % len(self.planets)

         # Exibir o planeta anterior (miniatura)
        previous_planet_image = self.planet_images[previous_index]
        previous_planet_image = pygame.transform.smoothscale(previous_planet_image, (150, 150))  # Reduzir tamanho
        previous_planet_rect = previous_planet_image.get_rect(center=(width // 2 - 550, height // 2 - 50))
        screen.blit(previous_planet_image, previous_planet_rect)
        
        # Aplicar filtro escuro no planeta anterior
        dark_filter = pygame.Surface((150, 150), pygame.SRCALPHA)  # Criar uma superfície transparente
        dark_filter.fill((0, 0, 0, 100))  # Preencher com preto semitransparente (100 de opacidade)
        screen.blit(dark_filter, previous_planet_rect)
        
        # Exibir o próximo planeta (miniatura)
        next_planet_image = self.planet_images[next_index]
        next_planet_image = pygame.transform.smoothscale(next_planet_image, (150, 150))  # Reduzir tamanho
        next_planet_rect = next_planet_image.get_rect(center=(width // 2 + 550, height // 2 - 50))
        screen.blit(next_planet_image, next_planet_rect)
        
        # Aplicar filtro escuro no próximo planeta
        dark_filter = pygame.Surface((150, 150), pygame.SRCALPHA)  # Criar uma superfície transparente
        dark_filter.fill((0, 0, 0, 100))  # Preencher com preto semitransparente (100 de opacidade)
        screen.blit(dark_filter, next_planet_rect)
        
        # Exibir o planeta selecionado
        planet_image = self.planet_images[self.current_index]
        scaled_width = int(planet_image.get_width() * self.brightness_scale)
        scaled_height = int(planet_image.get_height() * self.brightness_scale)
        bright_planet_image = pygame.transform.smoothscale(planet_image, (scaled_width, scaled_height))
        planet_rect = bright_planet_image.get_rect(center=(width // 2, height // 2 - 50))
        screen.blit(bright_planet_image, planet_rect)

        # Exibir o nome do planeta
        planet_name = self.planets[self.current_index]["name"]
        name_text = self.font.render(planet_name, True, (255, 255, 255))
        scaled_width = int(name_text.get_width() * self.text_scale)
        scaled_height = int(name_text.get_height() * self.text_scale)
        name_text = pygame.transform.smoothscale(name_text, (scaled_width, scaled_height))
        name_rect = name_text.get_rect(center=(width // 2, height // 2 + 300))
        screen.blit(name_text, name_rect)

        # Instruções
        instructions_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)  # Fonte menor
        instructions = instructions_font.render("Use ← → para navegar, Enter para selecionar", True, (200, 200, 200))
        instructions_rect = instructions.get_rect(center=(width // 2, height - 50))
        screen.blit(instructions, instructions_rect)
        
        # Exibir os símbolos de navegação
        nav_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 50)  # Fonte para os símbolos
        left_arrow_color = (150, 150, 150) if self.left_arrow_active else (255, 255, 255)
        right_arrow_color = (150, 150, 150) if self.right_arrow_active else (255, 255, 255)

        left_arrow = nav_font.render("<", True, left_arrow_color)
        right_arrow = nav_font.render(">", True, right_arrow_color)

        # Posicionar os símbolos nas laterais
        left_arrow_rect = left_arrow.get_rect(center=(50, height // 2 - 50))
        right_arrow_rect = right_arrow.get_rect(center=(width - 50, height // 2 - 50))

        # Desenhar os símbolos na tela
        screen.blit(left_arrow, left_arrow_rect)
        screen.blit(right_arrow, right_arrow_rect)