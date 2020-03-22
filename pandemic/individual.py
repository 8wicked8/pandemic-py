import pygame
import math
from enum import Enum
from pandemic.geometry import Point2D
from pandemic.color import *

# --------------------------------------------------------------
class Status(Enum):
    HEALTHY = 0,
    SICK = 1,
    CURED = 2,
    DEAD = 3

    def __str__(self):
        return self.name

# --------------------------------------------------------------
class Individual(pygame.sprite.Sprite):

    # -------------------
    def __init__(self, position: Point2D, speed: float, angleInDeg: float, radius: float, color: pygame.Color):

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.position = position
        self.speed = speed
        self.angleInDeg = angleInDeg
        self.radius = radius
        self.color = color
        self.status = None
        self.sickTime = None

        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.fill(BLACK) # Background color.
        self.image.set_colorkey(BLACK) # Transparent color.

        pygame.draw.circle(self.image, self.color, (radius, radius), radius, 0)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x - self.radius
        self.rect.y = self.position.y - self.radius

    # -------------------
    @classmethod
    def create(cls, position: Point2D, speed: float, angleInDeg: float, radius: float, status: Status):          

        res = cls(position, speed, angleInDeg, radius, cls.toColor(status))
        res.status = status
        return res

    # -------------------
    @classmethod
    def toColor(cls, status: Status) -> pygame.Color:

        if (status == Status.HEALTHY):
            color = GREEN
        elif (status == Status.SICK):
            color = RED
        elif (status == Status.CURED):
            color = BLUE    
        elif (status == Status.DEAD):
            color = WHITE 
        
        return color

    # -------------------
    def update(self):

        if (self.status != None):
            self.color = Individual.toColor(self.status)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, 0)        
        self.rect.x = self.position.x - self.radius
        self.rect.y = self.position.y - self.radius

