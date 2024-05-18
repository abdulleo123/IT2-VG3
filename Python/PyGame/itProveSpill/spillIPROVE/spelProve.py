import pygame
import sys
import random
import math

# Colors
player_color = (0, 255, 0)
enemy_color = (255, 0, 0)

# Screen dimensions
WIDTH, HEIGHT = 600, 400

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = 5

    def draw(self, screen):
        pygame.draw.circle(screen, player_color, (self.x, self.y), 15)

    def kill(self, keys, enemies):
        if keys[pygame.K_SPACE]:
            enemies_to_remove = []
            for enemy in enemies:
                if math.hypot(enemy.x - self.x, enemy.y - self.y) < 190:  # Kill range is 20 pixels
                    enemies_to_remove.append(enemy)
            for enemy in enemies_to_remove:
                enemies.remove(enemy)

    def move(self, keys):
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(2, 8) 
        self.size = 15  # Fixed size for the enemy

    def draw(self, screen):
        pygame.draw.circle(screen, enemy_color, (self.x, self.y), self.size)

    def move_towards_player(self, player):
        # Calculate direction vector
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist

        # Move enemy towards player
        self.x += dx * self.speed
        self.y += dy * self.speed




def checkCollision(enemies, player):
    player_rect = pygame.Rect(player.x - 15, player.y - 15, 30, 30)  # Create player's collision rectangle

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x - enemy.size, enemy.y - enemy.size, enemy.size * 2, enemy.size * 2)  # Create enemy's collision rectangle
        if player_rect.colliderect(enemy_rect):  # Check for collision between player and enemy
            pygame.quit()
            sys.exit()

def main():
    clock = pygame.time.Clock()

    player = Player()
    enemies = []
    
    enemy_spawn_delay = 2000  # Spawn an enemy every 2000 milliseconds (2 seconds)
    last_enemy_spawn_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > enemy_spawn_delay:
            enemies.append(Enemy())
            last_enemy_spawn_time = current_time

        screen.fill((150, 0, 255))
        player.draw(screen)

        player.kill(keys, enemies)

        checkCollision(enemies, player)

        for enemy in enemies:
            enemy.move_towards_player(player)
            enemy.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
