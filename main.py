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


class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.radius = 10
        self.color = (255, 255, 255)
        self.speed_x = random.randint(2, 5)
        self.speed_y = random.randint(2, 5)

    def update(self, dt):
        self.x += self.speed_x
        self.y += self.speed_y
        if self.x + self.radius >= WIDTH or self.x - self.radius <= 0:
            self.speed_x = -self.speed_x
        if self.y + self.radius >= HEIGHT or self.y - self.radius <= 0:
            if self.y + self.radius >= HEIGHT:
                global lives
                lives = lives - 1
            self.speed_y = -self.speed_y

    def draw(self):
        screen.draw.circle((self.x, self.y), self.radius, self.color)


class Obstacle:
	pass


pgzrun.go()
