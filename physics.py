"""Обработка столкновений"""

from math import pi, cos, sin
from random import uniform, randint

class Ball:
    """
    Класс шара на плоскости, обладающего
    радиусом, массой и скоростью
    """

    def __init__(self, id, coords, r, v, color):
        self.id = id
        self.x, self.y = coords
        self.r = r
        self.vx, self.vy = v
        self.m = r**2
        self.color = color


    def update(self, dt):
        """
        Обновление координат шара при движении
        """
        self.x += self.vx * dt
        self.y += self.vy * dt


    def dist2_to_other(self, other):
        """
        Квадрат евклидова расстояния
        между центрами двух шаров
        """
        dist2 = (self.x - other.x) ** 2 + (self.y - other.y) ** 2
        return dist2


def generate_balls(count, ball_rs, velicity, area_sizes):
    """
    Созадёт шары со случайными характеристиками
    в пределах заданных
    """
    balls = []
    min_r, max_r = ball_rs
    min_v, max_v = velicity

    for i in range(count):
        id = i
        r = uniform(min_r, max_r)
        v = uniform(min_v, max_v)

        angle = uniform(0, 2) * pi
        vx = v * cos(angle)
        vy = v * sin(angle)
        color = (randint(0, 255), randint(0, 255), randint(0, 255))

        x, y = generate_positions(balls, r, area_sizes)

        ball = Ball(id, (x, y), r, (vx, vy), color)

        balls.append(ball)

    return balls


def generate_positions(balls, radius, area_sizes):
    """
    Выбирает случайные начальные координаты для шара
    """
    width, height = area_sizes

    for _ in range(100):
        x = uniform(radius, width - radius)
        y = uniform(radius, height - radius)

        if not overlaps_any_ball(balls, x, y, radius):
            return x, y

    raise ValueError("Не удалось разместить шары без пересечений")


def overlaps_any_ball(balls, x, y, radius):
    """
    Проверяет корректность начального размещения 
    шаров: не должно быть пересечений
    """
    for ball in balls:
        min_distance = ball.r + radius

        if (ball.x - x) ** 2 + (ball.y - y) ** 2 < min_distance ** 2:
            return True

    return False


def resolve_wall_collision(ball, width, height):
    """
    Проверяет, коснулся ли шар границы 
    области, и отражает его
    """
    # Левая стена
    if ball.x - ball.r < 0:
        ball.x = ball.r
        ball.vx = -ball.vx

    # Прававя стена
    if ball.x + ball.r > width:
        ball.x = width - ball.r
        ball.vx = -ball.vx

    # Нижняя стена
    if ball.y - ball.r < 0:
        ball.y = ball.r
        ball.vy = -ball.vy

    # Прававя стена
    if ball.y + ball.r > height:
        ball.y = height - ball.r
        ball.vy = -ball.vy


def intersects(ball_1, ball_2):
    """
    Проверяет, пересекаются ли два шара.
    Если да - возвращает True
    """

    r_sum2 = (ball_1.r + ball_2.r) ** 2

    return ball_1.dist2_to_other(ball_2) < r_sum2


def resolve_ball_collision(ball_1, ball_2):
    """
    Обрабатывает абсолютно упругое 
    столкновение двух шаров - изменяет 
    скорость и направление движения
    """

    x12 = ball_2.x - ball_1.x
    y12 = ball_2.y - ball_1.y
    distance = ball_1.dist2_to_other(ball_2) ** 0.5

    if distance == 0:
        nx = 1
        ny = 0
    else:
        nx = x12 / distance
        ny = y12 / distance

    v1n = ball_1.vx * nx + ball_1.vy * ny
    v2n = ball_2.vx * nx + ball_2.vy * ny

    m1 = ball_1.m
    m2 = ball_2.m

    new_v1n = ((m1 - m2) * v1n + 2 * m2 * v2n) / (m1 + m2)
    new_v2n = ((m2 - m1) * v2n + 2 * m1 * v1n) / (m1 + m2)

    ball_1.vx += (new_v1n - v1n) * nx
    ball_1.vy += (new_v1n - v1n) * ny

    ball_2.vx += (new_v2n - v2n) * nx
    ball_2.vy += (new_v2n - v2n) * ny

    separate_balls(ball_1, ball_2, distance, nx, ny)


def separate_balls(ball_1, ball_2, distance, nx, ny):
    """
    Раздвигает два шара после обнаружения
    пересечения, чтобы они касались, но не
    проникали друг в друга
    """
    overlap = ball_1.r + ball_2.r - distance

    if overlap <= 0:
        return

    total_mass = ball_1.m + ball_2.m

    share_1 = ball_2.m / total_mass
    share_2 = ball_1.m / total_mass

    ball_1.x -= nx * overlap * share_1
    ball_1.y -= ny * overlap * share_1

    ball_2.x += nx * overlap * share_2
    ball_2.y += ny * overlap * share_2
