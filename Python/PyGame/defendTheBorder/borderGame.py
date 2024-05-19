import pygame
import os
import sys
import random

# Initialize Pygame modules
pygame.font.init()
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 900, 500
BORDER = pygame.Rect(WIDTH / 2 - 5, 0, 10, HEIGHT)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

PLAYER_WIDTH, PLAYER_HEIGHT = 115, 90

FPS = 60
VEL = 5

MAX_BULLETS = 3
BULLET_VEL = 8

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

PLAYER_HIT = pygame.USEREVENT + 1
ENEMY_HIT = pygame.USEREVENT + 2

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SoldierDuel2D")

# Load assets
PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'militaryPlayer.png'))
PLAYER = pygame.transform.rotate(pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)

ENEMY_IMAGE = pygame.image.load(os.path.join('Assets', 'player2.png'))
ENEMY = pygame.transform.rotate(pygame.transform.scale(ENEMY_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0)

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.jpg")), (WIDTH, HEIGHT))

class Soldier:
    def __init__(self, x, y, width, height, image, keys):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = image
        self.keys = keys
        self.bullets = []
        self.health = 10

    def shoot(self):
        if len(self.bullets) < MAX_BULLETS:
            bullet = pygame.Rect(self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2 - 2, 10, 5)
            self.bullets.append(bullet)

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, YELLOW if self.keys['shoot'] == pygame.K_LCTRL else RED, bullet)

class Enemy:
    def __init__(self, width, height, image):
        self.rect = pygame.Rect(random.randint(WIDTH//2 + 100, WIDTH - 50), random.randint(0, HEIGHT - height), width, height)
        self.image = image
        self.bullets = []
        self.health = 3  # Decreased initial health
        self.shoot_timer = 0

    def shoot(self):
        if len(self.bullets) < MAX_BULLETS:
            bullet = pygame.Rect(self.rect.x, self.rect.y + self.rect.height // 2 - 2, 10, 5)
            self.bullets.append(bullet)

    def draw(self, WIN):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, RED, bullet)

def handle_player_movement(keys_pressed, player):
    if keys_pressed[pygame.K_a] and player.rect.x - VEL > 0:  # LEFT
        player.rect.x -= VEL
    if keys_pressed[pygame.K_d] and player.rect.x + VEL + player.rect.width < BORDER.x:  # RIGHT
        player.rect.x += VEL
    if keys_pressed[pygame.K_w] and player.rect.y - VEL > 0:  # UP
        player.rect.y -= VEL
    if keys_pressed[pygame.K_s] and player.rect.y + VEL + player.rect.height < HEIGHT:  # DOWN
        player.rect.y += VEL

def draw_window(player, enemies):
    WIN.blit(BACKGROUND, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    player_health_text = HEALTH_FONT.render("Health: " + str(player.health), 1, WHITE)
    WIN.blit(player_health_text, (10, 10))

    player.draw(WIN)
    for enemy in enemies:
        enemy.draw(WIN)

    pygame.display.update()

def handle_bullets(player, enemies):
    for bullet in player.bullets:
        bullet.x += BULLET_VEL
        for enemy in enemies:
            if enemy.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(ENEMY_HIT, {'enemy': enemy}))
                player.bullets.remove(bullet)
                break
        if bullet.x > WIDTH:
            player.bullets.remove(bullet)

    for enemy in enemies:
        for bullet in enemy.bullets:
            bullet.x -= BULLET_VEL
            if player.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(PLAYER_HIT))
                enemy.bullets.remove(bullet)
            elif bullet.x < 0:
                enemy.bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    player = Soldier(100, 300, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER, {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'shoot': pygame.K_LCTRL})
    enemies = [Enemy(PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY)]

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == player.keys['shoot']:
                    player.shoot()

            if event.type == ENEMY_HIT:
                hit_enemy = event.dict['enemy']
                hit_enemy.health -= 1
                if hit_enemy.health <= 0:
                    enemies.remove(hit_enemy)

            if event.type == PLAYER_HIT:
                player.health -= 1

        winner_text = ""
        if player.health <= 0:
            winner_text = "Enemies Win!"

        if not enemies:
            winner_text = "Player Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        handle_player_movement(keys_pressed, player)

        handle_bullets(player, enemies)
        draw_window(player, enemies)

        # Randomly spawn a new enemy every 5 seconds
        if random.random() < 0.01:
            if len(enemies) < 5:
                enemies.append(Enemy(PLAYER_WIDTH, PLAYER_HEIGHT, ENEMY))

        # Make enemies shoot back
        for enemy in enemies:
            enemy.shoot_timer += 1
            if enemy.shoot_timer >= FPS:  # Enemies shoot every second
                enemy.shoot()
                enemy.shoot_timer = 0

    main()

if __name__ == "__main__":
    main()
