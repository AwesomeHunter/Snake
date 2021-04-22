import pygame as pg
from pygame.math import Vector2
from random import random

class Game:
    
    class Fruit:
        
        radius = 8
        color = 255, 0, 0
        
        def __init__(self):
            self.position = None

        def get_correct_position(self):
            return self.position * Game.block_size + Vector2(Game.block_size, Game.block_size) // 2
        
        def occupied(self):
            return [self.position]
        
        def set_position(self, pos):
            self.position = pos
        
        def draw(self, screen):
            position = self.get_correct_position()
            pg.draw.circle(screen, self.color, position, self.radius)
            
                
    class Snake:
        
        color = 0, 255, 0
        snake_block_size = 18
        directions = {
            pg.K_UP: Vector2(0, -1),
            pg.K_LEFT: Vector2(-1, 0),
            pg.K_DOWN: Vector2(0, 1),
            pg.K_RIGHT: Vector2(1, 0),
        }
        
        def __init__ (self):
            self.snake_body = []
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
        
        def set_init_position(self, pos):
            self.snake_body = [pos]
            
        def occupied(self):
            return self.snake_body
        
        def draw(self, screen):
            shift = self.get_position_shift()
            snake_part_size = Vector2(self.snake_block_size, self.snake_block_size)
            for snake_part in self.snake_body:
                snake_part_pos = snake_part * Game.block_size + shift
                snake_part_rect = pg.Rect(snake_part_pos, snake_part_size)
                pg.draw.rect(screen, self.color, snake_part_rect)


    block_size = 20
    number_of_obstacles = 10
    points = 0
    speed = 100  
    obstacles = []
    
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREY = 222, 222, 222

    def __init__(self, size):
        pg.init()
        pg.display.set_caption("Snake")
        self.font = pg.font.SysFont("monospace", 28)
        self.size = Vector2(size) 
        screen_size = self.size * self.block_size
        self.screen = pg.display.set_mode((int(screen_size.x), int(screen_size.y)))
        self.running = True
        self.snake = self.Snake()
        self.fruit = self.Fruit()
    
    def generate_random_position(self):
        x = int(random() * self.size.x)
        y = int(random() * self.size.y)
        return Vector2(x, y)
    
    def generate_correct_position(self):
        not_available = self.snake.occupied() + self.fruit.occupied() + self.obstacles
        pos = self.generate_random_position()
        while pos in not_available:
            pos = self.generate_random_position()
        return pos

    def generate_obstacles(self):
        while len(self.obstacles) < self.number_of_obstacles:
            obstacle = self.generate_correct_position()
            self.obstacles.append(obstacle)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle_size = Vector2(self.block_size, self.block_size)
            obstacle_rect = pg.Rect(obstacle  * self.block_size, obstacle_size)
            pg.draw.rect(self.screen, GREY, obstacle_rect)
            
    def draw_points(self):
        label = self.font.render("SCORE: " + str(self.points), 1, WHITE)
        self.screen.blit(label, Vector2(5, 5))

    def fruit_collision(self):
        if self.snake.get_head() in self.fruit.occupied():
            self.points += 50
            self.speed -= 1
            self.fruit.set_position(self.generate_correct_position())
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

    def game_update(self):
        self.snake.make_move(self.size)
        self.snake.draw(self.screen)
        self.draw_obstacles()
        self.deadly_collision()
        self.fruit_collision()
        self.fruit.draw(self.screen)
        self.draw_points()

    def run(self):
        self.generate_obstacles()
        self.snake.set_init_position(self.generate_correct_position())
        self.fruit.set_position(self.generate_correct_position())
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
