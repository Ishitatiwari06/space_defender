import pygame
import random
import time

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup FPS and clock
FPS = 60
clock = pygame.time.Clock()

time.sleep(0.5)  # small delay before fullscreen start

# Load sound and set volume
shoot_sound = pygame.mixer.Sound("sound.mp3")
shoot_sound.set_volume(0.4)

# Create fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

pygame.display.set_caption("Space Defender")

# Load and scale background image
space_bg = pygame.image.load("space_bg.jpg")
space_bg = pygame.transform.scale(space_bg, (WIDTH, HEIGHT))

# Load and scale spaceship and enemy images
spaceship_img = pygame.image.load("anyrgb.com.png")
enemy_img = pygame.image.load("space-invaders.png")
spaceship_img = pygame.transform.scale(spaceship_img, (50, 30))
enemy_img = pygame.transform.scale(enemy_img, (40, 30))

player_width, player_height = spaceship_img.get_size()
enemy_width, enemy_height = enemy_img.get_size()

# Player starting position
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 20

player_speed = 5

# Enemy setup
enemies = []
enemy_speed = 3

for _ in range(5):
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-1000, -40)
    enemies.append([x, y])

# Bullets
bullets = []
bullet_width, bullet_height = 5, 10
bullet_speed = 7

# Font and score
font = pygame.font.SysFont(None, 36)
score = 0
game_over = False

# Bullet firing cooldown (milliseconds)
last_shot = 0
cooldown = 300

running = True
# Button setup
button_width = 200
button_height = 60
button_x = WIDTH // 2 - button_width // 2
button_y = HEIGHT // 2 - button_height // 2
button_color = (0, 128, 255)
button_hover_color = (0, 180, 255)
button_text = font.render("START GAME", True, WHITE)

game_started = False  # Track whether the game has started
# Show start screen until player clicks the button
while not game_started:
    screen.fill(BLACK)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Button hover effect
    if button_x < mouse[0] < button_x + button_width and button_y < mouse[1] < button_y + button_height:
        pygame.draw.rect(screen, button_hover_color, (button_x, button_y, button_width, button_height))
        if click[0] == 1:  # Left mouse click
            pygame.time.delay(200)  # Small delay to prevent double-click
            game_started = True
    else:
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))

    # Draw button text centered
    screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2,
                              button_y + button_height // 2 - button_text.get_height() // 2))

    pygame.display.update()

    # Handle quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
while running:
    clock.tick(FPS)

    screen.blit(space_bg, (0, 0))

    # Get mouse position for player movement
    mouse_x, _ = pygame.mouse.get_pos()
    player_x = mouse_x - player_width // 2
    # Keep player within screen bounds
    player_x = max(0, min(WIDTH - player_width, player_x))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Exit fullscreen game on ESC key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # Fire bullet on mouse click with cooldown
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - last_shot > cooldown:
                bullets.append([player_x + player_width // 2, player_y])
                last_shot = current_time
                shoot_sound.play()

    # Move and draw bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, (0, 255, 0), (bullet[0], bullet[1], bullet_width, bullet_height))
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Move and draw enemies
    for enemy in enemies[:]:
        enemy[1] += enemy_speed
        screen.blit(enemy_img, (enemy[0], enemy[1]))
        if enemy[1] > HEIGHT:
            enemy[1] = random.randint(-100, -40)
            enemy[0] = random.randint(0, WIDTH - enemy_width)

    # Bullet-enemy collision detection
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                # Respawn enemy at random top position
                new_x = random.randint(0, WIDTH - enemy_width)
                new_y = random.randint(-100, -40)
                enemies.append([new_x, new_y])
                break

    # Draw player
    screen.blit(spaceship_img, (player_x, player_y))

    # Player-enemy collision detection
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            game_over = True

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(3000)
        running = False

    pygame.display.update()
def draw_button(screen, x, y, w, h, text, font, base_color, hover_color):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        if click[0]:
            pygame.time.delay(200)
            return True
    else:
        pygame.draw.rect(screen, base_color, rect)
    text_render = font.render(text, True, (255, 255, 255))
    screen.blit(text_render, (x + (w - text_render.get_width()) // 2,
                              y + (h - text_render.get_height()) // 2))
    return False


def show_game_over_screen():
    large_font = pygame.font.SysFont(None, 72)
    medium_font = pygame.font.SysFont(None, 48)

    while True:
        screen.fill((0, 0, 0))
        game_over_text = large_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        restart_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2, 200, 60, "RESTART", medium_font, (0, 128, 255), (0, 180, 255))
        exit_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 60, "EXIT", medium_font, (128, 0, 0), (180, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if restart_clicked:
            return True  # signal to restart

        if exit_clicked:
            return False  # signal to exit

        pygame.display.update()


# Main driver code
while True:
    restarted = main_game_loop()
    if not restarted:
        break
pygame.quit()