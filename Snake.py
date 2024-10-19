import pygame, sys, random  # Importing pygame for game mechanics, sys for system exit, and random for randomness in apple position.
from pygame.math import Vector2  # Importing the Vector2 class for 2D vector operations (snake movement, apple position).

# Defining the SNAKE class to represent the snake object in the game.
class SNAKE:  
    def __init__(self):
        self.reset()
    
    def reset(self):  # Resetting the snake's position and direction.  
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]  # The snake's body is a list of Vector2 objects representing each segment.
        self.direction = Vector2(0,0)  # Initial movement direction (no movement).
        self.new_block = False  # Flag to indicate if a new block should be added to the snake (after eating).

        # Loading different head images based on movement direction.
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        # Loading tail images based on movement direction.
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        # Loading body images (vertical, horizontal, and corners).
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_topright.png').convert_alpha()  # Top-right corner.
        self.body_tl = pygame.image.load('Graphics/body_topleft.png').convert_alpha()  # Top-left corner.
        self.body_br = pygame.image.load('Graphics/body_bottomright.png').convert_alpha()  # Bottom-right corner.
        self.body_bl = pygame.image.load('Graphics/body_bottomleft.png').convert_alpha()  # Bottom-left corner.

        # Loading sound for when the snake eats an apple.
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    # Method to draw the snake on the screen.
    def draw_snake(self):
        self.update_head_graphics()  # Update the head's direction.
        self.update_tail_graphics()  # Update the tail's direction.

        # Loop through each block (segment) of the snake and draw it.
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)  # Convert grid position to pixel position (x).
            y_pos = int(block.y * cell_size)  # Convert grid position to pixel position (y).
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)  # Create a rectangle for the segment.

            if index == 0:  # If it's the head, draw the head image.
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:  # If it's the tail, draw the tail image.
                screen.blit(self.tail, block_rect)
            else:  # For body segments.
                previous_block = self.body[index + 1] - block  # Vector difference between this block and the next.
                next_block = self.body[index - 1] - block  # Vector difference between this block and the previous.

                # If the previous and next blocks are aligned vertically, draw a vertical segment.
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                # If the previous and next blocks are aligned horizontally, draw a horizontal segment.
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:  # If it's a corner block, draw the appropriate corner image.
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)  # Top-left corner.
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)  # Top-right corner.
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)  # Bottom-left corner.
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)  # Bottom-right corner.

    # Method to update the head's appearance based on the current movement direction.
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]  # Get the direction the head is moving.
        if head_relation == Vector2(1,0):  # Moving to the right.
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):  # Moving to the left.
            self.head = self.head_right
        elif head_relation == Vector2(0,1):  # Moving down.
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):  # Moving up.
            self.head = self.head_down

    # Method to update the tail's appearance based on its direction.
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]  # Get the direction the tail is moving.
        if tail_relation == Vector2(1,0):  # Moving right.
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):  # Moving left.
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):  # Moving down.
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):  # Moving up.
            self.tail = self.tail_down

    # Method to move the snake in the current direction.
    def move_snake(self):
        if self.new_block:  # If a new block is to be added (after eating).
            body_copy = self.body[:]  # Create a copy of the body.
            body_copy.insert(0, body_copy[0] + self.direction)  # Add a new block in front of the head.
            self.new_block = False  # Reset the new block flag.
        else:
            body_copy = self.body[:-1]  # Create a copy of the body excluding the last segment.
            body_copy.insert(0, body_copy[0] + self.direction)  # Move the snake by adding a new head.
        self.body = body_copy[:]  # Update the body with the new segment list.

    # Method to add a new block to the snake after eating.
    def add_block(self):
        self.new_block = True  # Set the flag to add a new block.

    # Method to play the crunch sound when the snake eats.
    def play_crunch_sound(self):
        self.crunch_sound.play()  # Play the eating sound effect.

    # Method to check if the snake has collided with itself or the walls.
    def check_fail(self):
        # Check if the snake hits the boundaries of the screen.
        if not 0 <= self.body[0].x < cell_number or not 0 <= self.body[0].y < cell_number:
            return True  # Return True to indicate failure.

        # Check if the snake collides with itself.
        for block in self.body[1:]:  # Skip the head.
            if block == self.body[0]:
                return True  # Return True to indicate failure.

# Defining the FRUIT class to represent the apple the snake eats.
class FRUIT:
    def __init__(self):
        self.randomize()

    # Randomize the apple's position within the grid.
    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

    # Draw the apple on the screen.
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

# Defining the MAIN class to manage game logic.
class MAIN:
    def __init__(self):
        self.snake = SNAKE()  # Create a snake instance.
        self.fruit = FRUIT()  # Create a fruit (apple) instance.

    # Method to update the game (move snake, check for collisions, etc.).
    def update(self):
        self.snake.move_snake()  # Move the snake.
        self.check_collision()  # Check for collisions with the apple.
        self.check_fail()  # Check if the snake fails.

    # Method to draw all game elements (snake, fruit).
    def draw_elements(self):
        self.fruit.draw_fruit()  # Draw the apple.
        self.snake.draw_snake()  # Draw the snake.
        self.draw_score()  # Draw the score.
    
    # Checks if the snake's head has collided with the fruit (eating it).
    def check_collision(self):  
        if self.snake.body[0] == self.fruit.pos:  
            self.fruit.randomize()  # Respawn the fruit at a new location.
            self.snake.add_block()  # Add a new segment to the snake's body.
            self.snake.play_crunch_sound()  # Play the eating sound.
    
    # Checks if the snake hits the boundaries or itself (failure condition).
    def check_fail(self):  
        # Snake hits the screen borders.
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:  
            self.game_over()  
        
        # Snake hits itself (if head collides with any body segment).
        for block in self.snake.body[1:]:  
            if block == self.snake.body[0]:  
                self.game_over()  
    
    # Resets the game when the snake fails.
    def game_over(self):  
        self.snake.reset()  
    
    # Draws the player's score on the screen.
    def draw_score(self):  
        score_text = str(len(self.snake.body) - 3)  # The score is the length of the snake minus the initial 3 segments.
        score_surface = game_font.render(score_text, True, (56, 74, 12))  
        
        # Position the score in the bottom-right corner of the screen.
        score_x = int(cell_size * cell_number - 60)  
        score_y = int(cell_size * cell_number - 40)  
        
        # Render the score next to a small apple image.
        score_rect = score_surface.get_rect(center=(score_x, score_y))  
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))  
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6, apple_rect.height)  
        
        # Draw background rectangle and then score and apple image.
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)  
        screen.blit(score_surface, score_rect)  
        screen.blit(apple, apple_rect)  
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)  # Draw border.

# Initialize the mixer for sound effects.
pygame.mixer.pre_init(44100, -16, 2, 512)  
pygame.init()  # Initialize all Pygame modules.

# Game constants for grid size and window settings.
cell_size = 40  
cell_number = 20  
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))  
clock = pygame.time.Clock()  

# Load the apple image and set the font for the score.
apple = pygame.image.load('Graphics/apple.png').convert_alpha()  
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)  

# Set up a custom event to update the screen at a regular interval (150ms).
SCREEN_UPDATE = pygame.USEREVENT  
pygame.time.set_timer(SCREEN_UPDATE, 150)  

# Create the main game instance.
main_game = MAIN()  

# Main game loop to keep the game running.
while True:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  # If the user closes the window, quit the game.
            pygame.quit()  
            sys.exit()  
        if event.type == SCREEN_UPDATE:  # Update the game state at regular intervals.
            main_game.update()  
        if event.type == pygame.KEYDOWN:  # Check for user input to change snake direction.
            if event.key == pygame.K_UP:  
                if main_game.snake.direction.y != 1:  
                    main_game.snake.direction = Vector2(0, -1)  
            if event.key == pygame.K_RIGHT:  
                if main_game.snake.direction.x != -1:  
                    main_game.snake.direction = Vector2(1, 0)  
            if event.key == pygame.K_DOWN:  
                if main_game.snake.direction.y != -1:  
                    main_game.snake.direction = Vector2(0, 1)  
            if event.key == pygame.K_LEFT:  
                if main_game.snake.direction.x != 1:  
                    main_game.snake.direction = Vector2(-1, 0)  
    
    # Fill the screen with the background color and draw game elements.
    screen.fill((175, 215, 70))  
    main_game.draw_elements()  
    pygame.display.update()  # Refresh the display.
    clock.tick(60)  # Cap the frame rate at 60 frames per second.