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
        self.logs = []
    
    def update(self, FONT):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

        p1_text = FONT.render("PLAYER 1", True, WHITE)
        p1_text_rect = p1_text.get_rect()
        self.win.blit(p1_text, (150, 50))
        p2_text = FONT.render("PLAYER 2", True, WHITE)
        p2_text_rect = p2_text.get_rect()
        self.win.blit(p2_text, (150, 700))
        
        if self.turn == WHITE:
            pygame.draw.polygon(self.win, (255, 191, 0), ((110,50),(125,65),(110,80)))
        elif self.turn == BLUE:
            pygame.draw.polygon(self.win, (255, 191, 0), ((110,700),(125,715),(110,730)))

        pygame.draw.rect(self.win, WHITE, (OFFSET + SQUARE_SIZE*ROWS + OFFSET, OFFSET, 250, ROWS*SQUARE_SIZE))
        for i in range(len(self.logs)):
            self.win.blit(FONT.render(self.logs[i], True, BLACK), (OFFSET + SQUARE_SIZE*ROWS + OFFSET, OFFSET + i*50))


        pygame.display.update()

    def _init(self):
        self.game_state = State.MENU_STATE
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.valid_moves = {}

    def set_turn(self, turn):
        self.turn = turn

    def winner(self):
        if self.board.winner() != None:
            self.game_state = State.MENU_STATE
            return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE//2 + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE//2 + OFFSET), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.logs.append("White turn")
            self.turn = WHITE
        else:
            self.logs.append("Blue turn")
            self.turn = BLUE
        
