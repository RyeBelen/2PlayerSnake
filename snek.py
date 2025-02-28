import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 800
HEIGHT = 600
BLOCK_SIZE = 20
SPEED = 15

# Colors
BACKGROUND = (30, 30, 30)
BORDER = (100, 100, 100)
FOOD_COLOR = (255, 50, 50)
SCORE_COLORS = [(0, 200, 255), (255, 215, 0)]

# Player colors with gradients
PLAYER_COLORS = [
    [(0, 255 - i*5, 255) for i in range(20)],  # Cyan gradient
    [(255, 215 - i*5, 0) for i in range(20)]   # Gold gradient
]

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dual Snake Battle")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

class Snake:
    def __init__(self, start_pos, controls, color_gradient):
        self.segments = [start_pos]
        self.direction = (0, 0)
        self.controls = controls
        self.color_gradient = color_gradient
        self.score = 0

    def move(self):
        head = self.segments[0]
        new_head = (head[0] + self.direction[0] * BLOCK_SIZE,
                    head[1] + self.direction[1] * BLOCK_SIZE)
        self.segments.insert(0, new_head)
        self.segments.pop()

    def grow(self):
        self.segments.append(self.segments[-1])
        self.score += 1

    def draw(self):
        for i, (x, y) in enumerate(self.segments):
            color = self.color_gradient[min(i, len(self.color_gradient)-1)]
            pygame.draw.rect(screen, color, (x, y, BLOCK_SIZE-2, BLOCK_SIZE-2),
                             border_radius=8 if i == 0 else 4)

    def check_collision(self, other):
        head = self.segments[0]
        # Wall collision
        if (head[0] < 20 or head[0] >= WIDTH-40 or
            head[1] < 20 or head[1] >= HEIGHT-40):
            return True
        # Self collision
        if head in self.segments[1:]:
            return True
        # Other snake collision
        if head in other.segments:
            return True
        return False

# Initialize snakes
player1 = Snake((WIDTH//4, HEIGHT//2), {
    pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)
}, PLAYER_COLORS[0])

player2 = Snake((3*WIDTH//4, HEIGHT//2), {
    pygame.K_w: (0, -1), pygame.K_s: (0, 1),
    pygame.K_a: (-1, 0), pygame.K_d: (1, 0)
}, PLAYER_COLORS[1])

# Initial food
food = (random.randrange(20, WIDTH-40, BLOCK_SIZE),
        random.randrange(20, HEIGHT-40, BLOCK_SIZE))

def draw_food():
    pygame.draw.circle(screen, FOOD_COLOR, (food[0]+10, food[1]+10), 8)
    pygame.draw.circle(screen, (255, 150, 150), (food[0]+10, food[1]+10), 8, 2)

def draw_borders():
    pygame.draw.rect(screen, BORDER, (19, 19, WIDTH-38, HEIGHT-38), 2)

def draw_scores():
    score1 = font.render(f"Player 1: {player1.score}", True, SCORE_COLORS[0])
    score2 = font.render(f"Player 2: {player2.score}", True, SCORE_COLORS[1])
    screen.blit(score1, (30, 10))
    screen.blit(score2, (WIDTH - 150, 10))

def game_over():
    screen.fill(BACKGROUND)
    if player1.score > player2.score:
        text = font.render("Player 1 Wins!", True, SCORE_COLORS[0])
    elif player2.score > player1.score:
        text = font.render("Player 2 Wins!", True, SCORE_COLORS[1])
    else:
        text = font.render("It's a Tie!", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 20))
    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
# In the event handling section (lines 96-104), replace with:
        if event.type == pygame.KEYDOWN:
            for snake in [player1, player2]:
                if event.key in snake.controls:
                    new_dir = snake.controls[event.key]
                    # Prevent 180-degree turn
                    if (new_dir[0] != -snake.direction[0] or 
                        new_dir[1] != -snake.direction[1]):
                        snake.direction = new_dir
                        break  # Only one snake can respond to a key press

    # Initial movement check
    if player1.direction == (0, 0) and player2.direction == (0, 0):
        # Wait for both players to start moving
        screen.fill(BACKGROUND)
        start_text = font.render("Press any direction key to start!", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        pygame.display.update()
        continue

    # Move snakes
    player1.move()
    player2.move()

    # Check collisions
    if player1.check_collision(player2) or player2.check_collision(player1):
        game_over()

    # Food consumption
    if player1.segments[0] == food:
        player1.grow()
        food = (random.randrange(20, WIDTH-40, BLOCK_SIZE),
                random.randrange(20, HEIGHT-40, BLOCK_SIZE))
    if player2.segments[0] == food:
        player2.grow()
        food = (random.randrange(20, WIDTH-40, BLOCK_SIZE),
                random.randrange(20, HEIGHT-40, BLOCK_SIZE))

    # Drawing
    screen.fill(BACKGROUND)
    draw_borders()
    draw_food()
    player1.draw()
    player2.draw()
    draw_scores()
    
    pygame.display.update()
    clock.tick(SPEED)

pygame.quit()