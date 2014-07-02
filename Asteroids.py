import pygame
from math import sin, cos, radians
from jugador import Jugador


class Bala (pygame.sprite.Sprite):
    def __init__(self, imatge, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.angle = angle + 90
        self.image = pygame.transform.rotate(imatge, self.angle)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.v = 300

    def update(self, dt):
        self.rect.x += self.v * cos(radians(self.angle)) * dt
        self.rect.y -= self.v * sin(radians(self.angle)) * dt


class Nau(Jugador):
    def __init__(self, imatge, x, y):
        Jugador.__init__(self, imatge, x, y)
        self.angle = 0
        self.v_angular = 250
        self.original_image = self.image
        self.a = 400
        self.dispara = False
        self.rellotge_refredament = pygame.time.Clock()
        self.temps_ultim_tret = 0
        self.temps_refredament = 0.5

    def update(self, dt, joc):
        self.ax = self.a * cos(radians(self.angle + 90))
        self.ay = -1 * self.a * sin(radians(self.angle + 90))

        self.temps_ultim_tret += self.rellotge_refredament.tick() / 1000
        if self.dispara and self.temps_ultim_tret > self.temps_refredament:
            self.temps_ultim_tret = 0
            self.dispara_bala(joc)
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

    def dispara_bala(self, joc):
        joc.grup_bales.add(Bala(joc.img_bala, self.rect.centerx,
                                self.rect.centery, self.angle))


class Joc(object):
    def main(self, pantalla):
        rellotge = pygame.time.Clock()
        self.surt = False

        self.amplada = pantalla.get_width()
        self.alçada = pantalla.get_height()

        self.jugador = Nau("Imatges/Nau.png", 100, 100)
        self.grup_jugador = pygame.sprite.GroupSingle(self.jugador)

        self.img_bala = pygame.image.load(
            "Imatges/Sprites/12px-blue-comet.png")
        self.grup_bales = pygame.sprite.Group()

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
        elif event.key == pygame.K_SPACE:
            self.jugador.dispara = True

    def gestiona_alliberament(self, event):
        if event.key == pygame.K_RIGHT:
            self.jugador.dreta = False
        elif event.key == pygame.K_LEFT:
            self.jugador.esquerra = False
        elif event.key == pygame.K_UP:
            self.jugador.amunt = False
        elif event.key == pygame.K_SPACE:
            self.jugador.dispara = False

    def update(self, dt):
        self.grup_jugador.update(dt, self)
        self.grup_bales.update(dt)

    def draw(self, pantalla):
        pantalla.blit(pygame.Surface((self.amplada, self.alçada)), (0, 0))
        self.grup_bales.draw(pantalla)
        self.grup_jugador.draw(pantalla)
        pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    amplada = 800
    alçada = 600
    pantalla = pygame.display.set_mode((amplada, alçada))
    Joc().main(pantalla)
    pygame.quit()
