#!/usr/bin/python

import random
from os import system
import signal
from sys import setrecursionlimit

# Main class for grid
class GameBoard:

	# matrix - Main grid, 2 dimensional matrix
	# rows - Total rows
	# columns - Total columns
	# mines - Total mines
	# mine_cells - List of (x, y) tuples where mines are placed
	# left = Total safe cells left to mark (rows * columns - mines)

	# Each cell in grid
	class Cell:

		# value - Total number of adjacent cells with mines
		# state - Marked (1) or not (0)
		# mine - Has mine (1) or not (0)

		# Cell constructor
		def __init__(self, value, state):
			self.value = value
			self.state = state
			self.mine = False

	# GameBoard constructor
	def __init__(self, rows, columns, mines):
		self.rows = rows
		self.columns = columns
		self.mines = mines
		self.left = (rows * columns - mines)
		self.__initialize()

	# Initializes the grid by placing mines randomly and updating values of adjacent cells
	def __initialize(self):
		# Initialize all 'columns' number of cells for each row from 'rows'
		self.matrix = [[self.Cell(0, 0) for _ in xrange(self.columns)] for _ in xrange(self.rows)]
		self.mine_cells = []
		for _ in xrange(self.mines):
			x = random.randint(0, self.columns - 1)
			y = random.randint(0, self.rows - 1)
			# Repeat until new cell (where mine isn't already placed) is found
			while self.matrix[y][x].mine:
				x = random.randint(0, self.columns - 1)
				y = random.randint(0, self.rows - 1)
			# Add to mine_cells list and update in matrix
			self.mine_cells.append((x, y))
			self.matrix[y][x].mine = True
		# Update adjacent cells of mine cells
		self.__update_mine_territory()

	# Updates the adjacent cells of mine cells with appropriate values
	def __update_mine_territory(self):
		# For each mine cell
		for m in self.mine_cells:
			v = self.matrix[m[1]][m[0]]
			# Update all adjacent (x - 1, y - 1) through (x + 1, y + 1) cells
			for x in xrange(m[0] - 1, m[0] + 2):
				for y in xrange(m[1] - 1, m[1] + 2):
					if self.check_limits(x, y):
						continue
					c = self.matrix[y][x]
					# Only update the value if it's not a mine cell and is not marked
					if not self.matrix[y][x].mine and not c.state:
						self.matrix[y][x].value += 1
			self.matrix[m[1]][m[0]] = v

	# Performs basic checks to determine if given neighbor can be marked
	def __check_neighbor_to_mark(self, col, row):
		# Skip if contains mine
		if self.matrix[row][col].mine:
			return False
		# Skip if already marked
		if self.matrix[row][col].state:
			return False
		return True

	# Marks the neighbors of given cell recursively as applicable
	def __mark_neighbors(self, col, row):
		# Mark this cell and dDecrement count of unmarked cells
		self.matrix[row][col].state = 1
		self.left -= 1
		# If this cell surrounds no cells with mines, continue to mark neighbors
		if self.matrix[row][col].value:
			return
		# Maintain list of safe neighbors, these will be marked recursively
		safe_neighbors = []
		# For all adjacent cells (x - 1, y - 1) through (x + 1, y + 1)
		for x in xrange(col - 1, col + 2):
			for y in xrange(row - 1, row + 2):
				if self.check_limits(x, y):
					continue
				# Add neighbor if it has no mine
				if not self.matrix[y][x].mine:
					safe_neighbors.append((x, y))
					continue
				# Break if it has
				break
		# Remove the current cell from safe_neighbors list
		p = (col, row)
		if p in safe_neighbors:
			safe_neighbors.remove(p)
		# Mark all the safe neighbors recursively
		for n in safe_neighbors:
			if self.__check_neighbor_to_mark(n[0], n[1]):
				self.__mark_neighbors(n[0], n[1])
		return

	# Marks given cell and any neighbors (recursively) if it's value is 0
	def mark_cell(self, col, row):
		# Skip if already marked
		if self.matrix[row][col].state:
			return
		# Check if it has mine
		if self.matrix[row][col].mine:
			# Mine hit, reveal all mines and return True
			for x, y in self.mine_cells:
				self.matrix[y][x].state = 1
			return True
		# If cell value if non-zero, just mark it and return
		if self.matrix[row][col].value:
			self.left -= 1
			self.matrix[row][col].state = 1
			return False
		# Cell value is 0, recursively mark neighbors
		if self.__check_neighbor_to_mark(col, row):
			self.__mark_neighbors(col, row)
		return False

	# Prints the entire board on console (real = True if mines are to be revealed)
	def print_board(self, real):
		if real:
			print map(lambda (x, y): (x + 1, y + 1), self.mine_cells)
		print 
		# Print row and column indices
		print "%-2s"%0,
		for i in xrange(self.columns):
			print "%2s"%(i + 1),
		print
		i = 1
		for x in xrange(self.rows):
			print "%-2s"%i,
			for y in xrange(self.columns):
				if real or self.matrix[x][y].state:
					if self.matrix[x][y].mine:
						print " x",
					else:
						print "%2s"%self.matrix[x][y].value,
				else:
					print " -",
			print
			i += 1
		print

	# Checks whether given coordinates obey the limits
	def check_limits(self, x, y):
		if x < 0 or x >= self.columns or y < 0 or y >= self.rows:
			return True
		return False

# Prompts user with given message and requests for a number repeatedly until it is valid
def get_number(msg, default, limit):
	inv_msg = "Invalid number, try again"
	while True:
		try:
			n = input(msg)
			if not n:
				print inv_msg
				continue
			n = int(n)
			if n < 1 or n > limit:
				print inv_msg
				continue
			return n
		except SyntaxError:
			return default
		except StandardError:
			print inv_msg

# Invoked when interrupt is triggered and terminates game gracefully
def signal_handler(signal, frame):
	print "...game terminated."
	quit()

# Clears terminal and prints given message
def clear_and_prompt(msg):
	system('clear')
	print msg

# Main function encapsulating game play
def gameplay(board):
	inv_indices_msg = "Invalid indices, try again"
	clear_and_prompt("Let's begin...")
	while True:
		print "Safe cells left: ",board.left
		board.print_board(False)
		try:
			i = input("Mark cell (col, row): ")
			if not i or len(i) <> 2:
				clear_and_prompt(inv_indices_msg)
				continue
			x = i[0]
			y = i[1]
			x = int(x)
			y = int(y)
			if(board.check_limits(x - 1, y - 1)):
				clear_and_prompt(inv_indices_msg)
				continue
		except Exception:
			clear_and_prompt(inv_indices_msg)
			continue
		if(board.mark_cell(x - 1, y - 1)):
			clear_and_prompt("Stepped on a mine at [%d, %d]!"%(x, y))
			board.print_board(False)
			print "Game over!"
			break
		clear_and_prompt("Marked [%d, %d]... Safe!"%(x, y))
		if not board.left:
			board.print_board(False)
			print "Congratulations, you win!"
			break

# Preset configuration
MAX_ROWS = 50
MAX_COLS = 60
DEF_ROWS = 16
DEF_COLS = 16
DEF_MINES = 40

if __name__ == "__main__":
	# Set recursion limit for boards configured with huge number of cells
	setrecursionlimit(6000)
	# Set handler for interrupt signal (^c)
	signal.signal(signal.SIGINT, signal_handler)
	print "Welcome to Minesweeper for terminal!"
	print "Configure the mines grid to begin (skip for default)..."
	# Get configuration
	rows = get_number("Enter number of rows (max %d) [%d]: "%(MAX_ROWS, DEF_ROWS), DEF_ROWS, MAX_ROWS)
	columns = get_number("Enter number of columns (max %d) [%d]: "%(MAX_COLS, DEF_COLS), DEF_COLS, MAX_COLS)
	max_mines = (rows * columns - 1)
	def_mines = (max_mines if max_mines < DEF_MINES else DEF_MINES)
	mines = get_number("Enter number of mines (max %d) [%d]: "%(max_mines, def_mines), def_mines, max_mines)
	# Initialize the board
	board = GameBoard(rows, columns, mines)
	# Start gameplay
	gameplay(board)
