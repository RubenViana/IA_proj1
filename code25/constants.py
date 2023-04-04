import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 5, 5
OFFSET = 150
SQUARE_SIZE = (WIDTH - OFFSET*2) // ROWS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
BLUE_WHITE = (150, 150, 200)

WOOD = (186, 140, 99)

BTN = (65, 58, 83)
BTN_HOVER = (195, 74, 54)

BACKGROUND = (251, 234, 255)

WHITE_TILE = pygame.transform.scale(pygame.image.load('images/whiteTile.png'), (SQUARE_SIZE, SQUARE_SIZE))
BLUE_TILE = pygame.transform.scale(pygame.image.load('images/blueTile.png'), (SQUARE_SIZE, SQUARE_SIZE))
BLUE_WHITE_TILE = pygame.transform.scale(pygame.image.load('images/blueWhiteTile.jpg'), (SQUARE_SIZE, SQUARE_SIZE))

WHITE_PIECE = pygame.transform.scale(pygame.image.load('images/whitePiece.png'), (SQUARE_SIZE - 24, SQUARE_SIZE - 24))
BLUE_PIECE = pygame.transform.scale(pygame.image.load('images/bluePiece.png'), (SQUARE_SIZE - 24, SQUARE_SIZE - 24))

WOOD_BOARD = pygame.transform.scale(pygame.image.load('images/boardFrame.png'), (SQUARE_SIZE*ROWS + 40, SQUARE_SIZE*ROWS + 40))