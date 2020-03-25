import unittest
import pygame
import random
import math

# Screen dimensions.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

RADIUS = 10
SPEED = 10

# --------------------------------------------------------------
class Ball(pygame.sprite.Sprite):

    def __init__(self):

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([2*RADIUS, 2*RADIUS])
        self.image.fill(pygame.Color("black")) # Background color.
        self.image.set_colorkey(pygame.Color("black")) # Transparent color.

        pygame.draw.circle(self.image, pygame.Color("red"), (RADIUS, RADIUS), RADIUS, 0)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

        self.rect.center = (random.randrange(RADIUS, SCREEN_WIDTH-RADIUS), random.randrange(RADIUS, SCREEN_HEIGHT-RADIUS))
        self.angleInDeg = random.randrange(360)

    # -------------------
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    # -------------------
    def update(self):
        
        # Convert angle from degree to radian.
        angleInRad = self.angleInDeg * 2 * math.pi / 360

        # Compute the next X position.
        nextPosX = self.rect.x + RADIUS + SPEED * math.cos(angleInRad)

        # Eventually do a rebounce if individual cross the Window limits.
        if nextPosX < RADIUS or nextPosX > SCREEN_WIDTH-RADIUS:
            self.angleInDeg = 180 - self.angleInDeg

        # Compute the next Y position.
        nextPosY = self.rect.y + RADIUS + SPEED * math.sin(angleInRad)

        # Eventually do a rebounce if individual cross the Window limits.
        if nextPosY < RADIUS or nextPosY > SCREEN_HEIGHT-RADIUS:
            self.angleInDeg = -self.angleInDeg

        # Finally update the position X and Y.
        self.rect.center = (nextPosX, nextPosY)

# --------------------------------------------------------------
class TestBallRebounce(unittest.TestCase):

    def test_ballRebounce(self):

        # Initialize Pygame.
        pygame.init()

        # Create the window.
        self._screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(self.__str__())
        
        # Create the ball object.
        ball = Ball()

        # Initialize the timer at 60s that trigger the exit loop.
        pygame.time.set_timer(pygame.USEREVENT, 60000)

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
                ball.update()

                # Draw all the sprites
                ball.draw(self._screen)

                # Limit to 20 frames per second
                clock.tick(20)

                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

        # Dispose Pygame.
        pygame.quit()
