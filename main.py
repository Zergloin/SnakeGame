import pygame
import random
from pygame.math import Vector2

CELL_SIZE = 30
WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 205, 50)
RED = (255, 0, 0)

FPS = 60


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        try:
            self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        except FileNotFoundError as ex:
            print(f'Ошибка загрузки звука: {ex}')
            self.crunch_sound = None

    def draw(self):
        for block in self.body:
            block_rect = pygame.Rect(int(block.x * CELL_SIZE), int(block.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, block_rect)

    def move(self):
        if self.new_block:
            self.body.insert(0, self.body[0] + self.direction)
            self.new_block = False
        else:
            self.body.insert(0, self.body[0] + self.direction)
            self.body.pop()

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        if self.crunch_sound:
            self.crunch_sound.play()


class Fruit:
    def __init__(self):
        self.randomize()

    def draw(self):
        fruit_rect = pygame.Rect(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, fruit_rect)

    def randomize(self):
        self.pos = Vector2(random.randint(0, (WIDTH // CELL_SIZE) - 1), random.randint(0, (HEIGHT // CELL_SIZE) - 1))


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Snake')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
