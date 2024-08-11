import pygame
import os
import random

# Initialize Pygame
pygame.init()

# Initialize score and lives
score = 0
lives = 3
start_time = pygame.time.get_ticks()

# Game States
START_SCREEN = 0
PLAYING = 1
PAUSED = 2
GAME_OVER = 3
WIN = 4

# Initial game state
game_state = START_SCREEN

# Main loop flag
running = True

# Constants
FULLSCREEN = pygame.FULLSCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fullscreen state
fullscreen = False

# Function to set the screen mode
def set_screen_mode():
    global screen, fullscreen
    if fullscreen:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Center the window on the screen
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    
    pygame.display.set_caption("Shooter Game")

# Initialize screen
set_screen_mode()

# Load assets
def load_image(name):
    path = os.path.join('assets', name)
    return pygame.image.load(path).convert_alpha()

player_img = load_image('player.png')
player_img = pygame.transform.scale(player_img, (65, 65))
alien_img = load_image('alien.png')
alien_img = pygame.transform.scale(alien_img, (65, 65))
bullet_img = load_image('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (65, 65))
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

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()

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

# Alien class
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 2

    def update(self):
        self.rect.x += self.speedx
        # Change direction and move down if it hits the screen edge
        if self.rect.right > SCREEN_WIDTH or self.rect.left < 0:
            self.speedx *= -1.3
            self.rect.y += 30

# Function to create a fleet of aliens
def create_fleet():
    alien_rows = 5
    alien_cols = 10
    alien_spacing_x = 60
    alien_spacing_y = 60
    fleet = pygame.sprite.Group()

    for row in range(alien_rows):
        for col in range(alien_cols):
            alien = Alien(
                x=col * alien_spacing_x + 50,
                y=row * alien_spacing_y + 80
            )
            all_sprites.add(alien)
            fleet.add(alien)
    
    return fleet

# Create the fleet of aliens
aliens = create_fleet()

# Create player instance
player = Player()
all_sprites.add(player)

# Collision detection and game logic
def handle_collisions():
    global score, lives

    # Check for bullet-alien collisions
    hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()

    # Check for alien-player collisions
    collisions = pygame.sprite.spritecollide(player, aliens, True)
    if collisions:
        lives -= 1
        explosion_sound.play()
        if lives <= 0:
            game_over()

    # Check if all aliens are destroyed
    if not aliens:
        you_win()

def game_over():
    global running
    draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds
    running = False

def you_win():
    global running, game_state, start_time

    # Clear all sprites
    all_sprites.empty()
    aliens.empty()
    bullets.empty()

    # Calculate elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    # Update the display
    screen.fill(BLACK)
    pygame.display.flip()

    # Wait for 1 second
    pygame.time.wait(150)

    # Draw win screen with statistics
    screen.fill(BLACK)
    draw_text(screen, "YOU WIN!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, f"Time: {elapsed_time} seconds", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    draw_text(screen, "Press ENTER to Restart", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2)
    pygame.display.flip()

    game_state = WIN

def draw_score_and_lives(surface):
    draw_text(surface, f"Score: {score}", 24, SCREEN_WIDTH - 100, 10)
    draw_text(surface, f"Lives: {lives}", 24, 100, 10)

def draw_timer(surface):
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    draw_text(surface, f"Time: {elapsed_time} seconds", 24, SCREEN_WIDTH // 2, 10)

def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, "Shooter Game", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, "Press ENTER to Start", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press F to Toggle Fullscreen", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    pygame.display.flip()

def show_game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press ENTER to Restart", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    pygame.display.flip()

def show_win_screen():
    screen.fill(BLACK)
    draw_text(screen, "YOU WIN!", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(screen, f"Score: {score}", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text(screen, "Press ENTER to Restart", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2)
    pygame.display.flip()

def show_pause_screen():
    screen.fill(BLACK)
    draw_text(screen, "PAUSED", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(screen, "Press ESC to Resume", 36, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()

# Main game loop
while running:
    if game_state == START_SCREEN:
        show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press ENTER to start the game
                    game_state = PLAYING
                elif event.key == pygame.K_f:  # Press F to toggle fullscreen
                    fullscreen = not fullscreen
                    set_screen_mode()

    elif game_state == PLAYING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Press SPACE to shoot
                    player.shoot()
                elif event.key == pygame.K_f:  # Press F to toggle fullscreen
                    fullscreen = not fullscreen
                    set_screen_mode()
                elif event.key == pygame.K_ESCAPE:  # Press ESC to pause
                    game_state = PAUSED

        # Update all sprites
        all_sprites.update()

        # Handle collisions
        handle_collisions()

        # Clear the screen
        screen.fill(BLACK)

        # Draw all sprites
        all_sprites.draw(screen)

        # Draw score, lives, and timer
        draw_score_and_lives(screen)
        draw_timer(screen)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    elif game_state == PAUSED:
        show_pause_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to resume
                    game_state = PLAYING

    elif game_state == GAME_OVER:
        show_game_over_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press ENTER to restart the game
                    # Reset game state
                    score = 0
                    lives = 3
                    start_time = pygame.time.get_ticks()  # Reset start time
                    all_sprites.empty()
                    aliens = create_fleet()
                    player = Player()
                    all_sprites.add(player)
                    game_state = PLAYING

    elif game_state == WIN:
        show_win_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press ENTER to restart the game
                    # Reset game state
                    score = 0
                    lives = 3
                    start_time = pygame.time.get_ticks()  # Reset start time
                    all_sprites.empty()
                    aliens = create_fleet()
                    player = Player()
                    all_sprites.add(player)
                    game_state = PLAYING

pygame.quit()
