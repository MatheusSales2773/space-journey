import pygame, random

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, image, screen_width):
        super().__init__()
        scale = random.uniform(0.05, 0.1)
        w = int(image.get_width() * scale)
        h = int(image.get_height() * scale)
        scaled_img = pygame.transform.smoothscale(image, (w, h))

        self.original_image = scaled_img
        self.image = self.original_image

        x = random.randint(0, screen_width - w)
        self.rect = self.image.get_rect(topleft=(x, -h))

        self.speed = random.uniform(50, 100)

        self.angle = random.uniform(0, 360)
        self.rot_speed = random.uniform(-90, 90)  # graus por segundo

    def update(self, dt):
        self.rect.y += int(self.speed * dt)

        self.angle = (self.angle + self.rot_speed * dt) % 360

        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)

        if self.rect.top > pygame.display.get_surface().get_height():
            self.kill()
