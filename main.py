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
