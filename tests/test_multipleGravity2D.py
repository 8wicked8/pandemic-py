import unittest
import pygame
import random
import math
import time

# Number of animated balls.
NB_BALLS = 200

# Screen dimensions.
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

RADIUS = 3 # pixel
RESTITUTION_COEFFICIENT = 0.9 # The coefficient of restitution is the ratio of the final to initial relative velocity between two objects after they collide.
TIME_COEFFICIENT = 1 # = 1 : Normal, > 1 : Faster, < 1 : Slower.
SCALE = 1 # Number of pixel per meter.

# Earth mass.
MASS = 1000 # kg

# Gravitational constant.
G = 1 # m3 kg-1 s-2

BOXING_LIMIT = 200

# --------------------------------------------------------------
class Point2D:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# --------------------------------------------------------------
Vector2D = Point2D

# --------------------------------------------------------------
class Ball(pygame.sprite.Sprite):

    def __init__(self, mass: float, balls: pygame.sprite.Group, staticPosition: Point2D):

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.mass = mass
        self.balls = balls
        self.staticPosition = staticPosition

        self.timestamp = time.time()

        # All the measure below are in meters. We use SCALE factor to convert from pixel to meter.
        self.radius = RADIUS / SCALE # In meter.
        self.minLimits = Point2D(self.radius + BOXING_LIMIT, self.radius + BOXING_LIMIT) # In meter.
        self.maxLimits = Point2D(SCREEN_WIDTH / SCALE - self.radius - BOXING_LIMIT, SCREEN_HEIGHT / SCALE - self.radius - BOXING_LIMIT) # In meter.

        if (self.staticPosition != None):
            self.position = staticPosition
        else:    
            self.position = Point2D(random.uniform(self.minLimits.x, self.maxLimits.x), random.uniform(self.minLimits.y, self.maxLimits.y)) # In meter.

        self.speed = Vector2D(random.uniform(-10/SCALE, 10/SCALE), random.uniform(-10/SCALE, 10/SCALE)) # In meter/s.
        self.acceleration = Vector2D(0, 0) # In meter/s².
        
        self.image = pygame.Surface([2*RADIUS, 2*RADIUS])
        self.image.fill(pygame.Color("black")) # Background color.
        self.image.set_colorkey(pygame.Color("black")) # Transparent color.

        pygame.draw.circle(self.image, pygame.Color("red"), (RADIUS, RADIUS), RADIUS, 0)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        # We convert back from meter to pixel.
        self.rect.center = (self.position.x * SCALE, self.position.y * SCALE) # In pixel.

    # -------------------
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    # -------------------
    def update(self):
        
        if (self.staticPosition != None):
            return

        # New time measure.
        now = time.time()
        dt = (now - self.timestamp) * TIME_COEFFICIENT

        # New acceleration computation : Acceleration is always the same.
        # Using Newton's law of universal gravitation : F = G . ml.m2 / r²
        self.acceleration = Vector2D(0, 0) 
        for ball in self.balls:
            if (ball != self):
                # We ignore ourself among the ball set.
                dx = ball.position.x - self.position.x
                dy = ball.position.y - self.position.y
                # Using the Pythagorean theorem, we can compute the distance between me and the other ball.
                r = math.sqrt(dx * dx + dy * dy)
                a = G * ball.mass / (r * r)
                # Using the Thales theorem, we can deduce acceleration components x and y.
                self.acceleration.x += dx * a / r
                self.acceleration.y += dy * a / r

        # New speed computation.
        self.speed.x += self.acceleration.x * dt
        self.speed.y += self.acceleration.y * dt
        
        # New position computation.
        self.position.x += self.speed.x * dt
        self.position.y += self.speed.y * dt

        # # Eventually do a rebounce if individual cross the Window limits.
        # if self.position.x < self.minLimits.x or self.position.x > self.maxLimits.x:
        #     self.speed.x = -self.speed.x * RESTITUTION_COEFFICIENT
        #     # Readjust the position inside the limit.
        #     self.position.x = min(max(self.position.x, self.minLimits.x), self.maxLimits.x)

        # if self.position.y < self.minLimits.y or self.position.y > self.maxLimits.y:
        #     self.speed.y = -self.speed.y * RESTITUTION_COEFFICIENT
        #     # Readjust the position inside the limit.
        #     self.position.y = min(max(self.position.y, self.minLimits.y), self.maxLimits.y)

        # Finally update the position X and Y.
        self.rect.center = (self.position.x * SCALE, self.position.y * SCALE)

        # Update the timestamp.
        self.timestamp = now

# --------------------------------------------------------------
class TestMultipleGravity2D(unittest.TestCase):

    def test_multipleGravity2D(self):

        # Initialize Pygame.
        pygame.init()

        # Create the window.
        self._screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(self.__str__())

        # Create all the ball objects.
        balls = pygame.sprite.Group()
        massiveBall = Ball(1000 * MASS, balls, Point2D(SCREEN_WIDTH / 2 / SCALE, SCREEN_HEIGHT / 2 / SCALE)) # Create at the center a static massive ball.
        balls.add(massiveBall)
        for i in range(0, NB_BALLS-1):           
            ball = Ball(MASS, balls, None)
            balls.add(ball)

        # Initialize the timer at 60s that trigger the exit loop.
        #pygame.time.set_timer(pygame.USEREVENT, 120000)

        # Loop until the user clicks the close button.
        done = False
        
        # Used to manage how fast the screen updates
        clock = pygame.time.Clock()

        # -------- Main Program Loop -----------
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    done = True
                if event.type == pygame.QUIT:
                    done = True
            else:
                        
                # Clear the screen
                self._screen.fill(pygame.Color("black"))

                # Calls update() method on every sprite in the list
                balls.update()

                # Draw all the sprites
                balls.draw(self._screen)

                # Limit to 60 frames per second
                clock.tick(60)

                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

        # Dispose Pygame.
        pygame.quit()
