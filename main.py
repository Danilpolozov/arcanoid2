import pgzrun
from pgzero.rect import Rect
import random

WIDTH = 602
HEIGHT = 800


class Paddle:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT - 20
        self.width = 80
        self.height = 20
        self.color = (255, 255, 255)

    def draw(self):
        screen.draw.filled_rect(Rect((self.x - self.width / 2, self.y - self.height / 2), (self.width, self.height)),
                                self.color)




pgzrun.go()
