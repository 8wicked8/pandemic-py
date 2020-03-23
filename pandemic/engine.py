
import math
import pygame
import time
import random
from abc import ABC, abstractmethod
from pandemic.individual import Status, Individual
from pandemic.historygraph import HistoryGraph

# --------------------------------------------------------------
class IEngine(ABC):

    @abstractmethod
    def move(self, individual: Individual):
        pass

# --------------------------------------------------------------
class BasicMoveEngine(IEngine):

    def __init__(self, population: pygame.sprite.Group, screenWidth: int, screenHeight: int):
        self._population = population
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):

        # Convert angle from degree to radian.
        angleInRad = individual.angleInDeg * 2 * math.pi / 360

        # Compute the next X position.
        nextPosX = individual.position.x + individual.speed * math.cos(angleInRad)

        # Eventually do a rebounce if individual cross the Window limits.
        if nextPosX < individual.radius or nextPosX > self._screenWidth-individual.radius:
            individual.angleInDeg = 180 - individual.angleInDeg

        # Compute the next Y position.
        nextPosY = individual.position.y + individual.speed * math.sin(angleInRad)

        # Eventually do a rebounce if individual cross the Window limits.
        if nextPosY < individual.radius or nextPosY > self._screenHeight-individual.radius:
            individual.angleInDeg = - individual.angleInDeg

        # Finally update the position X and Y.
        individual.position.x = nextPosX
        individual.position.y = nextPosY

# --------------------------------------------------------------
class MoveSickEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, screenWidth: int, screenHeight: int):
        self._population = population
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):
        # In this method, we only have to modify the individual input parameter and nothing else.
        # We must not change the status (or anything else) of other individuals in the population.

        # Move the individual.
        super().move(individual)

        # Collect all the individuals that were hit due to the move (including myself since I am also part of the population).
        hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)

        # Every sick individual I meet, make me sick.
        for hitIndividual in hitIndividuals:
            if (hitIndividual != individual):
                # I have to exclude myself.                
                hitIndividual.status = Status.SICK
                break

# --------------------------------------------------------------
class MoveSickCureEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, healingTimeInSec: float, screenWidth: int, screenHeight: int):
        self._population = population
        self._healingTimeInSec = healingTimeInSec
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):
        # In this method, we only have to modify the individual input parameter and nothing else.
        # We must not change the status (or anything else) of other individuals in the population.

        # Move the individual.
        super().move(individual)

        # Only healthy individual may become sick on hit.
        if (individual.status == Status.HEALTHY):
            # Collect all the individuals that were hit due to the move (including myself since I am also part of the population).
            hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)
            # Every hit with a sick individual I meet, make me sick.
            for hitIndividual in hitIndividuals:
                if (hitIndividual != individual and hitIndividual.status == Status.SICK):
                    individual.status = Status.SICK
                    # Initialize the timer that measures time until I am cured.
                    individual.sickTime = time.time()
                    break
        else:
            # After healing time elapsed, an individual is cured.
            if time.time() - individual.sickTime > self._healingTimeInSec:
                individual.status = Status.CURED

# --------------------------------------------------------------
class MoveSickDeadEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, deadTimeInSec: float, screenWidth: int, screenHeight: int):
        self._population = population
        self._deadTimeInSec = deadTimeInSec
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):
        # In this method, we only have to modify the individual input parameter and nothing else.
        # We must not change the status (or anything else) of other individuals in the population.

        # Only alive individual can do something : move...
        if (individual.status != Status.DEAD):
            super().move(individual)

            # Only healthy individual may become sick on hit.
            if (individual.status == Status.HEALTHY):
                # Collect all the individuals that were hit due to the move (including myself since I am also part of the population).
                hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)
                # Every hit with a sick individual I meet, make me sick.
                for hitIndividual in hitIndividuals:
                    if (hitIndividual != individual and hitIndividual.status == Status.SICK):
                        individual.status = Status.SICK
                        # Initialize the timer that measures time until I am cured.
                        individual.sickTime = time.time()
                        break
            else:
                # After dead time elapsed, an individual is dead.
                if time.time() - individual.sickTime > self._deadTimeInSec:
                    individual.status = Status.DEAD

# --------------------------------------------------------------
class MoveSickCureWithGraphEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, historygraph: HistoryGraph, healingTimeInSec: float, screenWidth: int, screenHeight: int):
        self._population = population
        self._historygraph = historygraph
        self._healingTimeInSec = healingTimeInSec
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):
        # In this method, we only have to modify the individual input parameter and nothing else.
        # We must not change the status (or anything else) of other individuals in the population.

        # Move the individual.
        super().move(individual)

        # Only healthy individual may become sick on hit.
        if (individual.status == Status.HEALTHY):
            # Collect all the individuals that were hit due to the move (including myself since I am also part of the population).
            hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)
            # Every hit with a sick individual I meet, make me sick.
            for hitIndividual in hitIndividuals:
                if (hitIndividual != individual and hitIndividual.status == Status.SICK):
                    individual.status = Status.SICK
                    # Initialize the timer that measures time until I am cured.
                    individual.sickTime = time.time()
                    # Increment the sick counter on graph.
                    self._historygraph.incrementSick()
                    # Decrement the healthy counter on the graph.
                    self._historygraph.decrementHealthy()
                    break
        else:
            # After healing time elapsed, an individual is cured.
            if individual.status == Status.SICK and time.time() - individual.sickTime > self._healingTimeInSec:
                individual.status = Status.CURED
                # Increment the cured counter on graph.
                self._historygraph.incrementCured()
                # Decrement the sick counter on the graph.
                self._historygraph.decrementSick()
            
# --------------------------------------------------------------
class FullEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, historygraph: HistoryGraph, healingTimeInSec: float, sickProbability: float, deathProbability: float, screenWidth: int, screenHeight: int):
        self._population = population
        self._historygraph = historygraph
        self._healingTimeInSec = healingTimeInSec
        self._sickProbability = sickProbability
        self._deathProbability = deathProbability
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):
        # In this method, we only have to modify the individual input parameter and nothing else.
        # We must not change the status (or anything else) of other individuals in the population.

        # Only alive individual can do something : move...
        if (individual.status != Status.DEAD):
            # Move the individual.
            super().move(individual)

            # Only healthy individual may become sick on hit.
            if (individual.status == Status.HEALTHY):
                # Collect all the individuals that were hit due to the move (including myself since I am also part of the population).
                hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)
                # Every hit with a sick individual I meet, make me sick.
                for hitIndividual in hitIndividuals:
                    if (hitIndividual != individual and hitIndividual.status == Status.SICK):
                        rand = random.random()
                        # Apply probability of being sick.
                        if (rand < self._sickProbability):
                            individual.status = Status.SICK
                            # Initialize the timer that measures time until I am cured.
                            individual.sickTime = time.time()
                            # Increment the sick counter on graph.
                            self._historygraph.incrementSick()
                            # Decrement the healthy counter on the graph.
                            self._historygraph.decrementHealthy()
                            break
            else:
                # After healing time elapsed, an individual is cured.
                if individual.status == Status.SICK and time.time() - individual.sickTime > self._healingTimeInSec:
                    rand = random.random()
                    # Apply probability of being dead.
                    if (rand < self._deathProbability):
                        individual.status = Status.DEAD
                        # Increment the dead counter on graph.
                        self._historygraph.incrementDead()
                        # Decrement the sick counter on the graph.
                        self._historygraph.decrementSick()
                    else:
                        individual.status = Status.CURED
                        # Increment the cured counter on graph.
                        self._historygraph.incrementCured()
                        # Decrement the sick counter on the graph.
                        self._historygraph.decrementSick()