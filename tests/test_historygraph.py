import unittest
import pygame
import random
from pandemic.historygraph import HistoryGraph
from pandemic.geometry import Point2D
from pandemic.color import *

# Screen dimensions.
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

HISTORYGRAPH_HEIGHT = 100

# --------------------------------------------------------------
class TestHistoryGraph(unittest.TestCase):

    # -------------------
    def setUp(self):
        pygame.init()
        self._screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption(self.__str__())

    # -------------------
    def tearDown(self):
        pygame.quit()

    # -------------------
    def test_displayEmptyHistoryGraph(self):
        historygraph = HistoryGraph(50, Point2D(0, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT), SCREEN_WIDTH, HISTORYGRAPH_HEIGHT, WHITE)

        self._eventLoop(historygraph, 2000)

    # -------------------
    def test_displayHealthyHistoryGraph(self):
        historygraph = HistoryGraph(20, Point2D(0, SCREEN_HEIGHT-HISTORYGRAPH_HEIGHT), SCREEN_WIDTH, HISTORYGRAPH_HEIGHT, WHITE)

        self._eventLoop(historygraph, 2000)        

    # -------------------
    def _eventLoop(self, historygraph: HistoryGraph, timeInMillis: int):
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

                # Change counters on the graph.
                if (historygraph._healthyCount > 0):
                    historygraph.decrementHealthy()
                    historygraph.incrementSick()
                    pygame.time.delay(random.randrange(100))

                # Calls update() method on every sprite in the list
                historygraph.update()

                # Draw all the sprites
                historygraph.draw(self._screen)

                # Limit to 20 frames per second
                clock.tick(20)

                # Go ahead and update the screen with what we've drawn.
                pygame.display.flip()
