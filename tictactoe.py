#!/usr/bin/env python3

import pygame as pg
import random
import math
import time
from enum import Enum
from argparse import ArgumentParser

HEIGHT = WIDTH = 600
FPS = 24

class Mode(Enum):
    RANDOM = 0
    MINIMAX = 1
    NEGAMAX = 2
    MINIMAX_AB = 3

    def new(mode):
        if isinstance(mode, int):
            return Mode(mode)
        elif isinstance(mode, str):
            mode = mode.lower()
            if mode == "random":
                return Mode.RANDOM
            elif mode == "minimax":
                return Mode.MINIMAX
            elif mode == "negamax":
                return Mode.NEGAMAX
            elif mode == "minimax-ab":
                return Mode.MINIMAX_AB
            else:
                raise ValueError(f"Invalid mode: {mode}")
        else:
            raise TypeError(f"Mode must be int or str, not {type(mode).__name__}")


class State(Enum):
    GAME_OVER = 0
    PLAYERS_TURN = 1
    COMPUTERS_TURN = 2

    def new(computers_turn):
        if computers_turn:
            return State.COMPUTERS_TURN
        else:
            return State.PLAYERS_TURN


class Result():
    TIE = 0
    PLAYER_WON = -1
    COMPUTER_WON = 1


EMPTY = ""
PLAYER = "X"
COMPUTER = "O"


class TicTacToe:
    def __init__(self, mode, state):
        self.board = self.reset_board()
        self.result = None
        self.mode = Mode(mode)
        self.starting_player = State(state)
        self.counter = 0

    def runGame(self):
        pg.init()

        # draw window screen
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Tic Tac Toe")
        clock = pg.time.Clock()
        updateDelay = 0

        # starting player
        state = self.starting_player
        
        # main loop
        running = True
        while running:
            # Clear event queue at the start of each frame
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                
                # Handle mouse clicks in appropriate states
                if event.type == pg.MOUSEBUTTONDOWN:
                    if state == State.PLAYERS_TURN:
                        # find coordinates from the box that got clicked
                        box_coordinates = self.calculate_box(pg.mouse.get_pos())
                        # check if box is empty and set cross
                        if self.board[box_coordinates[0]][box_coordinates[1]] == EMPTY:
                            self.board[box_coordinates[0]][box_coordinates[1]] = PLAYER
                            # switch to computers turn
                            state = State.COMPUTERS_TURN
                            # check if game has ended
                            result = self.check_game_result(self.board)
                            if result is not None:
                                self.result = result
                                state = State.GAME_OVER
                            updateDelay = time.time() + 0.7
                    elif state == State.GAME_OVER:
                        # game starts again so reset board
                        self.board = self.reset_board()
                        # switching player
                        self.starting_player = (
                            State.COMPUTERS_TURN
                            if self.starting_player == State.PLAYERS_TURN
                            else State.PLAYERS_TURN
                            )
                        state = self.starting_player


            # State-specific updates (outside of event handling)
            if state == State.COMPUTERS_TURN:
                self.computer_makes_a_move()
                # players move again
                state = State.PLAYERS_TURN
                # check if game has ended
                result = self.check_game_result(self.board)
                if result is not None:
                    self.result = result
                    state = State.GAME_OVER
                updateDelay = time.time() + 0.5

            # Game over state handling
            if state == State.GAME_OVER and time.time() > updateDelay:
                self.draw_end_screen(screen)
            else:
                self.draw_board(screen)

            pg.display.flip()
            clock.tick(FPS)

        # Properly quit pygame when the loop ends
        pg.quit()


    # calculate box coordinates from screen coordinates
    # (x,y) -> (row, col)
    def calculate_box(self, position):
        return (int(position[1] // (WIDTH / 3)), int(position[0] // (HEIGHT / 3)))

    # computers move based on the selected game mode
    def computer_makes_a_move(self):
        if self.mode == Mode.RANDOM:
            self.random_move()
        else:
            self.best_move()

    # computer does a random move
    def random_move(self):
        while True:
            x = random.randint(0, 2)
            y = random.randint(0, 2)
            # if the cell is empty, make the move and exit the loop
            if self.board[x][y] == EMPTY:
                self.board[x][y] = COMPUTER
                return

    # computer does move according to the minimax/negamax algorithm
    def best_move(self):
        best_score = -math.inf
        best_move = (0, 0)

        # select the scoring function based on current mode
        strategies = {
            Mode.MINIMAX: lambda b: self.minimax_search(1, b, False),
            Mode.MINIMAX_AB: lambda b: self.minimax_alpha_beta_search(1, -math.inf, math.inf, b, False),
            Mode.NEGAMAX: lambda b: -self.negamax_search(1, b, -1),
        }
        strategy = strategies.get(self.mode)

        # deep copy board
        board = [row[:] for row in self.board]

        # evaluate all possible moves and find the best one
        # using negamax search to determine optimal play
        for (row, col) in self.possible_moves(board):
            board[row][col] = COMPUTER # simulate move
            score = strategy(board)    # evaluate the move
            board[row][col] = EMPTY    # undo the move
            # update best move if this one scores higher
            if score > best_score:
                best_score = score
                best_move = (row, col)

        # apply the best move
        self.board[best_move[0]][best_move[1]] = COMPUTER
        print(self.counter)

    def minimax_search(self, depth, board, max_player):
        self.counter += 1
        # if game is finished stop search and return result
        result = self.check_game_result(board)
        if result is not None:
            # there is a win, loss or tie
            return result/depth

        # if max players turn
        if max_player:
            max_score = -math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = COMPUTER
                score = self.minimax_search(depth + 1, board, False)
                board[move[0]][move[1]] = EMPTY
                max_score = max(max_score, score)
            return max_score
        # else min players turn
        else:
            min_score = math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = PLAYER
                score = self.minimax_search(depth + 1, board, True)
                board[move[0]][move[1]] = EMPTY
                min_score = min(min_score, score)
            return min_score

    def minimax_alpha_beta_search(self, depth, alpha, beta, board, max_player):
        self.counter += 1
        # if game is finished stop search and return result
        result = self.check_game_result(board)
        if result is not None:
            # there is a win, loss or tie
            return result/depth

        # if max players turn
        if max_player:
            max_score = -math.inf
            for move in self.possible_moves(board):
                board[move[0]][move[1]] = COMPUTER
                score = self.minimax_alpha_beta_search(depth + 1, alpha, beta, board, False)
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
                score = self.minimax_alpha_beta_search(depth + 1, alpha, beta, board, True)
                board[move[0]][move[1]] = EMPTY
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return min_score

    def negamax_search(self, depth, board, color):
        self.counter += 1
        # if game is finished stop search and return result
        result = self.check_game_result(board)
        if result is not None:
            # there is a win, loss or tie
            return (result * color) / depth

        max_score = -math.inf
        for move in self.possible_moves(board):
            if color == 1:
                board[move[0]][move[1]] = COMPUTER
            else:
                board[move[0]][move[1]] = PLAYER
            score = -self.negamax_search(depth + 1, board, -color)
            max_score = max(max_score, score)
            board[move[0]][move[1]] = EMPTY
        return max_score

    # returns all possible moves
    def possible_moves(self, board):
        return [
            (row, col) for row in range(3) for col in range(3) if board[row][col] == EMPTY
        ]
        

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
                return Result.PLAYER_WON
            elif "OOO" in (row_values, col_values, diagonal_left, diagonal_right):
                # computer won
                return Result.COMPUTER_WON

        # check if board is full (tie)
        if not any(EMPTY in row for row in board):
            return Result.TIE

        # Game still running
        return None


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
        text_type = ["You Won!", "It's a Tie!", "You Lost!"]
        text = font.render(text_type[self.result + 1], True, "black")
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
    # parsing arguments
    parser = ArgumentParser(
        prog='Tic Tac Toe',
        description='Small Pygame with different Computer enemys')
    parser.add_argument('-c', '--computer', required=False, action="store_true",
        help="Let the computer make the first move instead of the player.")
    parser.add_argument('-m', '--mode', type=str, choices=["random", "minimax", "minimax-ab", "negamax"], default= "minimax-ab",
        help="Select the algorithm the computer will use to make moves.")
    args = parser.parse_args()

    ttt = TicTacToe(Mode.new(args.mode), State.new(args.computer))
    ttt.runGame()


if __name__ == "__main__":
    main()
