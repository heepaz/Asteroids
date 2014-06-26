import pygame


class Jugador(pygame.sprite.Sprite):
    def __init__(self, imatge="Imatges/Jugador.png", x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imatge)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.esquerra = False
        self.dreta = False
        self.amunt = False
        self.avall = False

    def update(self, dt):
        return
