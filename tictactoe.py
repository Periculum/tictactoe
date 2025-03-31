#!/usr/bin/env python3

import pygame as pg
import random

HEIGHT = WIDTH = 600
FPS = 60

class tictactoe:
    def __init__(self):
        self.board = self.reset_board()
        self.state = "running" # can be "running" or "game_over"
        self.result = 0 # 0 = tie, 1 = player won, 2 = computer won

    def runGame(self):
        pg.init()

        # draw window screen
        screen = pg.display.set_mode((WIDTH,HEIGHT))
        clock = pg.time.Clock()

        # controls who starts the game
        players_turn = True

        while True:
            # player inputs
            for event in pg.event.get():
                # close game
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

                if self.state == "running":
                    # player makes a move
                    if event.type == pg.MOUSEBUTTONDOWN and players_turn:
                        # find coordinates from the box that got clicked
                        box_coordinates = self.calculate_box(pg.mouse.get_pos())
                        # check if box is empty and set cross
                        if self.board[box_coordinates[0]][box_coordinates[1]] == '':
                            self.board[box_coordinates[0]][box_coordinates[1]] = 'X'
                            self.check_game_result()
                            # switch to computers turn
                            players_turn = False
                    # Computers turn, if possible he makes a move
                    # must be elif, because with if, the computer would have a turn even when player won in the move before
                    elif self.turns_left() and not players_turn:
                        self.random_move()
                        self.check_game_result()
                        # players move again
                        players_turn = True
                # if game is over show endscreen and reset board
                elif self.state == "game_over":
                    if event.type  == pg.MOUSEBUTTONDOWN:
                        # reset everything
                        self.board = self.reset_board()  
                        self.state = "running"
                        players_turn = True
           
            
            # draws tictactoe board, crosses and circles              
            self.draw_board(screen)
                

            # if game ends draw endscreen
            if self.state == "game_over":
                pg.time.delay(200)
                self.draw_end_screen(screen)


            # rendering
            pg.display.flip()
            clock.tick(FPS)


    # calculates the coordinates from the clicked box
    def calculate_box(self, position):
        # inverting the order of the coordinates to made them more logically readable
        return (int(position[1] // (WIDTH/3)), int(position[0] // (HEIGHT/3)))


    # computer does a random move
    def random_move(self):
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if self.board[x][y] == '':
                # computer does a turn
                self.board[x][y] = 'O'
                return


    # checks if moves are still possible
    def turns_left(self):
        return any('' in row for row in self.board)


    # checks if game ends by a tie, win or loss
    def check_game_result(self):

        # diagonal strings
        diagonal_left = ''.join(self.board[i][i] for i in range(3))
        diagonal_right = ''.join(self.board[i][2 - i] for i in range(3))
        for row in range(3):
            for col in range(3):
                # row and columns
                col_values = ''.join(self.board[row][c] for c in range(3))
                row_values = ''.join(self.board[r][col] for r in range(3))
                if 'XXX' in (row_values, col_values, diagonal_left, diagonal_right):
                    # player won
                    self.result = 1
                    self.state = "game_over"
                    return
                elif 'OOO' in (row_values, col_values, diagonal_left, diagonal_right):
                    # computer won
                    self.result = 2
                    self.state = "game_over"
                    return

        # game is a tie
        if not self.turns_left():
            self.result = 0
            self.state = "game_over"


    def draw_board(self, screen):
        # fill background and draw tictactoe-field
        screen.fill("white")
        for i in range(1, 3):
            pg.draw.line(screen, "black", (WIDTH * i / 3, 0), (WIDTH * i / 3, HEIGHT))
            pg.draw.line(screen, "black", (0, HEIGHT * i / 3), (WIDTH, HEIGHT * i / 3))

        # draw crosses and circles
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == 'O':
                    # draw circle
                    circle_size = WIDTH / 8
                    pg.draw.circle(screen, "black", ((WIDTH * col / 3) + WIDTH / 6, (HEIGHT * row / 3) + HEIGHT / 6), circle_size)
                    pg.draw.circle(screen, "white", ((WIDTH * col / 3) + WIDTH / 6, (HEIGHT * row / 3) + HEIGHT / 6), circle_size - 1)
                elif self.board[row][col] == 'X':
                    # draw cross
                    offset = WIDTH / 12
                    pg.draw.line(screen, "black", (WIDTH * col / 3 + offset, HEIGHT * row / 3 + offset), (WIDTH * col / 3 + offset * 3, HEIGHT * row / 3 + offset * 3))
                    pg.draw.line(screen, "black", (WIDTH * col / 3 + offset, HEIGHT * row / 3 + offset * 3), (WIDTH * col / 3 + offset * 3, HEIGHT * row / 3 + offset))


    def draw_end_screen(self, screen):
        # fonts
        font = pg.font.Font(None, 100)
        font_small = pg.font.Font(None, 40)

        # texts
        text_type = ["It's a Tie!", "You Won!", "You Lost!"]
        text = font.render(text_type[self.result], True, "black")
        text_klick = font_small.render("Click anywhere to start again", True, "black")
        
        # draw screen and texts
        screen.fill("white")
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height() * 3))
        screen.blit(text_klick, (WIDTH//2 - text.get_width() * 0.6, HEIGHT//2 - text.get_height()))


    # reset board
    def reset_board(self):
        board = [['','',''],['','',''],['','','']]
        return board


def main():
    ttt = tictactoe()
    ttt.runGame()


if __name__ == '__main__':
    main()
