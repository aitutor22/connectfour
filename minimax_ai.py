import time

from connectfour import *

max_depth = 6

hash_table = {}

#evaluation function
#+ if it favours player 1, - if it favours player 2
def evaluate(board):
	#weight by 0.1
	return (total_consecutive_threes(board, True) - total_consecutive_threes(board, False)) * 0.1

#returns total number of 3s in a board
#note that if the 3s have no space next to it to become connect four, we do not count it
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
	#we do not include diagonals that have max length of 3 since we can't win with them
	for offset in range(-2, 4):
		total_threes += total_consecutive_threes_helper(np.diag(board, k=offset), player_mark)
		total_threes += total_consecutive_threes_helper(np.diag(flipped_board, k=offset), player_mark)
	return total_threes

#return number of 3 consecutive items in a list
def total_consecutive_threes_helper(li, player_mark):
	total_threes = 0

	#counter used to track number of consecutive pieces
	counter = 0
	start_index = None
	for i, val in enumerate(li):
		if val == player_mark:
			counter += 1
			if start_index == None:
				start_index = i
		else:
			counter = 0
			start_index = None
		
		if counter >= 3:
			#tests for empty space either before or after the sequence
			if ((start_index - 1 >= 0) and (li[start_index - 1] == 0)) or ((i + 1 < len(li) - 1) and (li[i + 1] == 0)):
				total_threes += 1
	return total_threes

def minimax(board, player_one_turn=True):
	#opening move when board is empty (place in center)
	if len(np.where(board == 0)[0]) == 6 * 7:
		return 3
	return minimax_helper(board, player_one_turn, -100000, 100000)

#http://aima.cs.berkeley.edu/python/games.html
def minimax_helper(board, max_player, alpha, beta, status='ongoing', depth=0):
	previous_player = not max_player
	best_val = -100000 if max_player else 100000

	#see if value is already stored
	hashed_board = board.tostring()
	if depth > 0 and hashed_board in hash_table:
		return hash_table[hashed_board]

	#game has ended
	elif status != 'ongoing':
		#if previous_player is player 1 (max) and he won, then reward is positive
		#if previous_player is player 2 (min) and he won, then reward is negative
		return get_reward(status) * (1 if previous_player else -1)
	elif depth == max_depth:
		return evaluate(board)

	moves = get_available_moves(board)

	for move in moves:
		possible_board = init_game(board)[0]
		possible_board, status = make_move(possible_board, move, max_player)
		score = minimax_helper(possible_board, (not max_player), alpha, beta, status, depth + 1)

		#for max_player
		if max_player and score > best_val:
			best_val = score
			best_move = move

			if best_val >= beta:
				break

			alpha = max(alpha, score)

		#for min player
		elif (not max_player) and score < best_val:
			best_val = score
			best_move = move

			if best_val <= alpha:
				break
			beta = min(beta, score)

	#return best move if at root node, else return the best value
	if depth == 0:	
		return best_move
	else:
		#store value in hash table
		hash_table[board.tostring()] = best_val
		return best_val

if __name__ == '__main__':
	# s = convert(board)
	# print(s)
	# print('***')
	# print(convert(s, False))

	# board, _, _ = make_move(board, 0, False)
	# board, _, _ = make_move(board, 1, False)
	# # board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, False)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, True)
	# board, _, _ = make_move(board, 0, False)
	# # board, _, _ = make_move(board, 1, False)
	# board, ongoing, reward = make_move(board, 0, False)
	# board, ongoing, reward = make_move(board, 0, False)
	# board, ongoing, reward = make_move(board, 0, False)

	# print(board)
	# print(total_consecutive_threes(board, True))
	# start_time = time.time()
	# minimax(board, False)
	# print(time.time() - start_time)
	# print(board)

	b, status = init_game()
	player_one_turn = True
	total_time = 0
	while status == 'ongoing':
		if player_one_turn:
			start_time = time.time()
			move = minimax(b, player_one_turn)
			print('Time taken: {:.2f}s'.format(time.time() - start_time))
			total_time += time.time() - start_time
			print('AI Move: {}'.format(move))
			b, status = make_move(b, move, player_one_turn)
		else:
			user_move = int(input('plese make a move\n'))
			b, status = make_move(b, user_move, player_one_turn)

		print(b)
		print('\n*******NEXT PLAYER*******\n')
		player_one_turn = not player_one_turn

	print('Time: {}'.format(total_time))
