#!/usr/bin/env python3

import pygame as pg
import random

HEIGHT = WIDTH = 600
FPS = 60

class tictactoe:
    def __init__(self):
        self.board = self.reset_board()


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
                # track mouseclick from user
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # find coordinates from the box that got clicked
                    box_coordinates = self.calculate_box(pg.mouse.get_pos())
                    print(box_coordinates)
                    # if players turn, check if box is empty and set cross
                    if players_turn and self.board[box_coordinates[0]][box_coordinates[1]] == '':
                        self.board[box_coordinates[0]][box_coordinates[1]] = 'X'
                        # switch to computers turn
                        players_turn = False

            # Computer takes a turn if possible
            if players_turn == False and self.turns_left():
                self.random_move()
                # player moves now
                players_turn = True


            # check if Game ended with win, loss or tie
            status = self.game_ends()
            if status > 0 or self.turns_left() == False:
                print("Game is over")
                #self.game_over_screen(status)


            # fill background and draw tictactoe-field
            screen.fill("white")
            for row in range(1, 3):
                for col in range(1, 3):
                    pg.draw.line(screen, "black", (WIDTH * col / 3, 0), (WIDTH * col / 3, HEIGHT))
                    pg.draw.line(screen, "black", (0, HEIGHT * row / 3), (WIDTH, HEIGHT * row / 3))

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
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '':
                    return True
        return False


    # checks if game ends by a win or loss
    def game_ends(self):
        # diagonal strings
        diagonal_left = ''.join(self.board[i][i] for i in range(3))
        diagonal_right = ''.join(self.board[i][2 - i] for i in range(3))
        # row and columns
        for row in range(3):
            for col in range(3):
                col_values = ''.join(self.board[row][c] for c in range(3))
                row_values = ''.join(self.board[r][col] for r in range(3))
                if row_values == 'XXX' or col_values == 'XXX' or diagonal_left == 'XXX' or diagonal_right == 'XXX':
                    return 1
                elif row_values == 'OOO' or col_values == 'OOO' or diagonal_left == 'OOO' or diagonal_right == 'OOO':
                    return 2
        return 0


    # reset board
    def reset_board(self):
        board = [['','',''],
                ['','',''],
                ['','','']]
        return board


def main():
    ttt = tictactoe()
    ttt.runGame()


if __name__ == '__main__':
    main()
