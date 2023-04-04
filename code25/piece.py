# Import constants used in the class
from .constants import RED, WHITE, SQUARE_SIZE, OFFSET, BLUE, WHITE_PIECE, BLUE_PIECE
# Import the Pygame library
import pygame

# Define a class to represent a checkers piece
class Piece:
    # Define class-level constants
    PADDING = 15
    OUTLINE = 3

    # Define the constructor method for the Piece class
    def __init__(self, row, col, color):
        # Set the row, column, and color attributes of the piece
        self.row = row
        self.col = col
        self.color = color
        # Set a flag indicating whether the piece has become a king
        self.goal = False
        # Calculate the initial position of the piece on the board
        self.x = OFFSET
        self.y = OFFSET
        self.calc_pos()

    # Method to calculate the position of the piece on the board
    def calc_pos(self):
        self.x = OFFSET + SQUARE_SIZE * self.col + (SQUARE_SIZE // 2)
        self.y = OFFSET + SQUARE_SIZE * self.row + (SQUARE_SIZE // 2) 

    # Method to set the "goal" flag of the piece
    def make_goal(self):
        self.goal = True
    
    # Method to draw the piece on the board
    def draw(self, win):
        # Calculate the radius of the piece
        radius = SQUARE_SIZE//2 - self.PADDING
        # If the piece is white, draw a white game piece image at its position
        if self.color == WHITE:
            win.blit(WHITE_PIECE, (OFFSET + SQUARE_SIZE * self.col + 12, OFFSET + SQUARE_SIZE * self.row + 12))
        # If the piece is blue, draw a blue game piece image at its position
        elif self.color == BLUE:
            win.blit(BLUE_PIECE, (OFFSET + SQUARE_SIZE * self.col + 12, OFFSET + SQUARE_SIZE * self.row + 12))

    # Method to move the piece to a new position on the board
    def move(self, row, col):
        # Update the row and column attributes of the piece
        self.row = row
        self.col = col
        # Calculate the new position of the piece on the board
        self.calc_pos()

    # Method to return a string representation of the piece
    def __repr__(self):
        return str(self.color)
