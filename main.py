import pygame as pg
from pygame.math import Vector2
from random import random

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0
GREY = 222, 222, 222

class Game:
    
    class Fruit:
        
        radius = 8
        color = RED
        
        def __init__(self, position):
            self.position = position

        def get_correct_position(self):
            return self.position * Game.block_size + Vector2(Game.block_size, Game.block_size) // 2
        
            
    class Snake:
        
        snake_block_size = 18
        directions = {
            pg.K_UP: Vector2(0, -1),
            pg.K_LEFT: Vector2(-1, 0),
            pg.K_DOWN: Vector2(0, 1),
            pg.K_RIGHT: Vector2(1, 0),
        }
        
        def __init__ (self, position):
            self.snake_body = [position]
            self.direction = Vector2(0, 0)

        def get_head(self):
            return self.snake_body[0]
        
        def get_tail(self):
            return self.snake_body[1:]
        
        def append_last_bodypart(self):
            self.snake_body.append(self.snake_body[-1])
        
        def set_direction(self, action):
            self.direction = directions[action]
            
        def correct_head_position(self, board_size):
            self.snake_body[0] += board_size
            self.snake_body[0].x %= board_size.x
            self.snake_body[0].y %= board_size.y
        
        def make_move(self, board_size):
            new_head = self.get_head() + self.direction
            self.snake_body.insert(0, new_head)
            self.snake_body.pop()
            self.correct_head_position(board_size)
            
        def get_position_shift(self):
            shift = (Game.block_size - self.snake_block_size) // 2
            return Vector2(shift, shift)


    running = True
    block_size = 20
    number_of_obstacles = 10
    points = 0
    speed = 100  
    obstacles = []

    def __init__(self, size):
        pg.init()
        pg.display.set_caption("SNAKE")
        self.font = pg.font.SysFont("monospace", 28)
        self.size = Vector2(size) 
        screen_size = self.size * self.block_size
        self.screen = pg.display.set_mode((int(screen_size.x), int(screen_size.y)))
        self.snake = None
        self.fruit = None
        
    def generate_random_position(self):
        x = int(random() * self.size.x)
        y = int(random() * self.size.y)
        return Vector2(x, y)

    def draw_snake(self):
        shift = self.snake.get_position_shift()
        snake_part_size = Vector2(self.snake.snake_block_size, self.snake.snake_block_size)
        for snake_part in self.snake.snake_body:
            snake_part_pos = snake_part * self.block_size + shift
            snake_part_rect = pg.Rect(snake_part_pos, snake_part_size)
            pg.draw.rect(self.screen, GREEN, snake_part_rect)

    def draw_fruit(self):
        fruit_position = self.fruit.get_correct_position()
        pg.draw.circle(self.screen, self.fruit.color, fruit_position, self.fruit.radius)

    def generate_obstacles(self):
        while len(self.obstacles) < self.number_of_obstacles:
            obstacle = self.generate_random_position()
            if obstacle not in self.obstacles:
                self.obstacles.append(obstacle)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle_size = Vector2(self.block_size, self.block_size)
            obstacle_rect = pg.Rect(obstacle  * self.block_size, obstacle_size)
            pg.draw.rect(self.screen, GREY, obstacle_rect)

    def draw_points(self):
        label = self.font.render("SCORE: " + str(self.points), 1, WHITE)
        self.screen.blit(label, Vector2(5, 5))
        
    def gen_fruit_position(self):
        pos = self.generate_random_position()
        while pos in self.obstacles + self.snake.snake_body:
            pos = self.generate_random_position()
        return pos
        
    def gen_snake(self):
        pos = self.generate_random_position()
        while pos in self.obstacles:
            pos = self.generate_random_position()
        self.snake = self.Snake(pos)
    
    def gen_fruit(self):
        pos = self.gen_fruit_position()
        self.fruit = self.Fruit(pos)

    def fruit_collision(self):
        if self.fruit.position == self.snake.get_head():
            self.points += 50
            self.speed -= 1
            self.fruit.position = self.gen_fruit_position()
            self.snake.append_last_bodypart()
            
    def deadly_collision(self):
        if self.snake.get_head() in self.snake.get_tail() + self.obstacles:
            self.running = False

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key in self.snake.directions and self.snake.directions[event.key] != self.snake.direction * -1:
                    self.snake.direction = self.snake.directions[event.key]
                    break
                
    def init_game(self):
        self.generate_obstacles()
        self.gen_snake()
        self.gen_fruit()

    def game_update(self):
        self.fruit_collision()
        self.draw_snake()
        self.draw_obstacles()
        self.snake.make_move(self.size)
        self.draw_fruit()
        self.deadly_collision()
        self.draw_points()

    def run(self):
        self.init_game()
        while self.running:
            self.handle_events()
            self.screen.fill(BLACK)
            self.game_update()
            pg.display.flip()
            pg.time.wait(max(self.speed, 50))
        pg.quit()


SIZE = 30, 30
game = Game(SIZE)
game.run()
