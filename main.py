import pygame
from board import Board

HEIGHT, WIDTH = 720, 1060
BLOCK_SIZE = 42.4
ROWS, COLS = 15, 23
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_START_MENU = 3

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Tiles")
clock = pygame.time.Clock()
running = True
pygame.mixer.init()
counter = 120
time_delay = 1000
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, time_delay)

# Color Tiles setup
board = Board(BLOCK_SIZE, ROWS, COLS)
state = STATE_START_MENU
has_played_game_over = False
is_dark_mode = False
is_timer_on = False
points = 0

# Load sound files
break_sound = pygame.mixer.Sound("sounds/tile_remove.mp3")
wrong_move_sound = pygame.mixer.Sound("sounds/wrong.mp3")
game_end_sound = pygame.mixer.Sound("sounds/game_end.mp3")

# Fonts setup
score_font = pygame.font.Font(None, 30)
time_font = pygame.font.Font(None, 30)
game_over_font = pygame.font.Font(None, 100)
button_font = pygame.font.Font(None, 50)

# Title setup
title = pygame.image.load("images/title.png")
title_pos = (WIDTH // 2 - title.get_width() // 2, 50)

# Start button setup
button_back = pygame.image.load("images/button_back.png")
start_button_text = button_font.render("Start", True, (255, 255, 255))
start_button_text_pos = (WIDTH // 2 - start_button_text.get_width() // 2,
                         (HEIGHT // 2 + start_button_text.get_height() // 2) + 120)
start_button_back_pos = (WIDTH // 2 - button_back.get_width() // 2, start_button_text_pos[1] - 8)
start_button_rect = button_back.get_rect(topleft=start_button_back_pos)

# Play Again button setup
play_again_button_text = button_font.render("Play Again", True, (255, 255, 255))
play_again_button_text_pos = (WIDTH // 2 - play_again_button_text.get_width() // 2,
                              HEIGHT // 2 + play_again_button_text.get_height() // 2 + 50)
play_again_button_pos = (play_again_button_text_pos[0] - 15, play_again_button_text_pos[1] - 5)
play_again_button_rect = button_back.get_rect(topleft=play_again_button_pos)

# Reset button setup
reset_button = pygame.image.load("images/reset_button.png")
reset_button_pos = (WIDTH // 2 - reset_button.get_width() // 2, 685)
reset_button_rect = reset_button.get_rect(topleft=reset_button_pos)

# Timer button setup
timer_button_on = pygame.image.load("images/timer_on.png")
timer_button_off = pygame.image.load("images/timer_off.png")
timer_button_pos = (70, 685)
timer_button_rect = timer_button_on.get_rect(topleft=timer_button_pos)

# Theme mode button
dark_mode_button = pygame.image.load("images/dark_mode.png")
light_mode_button = pygame.image.load("images/light_mode.png")
theme_mode_button_pos = (WIDTH // 2 - light_mode_button.get_width() // 2, 10)
theme_mode_button_rect = light_mode_button.get_rect(topleft=theme_mode_button_pos)

# Game over text
game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
game_over_text_pos = (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2.5 - game_over_text.get_height() // 2)

# Background setup
background = pygame.image.load('images/background.jpg').convert()
background = pygame.transform.smoothscale(background, screen.get_size())
screen.blit(background, (0, 0))

while running:
    # Poll for events
    # pygame.QUIT event means the user clicked X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if state == STATE_START_MENU and start_button_rect.collidepoint(event.pos):
                state = STATE_PLAYING
                is_timer_on = True
            elif state == STATE_GAME_OVER and play_again_button_rect.collidepoint(event.pos) or state == STATE_PLAYING and reset_button_rect.collidepoint(event.pos):
                state = STATE_PLAYING
                board.randomize_matrix()
                points = 0
                counter = 120
                has_played_game_over = False
                continue
            elif state == STATE_PLAYING:
                if timer_button_rect.collidepoint(event.pos):
                    if not is_timer_on:
                        points = 0
                    is_timer_on = not is_timer_on
                if theme_mode_button_rect.collidepoint(event.pos):
                    is_dark_mode = not is_dark_mode
                mouse_click_pos = (int(pygame.mouse.get_pos()[1] // BLOCK_SIZE) - 1), int((pygame.mouse.get_pos()[0] // BLOCK_SIZE) - 1)
                curr_points = board.calculate_points(mouse_click_pos)
                if curr_points == 0:
                    if is_timer_on:
                        counter -= 10
                    wrong_move_sound.play()
                elif curr_points > 0:
                    break_sound.play()
                    points += curr_points
        if event.type == timer_event and is_timer_on:
            counter -= 1
        if counter <= 0 and state == STATE_PLAYING:
            state = STATE_GAME_OVER

    # Fill the screen with a color to wipe away anything from last frame
    screen.fill('white')
    background = pygame.image.load('images/background.jpg' if not is_dark_mode else 'images/background_dark.jpg').convert()
    background = pygame.transform.smoothscale(background, screen.get_size())
    screen.blit(background, (0, 0))

    # Game render
    if state == STATE_START_MENU:
        screen.blit(title, title_pos)
        screen.blit(button_back, start_button_back_pos)
        screen.blit(start_button_text, start_button_text_pos)

    if state == STATE_PLAYING:
        score_text = score_font.render("Score: " + str(points), True, (0, 0, 0) if not is_dark_mode else (255, 255, 255))
        screen.blit(score_text, (900, 10))
        screen.blit(timer_button_on if is_timer_on else timer_button_off, (70, 685))
        screen.blit(dark_mode_button if not is_dark_mode else light_mode_button, (WIDTH // 2 - light_mode_button.get_width() // 2, 10))
        timer_text = time_font.render(f"Time: {str(counter) if is_timer_on else 'Unlimited'}", True,  (0, 0, 0) if not is_dark_mode else (255, 255, 255))
        screen.blit(timer_text, (10, 10))
        screen.blit(reset_button, reset_button_pos)
        board.draw_board(screen)

    if state == STATE_GAME_OVER:
        game_over_text_2 = game_over_font.render(f"Final score: {points}", True, (255, 0, 0))
        game_over_text_2_pos = (WIDTH // 2 - game_over_text_2.get_width() // 2, HEIGHT // 2 - game_over_text_2.get_height() // 2)
        screen.blit(game_over_text, game_over_text_pos)
        screen.blit(game_over_text_2, game_over_text_2_pos)
        screen.blit(button_back, play_again_button_pos)
        screen.blit(play_again_button_text, play_again_button_text_pos)
        if not has_played_game_over:
            game_end_sound.play()
            has_played_game_over = True

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
