import random
import math
import heapq

myHeap = []
def manhattanDist(a, b):
	return math.fabs(a[0] - b[0]) + math.fabs(a[1] - b[1])

class Board():
	def __init__(self, size):
		assert size > 2 and size < 10
		self.size = size
		self.moves = ['down', 'up', 'right', 'left']
		self.board = [[0 for i in range(size)] for j in range(size)]
		for i in range(size):
			for j in range(size):
				self.board[i][j] = size*i+j

	def printBoard(self):
		for i in range(self.size):
			for j in range(self.size):
				temp = self.board[i][j]
				if temp == 0:
					print("  ", end = ' ')
				elif 0 < temp and temp < 10:
					print(" " + str(temp), end = ' ')
				else:
					print(temp, end = ' ')
			print()
		print()

	def findPos(self, num):
		assert 0 <= num and num < self.size*self.size
		for i in range(self.size):
			for j in range(self.size):
				if self.board[i][j] == num:
					return (i,j)

	def findZero(self):
		return self.findPos(0)

	def possibleMoves(self):
		answer = []
		row, col = self.findZero()
		if row > 0:
			answer.append('down')
		if row < self.size - 1:
			answer.append('up')
		if col > 0:
			answer.append('right')
		if col < self.size - 1:
			answer.append('left')
		return answer

	def makeMove(self, direction):
		assert direction in self.moves and direction in self.possibleMoves()

		row, col = self.findZero()
		if direction == 'down':
			self.board[row][col] = self.board[row-1][col]
			self.board[row-1][col] = 0
		if direction == 'up':
			self.board[row][col] = self.board[row+1][col]
			self.board[row+1][col] = 0
		if direction == 'right':
			self.board[row][col] = self.board[row][col-1]
			self.board[row][col-1] = 0
		if direction == 'left':
			self.board[row][col] = self.board[row][col+1]
			self.board[row][col+1] = 0
		#self.printBoard()

	def shuffle(self, n):
		for i in range(n):
			self.makeMove(random.choice(self.possibleMoves()))

	def finished(self):
		count = 0
		for i in range(self.size):
			for j in range(self.size):
				if i == self.size-1 and j == self.size-1:
					if self.board[i][j] == 0:
						count+=1
				else:
					if self.board[i][j] == i*self.size + j + 1:
						count+=1
		return count == self.size*self.size

	def copy(self):
		answer = Board(self.size)
		for i in range(self.size):
			for j in range(self.size):
				answer.board[i][j] = self.board[i][j]
		return answer

# Can actually play the game by creating an object of this class and running play function.
class Game():
	def __init__(self, size):
		self.board = Board(size)
		self.board.shuffle(1000)
		self.input = ['w','a','s','d']
		self.map = {'w': 'up', 'a': 'left', 's': 'down', 'd': 'right'}
	def getMove(self):
		move = input("Enter move (w, a, s or d): ")
		while not move in self.input:
			move = input("Enter move (w, a, s or d): ")
		return self.map[move]
	def play(self):
		while not self.board.finished():
			self.board.printBoard()
			direction = self.getMove()
			if direction not in self.board.possibleMoves():
				print("Illegal move!")
				continue
			self.board.makeMove(direction)
		self.board.printBoard()
		print("Congratulations")

class State():
	def __init__(self, size, depth, nxt, prev):
		self.Board = Board(size)
		self.Board.shuffle(1000)
		self.depth = depth
		self.next = nxt
		self.previous = prev

	def __gt__(self, rhs):
		return self.depth > rhs.depth

	def copy(self):
		temp = self.Board.copy()
		answer = State(self.Board.size, self.depth, self.next, self.previous)
		answer.Board = temp
		return answer

	def printState(self):
		self.Board.printBoard()

	# Given a State, find out what next possible states can be visited
	def nextPossibleStates(self):
		answer = []
		possible = self.Board.possibleMoves()
		for m in possible:
			temp = self.copy()
			temp.Board.makeMove(m)
			temp.depth = self.depth + 1
			temp.previous = self
			temp.next = None
			answer.append(temp)
		return answer

	# Heuristic function
	# For each entry on the board, calculates sum of Manhattan Distances to true postitions
	def h(self):
		goal = Board(self.Board.size)
		temp = [[0 for i in range(self.Board.size)] for j in range(self.Board.size)]
		for i in range(self.Board.size):
			for j in range(self.Board.size):
				temp[i][j] = self.Board.size*i+j+1
		temp[self.Board.size-1][self.Board.size-1] = 0
		goal.board = temp

		# Goal State created
		goalState = State(self.Board.size, 0, None, None)
		goalState.Board = goal

		# Sum of Manhattan distances
		answer = 0
		for i in range(self.Board.size * self.Board.size):
			answer += manhattanDist(self.Board.findPos(i), goalState.Board.findPos(i))
		return int(answer)

	# Compare 2 States (to distinguish visited states)
	def isSame(self, state):
		assert self.Board.size == state.Board.size
		answer = True
		for i in range(self.Board.size):
			for j in range(self.Board.size):
				if self.Board.board[i][j] != state.Board.board[i][j]:
					answer = False
		return answer

	# Heuristic function is 0 only for goal state
	def isGoalState(self):
		return self.h() == 0

# Start state
a = State(4, 0, None, None)
a.printState()


visitedStates = []
last = None
def isVisited(state):
	answer = False
	for s in visitedStates:
		if s.isSame(state):
			answer = True
	return answer

# Running A* Search Algorithm
heapq.heappush(myHeap, ( a.depth + a.h() , a))
while len(myHeap) != 0:
	depth, state = heapq.heappop(myHeap)
	visitedStates.append(state)
	print("Visiting")
	state.printState()
	if state.isGoalState():
		last = state
		break
	else:
		for s in state.nextPossibleStates():
			if not isVisited(s):
				heapq.heappush(myHeap, (s.depth + s.h(), s))

# Going backwards to starting state
temp = last
while not temp.isSame(a):
	temp.previous.next = temp
	temp = temp.previous

# Printing sequence of moves to finish the puzzle
print("Solution")
temp = a
while not temp.isSame(last):
	temp.printState()
	temp = temp.next