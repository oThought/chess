import copy
class Board:
    
    def __init__(self): 

        self.state = [[-4, -2, -3, -5, -6, -3, -2, -4],
                      [-1, -1, -1, -1, -1, -1, -1, -1],
                      [ 0,  0,  0,  0,  0,  0,  0,  0],
                      [ 0,  0,  0,  0,  0,  0,  0,  0],
                      [ 0,  0,  0,  0,  0,  0,  0,  0],
                      [ 0,  0,  0,  0,  0,  0,  0,  0],
                      [ 1,  1,  1,  1,  1,  1,  1,  1],
                      [ 4,  2,  3,  5,  6,  3,  2,  4]]
        
        self.white_king_moved  , self.black_king_moved   = False, False
        self.white_a_rook_moved, self.black_a_rook_moved = False, False
        self.white_h_rook_moved, self.black_h_rook_moved = False, False
        self.white_promotion   , self.black_promotion    = None , None

        self.white_pieces = {0:  5, 1:  4, 2:  3, 3:  2}
        self.black_pieces = {7: -5, 6: -4, 5: -3, 4: -2}
        self.white_en_passant_columns = [False, False, False, False, False, False, False, False]
        self.black_en_passant_columns = [False, False, False, False, False, False, False, False]

    def get_legal_moves(self, board, y, x):

        legal_moves = []
        piece = board[y][x]

        if piece in [6, -6]:
            # KING
            for yx in [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]:
                if y + yx[0] >= 0 and y + yx[0] <= 7 and x + yx[1] >= 0 and x + yx[1] <= 7:
                    if board[y + yx[0]][x + yx[1]] * piece <= 0:
                        legal_moves.append([y + yx[0], x + yx[1]])

            if not self.white_king_moved:
                if not self.white_h_rook_moved:
                    if board[7][5] == 0 and board[7][6] == 0 and board[7][7] == 4:
                        legal_moves.append([7, 6])
                if not self.white_a_rook_moved:
                    if board[7][1] == 0 and board[7][2] == 0 and board[7][3] == 0 and board[7][0] == 4:
                        legal_moves.append([7, 2])

            if not self.black_king_moved:
                if not self.black_h_rook_moved:
                    if board[0][5] == 0 and board[0][6] == 0 and board[0][7] == -4:
                        legal_moves.append([0, 6])
                if not self.black_a_rook_moved:
                    if board[0][1] == 0 and board[0][2] == 0 and board[0][3] == 0 and board[0][0] == -4:
                        legal_moves.append([0, 2])

        if piece in [5, -5, 4, -4, 3, -3]:

            if piece in [5, -5]:
                # QUEEN
                directions = [[1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1], [0, 1]]
            if piece in [4, -4]:
                # ROOK
                directions = [[1, 0], [0, -1], [-1, 0], [0, 1]]
            if piece in [3, -3]:
                # BISHOP
                directions = [[1, 1], [1, -1],  [-1, -1], [-1, 1]]

            for yx in directions:
                while True:
                    if y + yx[0] >= 0 and y + yx[0] <= 7 and x + yx[1] >= 0 and x + yx[1] <= 7:
                        if board[y + yx[0]][x + yx[1]] * piece < 0:
                            legal_moves.append([y + yx[0], x + yx[1]])
                            break
                        elif board[y + yx[0]][x + yx[1]] == 0:
                            legal_moves.append([y + yx[0], x + yx[1]])
                        else:
                            break
                    else:
                        break

                    yx[0] = yx[0] + 1 if yx[0] >= 1 else yx[0]
                    yx[0] = yx[0] - 1 if yx[0] <= -1 else yx[0]
                    yx[1] = yx[1] + 1 if yx[1] >= 1 else yx[1]
                    yx[1] = yx[1] - 1 if yx[1] <= -1 else yx[1]
            
        if piece in [2, -2]:
            # KNIGHT
            for yx in [[2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2], [1, 2]]:
                if y + yx[0] >= 0 and y + yx[0] <= 7 and x + yx[1] >= 0 and x + yx[1] <= 7:
                    if board[y + yx[0]][x + yx[1]] * piece <= 0:
                        legal_moves.append([y + yx[0], x + yx[1]])

        if piece in [1, -1]:
            # PAWN
            if board[y - piece][x] == 0:
                legal_moves.append([y - piece, x])
                if (y == 1 and board[y + 2][x] == 0 and piece == -1) or (y == 6 and board[y - 2][x] == 0 and piece == 1):
                    legal_moves.append([y - 2 * piece, x])

            for yx in [[-1 * piece, -1], [-1 * piece, 1]]:
                if x + yx[1] >= 0 and x + yx[1] <= 7:
                    if board[y + yx[0]][x + yx[1]] * piece < 0:
                        legal_moves.append([y + yx[0], x + yx[1]])
                        
                    if piece == 1 and y == 3 and board[y + yx[0]][x + yx[1]] == 0 and self.black_en_passant_columns[x + yx[1]] == True:
                        legal_moves.append([y + yx[0], x + yx[1]])
                    if piece == -1 and y == 4 and board[y + yx[0]][x + yx[1]] == 0 and self.white_en_passant_columns[x + yx[1]] == True:
                        legal_moves.append([y + yx[0], x + yx[1]])
            
        return legal_moves

    def refine_legal_moves(self, boardcopy, y, x, legal_moves, current_colour):
        refined_moves = []

        for move in legal_moves:
            board = copy.deepcopy(boardcopy)

            castle_out_of_check = False

            if not self.white_king_moved:
                if board[y][x] == 6:
                    if move[1] == 6:
                        board[y][5] = 6
                        castle_out_of_check = True
                    elif move[1] == 2:
                        board[y][3] = 6
                        castle_out_of_check = True

            if not self.black_king_moved:
                if board[y][x] == -6:
                    if move[1] == 6:
                        board[y][5] = -6
                        castle_out_of_check = True
                    elif move[1] == 2:
                        board[y][3] = -6
                        castle_out_of_check = True 

            if abs(board[y][x]) == 1 and board[move[0]][move[1]] == 0 and x != move[1]:
                board[y][move[1]] = 0

            if (board[y][x] == 1 and move[0] == 0) or (board[y][x] == -1 and move[0] == 7):
                board[y][x] = board[y][x] * 5

            board[move[0]][move[1]] = board[y][x]
            board[y][x] = 0 if not castle_out_of_check else board[y][x]

            white_controlled, black_controlled = self.checks(board)
            king_in_check = False

            for row in range(8):
                for col in range(8):
                    if board[row][col] == 6 and [row, col] in black_controlled and current_colour == "White":
                        king_in_check = True
                    if board[row][col] == -6 and [row, col] in white_controlled and current_colour == "Black": 
                        king_in_check = True

            if not king_in_check:
                refined_moves.append(move)
                        
        return refined_moves

    def checks(self, board):

        white_controlled, black_controlled = [], []

        for row in range(8):
            for col in range(8):

                if board[row][col] > 0:
                    controlled = self.get_legal_moves(board, row, col)
                    for square in controlled:
                        if square not in white_controlled:
                            white_controlled.append(square)

                elif board[row][col] < 0:
                    controlled = self.get_legal_moves(board, row, col)
                    for square in controlled:
                        if square not in black_controlled:
                            black_controlled.append(square)

        return white_controlled, black_controlled
                                            
