import pygame
from random import choice
from pprint import pprint

pygame.init()

main_font = pygame.font.Font(None, 30)
score_font = pygame.font.Font(None, 50)


class Brick:
    def __init__(self, board, level, size):
        self.board = board
        self.level = level
        self.size = size
        self.surf = pygame.Surface((size, size))
        self.surf.fill(board.colors[level] if level in board.colors else (236, 195, 45))
        self.text_surf = main_font.render(str(self.level), True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center=(40, 40))

    def __iadd__(self, other):
        self.board.score += self.level + other.level
        return Brick(self.board, self.level + other.level, self.size)

    def draw(self, pos):
        self.centerX = (pos[0] + 1) * 5 + pos[0] * 80 + 40
        self.centerY = (pos[1] + 1) * 5 + pos[1] * 80 + 40
        self.rect = self.surf.get_rect(center=(self.centerX, self.centerY))
        if self.size == self.board.brick_size:
            self.surf.blit(self.text_surf, self.text_rect)
        self.board.surf.blit(self.surf, self.rect)

    def change_size(self, new_size):
        self.size = new_size
        self.surf = pygame.Surface((new_size, new_size))
        self.surf.fill(self.board.colors[self.level] if self.level in self.board.colors else (236, 195, 45))

    def __eq__(self, other):
        if self.level == other.level:
            return True
        return False

    def __str__(self):
        return f"Brick(level: {self.level}, pos: {self.pos})"


class Board:
    def __init__(self, surface):
        self.screen_surface = surface
        self.size = 4
        self.surf = pygame.Surface((345, 345))
        self.surf.fill((186, 172, 159))
        self.rect = self.surf.get_rect(topleft=(0, 55))
        self.board = [[None] * 4 for _ in range(self.size)]
        self.score = 0
        self.brick_size = 80
        self.brick_drawing = False
        self.new_brick_size = self.new_brick_size_ = 2
        self.colors = {2: (236, 228, 217),
                       4: (236, 224, 198),
                       8: (242, 177, 121),
                       16: (245, 149, 98),
                       32: (243, 124, 94),
                       64: (244, 94, 57),
                       128: (236, 207, 113),
                       256: (235, 205, 95),
                       512: (236, 200, 78),
                       1024: (235, 197, 62),
                       2048: (236, 195, 45)}
        self.create_random()

    def get_board(self):
        board_num_format = [[] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    board_num_format[i].append(self.board[i][j].level)
                else:
                    board_num_format[i].append(0)
        return board_num_format

    def create_random(self):
        available = []
        for i in range(self.size):
            for j in range(self.size):
                if self.board[j][i] is None:
                    available.append((i, j))
        if len(available) == 0:
            print('Lose')
        else:
            x, y = choice(available)
            self.last_brick = Brick(self, choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4]), self.new_brick_size)
            self.board[y][x] = self.last_brick
            self.brick_drawing = True

    def update_new(self):
        if self.new_brick_size < self.brick_size:
            self.new_brick_size += self.new_brick_size_
            self.last_brick.change_size(self.new_brick_size)
        else:
            self.brick_drawing = False
            self.new_brick_size = self.new_brick_size_

    def get_score(self):
        return self.score

    def draw_bricks(self):
        self.surf.fill((186, 172, 159))
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    self.board[i][j].draw((j, i))

    def draw(self):
        self.draw_bricks()
        self.screen_surface.blit(self.surf, self.rect)

    def move_left(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    for k in range(j + 1, self.size):
                        if self.board[i][k] is not None:
                            if self.board[i][j] == self.board[i][k]:
                                self.board[i][j] += self.board[i][k]
                                self.board[i][k] = None
                            break
                    for k in range(j):
                        if self.board[i][k] is None:
                            self.board[i][k] = self.board[i][j]
                            self.board[i][j] = None
                            break

    def move_right(self):
        for i in range(self.size):
            self.board[i] = self.board[i][::-1]
        self.move_left()
        for i in range(self.size):
            self.board[i] = self.board[i][::-1]

    def move_down(self):
        self.board = [[x[i] for x in self.board][::-1] for i in range(self.size)]
        self.move_left()
        self.board = [[i[j] for i in self.board] for j in range(self.size - 1, -1, -1)]

    def move_up(self):
        self.board = [[x[i] for x in self.board][::-1] for i in range(self.size)]
        self.move_right()
        self.board = [[i[j] for i in self.board] for j in range(self.size - 1, -1, -1)]

    def move(self, direction):
        last_board = self.get_board()
        if direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()
        elif direction == 'right':
            self.move_right()
        elif direction == 'left':
            self.move_left()
        if last_board != self.get_board():
            self.create_random()


def draw_all(screen, surf_restart, rect_restart):
    surf_score = score_font.render(str(board.get_score()), True, (0, 0, 0))
    rect_score = surf_score.get_rect(center=(width // 2 - 50, 27))

    screen.fill((255, 255, 255))
    screen.blit(surf_score, rect_score)
    screen.blit(surf_restart, rect_restart)
    pygame.draw.line(screen, (186, 172, 159), (257, 0), (257, 55), 3)


def main():
    global last_board, width, board
    width = 345
    height = 400
    FPS = 120

    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))

    clock = pygame.time.Clock()

    board = Board(screen)
    board.draw()

    surf_score = score_font.render(str(board.get_score()), True, (0, 0, 0))
    rect_score = surf_score.get_rect(center=(width // 2 - 50, 27))

    surf_restart = main_font.render('Restart', True, (0, 0, 0))
    rect_restart = surf_restart.get_rect(center=(302, 27))

    screen.blit(surf_score, rect_score)
    screen.blit(surf_restart, rect_restart)
    pygame.draw.line(screen, (186, 172, 159), (257, 0), (257, 55), 3)

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and not board.brick_drawing:
                    board.create_random()
                    board.draw()
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not board.brick_drawing:
                    board.move('left')
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not board.brick_drawing:
                    board.move('right')
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and not board.brick_drawing:
                    board.move('down')
                elif (event.key == pygame.K_UP or event.key == pygame.K_w) and not board.brick_drawing:
                    board.move('up')

                draw_all(screen, surf_restart, rect_restart)
                board.draw()
            elif event.type == pygame.MOUSEBUTTONUP:
                if rect_restart.collidepoint(event.pos) and event.button == 1:
                    board = Board(screen)
                    draw_all(screen, surf_restart, rect_restart)
                    board.draw()

        if board.brick_drawing:
            board.update_new()
            board.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
