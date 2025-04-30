import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames, center, frame_rate=75):
        super().__init__()
        self.frames = frames                  # lista de surfaces
        self.frame_rate = frame_rate          # tempo por frame em ms
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=center)
        self.time_accum = 0                   # tempo acumulado em ms

    def update(self, dt):
        # dt é em segundos → converter para ms
        self.time_accum += dt * 1000
        if self.time_accum >= self.frame_rate:
            self.time_accum -= self.frame_rate
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.kill()  # fim da animação, remove sprite
            else:
                # atualiza a imagem e mantém o centro
                center = self.rect.center
                self.image = self.frames[self.current_frame]
                self.rect = self.image.get_rect(center=center)
