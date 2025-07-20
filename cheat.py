import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PIPE_COLOR = (0, 200, 0)
BIRD_COLOR = (255, 200, 0)

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -8
PIPE_GAP = 150
PIPE_WIDTH = 60
PIPE_SPEED = 3
FPS = 60

# Bird class
class Bird:
  def __init__(self):
    self.x = 60
    self.y = HEIGHT // 2
    self.radius = 20
    self.vel = 0

  def update(self):
    self.vel += GRAVITY
    self.y += self.vel

  def jump(self):
    self.vel = BIRD_JUMP

  def draw(self):
    pygame.draw.circle(SCREEN, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)

  def get_rect(self):
    return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

# Pipe class
class Pipe:
  def __init__(self):
    self.x = WIDTH
    self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)
    self.passed = False

  def update(self):
    self.x -= PIPE_SPEED

  def draw(self):
    # Top pipe
    pygame.draw.rect(SCREEN, PIPE_COLOR, (self.x, 0, PIPE_WIDTH, self.height))
    # Bottom pipe
    pygame.draw.rect(SCREEN, PIPE_COLOR, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP))

  def collide(self, bird):
    bird_rect = bird.get_rect()
    top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
    bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - self.height - PIPE_GAP)
    return bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect)

def draw_text(text, size, x, y):
  font = pygame.font.SysFont("Arial", size)
  label = font.render(text, True, BLACK)
  SCREEN.blit(label, (x, y))

def main():
  clock = pygame.time.Clock()
  bird = Bird()
  pipes = [Pipe()]
  score = 0
  running = True
  game_over = False

  while running:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      if not game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        bird.jump()
      if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        main()
        return

    if not game_over:
      bird.update()
      remove = []
      add_pipe = False
      for pipe in pipes:
        pipe.update()
        if pipe.collide(bird):
          game_over = True
        if pipe.x + PIPE_WIDTH < 0:
          remove.append(pipe)
        if not pipe.passed and pipe.x < bird.x:
          pipe.passed = True
          score += 1
          add_pipe = True
      if add_pipe:
        pipes.append(Pipe())
      for r in remove:
        pipes.remove(r)
      if bird.y - bird.radius < 0 or bird.y + bird.radius > HEIGHT:
        game_over = True

    SCREEN.fill(WHITE)
    for pipe in pipes:
      pipe.draw()
    bird.draw()
    draw_text(f"Score: {score}", 32, 10, 10)
    if game_over:
      draw_text("Game Over! Press R to Restart", 28, 40, HEIGHT//2 - 30)
    pygame.display.flip()

  pygame.quit()
  sys.exit()

if __name__ == "__main__":
  main()