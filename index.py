import pygame
import random
from pygame.locals import *

pygame.init()

# TODO - refine pipe sprite
# TODO - explosion on collision? OR spawn a buch of turds?

COLOR_WHITE = pygame.Color(255, 255, 255)   # White
COLOR_BROWN = pygame.Color(139, 69, 19)    # Brown
COLOR_GREEN = pygame.Color(0, 255, 0)      # Green
COLOR_BLACK = pygame.Color(0, 0, 0)        # Black
COLOR_RED = pygame.Color(255, 0, 0)        # Red
COLOR_SKY_BLUE = pygame.Color(135, 206, 235)  # Sky Blue

# Initialize the game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN.fill(COLOR_SKY_BLUE)  # Fill the screen with black

GRAVITY = 1.9  # Gravity constant
GAP = 150  # Gap between pipes
GUTTER = 75 # Gutter space at the top and bottom of the screen
START_X = 160 # Starting X position for the turd
# sizeOfGrid = 50  # Size of the grid for the game
font = pygame.font.Font(None, 36)  # Font for rendering text

previous_score = 0
best_score = 0
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

        self.image = pygame.Surface((50, topPipeMaxY), 0, 32)
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

      def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.bottomSprite.image, self.bottomSprite.rect)

class Turd(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("turd.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (START_X, SCREEN_HEIGHT / 2)
        self.velocity = 0
        self.speed = 4

    def update(self):
        if self.velocity < self.speed * 3:
          self.velocity += GRAVITY

        pressed_keys = pygame.key.get_pressed()

        if self.rect.centery > self.speed * 2.5:
              if pressed_keys[K_RETURN]:
                  self.velocity = -self.speed * 2.5

        self.rect.centery += self.velocity

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, size, speed):
        super().__init__()
        self.image = pygame.image.load("cloud.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT - size[1]))
        self.speed = speed

    def update(self):
        self.rect.centerx -= self.speed
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def main():
    global previous_score
    global best_score
    best_score_isset = False
    turd = Turd()
    pipes = [Pipes()]
    clouds = [Cloud((50, 50), 1), Cloud((100, 100), 3)]  # List of clouds
    score = 0 

    # Main game loop
    check = False
    gameOver = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                if gameOver == True:
                  if event.key == K_RETURN:
                    print(f"previous score: {score}")
                    previous_score = score
                    main()
                    return

        if gameOver:
            text = font.render("hit return to restart", 1, COLOR_BLACK)
            SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        if not gameOver:
          # Your game logic and rendering code would go here

          for cloud in clouds:
            cloud.update()

          for pipe in pipes:
            pipe.update()

          turd.update()

          if pipes[0].rect.centerx < SCREEN_WIDTH - 200:
            pipes.insert(0,Pipes())

          if clouds[0].rect.centerx < SCREEN_WIDTH - 200:
            clouds.insert(0,Cloud((50, 50), 1))
            clouds.insert(0,Cloud((100, 100), 3))

          # Remove pipes that have moved off the screen
          if pipes and pipes[-1].rect.left <= 0:
            pipes.pop()
            check = False

          SCREEN.fill(COLOR_SKY_BLUE)  # Fill the screen with white
          text = font.render("%d" % score, 1, COLOR_BLACK)
          SCREEN.blit(text, (10, 10))  # Draw the text at position (10, 10)
          
          if previous_score > 0:
            print(f"bullshit{previous_score}")
            oldscore = font.render("Previous: %d" % previous_score, 1, COLOR_BLACK)
            SCREEN.blit(oldscore, (10, 50))  # Draw below the current score

          if best_score > 0: 
             text = font.render("Best: %d" % best_score, 1, COLOR_RED)
             SCREEN.blit(text, (10, 80))  # Draw the text at position (10, 10)

          if previous_score >= best_score:
             best_score = previous_score
             text = font.render("Best: %d" % best_score, 1, COLOR_RED)
             SCREEN.blit(text, (10, 80))  # Draw the text at position (10, 10)

          for cloud in clouds:
            cloud.draw(SCREEN)

          for pipe in pipes:
            pipe.draw(SCREEN)

          turd.draw(SCREEN)

          for pipe in pipes:
              if turd.rect.colliderect(pipe.rect) or turd.rect.colliderect(pipe.bottomSprite.rect) or turd.rect.top <= 0 or turd.rect.bottom >= SCREEN_HEIGHT:
                  gameOver = True
          if pipes[-1].rect.centerx < START_X and not check:
              score += 1
              check = True

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Limit the frame rate to 30 FPS

gameStarted = False
while True:
    SCREEN.fill(COLOR_SKY_BLUE)  # Fill the screen with white

    for event in pygame.event.get():
      if event.type == QUIT:
          pygame.quit()
          exit()
      elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
              pygame.quit()
              exit()
          if event.key == K_RETURN:
            if gameStarted == False:
              gameStarted = True
              print("Game started!")
              main()

    if not gameStarted:
       text = font.render("hit return to start", 1, COLOR_BLACK)
       SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()  # Update the display
