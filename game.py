import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 5
ENEMY_SPEED = 2
BULLET_SPEED = 7
ENEMY_ROWS = 5
ENEMY_COLS = 8
ENEMY_SPACING = 60
ENEMY_SHOOT_CHANCE = 0.001  # Reduced from 2% chance per enemy per frame
PLAYER_MAX_HEALTH = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# Font setup
font = pygame.font.SysFont('Arial', 48)
small_font = pygame.font.SysFont('Arial', 36)

class Player:
    def __init__(self):
        self.width = 50
        self.height = 30
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - self.height - 20
        self.speed = PLAYER_SPEED
        self.bullets = []
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.health = PLAYER_MAX_HEALTH

    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < WIDTH - self.width:
            self.x += self.speed
        self.rect.x = self.x

    def shoot(self):
        self.bullets.append([self.x + self.width // 2 - 2, self.y])

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet[1] -= BULLET_SPEED
            if bullet[1] < 0:
                self.bullets.remove(bullet)

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], 4, 10))
        # Draw health bar
        for i in range(self.health):
            pygame.draw.rect(screen, GREEN, (10 + i * 20, 10, 15, 15))

class Enemy:
    def __init__(self, x, y):
        self.width = 40
        self.height = 30
        self.x = x
        self.y = y
        self.speed = ENEMY_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self, direction):
        if direction == "right":
            self.x += self.speed
        else:
            self.x -= self.speed
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def try_shoot(self):
        if random.random() < ENEMY_SHOOT_CHANCE:  # nosec B311
            return [self.x + self.width // 2 - 2, self.y + self.height]
        return None

def create_enemies():
    enemies = []
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = col * ENEMY_SPACING + 100
            y = row * ENEMY_SPACING + 50
            enemies.append(Enemy(x, y))
    return enemies

def show_game_over_screen(win):
    screen.fill(BLACK)
    if win:
        text = font.render("You Win!", True, GREEN)
    else:
        text = font.render("Game Over", True, RED)
    restart_text = small_font.render("Press R to Play Again", True, WHITE)
    quit_text = small_font.render("Press Q to Quit", True, WHITE)
    
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 100))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    while True:  # Main game loop for restarting
        player = Player()
        enemies = create_enemies()
        enemy_direction = "right"
        enemy_bullets = []  # List to store enemy bullets
        game_over = False
        win = False

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.shoot()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.move("left")
            if keys[pygame.K_RIGHT]:
                player.move("right")

            # Update bullets
            player.update_bullets()

            # Update enemy bullets
            for bullet in enemy_bullets[:]:
                bullet[1] += BULLET_SPEED
                if bullet[1] > HEIGHT:
                    enemy_bullets.remove(bullet)
                # Check collision with player
                elif (bullet[0] >= player.x and bullet[0] <= player.x + player.width and
                      bullet[1] >= player.y and bullet[1] <= player.y + player.height):
                    enemy_bullets.remove(bullet)
                    player.health -= 1
                    if player.health <= 0:
                        game_over = True
                        win = False

            # Enemy shooting
            for enemy in enemies:
                bullet = enemy.try_shoot()
                if bullet:
                    enemy_bullets.append(bullet)

            # Move enemies
            move_down = False
            for enemy in enemies:
                if enemy.x <= 0 or enemy.x + enemy.width >= WIDTH:
                    move_down = True
                    break

            if move_down:
                enemy_direction = "left" if enemy_direction == "right" else "right"
                for enemy in enemies:
                    enemy.y += 20

            for enemy in enemies:
                enemy.move(enemy_direction)

            # Check collisions
            for bullet in player.bullets[:]:
                for enemy in enemies[:]:
                    if (bullet[0] >= enemy.x and bullet[0] <= enemy.x + enemy.width and
                        bullet[1] >= enemy.y and bullet[1] <= enemy.y + enemy.height):
                        if bullet in player.bullets:
                            player.bullets.remove(bullet)
                        if enemy in enemies:
                            enemies.remove(enemy)
                        break

            # Check if enemies reached bottom
            for enemy in enemies:
                if enemy.y + enemy.height >= HEIGHT - 50:
                    game_over = True
                    win = False
                    break

            # Check if all enemies are destroyed
            if not enemies:
                game_over = True
                win = True

            # Draw everything
            screen.fill(BLACK)
            player.draw()
            for enemy in enemies:
                enemy.draw()
            # Draw enemy bullets
            for bullet in enemy_bullets:
                pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 4, 10))

            pygame.display.flip()
            clock.tick(60)

        show_game_over_screen(win)

if __name__ == "__main__":
    main() 
