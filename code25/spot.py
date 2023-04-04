# import necessary constants and modules
from .constants import RED, WHITE, SQUARE_SIZE, BLUE, OFFSET, WOOD, WHITE_TILE, BLUE_TILE, BLUE_WHITE_TILE
import pygame

# define the Spot class
class Spot:
    def __init__(self, row, col, color):
        # initialize the row, column, and color attributes of the Spot instance
        self.row = row
        self.col = col
        self.color = color
        # set initial x and y positions to 0, will be calculated in calc_pos() method
        self.x = 0
        self.y = 0  
        # calculate the position of the spot on the board based on its row and column
        self.calc_pos() 
	
    def draw(self, win):
        # draw the spot on the screen
        if self.color == WHITE:
            # if the spot is white, blit the WHITE_TILE image onto the screen
            win.blit(WHITE_TILE, (self.x, self.y))
        elif self.color == BLUE:
            # if the spot is blue, blit the BLUE_TILE image onto the screen
            win.blit(BLUE_TILE, (self.x, self.y))
        else:
            # if the spot is neither white nor blue, blit the BLUE_WHITE_TILE image onto the screen
            win.blit(BLUE_WHITE_TILE, (self.x, self.y))
        # draw a rectangle around the spot with a border of 1 pixel and the WOOD color
        pygame.draw.rect(win, WOOD, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE), 1)
        
    def calc_pos(self):
        # calculate the x and y positions of the spot on the screen based on its row and column
        self.x = SQUARE_SIZE * self.col + OFFSET
        self.y = SQUARE_SIZE * self.row + OFFSET

    def get_pos(self):
        # return the row and column position of the spot as a tuple
        return self.row, self.col

    def get_color(self):
        # return the color of the spot
        return self.color
    
    def set_color(self, color):
        # set the color of the spot to the given value
        self.color = color
