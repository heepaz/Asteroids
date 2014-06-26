import pygame
from math import sin, cos, radians
from jugador import Jugador


class Nau(Jugador):
    def __init__(self, imatge, x, y):
        Jugador.__init__(self, imatge, x, y)
        self.angle = 0
        self.v_angular = 250
        self.original_image = self.image
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0
        self.a = 400

    def update(self, dt):
        self.ax = self.a * cos(radians(self.angle + 90))
        self.ay = -1 * self.a * sin(radians(self.angle + 90))
        if self.dreta and self.esquerra:
            pass
        elif self.dreta:
            self.gir(dt, 'dreta')
        elif self.esquerra:
            self.gir(dt, 'esquerra')
        if self.amunt:
            self.vx += self.ax * dt
            self.vy += self.ay * dt
            self.rect.x += self.vx * dt + 0.5 * self.ax * dt * dt
            self.rect.y += self.vy * dt + 0.5 * self.ay * dt * dt
        else:
            self.rect.x += self.vx * dt
            self.rect.y += self.vy * dt

    def gir(self, dt, direccio='dreta'):
        antic_centre = self.rect.center
        if direccio == 'dreta':
            self.angle -= (self.v_angular * dt) % 360
        elif direccio == 'esquerra':
            self.angle += (self.v_angular * dt) % 360
        self.image = pygame.transform.rotate(self.original_image,
                                             self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = antic_centre


class Joc(object):
    def main(self, pantalla):
        rellotge = pygame.time.Clock()
        self.surt = False

        self.jugador = Nau("Imatges/Nau.png", 100, 100)
        self.grup_jugador = pygame.sprite.GroupSingle(self.jugador)

        while not self.surt:
            dt = rellotge.tick(30)
            self.gestiona_esdeveniments()
            self.update(dt/1000)
            self.draw(pantalla)

    def gestiona_esdeveniments(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.surt = True
            elif event.type == pygame.KEYDOWN:
                self.gestiona_pressió(event)
            elif event.type == pygame.KEYUP:
                self.gestiona_alliberament(event)

    def gestiona_pressió(self, event):
        if event.key == pygame.K_ESCAPE:
            self.surt = True
        elif event.key == pygame.K_RIGHT:
            self.jugador.dreta = True
        elif event.key == pygame.K_LEFT:
            self.jugador.esquerra = True
        elif event.key == pygame.K_UP:
            self.jugador.amunt = True

    def gestiona_alliberament(self, event):
        if event.key == pygame.K_RIGHT:
            self.jugador.dreta = False
        elif event.key == pygame.K_LEFT:
            self.jugador.esquerra = False
        elif event.key == pygame.K_UP:
            self.jugador.amunt = False

    def update(self, dt):
        self.grup_jugador.update(dt)

    def draw(self, pantalla):
        pantalla.blit(pygame.Surface((800, 600)), (0, 0))
        self.grup_jugador.draw(pantalla)
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    Joc().main(pantalla)
