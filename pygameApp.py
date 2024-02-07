import pygame
import sys

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create Game Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Side-Scrolling Game")

# Fonts
font = pygame.font.Font(None, 36)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT - 100)
        self.speed = 15
        self.jump_power = 30
        self.gravity = 2
        self.vel_y = 0
        self.is_jumping = False
        self.health = 100
        self.max_health = 100
        self.lives = 5

    def update(self):
        # Apply gravity
        self.vel_y += self.gravity
        # Limit gravity speed
        if self.vel_y > 10:
            self.vel_y = 10
        # Apply vertical movement
        self.rect.y += self.vel_y
        # Check for ground collision
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.is_jumping = False
            self.vel_y = 0

    def jump(self):
        if not self.is_jumping:
            self.vel_y -= self.jump_power
            self.is_jumping = True
            
    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed
                
    def shoot(self):
        pass  # Implement shooting logic

# Projectile Class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Collectible Class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if self.type == "health":
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
        elif self.type == "life":
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Game Over Screen
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - game_over_text.get_height()//2))
    pygame.display.flip()
    pygame.time.wait(2000)

# Game Loop
def main():
    running = True
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    for i in range(5):
        enemy = Enemy(WIDTH + i * 200, HEIGHT - 100)
        all_sprites.add(enemy)
        enemies.add(enemy)

    for i in range(3):
        collectible = Collectible(WIDTH + i * 300, HEIGHT - 100, "health")
        all_sprites.add(collectible)
        collectibles.add(collectible)

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                elif event.key == pygame.K_LEFT:
                    player.move_left()
                elif event.key == pygame.K_RIGHT:
                    player.move_right()

        # Update game elements
        all_sprites.update()

        # Check for collisions
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 10
            if player.health <= 0:
                player.lives -= 1
                if player.lives <= 0:
                    game_over_screen()
                    running = False
                else:
                    player.health = player.max_health

        collect_hits = pygame.sprite.spritecollide(player, collectibles, True)
        for collect_hit in collect_hits:
            if collect_hit.type == "health":
                player.health += 20
                if player.health > player.max_health:
                    player.health = player.max_health
            elif collect_hit.type == "life":
                player.lives += 1

        # Draw everything to the screen
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw health bar
        pygame.draw.rect(screen, GREEN, (10, 10, player.health, 20))
        pygame.draw.rect(screen, WHITE, (10, 10, player.max_health, 20), 2)

        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()
