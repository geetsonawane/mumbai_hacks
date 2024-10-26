import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balance Ball with Bounce")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Game settings
FPS = 60
BALL_RADIUS = 20
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 5
GRAVITY = 0.5
BOUNCE_SPEED = -10  # Speed of the ball when it bounces up

# Ball class
class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 3
        self.speed_y = 0

    def move(self, platform):
        self.speed_y += GRAVITY  # Gravity pulls the ball down
        self.y += self.speed_y

        # Check collision with platform
        if platform.y - self.radius < self.y < platform.y and platform.x < self.x < platform.x + platform.width:
            self.y = platform.y - self.radius  # Adjust ball's position to sit on the platform
            self.speed_y = BOUNCE_SPEED  # Ball bounces upwards

        # Boundary checks (if ball falls off the screen)
        if self.y > SCREEN_HEIGHT:
            return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)

# Platform class
class Platform:
    def __init__(self):
        self.width = PLATFORM_WIDTH
        self.height = PLATFORM_HEIGHT
        self.x = (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - 100
        self.speed_x = 0

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -PLATFORM_SPEED
        elif keys[pygame.K_RIGHT]:
            self.speed_x = PLATFORM_SPEED
        else:
            self.speed_x = 0

        self.x += self.speed_x

        # Keep platform within screen boundaries
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Main game loop
def game():
    running = True
    clock = pygame.time.Clock()

    ball = Ball()
    platform = Platform()

    while running:
        clock.tick(FPS)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Move platform and ball
        platform.move()
        ball_on_platform = ball.move(platform)

        # Check if ball is still on the screen
        if not ball_on_platform:
            print("Game Over!")
            running = False

        # Redraw screen
        screen.fill(BLACK)
        ball.draw(screen)
        platform.draw(screen)

        pygame.display.flip()

    # Quit the game
    pygame.quit()
    sys.exit()

# Start the game
game()
