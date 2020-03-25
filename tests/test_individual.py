import unittest
import pygame
import random
import time
from pandemic.individual import Individual, Status
from pandemic.engine import IEngine, BasicMoveEngine, MoveSickEngine, MoveSickCureEngine, MoveSickDeadEngine, MoveSickCureWithGraphEngine, FullEngine
from pandemic.geometry import Point2D
from pandemic.color import *
from pandemic.historygraph import HistoryGraph

# Screen dimensions.
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

HISTORYGRAPH_HEIGHT = 200

# --------------------------------------------------------------
class TestIndividual(unittest.TestCase):

    # -------------------
    def setUp(self):
        pygame.init()
        self._screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(self.__str__())

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

        self._eventLoop(population, None, None, 2000)

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

        engine = BasicMoveEngine(population, SCREEN_WIDTH, SCREEN_HEIGHT)

        self._eventLoop(population, None, engine, 2000)

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

        engine = MoveSickEngine(population, SCREEN_WIDTH, SCREEN_HEIGHT)

        self._eventLoop(population, None, engine, 10000)        

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

        engine = MoveSickCureEngine(population, 10, SCREEN_WIDTH, SCREEN_HEIGHT)

        self._eventLoop(population, None, engine, 30000)             

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

        engine = MoveSickDeadEngine(population, 10, SCREEN_WIDTH, SCREEN_HEIGHT)

        self._eventLoop(population, None, engine, 30000)     

    # -------------------
    def test_cure_with_graph(self):

        historygraph = HistoryGraph(200, Point2D(0, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT), SCREEN_WIDTH, HISTORYGRAPH_HEIGHT, WHITE)
        population = pygame.sprite.Group()
        for i in range(0, 200):            
            speed = random.randrange(10)
            angle = random.randrange(360)
            radius = random.randrange(5)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT-radius))
            individual = Individual.create(randomPosition, speed, angle, radius, Status.HEALTHY)
            population.add(individual)

        # First individual is sick.
        population.sprites()[0].status = Status.SICK
        population.sprites()[0].sickTime = time.time()

        engine = MoveSickCureWithGraphEngine(population, historygraph, 10, SCREEN_WIDTH, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT)

        self._eventLoop(population, historygraph, engine, 30000)       

    # -------------------
    def test_full(self):

        historygraph = HistoryGraph(200, Point2D(0, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT), SCREEN_WIDTH, HISTORYGRAPH_HEIGHT, WHITE)
        population = pygame.sprite.Group()
        for i in range(0, 200):            
            speed = random.randrange(10)
            angle = random.randrange(360)
            radius = random.randrange(5)
            randomPosition = Point2D(random.randrange(radius, SCREEN_WIDTH-radius), random.randrange(radius, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT-radius))
            individual = Individual.create(randomPosition, speed, angle, radius, Status.HEALTHY)
            population.add(individual)

        # First individual is sick.
        population.sprites()[0].status = Status.SICK
        population.sprites()[0].sickTime = time.time()

        engine = FullEngine(population, historygraph, 10, 0.5, 0.02, SCREEN_WIDTH, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT)

        self._eventLoop(population, historygraph, engine, 120000)    

    # -------------------
    def _eventLoop(self, population: pygame.sprite.Group, historygraph: HistoryGraph, engine: IEngine, timeInMillis: int):
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
                    
                if (historygraph != None):
                    # Calls update() method on every sprite in the list
                    historygraph.update()

                    # Draw all the sprites
                    historygraph.draw(self._screen)

                # Calls update() method on every sprite in the list
                population.update()

                # Draw all the sprites
                population.draw(self._screen)

                # Limit to 20 frames per second
                clock.tick(20)

                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()

    # -------------------
    def _randomColor(self) -> pygame.Color:
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))