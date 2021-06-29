import pygame
import time
import random
'''
Rules
Any live cell with two or three live neighbours survives.
Any dead cell with three live neighbours becomes a live cell.
All other live cells die in the next generation. Similarly, all other dead cells stay dead
'''

def create_list(x, y):
    return [[0 for _ in range(x)] for _ in range(y)]

def update(board):
    updated_board = [[0 for _ in range(len(board))] for _ in range(len(board))]

    for  index, line in enumerate(board):
        for ind, number in enumerate(line):
            live = 0
            if index == 0 or index >= (len(board)-1) or ind == 0 or ind == (len(line)):
                updated_board[index][ind] = 0
                continue
            #print(index, ind)
            live += board[index-1][ind-1:ind+2].count(1) + board[index][ind-1:ind+2].count(1) + board[index+1][ind-1:ind+2].count(1)
            if number == 1:
                if live == 3 or live == 4:
                    updated_board[index][ind] = 1
            elif number == 0 and live == 3:
                updated_board[index][ind] = 1
            else:
                updated_board[index][ind] = 0

    return updated_board

def render(board):
    screen.fill((0, 0, 0))
    for index ,line in enumerate(board):
        for ind, cell in enumerate(line):
            if cell == 1:
                pygame.draw.rect(screen, (255, 255, 255), (2+ind*11, 70+index*11, 10, 10))

            else:
                pygame.draw.rect(screen, (30, 30, 30), (2 + ind * 11, 70+index*11, 10, 10))
    # Start stop button
    pygame.draw.rect(screen, start_button_color, (resolution * 5, 20, 80, 40))
    if running:
        screen.blit(text, (resolution * 5+5, 20))
    else:
        screen.blit(text, (resolution * 5, 20))

    # Restart button
    pygame.draw.rect(screen, (200, 200, 200), (resolution, 20, 80, 40))
    screen.blit((pygame.font.SysFont('Comic Sans MS', 20).render('Restart', True, (0, 0, 0))), (resolution+2, 25))

    # Random button
    pygame.draw.rect(screen, (200, 200, 200), (resolution*9, 20, 80, 40))
    screen.blit((pygame.font.SysFont('Comic Sans MS', 20).render('Random', True, (0, 0, 0))), (resolution*9 + 2, 25))

    pygame.display.update()

if __name__ == '__main__':
    black = (0, 0, 0)
    start_button_color = (0, 200, 0)
    pygame.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    text = font.render('Start', True, (0, 0, 0))
    # Resolution = number of cubes
    resolution = 80
    running = False
    board = create_list(resolution, resolution)
    screen = pygame.display.set_mode((resolution*11+2, resolution*11+70), 0, 32)
    render(board)
    cell = {0, 0}

    while True:
        ev = pygame.event.get()
        if running:
            for event in ev:
                if pygame.mouse.get_pressed(3)[0] == 1:
                    mouse_position_x, mouse_position_y = pygame.mouse.get_pos()
                    if mouse_position_y in range(20, 60) and mouse_position_x in range(resolution*5, resolution*5+80):
                        running = False
                        text = font.render('Start', True, (0, 0, 0))
                        start_button_color = (0, 200, 0)
            board = update(board)
            render(board)
            time.sleep(0.1)
        else:

            for event in ev:
                if pygame.mouse.get_pressed(3)[0] == 1:
                    mouse_position_x, mouse_position_y = pygame.mouse.get_pos()
                    if mouse_position_y in range(20, 60) and mouse_position_x in range(resolution*5, resolution*5+80):
                        running = True
                        start_button_color = (200, 0, 0)
                        text = font.render('Stop', True, (0, 0, 0))
                    for index, _ in enumerate(board):
                        if mouse_position_y-70 in range(index*11, index*11+11):
                            for x in range(0, resolution):
                                if mouse_position_x in range(x*11, x*11+11):
                                    new_cell = {index, x}
                                    if new_cell == cell:
                                        pass
                                    else:
                                        if board[index][x] == 1:
                                            board[index][x] = 0
                                        else:
                                            board[index][x] = 1
                                        cell = new_cell
                                    render(board)
                    if mouse_position_x in range(resolution, resolution+80) and mouse_position_y in range(20, 60):
                        for en, line in enumerate(board):
                            for numb, _ in enumerate(line):
                                board[en][numb] = 0
                        render(board)
                    if mouse_position_x in range(resolution*9, resolution*9+80) and mouse_position_y in range(20, 60):
                        for en, line in enumerate(board):
                            for numb, _ in enumerate(line):
                                board[en][numb] = random.randrange(2)
                        render(board)
                else:
                    cell = {0, 0}
