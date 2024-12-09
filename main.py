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


class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
        self.high_score = 0
        self.snake_speed = 150

    def update_speed(self, speed):
        self.snake_speed = speed
        pygame.time.set_timer(SCREEN_UPDATE, self.snake_speed)

    def update(self):
        self.snake.move()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.draw()
        self.snake.draw()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1

        while self.fruit.pos in self.snake.body:
            self.fruit.randomize()

    def check_fail(self):
        head = self.snake.body[0]
        if not (0 <= head.x < (WIDTH // CELL_SIZE)) or not (
                0 <= head.y < (HEIGHT // CELL_SIZE)) or head in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.snake.reset()
        self.score = 0

    def display_text(self, text, x, y):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (x, y))

    def draw_score(self):
        self.display_text(f'Score: {self.score}', 10, 10)
        self.display_text(f'High Score: {self.high_score}', WIDTH - 200, 10)


class Menu:
    def __init__(self):
        self.options = ['Новая игра', 'Настройки', 'Выход']
        self.selected_option = 0
        self.font = pygame.font.Font(None, 48)

    def draw(self):
        screen.fill(BLACK)
        for index, option in enumerate(self.options):
            text_surface = self.font.render(option, True, GREEN if index == self.selected_option else WHITE)
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 50 + index * 60))

    def move_up(self):
        self.selected_option = (self.selected_option - 1) % len(self.options)

    def move_down(self):
        self.selected_option = (self.selected_option + 1) % len(self.options)

    def select(self):
        if self.selected_option == 0:  # Новая игра
            return 'new_game'
        elif self.selected_option == 1:  # Настройки
            return 'settings'
        elif self.selected_option == 2:  # Выход
            return 'exit'


if __name__ == '__main__':
    pygame.init()

    pygame.display.set_caption('Snake')
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)
