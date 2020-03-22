
import math
import pygame
import time
from abc import ABC, abstractmethod
from pandemic.individual import Status, Individual

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
        angleInRad = individual.angleInDeg * 2 * math.pi / 360

        nextPosX = individual.position.x + individual.speed * math.cos(angleInRad)
        if nextPosX < individual.radius or nextPosX > self._screenWidth-individual.radius:
            individual.angleInDeg = 180 - individual.angleInDeg

        nextPosY = individual.position.y + individual.speed * math.sin(angleInRad)
        if nextPosY < individual.radius or nextPosY > self._screenHeight-individual.radius:
            individual.angleInDeg = - individual.angleInDeg

        individual.position.x = nextPosX
        individual.position.y = nextPosY

# --------------------------------------------------------------
class MoveSickEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, screenWidth: int, screenHeight: int):
        self._population = population
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):

        super().move(individual)

        hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)

        for hitIndividual in hitIndividuals:
            if (hitIndividual != individual):
                hitIndividual.status = Status.SICK

# --------------------------------------------------------------
class MoveSickCureEngine(BasicMoveEngine):

    def __init__(self, population: pygame.sprite.Group, healingTimeInSec: float, screenWidth: int, screenHeight: int):
        self._population = population
        self._healingTimeInSec = healingTimeInSec
        self._screenWidth = screenWidth
        self._screenHeight = screenHeight

    def move(self, individual: Individual):

        super().move(individual)

        if (individual.status == Status.HEALTHY):
            hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)

            for hitIndividual in hitIndividuals:
                if (hitIndividual != individual and hitIndividual.status == Status.SICK):
                    individual.status = Status.SICK
                    individual.sickTime = time.time()
        else:
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

        if (individual.status != Status.DEAD):
            super().move(individual)

            if (individual.status == Status.HEALTHY):
                hitIndividuals = pygame.sprite.spritecollide(individual, self._population, False, pygame.sprite.collide_circle)

                for hitIndividual in hitIndividuals:
                    if (hitIndividual != individual and hitIndividual.status == Status.SICK):
                        individual.status = Status.SICK
                        individual.sickTime = time.time()
            else:
                if time.time() - individual.sickTime > self._deadTimeInSec:
                    individual.status = Status.DEAD


            
