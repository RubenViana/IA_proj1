from copy import deepcopy
import pygame
from .constants import SQUARE_SIZE, OFFSET, GREY

DELAY = 0

def minimax(position, depth, max_player, color1, color2, game):     #position -> board_state
    if depth == 0 or position.winner() != None:
        return position.h1(color1), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_board_moves(position, color1, game):
            evaluation = minimax(move, depth-1, False, color1, color2, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_board_moves(position, color2, game):
            evaluation = minimax(move, depth-1, True, color1, color2, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, rp):
    if rp != None:
        board.remove(rp)
    board.move(piece, move[0], move[1])
    return board


def get_all_board_moves(board, color, game):
    board_moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece, color)
        for move in valid_moves:
            draw_valid_moves(game, board, piece)
            rp = None
            tmp_board = deepcopy(board)
            tmp_piece = tmp_board.get_piece(piece.row, piece.col)
            tmp_rp = tmp_board.get_piece(move[0], move[1])
            if tmp_rp != 0 and tmp_rp.color != tmp_piece.color:
                rp = tmp_rp
            new_board = simulate_move(tmp_piece, move, tmp_board, rp)
            board_moves.append(new_board)
    
    return board_moves

#draw to ilustrate bot moves
def draw_valid_moves(game, board, piece):
    moves = board.get_valid_moves(piece, piece.color)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), SQUARE_SIZE//2 - 5, 5)
    game.draw_valid_moves(moves)
    pygame.display.update()
    pygame.time.wait(DELAY)