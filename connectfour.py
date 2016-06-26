#tuple will be (board, status, reward)
#status is boolean; True if running

import numpy as np

rewards = {
    'win': 1,
    'illegal_move': -10,
    'draw': 0,
    'ongoing': 0
}

#neural network will always thinks it's 1; and it's opponent will always be -1
#can simply multiply the board by -1 to reverse
def get_available_boards(board, player):
    cols = board.shape[1]
    results = []

    for c in range(cols):
        #if we can add a piece to the col, create a copy of the board and add a piece to that board
        if available_row(board, c) != -1:
            b = np.copy(board)
            add_piece(b, player, c)
            results.append((b, c))

    return results

#modifies board inplace
#adds a piece and return the (row, col) of the piece added
#if it's invalid move, return None
def add_piece(board, player, col):
    row = available_row(board, col)

    if row != -1:
        add_piece_helper(board, player, row, col)
        return (row, col)
    #invalid Move
    else:
        return None

#return the first row where a piece can be placed
# if invalid, return -1
def available_row(board, col):
    row = np.where(board[:, col] != 0)
    rows = board.shape[0]

    #if entire column is empty, return last row
    # don't return -1 as last row since we are using -1 to signify invalid (i.e. entire column is full)
    return rows - 1 if len(row[0]) == 0 else row[0][0] - 1 

def add_piece_helper(board, player, row, col):
    board[row, col] = player

def check_victory(board, player, row, col):
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

#returns a tuple containing empty board, whether game is ongoing, and rewards
def init_game(rows=6, cols=7):
    board = np.zeros((rows, cols)).astype(int)
    return (board, True, rewards['ongoing'])

#returns a tuple containing the resulting board, whether game is in ongoing, and reward
def make_move(board, col, player_one_turn=True):
    player_mark = 1 if player_one_turn else -1 

    #note that add_piece modifies board inplace
    positions = add_piece(board, player_mark, col)

    #if illegal move
    if positions == None:
        return (board, False, rewards['illegal_move'])
    else:
        r, c = positions

    #returns rewards['win'] if player is player 1, otherwise returns -rewards['win']
    if check_victory(board, player_mark, r, c):
        return (board, False, rewards['win'] * player_mark)

    elif check_draw(board):
        return (board, False, rewards['draw'])

    #if not won or drawm, then game is ongoing
    else:
        return (board, True, rewards['ongoing'])
    
# def play(player_one_ai=None, player_two_ai=None, , ):
#     while True:
#         #this is for display purposes (First Player  vs Second Player)
#         player_display = 'first' if player_one else 'second'
#         player_mark = 1 if player_one else -1 

#         if (player_one and player_one_ai == None) or (not player_one and player_two_ai == None):
#             col = int(input('Please insert move {} player \n'.format(player_display)))
#         elif not player_one:
#             move = player_two_ai(board)

#         r, c = add_piece(board, player_mark, col)
#         if check_victory(board, player_mark, r, c):
#             print(board)
#             print('You have won {} player\n'.format(player_display))
#             break

#         print(board)
#         player_one = not player_one

if __name__ == '__main__':
    board, _, _ = init_game()
    board, _, _ = make_move(board, 0, True)
    board, _, _ = make_move(board, 1, False)
    board, _, _ = make_move(board, 0, True)
    board, _, _ = make_move(board, 1, False)
    board, _, _ = make_move(board, 0, True)
    board, _, _ = make_move(board, 1, False)
    state = make_move(board, 0,True)    
    print(state)