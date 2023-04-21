import random
board = [[None for _ in range(4)] for _ in range(4)]
pieces = [(color, shape, size, fill) for color in [0, 1] for shape in [0, 1] for size in [0, 1] for fill in [0, 1]]

def print_board():
    print("  0 1 2 3")
    for i in range(4):
        row = str(i) + " "
        for j in range(4):
            if board[i][j] is None:
                row += ". "
            else:
                row += str(board[i][j]) + " "
        print(row)


def get_possible_moves():
    return [(i, j) for i in range(4) for j in range(4) if board[i][j] is None]

def has_common_property(pieces):
    return any(all(piece[i] == pieces[0][i] for piece in pieces) for i in range(4))

def has_won():
    # Check rows
    for i in range(4):
        pieces_in_row = [piece for piece in board[i] if piece is not None]
        if len(pieces_in_row) == 4 and has_common_property(pieces_in_row):
            return True
    # Check columns
    for j in range(4):
        pieces_in_col = [board[i][j] for i in range(4) if board[i][j] is not None]
        if len(pieces_in_col) == 4 and has_common_property(pieces_in_col):
            return True
    # Check diagonals
    pieces_in_diag = [board[i][i] for i in range(4) if board[i][i] is not None]
    if len(pieces_in_diag) == 4 and has_common_property(pieces_in_diag):
        return True
    pieces_in_diag = [board[i][3-i] for i in range(4) if board[i][3-i] is not None]
    if len(pieces_in_diag) == 4 and has_common_property(pieces_in_diag):
        return True
    return False


def play():
    player = 0
    while True:
        print_board()
        possible_moves = get_possible_moves()
        if not possible_moves:
            print("Game over, it's a draw!")
            break
        print(f"Player {player+1}'s turn")
        row, col = map(int, input("Choose a row and column to place a piece (e.g. '1 2'): ").split())
        if board[row][col] is None:
            print("Available pieces:")
            for i, piece in enumerate(pieces):
                print(f"{i}: {piece}")
            piece_index = int(input("Choose a piece by index: "))
            piece = pieces.pop(piece_index)
            board[row][col] = piece

            if has_won():
                print_board()
                print(f"Player {player+1} has won!")
                break

            player = 1 - player
        else:
            print("Sorry, this cell is already occupied. Please choose another cell.")


play()
