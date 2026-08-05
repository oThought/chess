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

    def get_legal_moves(x, y):
        legal_moves = []

        return legal_moves

