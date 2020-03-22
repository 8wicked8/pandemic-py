import unittest
import pygame
import random
from pandemic.individual import Individual
from pandemic.engine import Engine
from pandemic.geometry import Point2D

# Screen dimensions.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)

# --------------------------------------------------------------
class TestIndividual(unittest.TestCase):

    # -------------------
    def setUp(self):
        pygame.init()
        self._screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    # -------------------
    def tearDown(self):
        pygame.quit()

    # -------------------
    def test_display(self):

        population = pygame.sprite.Group()
        for i in range(0, 50):
            speed = 0
            angle = 0
            radius = random.randrange(30)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-radius))
            individual = Individual(randomPosition, speed, angle, radius, self._randomColor())
            population.add(individual)

        self._eventLoop(population, None, 5000)

    # -------------------
    def test_move(self):

        population = pygame.sprite.Group()
        for i in range(0, 50):            
            speed = random.randrange(10)
            angle = random.randrange(360)
            radius = random.randrange(30)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-radius))
            individual = Individual(randomPosition, speed, angle, radius, self._randomColor())
            population.add(individual)

        engine = Engine(640, 480)

        self._eventLoop(population, engine, 30000)

    # -------------------
    def _eventLoop(self, population: pygame.sprite.Group, engine: Engine, timeInMillis: int):
        pygame.time.set_timer(pygame.USEREVENT, timeInMillis)

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
                self._screen.fill(BLACK)

                # Move every individuals of the population.
                if (engine != None):
                    for individual in population:
                        engine.move(individual)
                    
                # Calls update() method on every sprite in the list
                population.update()

                # Draw all the spites
                population.draw(self._screen)

                # Limit to 20 frames per second
                clock.tick(20)

                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

    # -------------------
    def _randomColor(self) -> pygame.Color:
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))