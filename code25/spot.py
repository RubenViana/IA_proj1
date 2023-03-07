from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN, BLACK, OFFSET
import pygame

class Spot:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0  
        self.calc_pos() 
	
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(win, BLACK, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE), 1)
        

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + OFFSET
        self.y = SQUARE_SIZE * self.row + OFFSET

    def get_pos(self):
        return self.row, self.col


    def get_color(self):
            return self.color