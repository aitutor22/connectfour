import numpy as np
from connectfour import *
from minimax_ai import *

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def main():
	return render_template('main.html')

#converts 2d array to str
def convert_to_str(arr):
	arr = arr.astype(str)
	result = ''
	for row in arr[:-1]:
		result += ','.join(row)
		result += ';'
	result += ','.join(arr[-1])
	return result

#converts str to 2d array
def convert_to_arr(s):
	result = []
	for row in s.split(';'):
		result += [row.split(',')]

	result = np.array(result).astype(int)
	return result

@app.route('/move', methods=['POST'])
def get_ai_move():
	#string_board is a string; if it is blank, implies new game
	col, string_board = int(request.form['col']), request.form['board']

	#new game
	if string_board == '':
		state = init_game()
	#convert string to numpy array of int
	else:
		temp_board = convert_to_arr(string_board)
		state = init_game(temp_board)

	#make human move
	board, status = make_move(state[0], col, True)		

	#test if human player wins
	if status != 'ongoing':
		return jsonify(status=status, last_move='player_one')
	else:
		#gets col
		move = minimax(board, False)
		#we don't need the row for minimax, but we need to return to front-end
		row = get_available_row(board, move)
		board, status = make_move(board, move, False)

		if status != 'ongoing':
			return jsonify(status=status, last_move='player_two', col=move, row=row)

		return jsonify(status=status, col=move, row=row, board=convert_to_str(board))

if __name__ == '__main__':
	app.run()