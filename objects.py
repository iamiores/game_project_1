import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, file, x, y):
        super().__init__()
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
