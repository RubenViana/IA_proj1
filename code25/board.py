import pygame
import random
from .constants import BLACK, ROWS, BLUE, SQUARE_SIZE, COLS, WHITE, BLUE_WHITE
from .piece import Piece
from .spot import Spot

class Board:
    def __init__(self):
        self.board = []
        self.pieces = []
        self.blue_left = self.white_left = 5
        self.blue_goal = self.white_goal = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col].draw(win)

    def rotate_board(self):
        rotated_board = [list(row)[::-1] for row in zip(*self.board)]

        for row in range(ROWS):
            for col in range(COLS):
                self.board[row][col] = Spot(row, col, rotated_board[row][col].color)

    def set_pieces(self, c1, c2):
        for row in range(ROWS):
            for col in range(COLS):
                if row == 0:
                    self.pieces[row][col] = Piece(row, col, c2)
                elif row == ROWS - 1:
                    self.pieces[row][col] = Piece(row, col, c1)


    def move(self, piece, row, col):
        self.pieces[piece.row][piece.col], self.pieces[row][col] = self.pieces[row][col], self.pieces[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 and piece.color == WHITE) or (row == 0 and piece.color == BLUE):
            piece.make_goal()
            if piece.color == WHITE:
                self.white_goal += 1
            else:
                self.blue_goal += 1 

    def get_piece(self, row, col):
        return self.pieces[row][col]

    def create_board(self):

        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                self.board[row].append(Spot(row, col, WHITE))

        self.board[ROWS // 2][ROWS // 2] = Spot(ROWS // 2, ROWS // 2, BLUE_WHITE)

        i = 0
        while i < (ROWS*ROWS - 1) / 2:
            x = random.randrange(ROWS)
            y = random.randrange(ROWS)
            if (self.board[x][y].get_color() != BLUE) and (self.board[x][y].get_color() != BLUE_WHITE):
                self.board[x][y] = Spot(x, y, BLUE)
                i += 1
        
        for row in range(ROWS):
            self.pieces.append([])
            for col in range(COLS):
                self.pieces[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.pieces[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, piece):
        if self.pieces[piece.row][piece.col].color == BLUE: 
            self.blue_left -= 1
        else:
            self.white_left -= 1
            
        self.pieces[piece.row][piece.col] = 0
    
    
    #o que deve acontecer se, por ex., o branco tiver uma peça goal mas todas as suas restantes peças forem comidas, mas sem o blue 
    # ter uma única peça goal? Ganha o branco por ter todas as suas peças como goal ou ganha o blue por ter comido todas as peças do branco?
    def winner(self):
        if self.white_goal > self.blue_goal and self.white_left == self.white_goal:
            return WHITE
        elif self.blue_left <= 0:
            return WHITE
        
        if self.blue_goal > self.white_goal and self.blue_left == self.blue_goal:
            return BLUE
        elif self.white_left <= 0: 
            return BLUE
        
        return None
    