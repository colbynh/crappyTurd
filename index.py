import pygame
import random
from pygame.locals import *

pygame.init()

COLOR_BLACK = pygame.Color(0, 0, 0)         # Black
COLOR_WHITE = pygame.Color(255, 255, 255)   # White
COLOR_GREY = pygame.Color(128, 128, 128)   # Grey
COLOR_RED = pygame.Color(255, 0, 0)       # Red

# Initialize the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill(COLOR_WHITE)  # Fill the screen with black


# Load resources (images, sounds, etc.)
# Example: background_image = pygame.image.load('background.png')
# Example: sound_effect = pygame.mixer.Sound('sound.wav')
# Set up the game clock
FPS = 20
clock = pygame.time.Clock()

pygame.display.set_caption('Crappy Turd')

# Define some game objects
class Pipe(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(COLOR_RED)  # Fill the enemy rectangle with red color
        # self.rect = self.image.get_rect()

        # x = random.randint(40,SCREEN_WIDTH-40)
        y = random.randint(40,SCREEN_HEIGHT-40)
        self.rect.center=(SCREEN_WIDTH,y)

      def update(self):
        self.rect.center = (self.rect.centerx - 5, self.rect.centery)

      def draw(self, surface):
        surface.blit(self.image, self.rect)


class Turd(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load("Player.png")
        # self.rect = self.image.get_rect()
        self.image = pygame.Surface((50, 50))
        self.image.fill(COLOR_GREY)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.centery > 5:
              if pressed_keys[K_SPACE]:
                  self.rect.center = (self.rect.centerx, self.rect.centery - 5)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


P1 = Turd()
E1 = Pipe()
E2 = Pipe()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                exit()

    # Your game logic and rendering code would go here
    P1.update()
    E1.update()
    E2.update()

    SCREEN.fill(COLOR_WHITE)  # Fill the screen with white
    P1.draw(SCREEN)
    E1.draw(SCREEN)
    E2.draw(SCREEN)

    if P1.rect.colliderect(E1.rect):
        print("Collision detected!")
        # pygame.quit()
        # exit()

    pygame.display.flip()  # Update the display
    # pygame.time.delay(100)  # Delay to control frame rate
    clock.tick(FPS)  # Limit the frame rate to 60 FPS


# Clean up and exit
pygame.quit()
exit()
