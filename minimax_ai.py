from connectfour import *

max_depth = 5

#evaluation function
def total_consecutive_threes(board, player_one_turn=True):
	player_mark = 1 if player_one_turn else -1 
	total_threes = 0
	#for diagonals
	flipped_board = np.fliplr(board)
	#horizontal
	total_threes += sum([total_consecutive_threes_helper(row, player_mark) for row in board])
	#vertical (transpose the board)
	total_threes += sum([total_consecutive_threes_helper(row, player_mark) for row in board.T])

	#for diagonals - KIV (note that this is only for a 6x7 connect four board)
	for offset in range(-3, 5):
		total_threes += total_consecutive_threes_helper(np.diag(board, k=offset), player_mark)
		total_threes += total_consecutive_threes_helper(np.diag(flipped_board, k=offset), player_mark)
	return total_threes

#return number of 3 consecutive items in a list
def total_consecutive_threes_helper(li, player_mark):
	total_threes = 0
	#counter used to track number of consecutive pieces
	counter = 0
	for val in li:
		if val == player_mark:
			counter += 1
		else:
			counter = 0
		
		if counter >= 3:
			total_threes += 1
	return total_threes

class Node(object):
	def __init__(self, board, player_one_turn, value=None, depth=0):
		self.board = board
		self.children = []
		self.player_one_turn = player_one_turn
		self.value = value
		self.depth = depth



	def create_children(self):
		child_turn = not self.player_one_turn
		child_depth = self.depth + 1

		#list of potential moves (in terms of col index)
		available_cols = get_available_cols(self.board)
		for col in available_cols:
			#creates a copy of the parent board, and then add each move to it 
			#and save it as child's board
			child_board, _, _ = init_game(self.board)
			
			#add move
			child_board, ongoing, reward = make_move(child_board, col, child_turn)
			# print(child_board)
			
			#if game has ended, assign reward function as value
			if not ongoing:
				child_value = reward
			#if we have reached max depth, then use heuristic evaluation function to get value
			elif child_depth == max_depth: 
				child_value = total_consecutive_threes(child_board, child_turn)
			else:
				child_value = None

			child = Node(child_board, child_turn, child_value, child_depth)
			self.children.append(child)

	def __str__(self):
		return '{}\nvalue: {}'.format(self.board, self.value)

if __name__ == '__main__':
	board, _, _ = init_game()

	n = Node(board, True)
	n.create_children()
	for c in n.children:
		print(c)

	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 1, False)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 1, False)
	# board, _, _ = make_move(board, 0, True)

	# board, _, _ = make_move(board, 3, True)
	# board, _, _ = make_move(board, 4, True)
	# board, _, _ = make_move(board, 4, True)
	# board, _, _ = make_move(board, 5, True)
	# board, _, _ = make_move(board, 5, False)
	# board, _, _ = make_move(board, 5, True)
	# print(total_consecutive_threes(board))
	# print(board)
	# board, _, _ = make_move(board, 1, False)
	# state = make_move(board, 0,True)    
	# print(state)