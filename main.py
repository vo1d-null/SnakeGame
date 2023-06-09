import random
import time
import pygame
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (123, 212, 15)


class Mouse:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/mice.png").convert_alpha(self.parent_screen)
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2, 24) * SIZE
        self.y = random.randint(2, 19) * SIZE


class Skull:
    def __init__(self, parent_screen,):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/skull2.png").convert_alpha(self.parent_screen)
        self.length = 1
        self.x = random.randint(2, 19) * SIZE
        self.y = random.randint(2, 19) * SIZE
        random_direction = ['left', 'right', 'up', 'down']
        random_direction2 = random.choice(random_direction)
        self.direction = random_direction2

    def move(self):
        self.y = random.randint(2, 19) * SIZE
        self.x = random.randint(2, 19) * SIZE

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x = self.x[i - 1]
            self.y = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x -= SIZE / 4
        if self.direction == 'right':
            self.x += SIZE / 4
        if self.direction == 'up':
            self.y -= SIZE / 4
        if self.direction == 'down':
            self.y += SIZE / 4

        self.draw()

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x, self.y))


class Mouse2:
    def __init__(self, parent_screen,):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/Mouse2.png").convert_alpha(self.parent_screen)
        self.length = 1
        self.x = random.randint(2, 19) * SIZE
        self.y = random.randint(2, 19) * SIZE
        random_direction = ['left', 'down', 'up', 'right']
        random_direction2 = random.choice(random_direction)
        self.direction = random_direction2

    def move(self):
        self.y = random.randint(2, 19) * SIZE
        self.x = random.randint(2, 19) * SIZE

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x = self.x[i - 1]
            self.y = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x -= SIZE / 4
        if self.direction == 'right':
            self.x += SIZE / 4
        if self.direction == 'up':
            self.y -= SIZE / 4
        if self.direction == 'down':
            self.y += SIZE / 4

        self.draw()

    def draw(self):

        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x, self.y))


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/snake_head.png").convert_alpha(self.parent_screen)
        self.image2 = pygame.image.load("resources/snake4.jpg").convert(self.parent_screen)
        self.direction = 'down'

        self.length = length
        self.x = [40] * length
        self.y = [40] * length

    def move_left(self):
        self.direction = 'left'
        # self.image = pygame.transform.flip(self.image, True, False)
        # self.image = pygame.transform.rotate(self.image, -180.0)

    def move_right(self):
        self.direction = 'right'
        # self.image = pygame.transform.flip(self.image, True, False)
        # self.image = pygame.transform.rotate(self.image, 180.0)

    def move_up(self):
        self.direction = 'up'
        # self.image = pygame.transform.flip(self.image, False, True)
        # self.image = pygame.transform.rotate(self.image, 360.0)

    def move_down(self):
        self.direction = 'down'
        # self.image = pygame.transform.flip(self.image, False, True)
        # self.image = pygame.transform.rotate(self.image, -360.0)

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[0], self.y[0]))
            self.parent_screen.blit(self.image2, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def decrease_length(self):
        self.length -= 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake and Mouse game by vo1d.null")

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.skull = Skull(self.surface)
        self.skull.draw()
        self.Mouse = Mouse(self.surface)
        self.Mouse.draw()
        self.Mouse2 = Mouse2(self.surface)
        self.Mouse2.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('Bauhaus 93', 50)
        score = font.render(f"Score: {self.snake.length}", True, (250, 250, 250))
        self.surface.blit(score, (750, 20))

    def play_background_music(self):
        pygame.mixer.music.load("resources/background_music.mp3")
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(10000)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        sound.set_volume(0.1)
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        background = pygame.image.load("resources/background1.png")
        self.surface.blit(background, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.Mouse.draw()
        self.Mouse2.walk()
        self.skull.walk()
        self.display_score()
        pygame.display.flip()

        # snake colliding with mouse
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.Mouse.x, self.Mouse.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.Mouse.move()

        # snake eating skull scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.skull.x, self.skull.y):
            for i in range(self.snake.length):
                self.snake.decrease_length()
            self.skull.move()

        # snake colliding with itself
        for i in range(4, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("death1")
                raise "Game Over"

            # snake colliding with boundary
        if not (0 <= self.snake.x[0] <= 960 and 0 <= self.snake.y[0] <= 760):
            self.play_sound('death1')
            raise "Collision with boundary"

        # skull colliding with SNAKE BODY
        for i in range(2, self.snake.length):
            if self.is_collision(self.skull.x, self.skull.y, self.snake.x[i], self.snake.y[i]):
                for snakeBody in range(self.snake.length):
                    self.snake.decrease_length()
                self.skull.move()

            # skull colliding with boundary
        if not (0 <= self.skull.x <= 960 and 0 <= self.skull.y <= 760):
            self.skull = Skull(self.surface)
            self.skull.walk()

            # Mouse2 colliding with snake
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.Mouse.x, self.Mouse.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.Mouse2.move()

            # Mouse2 colliding with SNAKE BODY
        for i in range(2, self.snake.length):
            if self.is_collision(self.Mouse2.x, self.Mouse2.y, self.snake.x[i], self.snake.y[i]):
                for snakeBody in range(self.snake.length - self.snake.length + 3):
                    self.snake.decrease_length()
                self.Mouse2.move()

            # Mouse2 colliding with boundary
        if not (0 <= self.Mouse2.x <= 960 and 0 <= self.Mouse2.y <= 760):
            self.Mouse2 = Mouse2(self.surface)
            self.Mouse2.walk()

            # Mouse2 colliding with snake Head
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.Mouse2.x, self.Mouse2.y):
            for i in range(self.snake.length - self.snake.length - 3):
                self.snake.increase_length()
            self.Mouse2.move()

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Bauhaus 93', 50)
        line1 = font.render(f"Game over!", True, (250, 250, 250))
        self.surface.blit(line1, (200, 200))
        line4 = font.render(f"Score: {self.snake.length}", True, (250, 250, 250))
        self.surface.blit(line4, (200, 300))
        line2 = font.render(f"To play again - press SPACE.", True, (250, 250, 250))
        self.surface.blit(line2, (200, 400))
        line3 = font.render(f"To exit - Press ESC", True, (250, 250, 250))
        self.surface.blit(line3, (200, 500))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.Mouse = Mouse(self.surface)
        self.skull = Skull(self.surface)

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_SPACE:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_w:
                            self.snake.move_up()
                        if event.key == K_s:
                            self.snake.move_down()
                        if event.key == K_a:
                            self.snake.move_left()
                        if event.key == K_d:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)


if __name__ == '__main__':
    game = Game()
    game.run()
