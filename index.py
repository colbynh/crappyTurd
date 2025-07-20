import pygame
import random
from pygame.locals import *

pygame.init()

COLOR_WHITE = pygame.Color(255, 255, 255)   # White
COLOR_BROWN = pygame.Color(139, 69, 19)    # Brown
COLOR_GREEN = pygame.Color(0, 255, 0)      # Green
COLOR_RED = pygame.Color(255, 0, 0)        # Red

# Initialize the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill(COLOR_WHITE)  # Fill the screen with black

GRAVITY = 1  # Gravity constant
GAP = 150  # Gap between pipes
GUTTER = 75 # Gutter space at the top and bottom of the screen

# Set up the game clock
FPS = 30
clock = pygame.time.Clock()

pygame.display.set_caption('Crappy Turd')

# Define some game objects
class Pipes(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__()
        self.bottomSprite = pygame.sprite.Sprite()
        self.reset()
        self.speed = 8

      def reset(self):
        topPipeMaxY = random.randint(GUTTER, round((SCREEN_HEIGHT - GUTTER - GAP)))

        # self.image = pygame.image.load("enemy.png")
        self.image = pygame.Surface((50, topPipeMaxY))
        self.image.fill(COLOR_GREEN)  # Fill the enemy rectangle with black color

        self.rect = self.image.get_rect()
        self.rect.topleft = (SCREEN_WIDTH, 0)

        self.bottomSprite.image = pygame.Surface((50, SCREEN_HEIGHT - topPipeMaxY - GAP))
        self.bottomSprite.image.fill(COLOR_GREEN)  # Fill the enemy rectangle with black color

        self.bottomSprite.rect = self.bottomSprite.image.get_rect()
        self.bottomSprite.rect.bottomleft = (SCREEN_WIDTH, SCREEN_HEIGHT)


      def update(self):
        if self.rect.centerx > 0:
          self.rect.center = (self.rect.centerx - self.speed, self.rect.centery)
          self.bottomSprite.rect.center = (self.bottomSprite.rect.centerx - self.speed, self.bottomSprite.rect.centery)
        # else:
        #   self.reset()


      def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.bottomSprite.image, self.bottomSprite.rect)


class Turd(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load("Player.png")
        # self.rect = self.image.get_rect()
        self.image = pygame.Surface((40, 40))
        self.image.fill(COLOR_BROWN)
        self.rect = self.image.get_rect()
        self.rect.center = (160, SCREEN_HEIGHT / 2)
        self.velocity = 0
        self.speed = 4

    def update(self):
        if self.velocity < self.speed * 3:
          self.velocity += GRAVITY

        pressed_keys = pygame.key.get_pressed()

        if self.rect.centery > self.speed * 2.5:
              if pressed_keys[K_SPACE]:
                  self.velocity = -self.speed * 2.5

        self.rect.centery += self.velocity

    def draw(self, surface):
        surface.blit(self.image, self.rect)


turd = Turd()
pipes = [Pipes()]

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
    turd.update()

    for pipe in pipes:
      pipe.update()
      pipe.draw(SCREEN)

    if pipes[0].rect.centerx < SCREEN_WIDTH - 200:
      pipes.insert(0,Pipes())

    # Remove pipes that have moved off the screen
    if pipes and pipes[-1].rect.right <= 0:
      pipes.pop()

    SCREEN.fill(COLOR_WHITE)  # Fill the screen with white
    turd.draw(SCREEN)
    for pipe in pipes:
      pipe.draw(SCREEN)

    for pipe in pipes:
        if turd.rect.colliderect(pipe.rect) or turd.rect.colliderect(pipe.bottomSprite.rect):
            print("Collision detected!")
            pygame.quit()
            exit()


    pygame.display.flip()  # Update the display
    clock.tick(FPS)  # Limit the frame rate to 30 FPS


# Clean up and exit
pygame.quit()
exit()
