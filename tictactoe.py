#!/usr/bin/env python3

import pygame as pg
import random
from enum import Enum

HEIGHT = WIDTH = 600
FPS = 24

class State(Enum):
    GAME_OVER = 0
    PLAYERS_TURN = 1
    COMPUTERS_TURN = 2

class Result(Enum):
    TIE = 0
    PLAYER_WON = 1
    COMPUTER_WON = 2

class TicTacToe:
    def __init__(self):
        self.board = self.reset_board()
        # controls who starts the game and the result
        self.result = Result.TIE
        self.state = State.PLAYERS_TURN

    def runGame(self):
        pg.init()

        # draw window screen
        screen = pg.display.set_mode((WIDTH,HEIGHT))
        clock = pg.time.Clock()

        # main loop
        while True:
            # player inputs
            for event in pg.event.get():
                # close game
                if event.type == pg.QUIT:
                    pg.quit()
                    raise SystemExit

                # players move
                if self.state == State.PLAYERS_TURN:
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # find coordinates from the box that got clicked
                        box_coordinates = self.calculate_box(pg.mouse.get_pos())
                        # check if box is empty and set cross
                        if self.board[box_coordinates[0]][box_coordinates[1]] == '':
                            self.board[box_coordinates[0]][box_coordinates[1]] = 'X'
                            # switch to computers turn
                            self.state = State.COMPUTERS_TURN
                            if self.check_game_result(self.board) != 0:
                                self.result = Result.PLAYER_WON
                                self.state = State.GAME_OVER
                            elif not self.turns_left(self.board):
                                self.result = Result.TIE
                                self.state = State.GAME_OVER
                # if possible Computer makes a move
                # must be elif, because with if, the computer could move even when player won in the move before
                elif self.state == State.COMPUTERS_TURN:
                    if self.turns_left(self.board):
                        # self.random_move()
                        self.best_move()
                        # players move again
                        self.state = State.PLAYERS_TURN
                        if self.check_game_result(self.board) != 0:
                            self.result = Result.COMPUTER_WON
                            self.state = State.GAME_OVER
                        elif not self.turns_left(self.board):
                            self.result = Result.TIE
                            self.state = State.GAME_OVER
                # Game is over
                elif self.state == State.GAME_OVER:
                    # if player decides to play further
                    if event.type == pg.MOUSEBUTTONDOWN:
                        # game starts again so reset everything
                        self.board = self.reset_board()  
                        self.state = State.PLAYERS_TURN
                        self.result = Result.TIE
                      
            # draws tictactoe board, crosses and circles          
            self.draw_board(screen)

            # if game ends draw endscreen
            if self.state == State.GAME_OVER:
                pg.time.delay(700)
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


   # computer does move accordingly to the minimax algorithm
    def best_move(self):
        best_eval = -2
        best_move = 0
        # copy board
        board = list(self.board)
        # for every possible move find via minimax-search the evaluation
        # and choose at the end the best move
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    evaluation = self.minimax_search(board, False)
                    board[row][col] = ''
                    if evaluation > best_eval:
                        best_eval = evaluation
                        best_move = (row,col)

        # computer makes the best move
        self.board[best_move[0]][best_move[1]] = 'O'


    def minimax_search(self, board, max_player):
        # if game is conclusive stop search and return result
        result = self.check_game_result(board)
        if result != 0:
            # someone won
            return result
        elif not self.turns_left(board):
            # tie
            return 0

        # if max players turn
        if max_player:
            max_evaluation = -2
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = 'O'
                evaluation = self.minimax_search(board, False)
                board[move[0]][move[1]] = ''
                max_evaluation = max(max_evaluation, evaluation)
            return max_evaluation
        # else min players turn
        else:  
            min_evaluation = 2
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = 'X'
                evaluation = self.minimax_search(board, True)
                board[move[0]][move[1]] = ''
                min_evaluation = min(min_evaluation, evaluation)
            return min_evaluation

    # returns all possible moves
    def possible_moves(self, board):
        list_of_moves = []
        for row in range(3):
            for col in range(3):
                if board[row][col] == '':
                    list_of_moves.append((row,col))

        return list_of_moves


    # checks if moves are still possible
    def turns_left(self, board):
        return any('' in row for row in board)


    # checks if game ends by a tie, win or loss
    def check_game_result(self, board):
        # diagonal strings
        diagonal_left = ''.join(board[i][i] for i in range(3))
        diagonal_right = ''.join(board[i][2 - i] for i in range(3))
        # row and columns
        for i in range(3):
            row_values = ''.join(board[i])
            col_values = ''.join(board[r][i] for r in range(3))
            if 'XXX' in (row_values, col_values, diagonal_left, diagonal_right):
                # player won
                return -1
            elif 'OOO' in (row_values, col_values, diagonal_left, diagonal_right):
                # computer won
                return 1

        # no winner
        return 0


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
        text = font.render(text_type[self.result.value], True, "black")
        text_klick = font_small.render("Click anywhere to start again", True, "black")
        
        # draw screen and texts
        screen.fill("white")
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height() * 3))
        screen.blit(text_klick, (WIDTH//2 - text.get_width() * 0.6, HEIGHT//2 - text.get_height()))


    # reset board
    def reset_board(self):
        return [['','',''],['','',''],['','','']]
        #return [['','','X'],['X','','O'],['O','O','X']] # position from infographic


def main():
    ttt = TicTacToe()
    ttt.runGame()


if __name__ == '__main__':
    main()
