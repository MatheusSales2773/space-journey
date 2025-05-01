import pygame
import math
from core.state_manager import State
from screens.gameplay import GameplayState

class LevelSelectionState(State):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        # Configuração dos planetas
        self.planets = [
            {"name": "Mercúrio", "image": "assets/images/earth.png"}, # mudar imagem
            {"name": "Vênus", "image": "assets/images/earth.png"}, # mudar imagem
            {"name": "Terra", "image": "assets/images/earth.png"},
            {"name": "Marte", "image": "assets/images/earth.png"}, # mudar imagem
            {"name": "Júpiter", "image": "assets/images/earth.png"}, # mudar imagem
            {"name": "Saturno", "image": "assets/images/earth.png"}, # mudar imagem
            {"name": "Urano", "image": "assets/images/earth.png"}, # mudar imagem
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
                    selected_planet = self.planets[self.current_index]["name"]
                    self.manager.set_state(GameplayState(self.manager, selected_planet))
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

    def draw(self, screen):
        screen.fill((0, 0, 0))  # Fundo preto
        width, height = screen.get_size()

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
        left_arrow_rect = left_arrow.get_rect(center=(50, height // 2))
        right_arrow_rect = right_arrow.get_rect(center=(width - 50, height // 2))

        # Desenhar os símbolos na tela
        screen.blit(left_arrow, left_arrow_rect)
        screen.blit(right_arrow, right_arrow_rect)