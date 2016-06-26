import numpy as np

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

#adds a piece and return the (row, col) of the piece added
def add_piece(board, player, col):
    row = available_row(board, col)

    if row != -1:
        add_piece_helper(board, player, row, col)
        return (row, col)
    else:
        print('Invalid Move')
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

def total_consecutive_threes(board, player):
    total_threes = 0
    total_threes += sum([total_consecutive_threes_helper(row, player) for row in board])
    return total_threes

#return number of 3 consecutive items in a list
def total_consecutive_threes_helper(li, player):
    total_threes = 0

    #counter used to track number of consecutive pieces
    counter = 0
    for val in li:
        if val == player:
            counter += 1
        else:
            counter = 0

        if counter >= 3:
            total_threes += 1

    return total_threes

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

def play(player_one_ai=None, player_two_ai=None, rows=6, cols=7, player_one_starts=True):
    player_one = player_one_starts
    board = np.zeros((rows, cols))    

    while True:
        player = 1 if player_one else 2

        if (player_one and player_one_ai == None) or (not player_one and player_two_ai == None):
            col = int(input('Please insert move Player {}\n'.format(player)))
        elif not player_one:
            move = player_two_ai(board, get_available_boards)

        r, c = add_piece(board, player, col)
        print(total_consecutive_threes(board, player))
        if check_victory(board, player, r, c):
            print(board)
            print('You have won Player {}'.format(player))
            break

        print(board)
        player_one = not player_one

if __name__ == '__main__':
    play()
    # li = [1, 1, 1, 2, 1, 1, 1]
    # print(check_three_in_list(li, 1))