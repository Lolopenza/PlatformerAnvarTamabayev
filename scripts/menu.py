import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Pygame Menu")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Define button dimensions and positions
button_width, button_height = 200, 50
play_button_pos = (screen_width // 2 - button_width // 2, 200)
options_button_pos = (screen_width // 2 - button_width // 2, 300)
quit_button_pos = (screen_width // 2 - button_width // 2, 400)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if buttons are clicked
            if play_button_pos[0] < mouse_x < play_button_pos[0] + button_width and \
               play_button_pos[1] < mouse_y < play_button_pos[1] + button_height:
                print("Play button clicked")

            elif options_button_pos[0] < mouse_x < options_button_pos[0] + button_width and \
                 options_button_pos[1] < mouse_y < options_button_pos[1] + button_height:
                print("Options button clicked")

            elif quit_button_pos[0] < mouse_x < quit_button_pos[0] + button_width and \
                 quit_button_pos[1] < mouse_y < quit_button_pos[1] + button_height:
                pygame.quit()
                sys.exit()

    # Draw background
    screen.fill(GRAY)

    # Draw buttons
    pygame.draw.rect(screen, WHITE, (play_button_pos[0], play_button_pos[1], button_width, button_height))
    pygame.draw.rect(screen, WHITE, (options_button_pos[0], options_button_pos[1], button_width, button_height))
    pygame.draw.rect(screen, WHITE, (quit_button_pos[0], quit_button_pos[1], button_width, button_height))

    # Draw text on buttons
    font = pygame.font.Font(None, 36)
    play_text = font.render("Play", True, BLACK)
    options_text = font.render("Options", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(play_text, (play_button_pos[0] + 50, play_button_pos[1] + 15))
    screen.blit(options_text, (options_button_pos[0] + 30, options_button_pos[1] + 15))
    screen.blit(quit_text, (quit_button_pos[0] + 50, quit_button_pos[1] + 15))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

