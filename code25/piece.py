from .constants import RED, WHITE, SQUARE_SIZE, OFFSET, BLUE, WHITE, WHITE_PIECE, BLUE_PIECE
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 3

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.goal = False
        self.x = OFFSET
        self.y = OFFSET
        self.calc_pos()

    def calc_pos(self):
        self.x = OFFSET + SQUARE_SIZE * self.col + (SQUARE_SIZE // 2)
        self.y = OFFSET + SQUARE_SIZE * self.row + (SQUARE_SIZE // 2) 

    def make_goal(self):
        self.goal = True
    
    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING
        if self.color == WHITE:
            #pygame.draw.circle(win, BLUE, (self.x, self.y), radius + self.OUTLINE)
            win.blit(WHITE_PIECE, (OFFSET + SQUARE_SIZE * self.col + 5, OFFSET + SQUARE_SIZE * self.row + 5))
        elif self.color == BLUE:
            #pygame.draw.circle(win, WHITE, (self.x, self.y), radius + self.OUTLINE)
            win.blit(BLUE_PIECE, (OFFSET + SQUARE_SIZE * self.col + 5, OFFSET + SQUARE_SIZE * self.row + 5))
        #pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)