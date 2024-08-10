import pygame
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Load assets
def load_image(name):
    path = os.path.join('assets', name)
    return pygame.image.load(path).convert_alpha()

player_img = load_image('player.png')
alien_img = load_image('alien.png')
bullet_img = load_image('bullet.png')

# Load sounds
def load_sound(name):
    path = os.path.join('assets', name)
    return pygame.mixer.Sound(path)

shoot_sound = load_sound('shoot.wav')
explosion_sound = load_sound('explosion.wav')

# Set up clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to draw text on the screen
def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Main loop flag
running = True

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -5
        if keys[pygame.K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # Kill the bullet if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player instance
player = Player()
all_sprites.add(player)
