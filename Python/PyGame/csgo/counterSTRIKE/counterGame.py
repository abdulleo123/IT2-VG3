import pygame
import os
import random

pygame.init()
pygame.mixer.init()

# Constants for screen size
WIDTH, HEIGHT = 900, 500
RED = (255, 0, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load image
image_path = os.path.join('Assets', 'terror.png')
enemy_image = pygame.image.load(image_path).convert_alpha()
enemy_width, enemy_height = enemy_image.get_width(), enemy_image.get_height()

class Game:
    def __init__(self):
        self.objects = []
        self.lives = 10

    def spawn_object(self):
        # Add a new falling object at a random x-position
        x = random.randint(0, WIDTH - enemy_width)
        y = random.randint(0, HEIGHT - enemy_height)
        self.objects.append(Enemy(x, y, enemy_width, enemy_height, enemy_image))

    def update(self):
        # Create a copy of the list to avoid modifying it while iterating
        for obj in self.objects[:]:
            # Update the object if necessary
            if obj.rect.y >= HEIGHT:
                self.objects.remove(obj)
                self.lives -= 1
                print("Object removed")

    def check_collisions(self, crosshair):
        for obj in self.objects[:]:
            if crosshair.get_rect().colliderect(obj.get_rect()):
                self.objects.remove(obj)
                print("Collision!")

class Enemy:
    def __init__(self, x, y, width, height, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))

    def get_rect(self):
        return self.rect

class Crosshair:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2

    def draw(self, screen):
        # Draw the crosshair
        pygame.draw.line(screen, RED, (self.x - 30, self.y), (self.x + 30, self.y), 4)
        pygame.draw.line(screen, RED, (self.x, self.y - 30), (self.x, self.y + 30), 4)

    def get_rect(self):
        return pygame.Rect(self.x - 10, self.y - 10, 20, 20)

game = Game()
crosshair = Crosshair()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or game.lives <= 0:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for collisions when the mouse is clicked
            game.check_collisions(crosshair)

    # Update the crosshair position to the mouse position
    crosshair.x, crosshair.y = pygame.mouse.get_pos()

    # Spawn new objects with a certain probability each frame
    if random.random() < 0.01:
        game.spawn_object()

    game.update()

    # Draw everything
    screen.fill((0, 0, 0))
    for obj in game.objects:
        obj.draw(screen)

    crosshair.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
