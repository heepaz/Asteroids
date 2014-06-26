import pygame


# Creem una classe jugador que agafi les característiques dels
# Sprites que defineix el pygame.
class Jugador(pygame.sprite.Sprite):
    # Definim la Funció que crearà un jugador a partir d'una imatge i
    # unes posicions, velocitats i acceleracions
    def __init__(self, imatge="Imatges/Jugador.png",
                 x=0, y=0, vx=0, vy=0):
        # Afegim al Jugador les característiques de l'Sprite
        pygame.sprite.Sprite.__init__(self)

        # Un Sprite necessita una imatge
        self.image = pygame.image.load(imatge)

        # I un pygame.Rect (un rectangle amb una posició (x,y)
        # i una amplada i altura
        self.rect = self.image.get_rect()

        # Establim les coordenades del rect,
        # que és on es dibuixarà la imatge
        self.rect.x = x
        self.rect.y = y

        # Definim unes velocitats i acceleracions
        self.vx = vx
        self.vy = vy

        # Definim quatre variables Booleanes (Cert/Fals) que
        # ens permetran actualitzar el jugador en funció d'elles
        self.esquerra = False
        self.dreta = False
        self.amunt = False
        self.avall = False

    def update(self, dt, joc):
        # Actualitzem el moviment lateral
        if self.dreta and self.esquerra:
            # Si estem anant cap a la dreta i l'esquerra alhora, no fem res
            pass
        elif self.esquerra:
            # Anem cap a l'esquerra si no xoquem amb el principi de la pantalla
            if self.rect.left <= 0:
                self.rect.left = 0
            else:
                self.rect.x -= self.vx * dt
        elif self.dreta:
            # Anem cap a l'esquerra si no xoquem amb el principi de la pantalla
            if self.rect.right >= joc.amplada:
                self.rect.right = joc.amplada
            else:
                self.rect.x += self.vx * dt

        # Actualitzem el moviment vertical
        if self.amunt and self.avall:
            pass
        elif self.amunt:
            self.rect.y -= self.vy * dt
        elif self.avall:
            self.rect.y += self.vy * dt
