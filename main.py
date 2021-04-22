import pygame
from random import random

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
GREY = 222, 222, 222


class Game:

    class Vector:
        def __init__(self, x=0, y=0):
            if isinstance(x, tuple):
                self.x = x[0]
                self.y = x[1]
            else:
                self.x = x
                self.y = y

        def __add__(self, other):
            if isinstance(other, Game.Vector):
                return Game.Vector(self.x + other.x, self.y + other.y)
            return Game.Vector(self.x + other, self.y + other)

        def __sub__(self, other):
            if isinstance(other, Game.Vector):
                return Game.Vector(self.x - other.x, self.y - other.y)
            return Game.Vector(self.x - other, self.y - other)

        def __mod__(self, other):
            if isinstance(other, Game.Vector):
                return Game.Vector(self.x % other.x, self.y % other.y)
            return Game.Vector(self.x % other, self.y % other)

        def __mul__(self, other):
            if isinstance(other, Game.Vector):
                return Game.Vector(self.x * other.x, self.y * other.y)
            return Game.Vector(self.x * other, self.y * other)

        def __eq__(self, other):
            if not isinstance(other, Game.Vector):
                return NotImplemented
            return self.x == other.x and self.y == other.y

        def tup(self):
            return self.x, self.y

    BLOCK_SIZE = 20
    FRUIT_SIZE = 8
    SNAKE_BLOCK_SIZE = 18
    START_POS = Vector(10, 10)
    fruit_pos = Vector()
    direction = Vector()
    points = 0
    speed = 100
    NUMBER_OF_OBSTACLES = 10
    keys = {
        pygame.K_UP: Vector(0, -1),
        pygame.K_LEFT: Vector(-1, 0),
        pygame.K_DOWN: Vector(0, 1),
        pygame.K_RIGHT: Vector(1, 0),
    }
    obstacles = []
    snake = [START_POS]

    def __init__(self, size):
        pygame.init()
        pygame.display.set_caption("SNAKE")
        self.font = pygame.font.SysFont("monospace", 28)
        self.SIZE = self.WIDTH, self.HEIGHT = size
        screen_size = Game.Vector(self.SIZE) * self.BLOCK_SIZE
        self.screen = pygame.display.set_mode(screen_size.tup())

    def move_snake(self):
        new_head = self.snake[0] + self.direction
        new_head %= Game.Vector(self.SIZE)
        del self.snake[-1]
        self.snake.insert(0, new_head)

    def draw_snake(self):
        shift = (self.BLOCK_SIZE - self.SNAKE_BLOCK_SIZE) // 2
        snake_part_size = (self.SNAKE_BLOCK_SIZE, self.SNAKE_BLOCK_SIZE)
        for snake_part in self.snake:
            snake_part_pos = snake_part * self.BLOCK_SIZE + shift
            snake_part_rect = pygame.Rect(snake_part_pos.tup(), snake_part_size)
            pygame.draw.rect(self.screen, GREEN, snake_part_rect)

    def get_rand_fruit_coords(self):
        x = int(random() * self.WIDTH)
        y = int(random() * self.HEIGHT)
        return Game.Vector(x, y)

    def generate_fruit_pos(self):
        fruit_coords = self.get_rand_fruit_coords()
        not_allowed_positions = self.snake + self.obstacles
        while fruit_coords in not_allowed_positions:
            fruit_coords = self.get_rand_fruit_coords()
        self.fruit_pos = fruit_coords

    def draw_fruit(self):
        fruit_position = self.fruit_pos * self.BLOCK_SIZE + self.BLOCK_SIZE // 2
        pygame.draw.circle(self.screen, RED, fruit_position.tup(), self.FRUIT_SIZE)

    def generate_obstacles(self):
        while len(self.obstacles) < self.NUMBER_OF_OBSTACLES:
            x = int(random() * self.WIDTH)
            y = int(random() * self.HEIGHT)
            rand_pos = Game.Vector(x, y)
            if rand_pos not in [self.START_POS, self.fruit_pos] + self.obstacles:
                self.obstacles.append(rand_pos)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle_pos = obstacle * self.BLOCK_SIZE
            obstacle_size = (self.BLOCK_SIZE, self.BLOCK_SIZE)
            obstacle_rect = pygame.Rect(obstacle_pos.tup(), obstacle_size)
            pygame.draw.rect(self.screen, GREY, obstacle_rect)

    def draw_points(self):
        label = self.font.render("SCORE: " + str(self.points), 1, WHITE)
        self.screen.blit(label, (5, 5))

    def fruit_collision(self):
        if self.fruit_pos == self.snake[0]:
            self.points += 50
            self.speed -= 1
            self.generate_fruit_pos()
            self.snake.append(self.snake[-1])

    def run(self):
        self.generate_fruit_pos()
        self.generate_obstacles()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in self.keys and self.keys[event.key] != self.direction * -1:
                        self.direction = self.keys[event.key]
                        break
            self.screen.fill(BLACK)
            self.fruit_collision()
            self.draw_obstacles()
            self.move_snake()
            if self.snake[0] in self.snake[1:] + self.obstacles:
                running = False
            self.draw_fruit()
            self.draw_snake()
            self.draw_points()
            pygame.display.flip()
            pygame.time.wait(max(self.speed, 50))
        pygame.quit()


SIZE = 30, 30
game = Game(SIZE)
game.run()
