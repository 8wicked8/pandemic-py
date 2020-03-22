
import math
from pandemic.individual import Individual

# --------------------------------------------------------------
class Engine:

    def __init__(self, screenWidth: int, screenHeight: int):
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

        