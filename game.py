import pygame
from board import Board

class Game: 

    def __init__(self):

        pygame.init()
        self.board = Board()

        self.start_square = None
        self.end_square = None
        self.current = "White"
        self.legal_moves = []

        self.white_controlled = []
        self.black_controlled = []
        self.white_king_checked = None
        self.black_king_checked = None

        self.total_white_moves = []
        self.total_black_moves = []

        self.white_win = False
        self.black_win = False
        self.draw = False

        self.piece_images = {

            1: pygame.transform.smoothscale(pygame.image.load('w_pawn_1024px.png'), (75, 75)),
            2: pygame.transform.smoothscale(pygame.image.load('w_knight_1024px.png'), (75, 75)),
            3: pygame.transform.smoothscale(pygame.image.load('w_bishop_1024px.png'), (75, 75)),
            4: pygame.transform.smoothscale(pygame.image.load('w_rook_1024px.png'), (75, 75)),
            5: pygame.transform.smoothscale(pygame.image.load('w_queen_1024px.png'), (75, 75)),
            6: pygame.transform.smoothscale(pygame.image.load('w_king_1024px.png'), (75, 75)),

            -1: pygame.transform.smoothscale(pygame.image.load('b_pawn_1024px.png'), (75, 75)),
            -2: pygame.transform.smoothscale(pygame.image.load('b_knight_1024px.png'), (75, 75)),
            -3: pygame.transform.smoothscale(pygame.image.load('b_bishop_1024px.png'), (75, 75)),
            -4: pygame.transform.smoothscale(pygame.image.load('b_rook_1024px.png'), (75, 75)),
            -5: pygame.transform.smoothscale(pygame.image.load('b_queen_1024px.png'), (75, 75)),
            -6: pygame.transform.smoothscale(pygame.image.load('b_king_1024px.png'), (75, 75))

        }

        self.screen = pygame.display.set_mode((1000, 1000))
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Chess Program")
        self.clock = pygame.time.Clock()
        self.running = True

    def check_click(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.white_controlled, self.black_controlled = self.board.checks(self.board.state)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:       
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= 100 and mouse_x <= 900 and mouse_y >= 100 and mouse_y <= 900:
                        square_x, square_y = mouse_x // 100 - 1, mouse_y // 100 - 1
                        
                        if self.start_square is None and ((self.board.state[square_y][square_x] > 0 and self.current == "White") or (self.board.state[square_y][square_x] < 0 and self.current == "Black")):
                            self.start_square = [square_y, square_x]
                            self.legal_moves = self.board.get_legal_moves(self.board.state, self.start_square[0], self.start_square[1])
                            self.legal_moves = self.board.refine_legal_moves(self.board.state, self.start_square[0], self.start_square[1], self.legal_moves, self.current)

                        elif self.start_square is not None and (square_y != self.start_square[0] or square_x != self.start_square[1]):
                            self.end_square = [square_y, square_x]
                    
                            if [self.end_square[0], self.end_square[1]] in self.legal_moves:

                                if not self.board.white_king_moved:
                                    if self.board.state[self.start_square[0]][self.start_square[1]] == 6:
                                        self.board.white_king_moved = True

                                        if self.end_square[1] == 6:
                                            self.board.white_h_rook_moved = True
                                            self.board.state[7][5] = 4
                                            self.board.state[7][7] = 0

                                        elif self.end_square[1] == 2:
                                            self.board.white_a_rook_moved = True
                                            self.board.state[7][3] = 4
                                            self.board.state[7][0] = 0

                                if not self.board.black_king_moved:
                                    if self.board.state[self.start_square[0]][self.start_square[1]] == -6:
                                        self.board.black_king_moved = True 

                                        if self.end_square[1] == 6:
                                            self.board.black_h_rook_moved = True
                                            self.board.state[0][5] = -4
                                            self.board.state[0][7] = 0

                                        elif self.end_square[1] == 2:
                                            self.board.black_a_rook_moved = True
                                            self.board.state[0][3] = -4
                                            self.board.state[0][0] = 0

                                if self.board.state[self.start_square[0]][self.start_square[1]] == 4:
                                    if self.start_square[0] == 7 and self.start_square[1] == 7:
                                        self.board.white_h_rook_moved = True
                                    elif self.start_square[0] == 7 and self.start_square[1] == 0:
                                        self.board.white_a_rook_moved = True
                                elif self.board.state[self.start_square[0]][self.start_square[1]] == -4:
                                    if self.start_square[0] == 0 and self.start_square[1] == 7:
                                        self.board.black_h_rook_moved = True
                                    elif self.start_square[0] == 0 and self.start_square[1] == 0:
                                        self.board.black_a_rook_moved = True

                                if abs(self.board.state[self.start_square[0]][self.start_square[1]]) == 1 and self.board.state[self.end_square[0]][self.end_square[1]] == 0 and self.start_square[1] != self.end_square[1]:
                                    self.board.state[self.start_square[0]][self.end_square[1]] = 0

                                self.board.white_en_passant_columns = [False, False, False, False, False, False, False, False] 
                                if self.board.state[self.start_square[0]][self.start_square[1]] == 1 and self.start_square[0] - self.end_square[0] == 2:
                                    self.board.white_en_passant_columns[self.start_square[1]] = True

                                self.board.black_en_passant_columns = [False, False, False, False, False, False, False, False] 
                                if self.board.state[self.start_square[0]][self.start_square[1]] == -1 and self.start_square[0] - self.end_square[0] == -2:
                                    self.board.black_en_passant_columns[self.start_square[1]] = True

                                if self.board.state[self.start_square[0]][self.start_square[1]] == 1 and self.end_square[0] == 0:
                                    self.board.white_promotion = self.end_square[1]
                                if self.board.state[self.start_square[0]][self.start_square[1]] == -1 and self.end_square[0] == 7:
                                    self.board.black_promotion = self.end_square[1]

                                self.board.state[self.end_square[0]][self.end_square[1]] = self.board.state[self.start_square[0]][self.start_square[1]]
                                self.board.state[self.start_square[0]][self.start_square[1]] = 0

                                if self.board.white_promotion in [0, 1, 2, 3, 4, 5, 6, 7] or self.board.black_promotion in [0, 1, 2, 3, 4, 5, 6, 7]:

                                    if self.board.white_promotion in [0, 1, 2, 3, 4, 5, 6, 7]:
                                        for p in [0, 1, 2, 3]:
                                            pygame.draw.circle(self.screen, "#BBBBBB", (self.board.white_promotion * 100 + 150, p * 100 + 150), 50)
                                            self.screen.blit(self.piece_images[self.board.white_pieces[p]], (self.board.white_promotion * 100 + 112.5, p * 100 + 112.5))

                                    if self.board.black_promotion in [0, 1, 2, 3, 4, 5, 6, 7]:
                                        for p in [7, 6, 5, 4]:
                                            pygame.draw.circle(self.screen, "#BBBBBB", (self.board.black_promotion * 100 + 150, p * 100 + 150), 50)
                                            self.screen.blit(self.piece_images[self.board.black_pieces[p]], (self.board.black_promotion * 100 + 112.5, p * 100 + 112.5))

                                    pygame.display.flip()  
                                    self.clock.tick(60)

                                    complete = False
                                    while True:

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                self.running = False
                                
                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if event.button == 1:       
                                                    mouse_x, mouse_y = pygame.mouse.get_pos()
                                                    square_x, square_y = mouse_x // 100 - 1, mouse_y // 100 - 1

                                                    if self.board.white_promotion == square_x:
                                                        if square_y in [0, 1, 2, 3]:
                                                            self.board.state[self.end_square[0]][self.end_square[1]] = self.board.white_pieces[square_y]
                                                            self.board.white_promotion = None
                                                            complete = True

                                                    if self.board.black_promotion == square_x:
                                                        if square_y in [7, 6, 5, 4]:
                                                            self.board.state[self.end_square[0]][self.end_square[1]] = self.board.black_pieces[square_y]
                                                            self.board.black_promotion = None
                                                            complete = True
                                            
                                        if complete:
                                            break

                                self.start_square = None
                                self.legal_moves = []
                                self.current = "White" if self.current == "Black" else "Black"
                            
                            elif self.board.state[self.end_square[0]][self.end_square[1]] * self.board.state[self.start_square[0]][self.start_square[1]] > 0:
                                self.start_square = [self.end_square[0], self.end_square[1]]
                                self.legal_moves = self.board.get_legal_moves(self.board.state, self.start_square[0], self.start_square[1])
                                self.legal_moves = self.board.refine_legal_moves(self.board.state, self.start_square[0], self.start_square[1], self.legal_moves, self.current)

                            else:
                                self.start_square = None
                                self.legal_moves = []

                    else:
                        self.start_square = None
                        self.legal_moves = []

    def check_result(self):

        self.white_king_checked = None
        self.black_king_checked = None
        self.total_white_moves = []
        self.total_black_moves = []

        for row in range(8):
            for col in range(8):

                if self.board.state[row][col] == 6 and [row, col] in self.black_controlled:
                    self.white_king_checked = [row, col]
                if self.board.state[row][col] == -6 and [row, col] in self.white_controlled:
                    self.black_king_checked = [row, col]

                l_moves = self.board.get_legal_moves(self.board.state, row, col)
                l_moves = self.board.refine_legal_moves(self.board.state, row, col, l_moves, self.current)
                
                if l_moves != [] and self.board.state[row][col] > 0:
                    self.total_white_moves.append(l_moves)
                if l_moves != [] and self.board.state[row][col] < 0:
                    self.total_black_moves.append(l_moves)

        if self.current == "White" and self.total_white_moves == []:
            if self.white_king_checked is not None:
                self.black_win = True
            else:
                self.draw = True
        if self.current == "Black" and self.total_black_moves == []:
            if self.black_king_checked is not None:
                self.white_win = True
            else:
                self.draw = True

    def draw_board(self):

        self.screen.fill("#000000")
        self.team = self.font.render(f"{self.current} to play", True, (255, 255, 255))
        self.screen.blit(self.team, (420, 50))

        for row in range(8):
            for col in range(8):

                x = (col + 1) * 100 
                y = (row + 1) * 100

                colour = "#4E3005" if (row + col) % 2 else "#8A775C"          
                pygame.draw.rect(self.screen, colour, (x, y, 100, 100))

                piece = self.board.state[row][col]
                if piece != 0:
                    self.screen.blit(self.piece_images[piece], (x + 12.5, y + 12.5))

        if self.start_square is not None:
            pygame.draw.rect(self.screen, "#0A2E13", (self.start_square[1] * 100 + 100, self.start_square[0] * 100 + 100, 100, 100), 4)
        
            for position in self.legal_moves:
                pygame.draw.circle(self.screen, "#272727", (position[1] * 100 + 150, position[0] * 100 + 150), 15)

        if self.white_king_checked is not None:
            pygame.draw.rect(self.screen, "#D94610", (self.white_king_checked[1] * 100 + 105, self.white_king_checked[0] * 100 + 105, 90, 90), 4)
        if self.black_king_checked is not None:
            pygame.draw.rect(self.screen, "#D94610", (self.black_king_checked[1] * 100 + 105, self.black_king_checked[0] * 100 + 105, 90, 90), 4)
 
    def run(self):
        while self.running:

            if self.white_win:
                print("White won!")
                break
            if self.black_win:
                print("Black won!")
                break
            if self.draw:
                print("It was a draw!")
                break

            self.check_click()
            self.check_result()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

game = Game()
game.run()