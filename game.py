import pygame
from board import Board

class Game: 

    def __init__(self):

        pygame.init()
        self.board = Board()

        self.screen_size = 1000
        self.square_size = 100
        self.piece_size = 80
        self.board_size = 8

        self.start_square = None
        self.end_square = None
        self.current = "White"

        self.white_win = False
        self.black_win = False
        self.draw = False

        self.piece_images = {

            1: pygame.transform.smoothscale(pygame.image.load('w_pawn_1024px.png'), (self.piece_size, self.piece_size)),
            2: pygame.transform.smoothscale(pygame.image.load('w_knight_1024px.png'), (self.piece_size, self.piece_size)),
            3: pygame.transform.smoothscale(pygame.image.load('w_bishop_1024px.png'), (self.piece_size, self.piece_size)),
            4: pygame.transform.smoothscale(pygame.image.load('w_rook_1024px.png'), (self.piece_size, self.piece_size)),
            5: pygame.transform.smoothscale(pygame.image.load('w_queen_1024px.png'), (self.piece_size, self.piece_size)),
            6: pygame.transform.smoothscale(pygame.image.load('w_king_1024px.png'), (self.piece_size, self.piece_size)),

            -1: pygame.transform.smoothscale(pygame.image.load('b_pawn_1024px.png'), (self.piece_size, self.piece_size)),
            -2: pygame.transform.smoothscale(pygame.image.load('b_knight_1024px.png'), (self.piece_size, self.piece_size)),
            -3: pygame.transform.smoothscale(pygame.image.load('b_bishop_1024px.png'), (self.piece_size, self.piece_size)),
            -4: pygame.transform.smoothscale(pygame.image.load('b_rook_1024px.png'), (self.piece_size, self.piece_size)),
            -5: pygame.transform.smoothscale(pygame.image.load('b_queen_1024px.png'), (self.piece_size, self.piece_size)),
            -6: pygame.transform.smoothscale(pygame.image.load('b_king_1024px.png'), (self.piece_size, self.piece_size)),

        }

        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        self.font = pygame.font.SysFont(None, 36)
        pygame.display.set_caption("Chess Program")
        self.clock = pygame.time.Clock()
        self.running = True

    def check_click(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:       
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x >= 100 and mouse_x <= 900 and mouse_y >= 100 and mouse_y <= 900:
                        square_x, square_y = mouse_x // 100 - 1, mouse_y // 100 - 1
                        
                        if self.start_square is None and ((self.board.state[square_y][square_x] > 0 and self.current == "White") or (self.board.state[square_y][square_x] < 0 and self.current == "Black")):
                            self.start_square = [square_x, square_y]
                        elif self.start_square is not None and (square_x != self.start_square[1] or square_y != self.start_square[0]):
                            self.end_square = [square_x, square_y]

                            # normal piece movement
                            if (self.board.state[self.start_square[1]][self.start_square[0]] * self.board.state[self.end_square[1]][self.end_square[0]]) <= 0:

                                self.board.state[self.end_square[1]][self.end_square[0]] = self.board.state[self.start_square[1]][self.start_square[0]]
                                self.board.state[self.start_square[1]][self.start_square[0]] = 0
                                
                                self.start_square = None
                                self.current = "White" if self.current == "Black" else "Black"
                                
                            elif self.board.state[self.end_square[1]][self.end_square[0]] != 0:
                                self.start_square = [self.end_square[0], self.end_square[1]]

                    else:
                        self.start_square = None



    def draw_board(self):

        self.screen.fill("#000000")
        team = self.font.render(f"{self.current} to play", True, (255, 255, 255))
        self.screen.blit(team, (420, 50))

        for row in range(self.board_size):
            for col in range(self.board_size):

                x = (col + 1) * self.square_size 
                y = (row + 1) * self.square_size
                colour = "#4E3005" if (row + col) % 2 else "#8A775C"
                piece = self.board.state[row][col]

                pygame.draw.rect(self.screen, colour, (x, y, self.square_size, self.square_size))
                if piece != 0:
                    self.screen.blit(self.piece_images[piece], (x + 0.1 * self.square_size, y + 0.1 * self.square_size))

        if self.start_square is not None:
            pygame.draw.rect(self.screen, "#0A2E13", (self.start_square[0] * 100 + 100, self.start_square[1] * 100 + 100, self.square_size, self.square_size), 4)

    def run(self):
        while self.running:
            self.check_click()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

game = Game()
game.run()