import pygame
import math
from pandemic.geometry import Point2D, Vector2D

BLACK = (  0,   0,   0)

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

        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.fill(BLACK) # Background color.
        self.image.set_colorkey(BLACK) # Transparent color.

        pygame.draw.circle(self.image, color, (radius, radius), radius, 0)

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x = self.position.x - self.radius
        self.rect.y = self.position.y - self.radius

    # -------------------
    def update(self):        
        self.rect.x = self.position.x - self.radius
        self.rect.y = self.position.y - self.radius

