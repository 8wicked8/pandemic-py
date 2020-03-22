import unittest
import pygame
import random
import time
from pandemic.individual import Individual, Status
from pandemic.engine import IEngine, BasicMoveEngine, MoveSickEngine, MoveSickCureEngine, MoveSickDeadEngine
from pandemic.geometry import Point2D
from pandemic.color import *

# Screen dimensions.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

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

        engine = BasicMoveEngine(population, 640, 480)

        self._eventLoop(population, engine, 10000)

    # -------------------
    def test_sick(self):

        population = pygame.sprite.Group()
        for i in range(0, 50):            
            speed = random.randrange(10)
            angle = random.randrange(360)
            radius = random.randrange(30)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-radius))
            individual = Individual.create(randomPosition, speed, angle, radius, Status.HEALTHY)
            population.add(individual)

        engine = MoveSickEngine(population, 640, 480)

        self._eventLoop(population, engine, 10000)        

    # -------------------
    def test_cure(self):

        population = pygame.sprite.Group()
        for i in range(0, 50):            
            speed = random.randrange(10)
            angle = random.randrange(360)
            radius = random.randrange(30)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-radius))
            individual = Individual.create(randomPosition, speed, angle, radius, Status.HEALTHY)
            population.add(individual)

        # First individual is sick.
        population.sprites()[0].status = Status.SICK
        population.sprites()[0].sickTime = time.time()

        engine = MoveSickCureEngine(population, 10, 640, 480)

        self._eventLoop(population, engine, 30000)             

    # -------------------
    def test_dead(self):

        population = pygame.sprite.Group()
        for i in range(0, 50):            
            speed = random.randrange(10)
            angle = random.randrange(360)
            radius = random.randrange(30)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-radius))
            individual = Individual.create(randomPosition, speed, angle, radius, Status.HEALTHY)
            population.add(individual)

        # First individual is sick.
        population.sprites()[0].status = Status.SICK
        population.sprites()[0].sickTime = time.time()

        engine = MoveSickDeadEngine(population, 10, 640, 480)

        self._eventLoop(population, engine, 30000)     

    # -------------------
    def _eventLoop(self, population: pygame.sprite.Group, engine: IEngine, timeInMillis: int):
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