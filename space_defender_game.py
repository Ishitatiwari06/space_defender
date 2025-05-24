import pygame
import random
import time
import os

high_score = 0

# Load high score from file
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())

# Initialize pygame
pygame.init()

# Load and play background music
pygame.mixer.music.load("background_music.mp3") 
pygame.mixer.music.set_volume(0.5)               # Volume: 0.0 to 1.0
pygame.mixer.music.play(-1)                      # -1 means infinite loop

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup FPS and clock
FPS = 60 #frames per second
clock = pygame.time.Clock()
time.sleep(0.5)

# Load sound and set volume
shoot_sound = pygame.mixer.Sound("sound.mp3")
shoot_sound.set_volume(0.4)

# Create fullscreen window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
pygame.display.set_caption("Space Defender")  #only displayed when switching b/w tabs or not inb full screen

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

# Font
font = pygame.font.SysFont(None, 36) 

# Button drawing function
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
    text_render = font.render(text, True, WHITE) #true for smooth edges
    screen.blit(text_render, (x + (w - text_render.get_width()) // 2,
                              y + (h - text_render.get_height()) // 2)) #horizontal center or vertical center
    return False

# Game Over screen with restart/exit buttons
def show_game_over_screen(score, high_score):
    large_font = pygame.font.SysFont(None, 72)
    medium_font = pygame.font.SysFont(None, 48)
    pygame.mixer.music.stop()
    while True:
        screen.fill(BLACK)
        score_text = font.render(f"Your Score: {score}", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 100)) #to center the text
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 - 60))

        game_over_text = large_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        restart_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2, 200, 60, "RESTART", medium_font, (0, 128, 255), (0, 180, 255))
        exit_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 60, "EXIT", medium_font, (128, 0, 0), (180, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if restart_clicked:
            return True  # Restart
        if exit_clicked:
            pygame.quit()
            exit()
        
        pygame.display.update() #or pygame.display.flip()

# Start screen
def show_start_screen():
    button_width = 200
    button_height = 60
    button_x = WIDTH // 2 - button_width // 2
    button_y = HEIGHT // 2 - button_height // 2
    button_color = (0, 128, 255)
    button_hover_color = (0, 180, 255)
    button_text = font.render("START GAME", True, WHITE)
    quit_x = WIDTH // 2 - button_width // 2
    quit_y = HEIGHT // 2 + 40
    while True:
        screen.fill(BLACK)
        if draw_button(screen, button_x, button_y, button_width, button_height, "START GAME", font, button_color, button_hover_color):
            return
        if draw_button(screen, quit_x, quit_y, button_width, button_height, "QUIT", font, button_color, button_hover_color):
            pygame.quit()
            exit()
        screen.blit(button_text, (button_x + button_width // 2 - button_text.get_width() // 2,
                                  button_y + button_height // 2 - button_text.get_height() // 2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.update()

def show_pause_screen():
    large_font = pygame.font.SysFont(None, 72)
    medium_font = pygame.font.SysFont(None, 48)
    paused = True

    while paused:
        screen.fill(BLACK)
        pause_text = large_font.render("PAUSED", True, (255, 255, 0))
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 4))

        resume_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2, 200, 60, "RESUME", medium_font, (0, 128, 255), (0, 180, 255))
        restart_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2 + 80, 200, 60, "RESTART", medium_font, (0, 128, 255), (0, 180, 255))
        exit_clicked = draw_button(screen, WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 60, "EXIT", medium_font, (128, 0, 0), (180, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        if resume_clicked:
            paused = False
        if restart_clicked:
            return "restart"
        if exit_clicked:
            pygame.quit()
            exit()

        pygame.display.update()


# Main game function
def run_game():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
    # Player starting position
    player_x = WIDTH // 2 - player_width // 2  #center
    player_y = HEIGHT - player_height - 20     #bottom
    player_speed = 10

    # Enemy setup
    enemies = []
    enemy_speed = 3
    for _ in range(5):
        x = random.randint(0, WIDTH - enemy_width)
        y = random.randint(-1000, -40)
        enemies.append([x, y])

    # Bullets
    bullets = []
    enemy_bullets = []
    enemy_bullet_width, enemy_bullet_height = 5, 10
    enemy_bullet_speed = 5
    enemy_shoot_delay = 1000  # milliseconds
    last_enemy_shot_time = 0
    bullet_width, bullet_height = 5, 10
    bullet_speed = 7

    # Score and state
    score = 0
    speed_increment_milestone = 0
    global high_score
    game_over = False
    last_shot = 0
    cooldown = 200
    running = True

    while running:
        clock.tick(FPS)  #control game frame rate
        screen.blit(space_bg, (0, 0)) #clear and redraw the background in every frame

        # Player movement by mouse
        mouse_x, _ = pygame.mouse.get_pos()
        player_x = mouse_x - player_width // 2
        player_x = max(0, min(WIDTH - player_width, player_x))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                    elif event.key == pygame.K_SPACE:
                        # Pause the game and check if restart was clicked
                        result = show_pause_screen()
                        if result == "restart":
                            return True  # to restart the game from run_game caller

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            #shooting bullets
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_time = pygame.time.get_ticks()
                if current_time - last_shot > cooldown:
                    bullets.append([player_x + player_width // 2, player_y])
                    last_shot = current_time
                    shoot_sound.play()
                

        # Move and draw bullets
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed #make the bullet go upward
            pygame.draw.rect(screen, (0, 255, 0), (bullet[0], bullet[1], bullet_width, bullet_height))
            if bullet[1] < 0:
                bullets.remove(bullet)

        # Move and draw enemies
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            screen.blit(enemy_img, (enemy[0], enemy[1])) #shift enemy as it move down
            if enemy[1] > HEIGHT:
                enemy[1] = random.randint(-100, -40)
                enemy[0] = random.randint(0, WIDTH - enemy_width)

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_shot_time > enemy_shoot_delay:
            for enemy in enemies:
                if random.random() < 0.3:  # 30% chance to shoot per enemy
                    bullet_x = enemy[0] + enemy_width // 2
                    bullet_y = enemy[1] + enemy_height
                    enemy_bullets.append([bullet_x, bullet_y])
            last_enemy_shot_time = current_time
        for bullet in enemy_bullets[:]:
            bullet[1] += enemy_bullet_speed
            pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))
            if bullet[1] > HEIGHT:
                enemy_bullets.remove(bullet)
            elif pygame.Rect(bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height).colliderect(
                pygame.Rect(player_x, player_y, player_width, player_height)):
                game_over = True
                break

        # Bullet-enemy collision
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
            for enemy in enemies[:]:
                enemy_rect = pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1

                    # Speed up every 10 points
                    if score % 10 == 0 and score > speed_increment_milestone:
                        enemy_speed += 0.5  
                        speed_increment_milestone = score

                    enemies.append([random.randint(0, WIDTH - enemy_width), random.randint(-100, -40)])
                    break


        # Draw player
        screen.blit(spaceship_img, (player_x, player_y))
        # Draw enemy bullets
        for bullet in enemy_bullets:
            pygame.draw.rect(screen, (255, 0, 0), (bullet[0], bullet[1], enemy_bullet_width, enemy_bullet_height))

        # Check for collision
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for enemy in enemies:
            if player_rect.colliderect(pygame.Rect(enemy[0], enemy[1], enemy_width, enemy_height)):
                game_over = True

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE) #text to render image
        screen.blit(score_text, (10, 10)) #draw score text image at (10,10)
        high_score_display = font.render(f"High Score: {high_score}", True, WHITE)
        screen.blit(high_score_display, (WIDTH - high_score_display.get_width() - 10, 10))

        pygame.display.update()

        if game_over:
            pygame.time.delay(1000)
            if show_game_over_screen(score, high_score):
                run_game()  # Restart
            return
        # Update high score if needed
        if score > high_score:
            high_score = score
            with open("high_score.txt", "w") as file:
                file.write(str(high_score))
            
    
        

# Show start screen and run the game
show_start_screen()
while True:
    restart = run_game()
    if not restart:
        break

