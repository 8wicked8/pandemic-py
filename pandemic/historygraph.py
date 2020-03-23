import pygame
import time
from typing import List
from pandemic.geometry import Point2D
from pandemic.color import *

# --------------------------------------------------------------
class Record:

    # -------------------
    def __init__(self, timestamp: float, counter: int):
        self.timestamp = timestamp
        self.counter = counter

# --------------------------------------------------------------
class HistoryGraph(pygame.sprite.Sprite):

    # -------------------
    def __init__(self, populationSize: int, position: Point2D, width: int, height: int, color: pygame.Color):

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.position = position
        self.width = width
        self.height = height
        self.color = color
        self._healthyCount = populationSize
        self._healthyRecords = []
        self._sickCount = 0
        self._sickRecords = []        
        self._curedCount = 0
        self._curedRecords = []
        self._deadCount = 0
        self._deadRecords = []

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK) # Background color.
        self.image.set_colorkey(BLACK) # Transparent color.

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height), 1)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x
        self.rect.y = self.position.y

    # -------------------
    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    # -------------------
    def update(self):
        self.rect.x = self.position.x
        self.rect.y = self.position.y

        self.image.fill(BLACK) # Background color.
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, self.width, self.height), 1)
        self.plot(self._healthyRecords, pygame.Color("green"))
        self.plot(self._sickRecords, pygame.Color("red"))
        self.plot(self._curedRecords, pygame.Color("blue"))
        self.plot(self._deadRecords, pygame.Color("white"))

    # -------------------
    def plot(self, records: List[Record], color: pygame.Color):
        if (len(records) > 1):
            xMin = records[0].timestamp
            xMax = records[len(records)-1].timestamp
            if (xMax > xMin):
                yMax = self._healthyCount + self._sickCount + self._curedCount + self._deadCount

                points = []
                for record in records:
                    points.append((self.rescaleX(record.timestamp-xMin, xMax-xMin), self.rescaleY(record.counter, yMax)))
                pygame.draw.lines(self.image, color, False, points)

    # -------------------
    def rescaleX(self, x: float, xMax: float) -> float:
        return x * self.width / xMax

    # -------------------
    def rescaleY(self, y: float, yMax: float) -> float:
        return round((yMax - y) * self.height / yMax)

    # -------------------
    def decrementHealthy(self):
        self._healthyCount -= 1
        self._healthyRecords.append(Record(time.time(), self._healthyCount))

    # -------------------
    def incrementSick(self):
        self._sickCount += 1 
        self._sickRecords.append(Record(time.time(), self._sickCount))

    # -------------------
    def decrementSick(self):
        self._sickCount -= 1  
        self._sickRecords.append(Record(time.time(), self._sickCount))

    # -------------------
    def incrementCured(self):
        self._curedCount += 1
        self._curedRecords.append(Record(time.time(), self._curedCount))

    # -------------------
    def incrementDead(self):
        self._deadCount += 1                            
        self._deadRecords.append(Record(time.time(), self._deadCount))
