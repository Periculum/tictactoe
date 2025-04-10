#!/usr/bin/env python3

import pygame as pg
import random
import math
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


EMPTY = ""
PLAYER = "X"
COMPUTER = "O"


class TicTacToe:
    def __init__(self):
        self.board = self.reset_board()
        # controls who starts the game and the result
        self.result = Result.TIE
        self.state = State.PLAYERS_TURN
        self.counter = 0

    def runGame(self):
        pg.init()

        # draw window screen
        screen = pg.display.set_mode((WIDTH, HEIGHT))
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
                        if self.board[box_coordinates[0]][box_coordinates[1]] == EMPTY:
                            self.board[box_coordinates[0]][box_coordinates[1]] = PLAYER
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

            # draws tictactoe board, crosses and circles
            self.draw_board(screen)

            # if game ends draw endscreen
            if self.state == State.GAME_OVER:
                pg.time.delay(700)
                self.draw_end_screen(screen)

            # rendering
            pg.display.flip()
            clock.tick(FPS)

    # calculate the coordinates from the clicked box
    def calculate_box(self, position):
        # inverting the order of the coordinates to made them more logically readable
        return (int(position[1] // (WIDTH / 3)), int(position[0] // (HEIGHT / 3)))

    # computer does a random move
    def random_move(self):
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            if self.board[x][y] == EMPTY:
                # computer does a turn
                self.board[x][y] = COMPUTER
                return

    # computer does move according to the minimax/negamax algorithm
    def best_move(self):
        best_score = -math.inf
        best_move = (0, 0)
        # copy board
        board = list(self.board)
        # Evaluate all possible moves and find the best one
        # using negamax search to determine optimal play
        for row in range(3):
            for col in range(3):
                if board[row][col] == "":
                    board[row][col] = COMPUTER
                    # score = self.minimax_search(board, False)
                    # score = self.minimax_alpha_beta_search(-math.inf, math.inf, board, False)
                    score = -self.negamax_search(board, -1)
                    board[row][col] = EMPTY
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        # computer makes the best move
        self.board[best_move[0]][best_move[1]] = COMPUTER
        print(self.counter)

    def minimax_search(self, board, max_player):
        self.counter += 1
        # if game is finished stop search and return result
        result = self.check_game_result(board)
        if result != 0:
            # someone won
            return result
        elif not self.turns_left(board):
            # tie
            return 0

        # if max players turn
        if max_player:
            max_score = -math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = COMPUTER
                score = self.minimax_search(board, False)
                board[move[0]][move[1]] = EMPTY
                max_score = max(max_score, score)
            return max_score
        # else min players turn
        else:
            min_score = math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = PLAYER
                score = self.minimax_search(board, True)
                board[move[0]][move[1]] = EMPTY
                min_score = min(min_score, score)
            return min_score

    def minimax_alpha_beta_search(self, alpha, beta, board, max_player):
        self.counter += 1
        # if game is finished stop search and return result
        result = self.check_game_result(board)
        if result != 0:
            # someone won
            return result
        elif not self.turns_left(board):
            # tie
            return 0

        # if max players turn
        if max_player:
            max_score = -math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = COMPUTER
                score = self.minimax_alpha_beta_search(alpha, beta, board, False)
                board[move[0]][move[1]] = EMPTY
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return max_score
        # else min players turn
        else:
            min_score = math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = PLAYER
                score = self.minimax_alpha_beta_search(alpha, beta, board, True)
                board[move[0]][move[1]] = EMPTY
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def negamax_search(self, board, color):
        self.counter += 1
        # if game is finished stop search and return result
        result = self.check_game_result(board)
        if result != 0:
            # someone won
            return result * color
        elif not self.turns_left(board):
            # tie
            return 0

        max_score = -math.inf
        for move in self.possible_moves(board):
            if color == 1:
                board[move[0]][move[1]] = COMPUTER
            else:
                board[move[0]][move[1]] = PLAYER
            score = -self.negamax_search(board, -color)
            max_score = max(max_score, score)
            board[move[0]][move[1]] = EMPTY
        return max_score

    # returns all possible moves
    def possible_moves(self, board):
        return [
            (row, col) for row in range(3) for col in range(3) if board[row][col] == ""
        ]

    # checks if moves are still possible
    def turns_left(self, board):
        return any("" in row for row in board)

    # checks if game ends by a tie, win or loss
    def check_game_result(self, board):
        # diagonal strings
        diagonal_left = "".join(board[i][i] for i in range(3))
        diagonal_right = "".join(board[i][2 - i] for i in range(3))
        # row and columns
        for i in range(3):
            row_values = "".join(board[i])
            col_values = "".join(board[r][i] for r in range(3))
            if "XXX" in (row_values, col_values, diagonal_left, diagonal_right):
                # player won
                return -1
            elif "OOO" in (row_values, col_values, diagonal_left, diagonal_right):
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
                if self.board[row][col] == COMPUTER:
                    # draw circle
                    circle_size = WIDTH / 8
                    pg.draw.circle(
                        screen,
                        "black",
                        (
                            (WIDTH * col / 3) + WIDTH / 6,
                            (HEIGHT * row / 3) + HEIGHT / 6,
                        ),
                        circle_size,
                    )
                    pg.draw.circle(
                        screen,
                        "white",
                        (
                            (WIDTH * col / 3) + WIDTH / 6,
                            (HEIGHT * row / 3) + HEIGHT / 6,
                        ),
                        circle_size - 1,
                    )
                elif self.board[row][col] == PLAYER:
                    # draw cross
                    offset = WIDTH / 12
                    pg.draw.line(
                        screen,
                        "black",
                        (WIDTH * col / 3 + offset, HEIGHT * row / 3 + offset),
                        (WIDTH * col / 3 + offset * 3, HEIGHT * row / 3 + offset * 3),
                    )
                    pg.draw.line(
                        screen,
                        "black",
                        (WIDTH * col / 3 + offset, HEIGHT * row / 3 + offset * 3),
                        (WIDTH * col / 3 + offset * 3, HEIGHT * row / 3 + offset),
                    )

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
        screen.blit(
            text,
            (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() * 3),
        )
        screen.blit(
            text_klick,
            (WIDTH // 2 - text.get_width() * 0.6, HEIGHT // 2 - text.get_height()),
        )

    # reset board
    def reset_board(self):
        return [[EMPTY for _ in range(3)] for _ in range(3)]
        # return [['','','X'],['X','','O'],['O','O','X']] # position from infographic


def main():
    ttt = TicTacToe()
    ttt.runGame()


if __name__ == "__main__":
    main()
