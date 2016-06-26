from connectfour import *

def total_consecutive_threes(board, player_one_turn=True):
	player_mark = 1 if player_one_turn else -1 
	total_threes = 0
	#for diagonals
	flipped_board = np.fliplr(board)
	#horizontal
	total_threes += sum([total_consecutive_threes_helper(row, player_mark) for row in board])
	#vertical (transpose the board)
	total_threes += sum([total_consecutive_threes_helper(row, player_mark) for row in board.T])

	#for diagonals
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
	# print(total_threes)
	return total_threes

if __name__ == '__main__':
	board, _, _ = init_game()
	board, _, _ = make_move(board, 0, True)
	board, _, _ = make_move(board, 1, False)
	board, _, _ = make_move(board, 0, True)
	board, _, _ = make_move(board, 1, False)
	board, _, _ = make_move(board, 0, True)

	board, _, _ = make_move(board, 3, True)
	board, _, _ = make_move(board, 4, True)
	board, _, _ = make_move(board, 4, True)
	board, _, _ = make_move(board, 5, True)
	board, _, _ = make_move(board, 5, False)
	board, _, _ = make_move(board, 5, True)
	print(total_consecutive_threes(board))
	print(board)
	# board, _, _ = make_move(board, 1, False)
	# state = make_move(board, 0,True)    
	# print(state)