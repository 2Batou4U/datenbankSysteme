import pygame
import random

# Fenstergröße
WIDTH = 800
HEIGHT = 600

# Farben
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


# Regentropfen-Klasse
class Raindrop(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(-50, -10)
        self.speed = random.randint(5, 15)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = random.randint(-50, -10)
            self.speed = random.randint(5, 15)


# Initialisierung
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Regen Simulation")
clock = pygame.time.Clock()

# Regentropfen-Gruppe
all_sprites = pygame.sprite.Group()
for _ in range(100):
    raindrop = Raindrop()
    all_sprites.add(raindrop)

# Hauptprogrammschleife
running = True
while running:
    # Ereignisse abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hintergrund löschen
    screen.fill(BLACK)

    # Regentropfen aktualisieren und zeichnen
    all_sprites.update()
    all_sprites.draw(screen)

    # Fenster aktualisieren
    pygame.display.flip()

    # Begrenzung der Framerate
    clock.tick(30)

# Pygame beenden
pygame.quit()
