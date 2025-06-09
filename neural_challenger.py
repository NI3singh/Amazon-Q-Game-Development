import pygame
import random
import math
import time
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
PUZZLE_PANEL_WIDTH = SCREEN_WIDTH // 2
REFLEX_PANEL_WIDTH = SCREEN_WIDTH // 2
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)

# Shape types
CIRCLE = "circle"
TRIANGLE = "triangle"
SQUARE = "square"

class Shape:
    def __init__(self, x, y, shape_type, color, size=30):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.color = color
        self.size = size
        self.speed = random.uniform(2, 5)
    
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        if self.shape_type == CIRCLE:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
        elif self.shape_type == TRIANGLE:
            points = [
                (self.x, self.y - self.size),
                (self.x - self.size, self.y + self.size),
                (self.x + self.size, self.y + self.size)
            ]
            pygame.draw.polygon(screen, self.color, points)
        elif self.shape_type == SQUARE:
            rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
            pygame.draw.rect(screen, self.color, rect)

class Puzzle:
    def __init__(self):
        self.puzzle_type = random.choice(["simon", "math", "stroop"])
        self.start_time = time.time()
        self.time_limit = 5.0
        self.completed = False
        self.failed = False
        self.user_input = ""
        self.generate_puzzle()
    
    def generate_puzzle(self):
        if self.puzzle_type == "simon":
            self.sequence_length = 3
            self.sequence = [random.randint(1, 4) for _ in range(self.sequence_length)]
            self.current_input = []
            self.showing_sequence = True
            self.sequence_start_time = time.time()
            self.show_duration = 2.0
        
        elif self.puzzle_type == "math":
            self.num1 = random.randint(10, 99)
            self.num2 = random.randint(10, 99)
            self.operation = random.choice(["+", "-", "*"])
            if self.operation == "+":
                self.answer = self.num1 + self.num2
            elif self.operation == "-":
                self.answer = self.num1 - self.num2
            else:  # multiplication
                self.answer = self.num1 * self.num2
        
        elif self.puzzle_type == "stroop":
            self.colors = ["RED", "BLUE", "GREEN", "YELLOW"]
            self.color_values = [RED, BLUE, GREEN, YELLOW]
            self.word = random.choice(self.colors)
            self.word_color = random.choice(self.color_values)
            # Answer is the color of the text, not the word itself
            self.answer = self.color_values.index(self.word_color)
    
    def get_time_remaining(self):
        return max(0, self.time_limit - (time.time() - self.start_time))
    
    def is_expired(self):
        return time.time() - self.start_time > self.time_limit
    
    def handle_input(self, key):
        if self.puzzle_type == "simon":
            if not self.showing_sequence:
                if key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    number = int(pygame.key.name(key))
                    self.current_input.append(number)
                    if len(self.current_input) == len(self.sequence):
                        self.completed = self.current_input == self.sequence
                        self.failed = not self.completed
        
        elif self.puzzle_type == "math":
            if key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            elif key == pygame.K_RETURN:
                try:
                    user_answer = int(self.user_input)
                    self.completed = user_answer == self.answer
                    self.failed = not self.completed
                except ValueError:
                    self.failed = True
            elif pygame.key.name(key).isdigit() or pygame.key.name(key) == "-":
                self.user_input += pygame.key.name(key)
        
        elif self.puzzle_type == "stroop":
            if key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                user_answer = int(pygame.key.name(key)) - 1
                self.completed = user_answer == self.answer
                self.failed = not self.completed
    
    def update(self):
        if self.puzzle_type == "simon" and self.showing_sequence:
            if time.time() - self.sequence_start_time > self.show_duration:
                self.showing_sequence = False
                self.start_time = time.time()  # Reset timer for input phase
    
    def draw(self, screen, x, y, width, height):
        # Draw puzzle panel background
        pygame.draw.rect(screen, LIGHT_GRAY, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 3)
        
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Draw timer
        time_remaining = self.get_time_remaining()
        timer_text = small_font.render(f"Time: {time_remaining:.1f}s", True, BLACK)
        screen.blit(timer_text, (x + 10, y + 10))
        
        # Draw timer bar
        bar_width = width - 20
        bar_height = 10
        bar_x = x + 10
        bar_y = y + 40
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        fill_width = int(bar_width * (time_remaining / self.time_limit))
        color = GREEN if time_remaining > 2 else RED
        pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height))
        
        if self.puzzle_type == "simon":
            title_text = font.render("SIMON SAYS", True, BLACK)
            screen.blit(title_text, (x + 20, y + 60))
            
            if self.showing_sequence:
                instruction_text = small_font.render("Watch the sequence!", True, BLACK)
                screen.blit(instruction_text, (x + 20, y + 100))
                
                # Draw sequence display
                current_time = time.time() - self.sequence_start_time
                highlight_index = int(current_time * 2) % len(self.sequence)
                
                for i, num in enumerate(self.sequence):
                    color = YELLOW if i == highlight_index and current_time < self.show_duration else GRAY
                    rect = pygame.Rect(x + 20 + i * 60, y + 130, 50, 50)
                    pygame.draw.rect(screen, color, rect)
                    pygame.draw.rect(screen, BLACK, rect, 2)
                    num_text = font.render(str(num), True, BLACK)
                    screen.blit(num_text, (rect.centerx - 10, rect.centery - 15))
            else:
                instruction_text = small_font.render("Enter sequence (1-4):", True, BLACK)
                screen.blit(instruction_text, (x + 20, y + 100))
                
                input_text = font.render(str(self.current_input), True, BLACK)
                screen.blit(input_text, (x + 20, y + 130))
        
        elif self.puzzle_type == "math":
            title_text = font.render("MATH PROBLEM", True, BLACK)
            screen.blit(title_text, (x + 20, y + 60))
            
            problem_text = font.render(f"{self.num1} {self.operation} {self.num2} = ?", True, BLACK)
            screen.blit(problem_text, (x + 20, y + 100))
            
            instruction_text = small_font.render("Enter answer and press ENTER:", True, BLACK)
            screen.blit(instruction_text, (x + 20, y + 140))
            
            input_text = font.render(self.user_input + "_", True, BLACK)
            screen.blit(input_text, (x + 20, y + 170))
        
        elif self.puzzle_type == "stroop":
            title_text = font.render("STROOP TEST", True, BLACK)
            screen.blit(title_text, (x + 20, y + 60))
            
            instruction_text = small_font.render("What COLOR is this word?", True, BLACK)
            screen.blit(instruction_text, (x + 20, y + 100))
            
            word_text = font.render(self.word, True, self.word_color)
            screen.blit(word_text, (x + 20, y + 130))
            
            options_text = small_font.render("1:RED 2:BLUE 3:GREEN 4:YELLOW", True, BLACK)
            screen.blit(options_text, (x + 20, y + 170))

class NeuralJuggler:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Neural Juggler")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.juggle_balls = 3
        self.score = 0
        self.game_over = False
        self.paused = False
        
        # Puzzle system
        self.current_puzzle = None
        self.next_puzzle_time = time.time() + 3.0  # First puzzle after 3 seconds
        self.puzzle_interval = 10.0  # New puzzle every 10 seconds
        
        # Reflex system
        self.shapes = []
        self.cursor_x = PUZZLE_PANEL_WIDTH + REFLEX_PANEL_WIDTH // 2
        self.cursor_y = SCREEN_HEIGHT - 50
        self.target_shape = random.choice([CIRCLE, TRIANGLE, SQUARE])
        self.last_shape_spawn = 0
        self.shape_spawn_interval = 1.5  # Spawn shape every 1.5 seconds
        
        # Fonts
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
    
    def spawn_shape(self):
        shape_type = random.choice([CIRCLE, TRIANGLE, SQUARE])
        color = random.choice([RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE])
        x = random.randint(PUZZLE_PANEL_WIDTH + 30, SCREEN_WIDTH - 30)
        y = -30
        self.shapes.append(Shape(x, y, shape_type, color))
    
    def handle_shape_collision(self, shape):
        # Check if cursor is close enough to the shape
        distance = math.sqrt((self.cursor_x - shape.x)**2 + (self.cursor_y - shape.y)**2)
        if distance < 40:  # Collision detected
            if shape.shape_type == self.target_shape:
                self.score += 10
                return True  # Shape should be removed
            else:
                self.juggle_balls -= 1
                return True  # Shape should be removed (penalty for wrong catch)
        return False
    
    def update_reflex_panel(self):
        # Spawn new shapes
        current_time = time.time()
        if current_time - self.last_shape_spawn > self.shape_spawn_interval:
            self.spawn_shape()
            self.last_shape_spawn = current_time
        
        # Update shapes
        shapes_to_remove = []
        for i, shape in enumerate(self.shapes):
            shape.update()
            
            # Check collision with cursor
            if self.handle_shape_collision(shape):
                shapes_to_remove.append(i)
            
            # Check if shape reached bottom
            elif shape.y > SCREEN_HEIGHT:
                if shape.shape_type == self.target_shape:
                    self.juggle_balls -= 1  # Penalty for missing target shape
                shapes_to_remove.append(i)
        
        # Remove shapes
        for i in reversed(shapes_to_remove):
            self.shapes.pop(i)
    
    def update_puzzle_panel(self):
        current_time = time.time()
        
        # Check if it's time for a new puzzle
        if self.current_puzzle is None and current_time >= self.next_puzzle_time:
            self.current_puzzle = Puzzle()
        
        # Update current puzzle
        if self.current_puzzle:
            self.current_puzzle.update()
            
            if self.current_puzzle.completed:
                self.score += 50
                self.current_puzzle = None
                self.next_puzzle_time = current_time + self.puzzle_interval
            elif self.current_puzzle.failed or self.current_puzzle.is_expired():
                self.juggle_balls -= 1
                self.current_puzzle = None
                self.next_puzzle_time = current_time + self.puzzle_interval
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.restart_game()
                    else:
                        self.paused = not self.paused
                
                elif not self.paused and not self.game_over:
                    # Handle puzzle input
                    if self.current_puzzle:
                        self.current_puzzle.handle_input(event.key)
                    
                    # Handle cursor movement
                    if event.key == pygame.K_LEFT:
                        self.cursor_x = max(PUZZLE_PANEL_WIDTH + 20, self.cursor_x - 20)
                    elif event.key == pygame.K_RIGHT:
                        self.cursor_x = min(SCREEN_WIDTH - 20, self.cursor_x + 20)
        
        # Continuous cursor movement
        if not self.paused and not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.cursor_x = max(PUZZLE_PANEL_WIDTH + 20, self.cursor_x - 5)
            if keys[pygame.K_RIGHT]:
                self.cursor_x = min(SCREEN_WIDTH - 20, self.cursor_x + 5)
        
        return True
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw vertical divider
        pygame.draw.line(self.screen, BLACK, (PUZZLE_PANEL_WIDTH, 0), (PUZZLE_PANEL_WIDTH, SCREEN_HEIGHT), 3)
        
        # Draw puzzle panel
        if self.current_puzzle:
            self.current_puzzle.draw(self.screen, 0, 100, PUZZLE_PANEL_WIDTH, SCREEN_HEIGHT - 200)
        else:
            pygame.draw.rect(self.screen, LIGHT_GRAY, (0, 100, PUZZLE_PANEL_WIDTH, SCREEN_HEIGHT - 200))
            pygame.draw.rect(self.screen, BLACK, (0, 100, PUZZLE_PANEL_WIDTH, SCREEN_HEIGHT - 200), 3)
            waiting_text = self.font.render("Waiting for next puzzle...", True, BLACK)
            self.screen.blit(waiting_text, (20, SCREEN_HEIGHT // 2))
        
        # Draw reflex panel
        pygame.draw.rect(self.screen, WHITE, (PUZZLE_PANEL_WIDTH, 100, REFLEX_PANEL_WIDTH, SCREEN_HEIGHT - 200))
        pygame.draw.rect(self.screen, BLACK, (PUZZLE_PANEL_WIDTH, 100, REFLEX_PANEL_WIDTH, SCREEN_HEIGHT - 200), 3)
        
        # Draw target shape indicator
        target_text = self.small_font.render(f"CATCH: {self.target_shape.upper()}S", True, BLACK)
        self.screen.blit(target_text, (PUZZLE_PANEL_WIDTH + 20, 110))
        
        # Draw shapes
        for shape in self.shapes:
            shape.draw(self.screen)
        
        # Draw cursor
        pygame.draw.circle(self.screen, BLACK, (int(self.cursor_x), int(self.cursor_y)), 25, 3)
        pygame.draw.circle(self.screen, WHITE, (int(self.cursor_x), int(self.cursor_y)), 22)
        
        # Draw UI
        self.draw_ui()
        
        # Draw game over or pause screen
        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause_screen()
        
        pygame.display.flip()
    
    def draw_ui(self):
        # Draw top panel
        pygame.draw.rect(self.screen, DARK_GRAY, (0, 0, SCREEN_WIDTH, 100))
        
        # Draw juggle balls
        balls_text = self.font.render("Juggle Balls:", True, WHITE)
        self.screen.blit(balls_text, (20, 20))
        
        for i in range(self.juggle_balls):
            pygame.draw.circle(self.screen, RED, (200 + i * 40, 40), 15)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 200, 20))
        
        # Draw instructions
        instructions = [
            "Left Panel: Solve puzzles as they appear",
            "Right Panel: Use LEFT/RIGHT arrows to catch target shapes",
            "SPACE: Pause/Resume"
        ]
        
        y_offset = SCREEN_HEIGHT - 90
        for instruction in instructions:
            text = self.small_font.render(instruction, True, BLACK)
            self.screen.blit(text, (20, y_offset))
            y_offset += 25
    
    def draw_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press SPACE to restart", True, WHITE)
        
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20))
    
    def draw_pause_screen(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Draw pause text
        pause_text = self.big_font.render("PAUSED", True, WHITE)
        resume_text = self.font.render("Press SPACE to resume", True, WHITE)
        
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 30))
        self.screen.blit(resume_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10))
    
    def restart_game(self):
        self.juggle_balls = 3
        self.score = 0
        self.game_over = False
        self.paused = False
        self.current_puzzle = None
        self.next_puzzle_time = time.time() + 3.0
        self.shapes = []
        self.cursor_x = PUZZLE_PANEL_WIDTH + REFLEX_PANEL_WIDTH // 2
        self.target_shape = random.choice([CIRCLE, TRIANGLE, SQUARE])
        self.last_shape_spawn = 0
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if not self.paused and not self.game_over:
                self.update_puzzle_panel()
                self.update_reflex_panel()
                
                # Check game over condition
                if self.juggle_balls <= 0:
                    self.game_over = True
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = NeuralJuggler()
    game.run()