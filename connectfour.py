import numpy as np

rewards = {
    'win': 1,
    'illegal_move': -10,
    'draw': 0,
    'ongoing': 0
}

#neural network will always thinks player 1 is 1 and opponent is -1
#can simply multiply the board by -1 to reverse player

#modifies board inplace
#adds a piece and return the (row, col) of the piece added
#if it's invalid move, return None
def add_piece(board, player, col):
    row = get_available_row(board, col)

    if row != -1:
        add_piece_helper(board, player, row, col)
        return (row, col)
    #invalid Move
    else:
        return None

#returns a list of available cols
def get_available_moves(board):
    return np.where(board[0] == 0)[0]

#return the first row where a piece can be placed
# if invalid, return -1
def get_available_row(board, col):
    row = np.where(board[:, col] != 0)
    rows = board.shape[0]

    #if entire column is empty, return last row
    # don't return -1 as last row since we are using -1 to signify invalid (i.e. entire column is full)
    return rows - 1 if len(row[0]) == 0 else row[0][0] - 1 

def add_piece_helper(board, player, row, col):
    board[row, col] = player

def check_victory(board, player, row, col):
    # print('making move {} {}'.format(row, col))
    return any([check_victory_helper(board, player, row, col, 0, 1), check_victory_helper(board, player, row, col, 1, 0), check_victory_helper(board, player, row, col, 1, 1), check_victory_helper(board, player, row, col, -1, 1)])

#if there are no more zeros on board, and player hasn't already won, implies draw (no empty space)
def check_draw(board):
    return len(np.where(board == 0)[0]) == 0

#use a higher level function that can be used to check horizontal, vertical and diagonal
def check_victory_helper(board, player, row, col, row_offset, col_offset):
    counter = 1

    r , c = row + row_offset, col + col_offset
    while not check_out_of_bounds(board, r, c) and board[r][c] == player:
        counter += 1
        r += row_offset
        c += col_offset

    r , c = row - row_offset, col - col_offset  
    while not check_out_of_bounds(board, r, c) and board[r][c] == player:
        counter += 1
        r -= row_offset
        c -= col_offset

    return counter == 4

def check_out_of_bounds(board, row, col):
    rows, cols = board.shape
    return row < 0 or row > rows - 1 or col < 0 or col > cols - 1

#returns a tuple containing board, whether game is ongoing, and rewards
def init_game(input_board=None, rows=6, cols=7):
    if input_board == None:
        board = np.zeros((rows, cols)).astype(int)
    else:
        board = np.copy(input_board)
    return (board, 'ongoing')

def get_reward(status):
    return rewards[status]

#returns a tuple containing the resulting board and status of game
def make_move(board, col, player_one_turn=True):
    player_mark = 1 if player_one_turn else -1 

    #note that add_piece modifies board inplace
    positions = add_piece(board, player_mark, col)

    #if illegal move
    if positions == None:
        return (board, 'illegal_move')
    else:
        r, c = positions

    if check_victory(board, player_mark, r, c):
        return (board, 'win')
    elif check_draw(board):
        return (board, 'draw')
    #if not won or drawn, then game is ongoing
    else:
        return (board, 'ongoing')

if __name__ == '__main__':
    state = init_game()
    state = make_move(state[0], 0, False)
    state = make_move(state[0], 0, False)
    state = make_move(state[0], 0, False)
    state = make_move(state[0], 0, False)
    print(state)
    state = make_move(state[0], 0, False)
 
    print(state)