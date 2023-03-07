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

        if row == ROWS - 1 or row == 0:
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

    def remove(self, pieces):
        for piece in pieces:
            self.pieces[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLUE:
                    self.blue_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.blue_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLUE
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLUE:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.pieces[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.pieces[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves