'''
Aamna's Snake Game!!! 

Do you get fidgety during lectures? Play this cute snake game!

'''

import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()


# Game constants
'''
Defining dimensions and colours (RGB values) that are used throughout the game
'''
INFO_PANEL_HEIGHT = 100  # Space for score and info
GAME_HEIGHT = 400        # Actual gameplay area
WIDTH = 600
HEIGHT = INFO_PANEL_HEIGHT + GAME_HEIGHT  # Total window height
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = GAME_HEIGHT // GRID_SIZE
INITIAL_FPS = 6  # Slower starting speed
MAX_FPS = 15     # Maximum speed

# PASTEL COLOURS! 
PASTEL_PINK = (255, 209, 220)      # Soft pink
PASTEL_LAVENDER = (220, 208, 255)  # Lavender 
PASTEL_MINT = (203, 255, 227)      # Mint
PASTEL_PEACH = (255, 218, 193)     # Peach
PASTEL_BLUE = (189, 224, 254)      # Baby blue
PASTEL_YELLOW = (255, 249, 196)    # Lemony
PASTEL_LILAC = (232, 203, 255)     # Lilac 
PASTEL_ROSE = (255, 192, 203)      # Rose 
PASTEL_AQUA = (179, 255, 247)      # Aqua 
PASTEL_CREAM = (255, 253, 230)     # Vanilla 
PASTEL_GRAPE = (180, 150, 220)     # Grape

# Background colour - UI Colours
BACKGROUND_COLOUR = PASTEL_LAVENDER
INFO_PANEL_COLOUR = PASTEL_PINK
GRID_COLOUR = (230, 220, 255)  # Lighter lavender for grid
# Text colours
TEXT_COLOUR = (120, 80, 120)       # Muted purple for text
ACCENT_COLOUR = (200, 120, 180)    # Pretty pink-purple


# Snake colour options 
# Dictionary
SNAKE_COLOURS = {
    "Pink": PASTEL_ROSE,
    "Lavender": PASTEL_LILAC,
    "Mint": PASTEL_MINT,
    "Peach": PASTEL_PEACH,
    "Aqua": PASTEL_AQUA
}

# Fruit types with colours
FRUIT_TYPES = {
    "Strawberry": (255, 150, 150),  # Soft strawberry pink
    "Lemon": PASTEL_YELLOW,         # Pastel lemon
    "Blueberry": PASTEL_BLUE,       # Baby blue blueberries
    "Orange": PASTEL_PEACH,         # Peach-orange
    "Grape": PASTEL_GRAPE           # NEW: Better visible grape colour!
}



# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # With our width and height 
pygame.display.set_caption("Aamna's Snake Game!")
clock = pygame.time.Clock() # Control game speed

# Font setup
large_font = pygame.font.SysFont('comicsansms', 50)
small_font = pygame.font.SysFont('comicsansms', 20)



'''
Snake class to manage snake properties and behaviour
'''
class Snake:
    def __init__(self, colour=PASTEL_ROSE):
        # Constructor called when creating a new snake
        self.reset(colour)
    
    def reset(self, colour):
        # Reset snake to initial state
        self.length = 3 # Default length
        # Start in middle of screen (column 15, row 10)
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        # Random initial direction
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        self.score = 0 # Starting score
        self.grow_pending = 1 # Grow by 1 segment on first move
        self.colour = colour   # Snake colour
        self.eye_colour = PASTEL_CREAM
        self.pupil_colour = (100, 80, 120)  # Pupil
    
    def get_head_position(self):
        # Return current head position
        return self.positions[0]
    
    def turn(self, point):
        # Change direction unless it's directly opposite
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return # Ignore opposite turn
        else:
            self.direction = point # Update direction
    
    def move(self):
        # Move snake in current direction
        head = self.get_head_position() # Current head position
        x, y = self.direction # Direction vector
        # Calculate new head position
        new_x = head[0] + x # New column 
        new_y = head[1] + y # New row
        
        # Game over if snake hits walls or goes out of bounds 
        if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
            return False # Game over
        
        new_position = (new_x, new_y)
        
        # Game over if snake hits itself
        if new_position in self.positions[1:]:
            return False
        
        # Insert new head position at the front of the list
        self.positions.insert(0, new_position)
        
        # Remove tail segment unless growing
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.positions.pop()
            
        return True
    
    def grow(self):
        # Increase snake length by 1 -> grow!
        self.grow_pending += 1
        self.length += 1 # Lenghth counter
        self.score += 1  # Score increases by 1 now
    
    def draw(self, surface):
        # Draw the snake on the screen
        for i, p in enumerate(self.positions):
            
            x = p[0] * GRID_SIZE  # Column to pixels
            y = p[1] * GRID_SIZE + INFO_PANEL_HEIGHT  # Row to pixels + top panel offset
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            

            body_colour = self.colour if i == 0 else (self.colour[0] - 30, self.colour[1] - 30, self.colour[2] - 30)
            
            # Draw rounded snake segments (rounded corners)
            pygame.draw.rect(surface, body_colour, rect, border_radius=6)
            # Draw border 
            pygame.draw.rect(surface, (body_colour[0]//2, body_colour[1]//2, body_colour[2]//2), rect, 2, border_radius=6)
            
            # Draw snake head with eyes and BLUSH! 
            if i == 0:
                self.draw_eyes(surface, rect)
    
    def draw_eyes(self, surface, head_rect):
        # Determine eye positions based on direction
        dx, dy = self.direction
        
        # Sparkly eyes! 
        eye_radius = GRID_SIZE // 6
        pupil_radius = GRID_SIZE // 12
        
        # Position eyes based on direction
        if dx == 1:  # Moving right
            left_eye = (head_rect.x + 3 * GRID_SIZE // 4, head_rect.y + GRID_SIZE // 3)
            right_eye = (head_rect.x + 3 * GRID_SIZE // 4, head_rect.y + 2 * GRID_SIZE // 3)
        elif dx == -1:  # Moving left
            left_eye = (head_rect.x + GRID_SIZE // 4, head_rect.y + GRID_SIZE // 3)
            right_eye = (head_rect.x + GRID_SIZE // 4, head_rect.y + 2 * GRID_SIZE // 3)
        elif dy == 1:  # Moving down
            left_eye = (head_rect.x + GRID_SIZE // 3, head_rect.y + 3 * GRID_SIZE // 4)
            right_eye = (head_rect.x + 2 * GRID_SIZE // 3, head_rect.y + 3 * GRID_SIZE // 4)
        else:  # Moving up or default
            left_eye = (head_rect.x + GRID_SIZE // 3, head_rect.y + GRID_SIZE // 4)
            right_eye = (head_rect.x + 2 * GRID_SIZE // 3, head_rect.y + GRID_SIZE // 4)
        
        # Draw cute sparkly eyes
        pygame.draw.circle(surface, self.eye_colour, left_eye, eye_radius)
        pygame.draw.circle(surface, self.eye_colour, right_eye, eye_radius)
        pygame.draw.circle(surface, self.pupil_colour, left_eye, pupil_radius)
        pygame.draw.circle(surface, self.pupil_colour, right_eye, pupil_radius)
        
        # Eye sparkles!
        sparkle_colour = PASTEL_CREAM
        pygame.draw.circle(surface, sparkle_colour, (left_eye[0] - 2, left_eye[1] - 2), 1)
        pygame.draw.circle(surface, sparkle_colour, (right_eye[0] + 2, right_eye[1] - 2), 1)
    

class Fruit:
    def __init__(self, fruit_type="Strawberry"):
        # Constructor for fruit 
        self.fruit_type = fruit_type
        self.colour = FRUIT_TYPES[fruit_type] # Get colour from dictionary
        self.position = (0, 0)
        self.randomize_position() # Random initial position
    
    def randomize_position(self):
        # Place fruit at random position on grid
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
    
    def draw(self, surface):
        # Adjust Y position for info panel
        # Draw fruit with cute shapes based on type
        rect = pygame.Rect((self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE + INFO_PANEL_HEIGHT), 
                          (GRID_SIZE, GRID_SIZE))
        
        # Draw different fruit shapes with CUTE details!
        if self.fruit_type == "Strawberry":
            # Cute strawberry with leaves
            pygame.draw.circle(surface, self.colour, rect.center, GRID_SIZE // 2 - 2)
            # Leaves
            leaf_colour = PASTEL_MINT
            pygame.draw.ellipse(surface, leaf_colour, (rect.centerx - 4, rect.top - 2, 8, 6))
            # Seeds
            seed_colour = PASTEL_YELLOW
            for seed_pos in [(rect.centerx - 3, rect.centery), (rect.centerx + 3, rect.centery),
                           (rect.centerx, rect.centery - 3), (rect.centerx, rect.centery + 3)]:
                pygame.draw.circle(surface, seed_colour, seed_pos, 1)
                
        elif self.fruit_type == "Lemon":
            # Sunny lemon
            pygame.draw.circle(surface, self.colour, rect.center, GRID_SIZE // 2 - 2)
            # Lemon details
            pygame.draw.arc(surface, PASTEL_PEACH, rect, 0.2, 2.8, 2)
            
        elif self.fruit_type == "Blueberry":
            # Cluster of blueberries
            main_berry = rect.center
            pygame.draw.circle(surface, self.colour, main_berry, GRID_SIZE // 3)
            # Smaller berries around
            berry_positions = [
                (main_berry[0] - 4, main_berry[1] - 4),
                (main_berry[0] + 4, main_berry[1] - 4),
                (main_berry[0] - 3, main_berry[1] + 4)
            ]
            for pos in berry_positions:
                pygame.draw.circle(surface, self.colour, pos, GRID_SIZE // 4)
                
        elif self.fruit_type == "Orange":
            # Juicy orange
            pygame.draw.circle(surface, self.colour, rect.center, GRID_SIZE // 2 - 2)
            # Orange segment lines
            segment_colour = PASTEL_YELLOW
            for i in range(4):
                angle = i * 90
                start_pos = (rect.centerx, rect.centery)
                end_x = rect.centerx + 6 * pygame.math.Vector2(1, 0).rotate(angle).x
                end_y = rect.centery + 6 * pygame.math.Vector2(1, 0).rotate(angle).y
                pygame.draw.line(surface, segment_colour, start_pos, (end_x, end_y), 1)
                
        elif self.fruit_type == "Grape":
            # Bunch of grapes - FIXED with better visibility!
            grape_colour = PASTEL_GRAPE  # Use the new distinct colour
            grape_positions = [
                (rect.centerx, rect.centery - 3),
                (rect.centerx - 3, rect.centery),
                (rect.centerx + 3, rect.centery),
                (rect.centerx, rect.centery + 3)
            ]
            for pos in grape_positions:
                pygame.draw.circle(surface, grape_colour, pos, GRID_SIZE // 3)
            # Add grape stem for cuteness!
            pygame.draw.line(surface, PASTEL_MINT, 
                           (rect.centerx, rect.top + 2), 
                           (rect.centerx, rect.centery - 6), 2)

def draw_grid(surface):
    # Only draw grid in gameplay area (below info panel) with soft colour
    for y in range(INFO_PANEL_HEIGHT, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect((x, y), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, GRID_COLOUR, rect, 1)

def draw_info_panel(surface, score, snake_colour, fruit_type, current_speed, game_paused=False):
    # Draw pretty info panel background
    info_rect = pygame.Rect(0, 0, WIDTH, INFO_PANEL_HEIGHT)
    pygame.draw.rect(surface, INFO_PANEL_COLOUR, info_rect)
    # Pretty border
    pygame.draw.line(surface, PASTEL_LILAC, (0, INFO_PANEL_HEIGHT), (WIDTH, INFO_PANEL_HEIGHT), 3)
    
    # Draw info text with cute colours
    score_text = font.render(f'Score: {score}', True, TEXT_COLOUR)
    snake_text = small_font.render(f'Snake: {list(SNAKE_COLOURS.keys())[list(SNAKE_COLOURS.values()).index(snake_colour)]}', True, TEXT_COLOUR)
    fruit_text = small_font.render(f'Fruit: {fruit_type}', True, TEXT_COLOUR)
    speed_text = small_font.render(f'Speed: {current_speed}', True, TEXT_COLOUR)
    
    # Pause indicator
    if game_paused:
        pause_text = font.render('PAUSED - Press P to resume', True, ACCENT_COLOUR)
        surface.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, INFO_PANEL_HEIGHT - 30))
    
    surface.blit(score_text, (10, 10))
    surface.blit(snake_text, (10, 40))
    surface.blit(fruit_text, (200, 40))
    surface.blit(speed_text, (400, 40))
    
    # Controls INFO
    controls_text = small_font.render('P: Pause | Q: Quit | ESC: Menu', True, TEXT_COLOUR)
    surface.blit(controls_text, (WIDTH - controls_text.get_width() - 10, 10))

def draw_game_over(surface, score):
    # Create pretty overlay only over gameplay area
    overlay = pygame.Surface((WIDTH, GAME_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(PASTEL_PINK)
    surface.blit(overlay, (0, INFO_PANEL_HEIGHT))
    
    game_over_text = large_font.render('Game Over', True, ACCENT_COLOUR)
    score_text = font.render(f'Final Score: {score}', True, TEXT_COLOUR)
    restart_text = font.render('Press SPACE to play again', True, TEXT_COLOUR)
    menu_text = font.render('Press M for main menu', True, TEXT_COLOUR)
    quit_text = font.render('Press Q to quit', True, TEXT_COLOUR)
    
    # Center in gameplay area
    center_y = INFO_PANEL_HEIGHT + GAME_HEIGHT // 2
    
    surface.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, center_y - 80))
    surface.blit(score_text, (WIDTH//2 - score_text.get_width()//2, center_y - 20))
    surface.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, center_y + 20))
    surface.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, center_y + 60))
    surface.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, center_y + 100))

def draw_pause_screen(surface):
    # Create pretty overlay only over gameplay area
    overlay = pygame.Surface((WIDTH, GAME_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(PASTEL_AQUA)
    surface.blit(overlay, (0, INFO_PANEL_HEIGHT))
    
    pause_text = large_font.render('Game Paused', True, ACCENT_COLOUR)
    resume_text = font.render('Press P to resume', True, TEXT_COLOUR)
    menu_text = font.render('Press M for main menu', True, TEXT_COLOUR)
    quit_text = font.render('Press Q to quit', True, TEXT_COLOUR)
    
    # Center in gameplay area
    center_y = INFO_PANEL_HEIGHT + GAME_HEIGHT // 2
    
    surface.blit(pause_text, (WIDTH//2 - pause_text.get_width()//2, center_y - 60))
    surface.blit(resume_text, (WIDTH//2 - resume_text.get_width()//2, center_y))
    surface.blit(menu_text, (WIDTH//2 - menu_text.get_width()//2, center_y + 40))
    surface.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, center_y + 80))

def draw_menu(surface, selected_snake_colour, selected_fruit):
    surface.fill(BACKGROUND_COLOUR)
    
    title = large_font.render('Snake Game', True, ACCENT_COLOUR)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, 30))
    
    # Snake colour selection
    snake_title = font.render('Choose Snake Colour:', True, TEXT_COLOUR)
    surface.blit(snake_title, (WIDTH//2 - snake_title.get_width()//2, 90))
    
    # Draw snake colour options in a row 
    snake_colours_list = list(SNAKE_COLOURS.items())
    option_width = 80
    spacing = 20
    total_width = len(snake_colours_list) * option_width + (len(snake_colours_list) - 1) * spacing
    start_x = WIDTH//2 - total_width//2
    
    for i, (name, colour) in enumerate(snake_colours_list):
        x_pos = start_x + i * (option_width + spacing)
        y_pos = 130
        
        # Pretty background for selected item
        if name == selected_snake_colour:
            pygame.draw.rect(surface, PASTEL_CREAM, (x_pos - 5, y_pos - 5, option_width + 10, 60), border_radius=10)
            pygame.draw.rect(surface, ACCENT_COLOUR, (x_pos - 5, y_pos - 5, option_width + 10, 60), 2, border_radius=10)
        
        # Colour preview (cute rounded square) 
        preview_rect = pygame.Rect(x_pos, y_pos, option_width, 30)
        pygame.draw.rect(surface, colour, preview_rect, border_radius=8)
        pygame.draw.rect(surface, (colour[0]//2, colour[1]//2, colour[2]//2), preview_rect, 2, border_radius=8)
        
        # Text
        text = small_font.render(name, True, TEXT_COLOUR)
        surface.blit(text, (x_pos + option_width//2 - text.get_width()//2, y_pos + 35))
    
    # Fruit selection
    fruit_title = font.render('Choose Fruit Type! ', True, TEXT_COLOUR)
    surface.blit(fruit_title, (WIDTH//2 - fruit_title.get_width()//2, 220))
    
    # Draw fruit options in a row 
    fruits_list = list(FRUIT_TYPES.items())
    total_width = len(fruits_list) * option_width + (len(fruits_list) - 1) * spacing
    start_x = WIDTH//2 - total_width//2
    
    for i, (name, colour) in enumerate(fruits_list):
        x_pos = start_x + i * (option_width + spacing)
        y_pos = 260
        
        # Pretty background for selected item
        if name == selected_fruit:
            pygame.draw.rect(surface, PASTEL_CREAM, (x_pos - 5, y_pos - 5, option_width + 10, 60), border_radius=10)
            pygame.draw.rect(surface, ACCENT_COLOUR, (x_pos - 5, y_pos - 5, option_width + 10, 60), 2, border_radius=10)
        
        # Fruit preview area 
        center_x = x_pos + option_width // 2
        center_y = y_pos + 15
        
        if name == "Strawberry":
            pygame.draw.circle(surface, colour, (center_x, center_y), 10)
            # Tiny leaves
            pygame.draw.ellipse(surface, PASTEL_MINT, (center_x - 4, center_y - 12, 8, 6))
        elif name == "Lemon":
            pygame.draw.circle(surface, colour, (center_x, center_y), 10)
        elif name == "Blueberry":
            pygame.draw.circle(surface, colour, (center_x, center_y), 8)
        elif name == "Orange":
            pygame.draw.circle(surface, colour, (center_x, center_y), 10)
        elif name == "Grape":
            # Use the new distinct grape colour
            grape_colour = PASTEL_GRAPE
            pygame.draw.circle(surface, grape_colour, (center_x, center_y), 8)
        
        # Text
        text = small_font.render(name, True, TEXT_COLOUR)
        surface.blit(text, (x_pos + option_width//2 - text.get_width()//2, y_pos + 35))
    
    # Cute controls instructions
    controls_y = 350
    controls = [
        " CONTROLS:",
        " </> Select Snake Colour",
        " ^/v: Select Fruit Type", 
        "ENTER: Start Game",
        "P: Pause Game",
        "Q or ESC: Quit"
    ]
    
    for i, text in enumerate(controls):
        control_text = small_font.render(text, True, TEXT_COLOUR)
        surface.blit(control_text, (WIDTH//2 - control_text.get_width()//2, controls_y + i * 25))

def calculate_speed(score):
    """Calculate game speed based on score - increases as you score more"""
    # Speed increases every 5 points, up to maximum
    speed_increase = min(score // 5, MAX_FPS - INITIAL_FPS)
    return INITIAL_FPS + speed_increase

def main():
    game_state = "menu"  # menu, playing, paused, game_over
    selected_snake_colour = "Pink"
    selected_fruit = "Strawberry"
    
    snake = Snake(SNAKE_COLOURS[selected_snake_colour])
    fruit = Fruit(selected_fruit)
    current_speed = INITIAL_FPS
    game_paused = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    if event.key == pygame.K_LEFT:
                        # Cycle through snake colours backward
                        colours = list(SNAKE_COLOURS.keys())
                        current_index = colours.index(selected_snake_colour)
                        selected_snake_colour = colours[(current_index - 1) % len(colours)]
                    elif event.key == pygame.K_RIGHT:
                        # Cycle through snake colours forward
                        colours = list(SNAKE_COLOURS.keys())
                        current_index = colours.index(selected_snake_colour)
                        selected_snake_colour = colours[(current_index + 1) % len(colours)]
                    elif event.key == pygame.K_UP:
                        # Cycle through fruits backward
                        fruits = list(FRUIT_TYPES.keys())
                        current_index = fruits.index(selected_fruit)
                        selected_fruit = fruits[(current_index - 1) % len(fruits)]
                    elif event.key == pygame.K_DOWN:
                        # Cycle through fruits forward
                        fruits = list(FRUIT_TYPES.keys())
                        current_index = fruits.index(selected_fruit)
                        selected_fruit = fruits[(current_index + 1) % len(fruits)]
                    elif event.key == pygame.K_RETURN:
                        # Start game
                        snake = Snake(SNAKE_COLOURS[selected_snake_colour])
                        fruit = Fruit(selected_fruit)
                        current_speed = INITIAL_FPS
                        game_paused = False
                        game_state = "playing"
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                
                elif game_state == "playing":
                    if event.key == pygame.K_p:
                        # Pause game
                        game_paused = True
                        game_state = "paused"
                    elif event.key == pygame.K_UP:
                        snake.turn((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.turn((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.turn((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.turn((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        game_state = "menu"
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                
                elif game_state == "paused":
                    if event.key == pygame.K_p:
                        # Resume game
                        game_paused = False
                        game_state = "playing"
                    elif event.key == pygame.K_m:
                        # Return to menu
                        game_state = "menu"
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                elif game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        # Restart game with same settings
                        snake = Snake(SNAKE_COLOURS[selected_snake_colour])
                        fruit = Fruit(selected_fruit)
                        current_speed = INITIAL_FPS
                        game_paused = False
                        game_state = "playing"
                    elif event.key == pygame.K_m:
                        # Return to menu
                        game_state = "menu"
                    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
        
        # Fill with pretty background colour
        screen.fill(BACKGROUND_COLOUR)
        
        if game_state == "menu":
            draw_menu(screen, selected_snake_colour, selected_fruit)
        
        elif game_state == "playing":
            # Draw info panel (always visible)
            draw_info_panel(screen, snake.score, snake.colour, fruit.fruit_type, current_speed, game_paused)
            
            # Draw gameplay elements
            draw_grid(screen)
            
            # Calculate current speed based on score
            current_speed = calculate_speed(snake.score)
            
            # Move snake
            if not snake.move():
                game_state = "game_over"
            
            # Check if snake ate food
            if snake.get_head_position() == fruit.position:
                snake.grow()
                fruit.randomize_position()
                # Make sure food doesn't appear on snake
                while fruit.position in snake.positions:
                    fruit.randomize_position()
            
            snake.draw(screen)
            fruit.draw(screen)
        
        elif game_state == "paused":
            # Draw info panel
            draw_info_panel(screen, snake.score, snake.colour, fruit.fruit_type, current_speed, True)
            
            # Draw gameplay elements (frozen)
            draw_grid(screen)
            snake.draw(screen)
            fruit.draw(screen)
            
            # Draw pause screen
            draw_pause_screen(screen)
        
        elif game_state == "game_over":
            # Draw info panel
            draw_info_panel(screen, snake.score, snake.colour, fruit.fruit_type, current_speed)
            
            # Draw gameplay elements (final state)
            draw_grid(screen)
            snake.draw(screen)
            fruit.draw(screen)
            
            # Draw game over screen
            draw_game_over(screen, snake.score)
        
        pygame.display.update()
        
        # Only tick the clock if we're actually playing (not paused or in menu)
        if game_state == "playing":
            clock.tick(current_speed)
        else:
            clock.tick(30)  # Lower FPS for menus to reduce CPU usage

if __name__ == "__main__":
    main()