import pygame
import random
from .constants import BLACK, ROWS, BLUE, COLS, WHITE, BLUE_WHITE, WOOD, OFFSET, SQUARE_SIZE, WOOD_BOARD
from .piece import Piece
from .spot import Spot

class Board:
    def __init__(self):
        self.board = []
        self.pieces = []
        self.p1_color = self.p2_color = 0
        self.blue_left = self.white_left = 5
        self.blue_goal = self.white_goal = 0
        self.create_board()
    
    def draw_squares(self, win):
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
                    self.pieces[row][col] = Piece(row, col, c1)
                elif row == ROWS - 1:
                    self.pieces[row][col] = Piece(row, col, c2)
        
        self.p1_color = c1
        self.p2_color = c2

    def get_all_pieces(self, color):
        pcs = []
        for pp in self.pieces:
            for piece in pp:
                if piece != 0 and piece.color == color and piece.goal == False:
                    pcs.append(piece)
        return pcs

    def get_piece(self, row, col):
        return self.pieces[row][col]
    
    def goal_distance(self, row, line):
        return abs(row - line)
    
    def h1(self, color):
        if color == BLUE and self.white_goal > self.blue_goal:
            return (self.blue_goal)*6 + (self.blue_left - self.white_left)*2
        elif color == BLUE and self.blue_goal >= self.white_goal:
            return (self.blue_goal)*4 + (self.blue_left - self.white_left)*10
        elif color == WHITE and self.blue_goal > self.white_goal:
            return (self.white_goal)*6 + (self.white_left - self.blue_left)*2
        elif color == WHITE and self.white_goal >= self.blue_goal:
            return (self.white_goal)*4 + (self.white_left - self.blue_left)*10

    def h2(self, color):
        dist = 0.01
        if color == self.p1_color:
            line = ROWS - 1
        else:
            line = 0
        pieces = self.get_all_pieces(color)
        for piece in pieces:
            row = piece.row
            dist += self.goal_distance(row, line)

        #print("dist:" + str(dist))
        return 0.5/dist + float(self.h1(color))

    def h3(self, color):
        dist = 0.01
        if color == self.p1_color:
            line = ROWS - 1
        else:
            line = 0
        pieces = self.get_all_pieces(color)
        for piece in pieces:
            row = piece.row
            dist += self.goal_distance(row, line)

        #print("dist:" + str(dist))
        return 0.5/dist

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
        #pygame.draw.rect(win, WOOD, (OFFSET - 20, OFFSET - 20, SQUARE_SIZE*ROWS + 40, SQUARE_SIZE*ROWS + 40), 0, 5)
        win.blit(WOOD_BOARD, (OFFSET - 20, OFFSET - 20))
        pygame.draw.rect(win, (92, 64, 51), (OFFSET - 20, OFFSET - 20, SQUARE_SIZE*ROWS + 40, SQUARE_SIZE*ROWS + 40), 3, 5)
        #pygame.draw.rect(win, (92, 64, 51), (OFFSET - 2, OFFSET - 2, SQUARE_SIZE*ROWS + 4, SQUARE_SIZE*ROWS + 4), 5, 5)
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
        if self.white_goal > self.blue_goal and (self.white_left == self.white_goal or self.blue_left == self.blue_goal):
            return WHITE
        elif self.white_goal == self.blue_goal and (self.white_left == self.white_goal or self.blue_left == self.blue_goal):
            if self.white_left > self.blue_left:
                return WHITE
        elif self.blue_left <= 0:
            return WHITE
        
        if self.blue_goal > self.white_goal and (self.white_left == self.white_goal or self.blue_left == self.blue_goal):
            return BLUE
        elif self.blue_goal == self.white_goal and (self.white_left == self.white_goal or self.blue_left == self.blue_goal):
            if self.blue_left > self.white_left:
                return BLUE
        elif self.white_left <= 0:
            return BLUE
        
        return None
    
    def get_intermediate_positions(self, start, end):

        intermediate_positions = []
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        
        x_direction = 1 if dx > 0 else -1
        y_direction = 1 if dy > 0 else -1
        
        abs_dx = abs(dx)
        abs_dy = abs(dy)
        
        max_steps = max(abs_dx, abs_dy)
        
        x_step = abs_dx / max_steps if max_steps > 0 else 0
        y_step = abs_dy / max_steps if max_steps > 0 else 0
        
        x = start[0]
        y = start[1]
        
        for i in range(max_steps):
            intermediate_positions.append((int(round(x)), int(round(y))))
            x += x_step * x_direction
            y += y_step * y_direction
        
        intermediate_positions.append(end)
        intermediate_positions.pop(0)
        
        return intermediate_positions

    def color_changes(self, piece, row, col, turn):
        piece.row_ = piece.row
        piece.col_ = piece.col
        color_changes = 0
        intermediate_pos = self.get_intermediate_positions((piece.row, piece.col), (row, col))
        self.board[ROWS//2][ROWS//2].set_color(turn)
        for int_pos in intermediate_pos:
            row_int, col_int = int_pos
            if (piece.color != self.board[row_int][col_int].get_color()) or (self.board[piece.row_][piece.col_].get_color() != self.board[row_int][col_int].get_color()):
                color_changes += 1
                piece.row_ = row_int
                piece.col_ = col_int
        self.board[ROWS//2][ROWS//2].set_color(BLUE_WHITE)
        return color_changes
    
    def stop_movement(self, piece, row, col):
        intermediate_pos = self.get_intermediate_positions((piece.row, piece.col), (row, col))

        for int_pos in intermediate_pos:
            row_int, col_int = int_pos
            if (self.get_piece(row_int, col_int) != 0 or (row_int == ROWS//2 and col_int == ROWS//2)) and (row_int != row or col_int != col):
                return True

    def get_valid_moves(self, piece, turn):
        possible_moves = set()
        valid_moves = set()
        left = piece.col
        right = piece.col
        up = piece.row
        down = piece.row
    	
        for i in range(0,ROWS-1):
            left -= 1
            right += 1
            up -= 1
            down += 1
            possible_moves.update({(piece.row, left), (piece.row, right), (up, piece.col), (down, piece.col), (up, left), (up, right), (down, left), (down, right)})
        

        for move in possible_moves:
            row, col = move
            if((0 <= row < ROWS) and (0 <= col < ROWS)):
                if self.get_piece(row, col) == 0 or (self.get_piece(row, col).color != turn and self.get_piece(row, col).goal == False):
                    if self.color_changes(piece, row, col, turn) < 2 and not(self.stop_movement(piece, row, col)):
                        valid_moves.add(move)
                            
        return valid_moves
    
    def move(self, piece, row, col):
        self.pieces[piece.row][piece.col], self.pieces[row][col] = self.pieces[row][col], self.pieces[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 and piece.color == WHITE and self.p1_color == WHITE) or (row == 0 and piece.color == WHITE and self.p1_color == BLUE) or (row == 0 and piece.color == BLUE and self.p1_color == WHITE) or (row == ROWS - 1 and piece.color == BLUE and self.p1_color == BLUE):
            piece.make_goal()
            if piece.color == WHITE:
                self.white_goal += 1
            else:
                self.blue_goal += 1
    