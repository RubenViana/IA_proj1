import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, GREY, OFFSET, WIDTH, BLACK, ROWS
from code25.board import Board
from enum import Enum

class State(Enum):
    MENU_STATE = 0
    PLAY_STATE = 1
    P2COLORSIDE_STATE = 2


class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.font = pygame.font.SysFont("arial", 30, bold=True)
        self.btn_font = pygame.font.SysFont("arial", 20, bold=True)
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

        esc_text = self.btn_font.render("[ESC] Back", True, BLACK)
        self.win.blit(esc_text, (10, 10))

        p1_text = self.font.render("PLAYER 1", True, BLACK)
        p1_text_rect = p1_text.get_rect()
        p1_text_rect.center = (OFFSET + (ROWS*SQUARE_SIZE) // 2, OFFSET - 50)
        self.win.blit(p1_text, p1_text_rect)
        p2_text = self.font.render("PLAYER 2", True, BLACK)
        p2_text_rect = p2_text.get_rect()
        p2_text_rect.center = (OFFSET + (ROWS*SQUARE_SIZE) // 2, OFFSET + (ROWS*SQUARE_SIZE) + 50)
        self.win.blit(p2_text, p2_text_rect)
        
        if self.game_state == State.PLAY_STATE:
            if self.turn == self.p1_color:
                pygame.draw.polygon(self.win, (255,215,0), ((110, 80),(125, 95),(110, 110)))
            elif self.turn == self.p2_color:
                pygame.draw.polygon(self.win, (255,215,0), ((110, 680),(125, 695),(110, 710)))

        if self.game_state == State.P2COLORSIDE_STATE:
            rotate_text = self.btn_font.render("[R] Rotate", True, BLACK)
            self.win.blit(rotate_text, (OFFSET + ROWS*SQUARE_SIZE // 2 - 240, OFFSET + (ROWS*SQUARE_SIZE) + 90))
            s_select_text = self.btn_font.render("[S] Switch Color", True, BLACK)
            self.win.blit(s_select_text, (OFFSET + ROWS*SQUARE_SIZE // 2 - 115, OFFSET + (ROWS*SQUARE_SIZE) + 90))
            sp_select_text = self.btn_font.render("[Space] Start Game", True, BLACK)
            self.win.blit(sp_select_text, (OFFSET + ROWS*SQUARE_SIZE // 2 + 60, OFFSET + (ROWS*SQUARE_SIZE) + 90))


        pygame.display.update()

    def _init(self):
        self.game_state = State.MENU_STATE
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.p1_color = WHITE
        self.p2_color = BLUE
        self.board.set_pieces(WHITE, BLUE)
        self.valid_moves = set()
        self.logs = []

    def set_turn(self, color):
        self.p1_color = color
        if color == WHITE:
            self.p2_color = BLUE
        else:
            self.p2_color = WHITE
        self.board.set_pieces(self.p1_color, self.p2_color)
        self.turn = self.p1_color

    def winner(self):
        if self.board.winner() != None:
            self.reset()
            return self.board.winner()

    def reset(self):
        self._init()

    def get_valid_moves(self, piece):
        possible_moves = set()
        valid_moves = set()
        left = piece.col - 1
        right = piece.col + 1
        up = piece.row - 1
        down = piece.row + 1

        possible_moves.update({(piece.row, left), (piece.row, right), (up, piece.col), (down, piece.col), (up, left), (up, right), (down, left), (down, right)})

        for move in possible_moves:
            row, col = move
            if((0 <= row < ROWS) and (0 <= col < ROWS)):
                if self.board.get_piece(row, col) == 0 or (self.board.get_piece(row, col).color != self.turn and self.board.get_piece(row, col).goal == False):
                    valid_moves.add(move)
       
        return valid_moves

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn and piece.goal == False:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves and piece != 0 and piece.color != self.turn:
            self.board.remove(piece)
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE//2 + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE//2 + OFFSET), SQUARE_SIZE//8)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.logs.append("White turn")
            self.turn = WHITE
        else:
            self.logs.append("Blue turn")
            self.turn = BLUE
        
