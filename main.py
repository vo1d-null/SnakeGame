import random
import time
import pygame
from pygame.locals import *

SIZE = 40
BACKGROUND_COLOR = (123, 212, 15)


class Mouse:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/mice.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(2, 24) * SIZE
        self.y = random.randint(2, 19) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/snake4.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [40] * length
        self.y = [40] * length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

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
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
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
        self.Mouse = Mouse(self.surface)
        self.Mouse.draw()

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
        pygame.mixer.music.play(10000)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        background = pygame.image.load("resources/background1.png")
        self.surface.blit(background, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.Mouse.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with mouse
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.Mouse.x, self.Mouse.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.Mouse.move()
        # snake colliding with itself
        for i in range(4, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("death1")
                raise "Game Over"
        if not (0 <= self.snake.x[0] <= 960 and 0 <= self.snake.y[0] <= 760):
            self.play_sound('death1')
            raise "Collision with boundary"

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

            time.sleep(.2)


if __name__ == '__main__':
    game = Game()
    game.run()
