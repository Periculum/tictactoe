#!/usr/bin/env python3

import pygame as pg

HEIGHT = WIDTH = 500
FPS = 60

class tictactoe:
	def init(self):
		board = [['','',''],
				['','',''],
				['','','']]


	def runGame(self):
		pg.init()

		screen = pg.display.set_mode((HEIGHT,WIDTH))
		clock = pg.time.Clock()

		while True:
			# player inputs
			for event in pg.event.get():
				# close game
				if event.type == pg.QUIT:
					pg.quit()
					raise SystemExit
				elif event.type == pg.MOUSEBUTTONDOWN:
					print(pg.mouse.get_pos())

			# Updates

			# fill background and draw tictactoe-field
			screen.fill("white")
			for row in range(1, 3):
				for col in range(1, 3):
					pg.draw.line(screen, "black", (WIDTH * col / 3, 0), (WIDTH * col / 3, HEIGHT))
					pg.draw.line(screen, "black", (0, HEIGHT * row / 3), (WIDTH, HEIGHT * row / 3))



			# graphics render

			# rendering
			pg.display.flip()
			clock.tick(FPS)



def main():
	ttt = tictactoe()
	ttt.runGame()


if __name__ == '__main__':
	main()
