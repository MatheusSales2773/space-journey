import pygame

class Earth(pygame.sprite.Sprite):
    def __init__(self, sheet, pos):
        super().__init__()
        self.frames = []
        self.frame_index = 0
        # Divide sprite sheet 32×32, 4 colunas
        for i in range(4):
            rect = pygame.Rect(i * 32, 0, 32, 32)
            image = sheet.subsurface(rect).convert_alpha()
            self.frames.append(image)
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        self.animation_speed = 0.2  # ajusta rotação

    def update(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
