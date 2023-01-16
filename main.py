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
    def __init__(self, x, y, width, height, strength, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.strength = strength

    def draw(self):
        screen.draw.filled_rect(Rect((self.x - self.width / 2, self.y - self.height / 2), (self.width, self.height)),
                                self.color)


obstacles = []
for row in range(3):
    for col in range(10):
        x = col * 60 + 20
        y = (row * 60) + 50
        width = 50
        height = 50
        strength = random.randint(1, 3)
        color = (255, 0, 0) if strength == 1 else (0, 255, 0) if strength == 2 else (0, 0, 255)
        obstacles.append(Obstacle(x, y, width, height, strength, color))


def update(dt):
    ball.update(dt)
    global heart_y
    global bonus_y
    global heart_x
    global bonus_x
    global lives
    if Rect((ball.x - ball.radius, ball.y - ball.radius), (ball.radius * 2, ball.radius * 2)).colliderect(
            Rect((paddle.x - paddle.width / 2, paddle.y - paddle.height / 2), (paddle.width, paddle.height))):
        ball.speed_y = -ball.speed_y
        ball.y = paddle.y - paddle.height / 2 - ball.radius
    for obstacle in obstacles:
        if (obstacle.x - obstacle.width / 2 < ball.x < obstacle.x + obstacle.width / 2 and
                obstacle.y - obstacle.height / 2 < ball.y < obstacle.y + obstacle.height / 2):
            obstacle.strength -= 1
            if abs(ball.x - (obstacle.x - obstacle.width / 2)) < abs(ball.x - (obstacle.x + obstacle.width / 2)):
                ball.speed_x = -ball.speed_x
            else:
                ball.speed_y = -ball.speed_y

            if obstacle.strength == 0:
                obstacles.remove(obstacle)
    if random.randint(0, 300) == 1:
        heart_y = 0
        heart_x = random.randint(0, WIDTH)
    if heart_y < HEIGHT:
        heart_y += 1
    if Rect((heart_x, heart_y), (20, 20)).colliderect(
            Rect((paddle.x - paddle.width / 2, paddle.y - paddle.height / 2), (paddle.width, paddle.height))):
        lives += 1
        heart_y = HEIGHT
    if random.randint(0, 200) == 2:
        bonus_y = 0
        bonus_x = random.randint(0, WIDTH)
    if bonus_y < HEIGHT:
        bonus_y += 1
    if Rect((bonus_x, bonus_y), (20, 20)).colliderect(
            Rect((paddle.x - paddle.width / 2, paddle.y - paddle.height / 2), (paddle.width, paddle.height))):
        paddle.width *= 1.5
        bonus_y = HEIGHT
        clock.schedule_unique(lambda: setattr(paddle, "width", paddle.width / 1.5), 3.0)


paddle = Paddle()
ball = Ball()
heart_y = HEIGHT
bonus_y = HEIGHT
heart_x = 0
bonus_x = 0
lives = 3
game_paused = False


def draw():
    global game_paused
    if not game_paused:
        screen.clear()
        paddle.draw()
        ball.draw()
        for obstacle in obstacles:
            obstacle.draw()
        if heart_y < HEIGHT:
            screen.draw.text("+", (heart_x, heart_y), color=(255, 0, 0), fontsize=50)
        if bonus_y < HEIGHT:
            screen.draw.text("+", (bonus_x, bonus_y), color=(255, 255, 0), fontsize=50)
        screen.draw.text(f'Lives: {lives if lives >= 0 else "-"}', (WIDTH / 2, 20), color=(255, 255, 255), fontsize=50)
        if lives < 0:
            screen.draw.text("GAME OVER", ((WIDTH / 2) - 80, (HEIGHT / 2) - 20), align="left", fontsize=60)
            game_paused = True
        if not obstacles:
            screen.draw.text("YOU WIN", ((WIDTH / 2) - 40, (HEIGHT / 2) - 20), align="left", fontsize=60)
            game_paused = True


def on_mouse_move(pos):
    x, y = pos
    paddle.x = x


pgzrun.go()
