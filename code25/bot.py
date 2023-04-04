from copy import deepcopy
import pygame
import random
import math
from .constants import SQUARE_SIZE, OFFSET, GREY

DELAY = 0

def minimax(position, depth, max_player, color1, color2, game, alpha=float('-inf'), beta=float('inf')):     #position -> board_state
    if depth == 0 or position.winner() != None:
        return position.h2(color1), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_board_moves(position, color1, game):
            evaluation = minimax(move, depth-1, False, color1, color2, game, alpha, beta)[0]
            maxEval = max(maxEval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha: break
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_board_moves(position, color2, game):
            evaluation = minimax(move, depth-1, True, color1, color2, game, alpha, beta)[0]
            minEval = min(minEval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha: break
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move


def simulate_move(piece, move, board, rp):
    if rp != None:
        board.remove(rp)
    board.move(piece, move[0], move[1])
    return board


def get_all_board_moves(board, color, game=None):
    board_moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece, color)
        for move in valid_moves:
            #draw_valid_moves(game, board, piece)
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



def randomPlay(board, color, game):
    board_states = get_all_board_moves(board, color, game)
    random_move = random.choice(board_states)
    return random_move


# Monte Carlo

class Node:
    def __init__(self, state, turn, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0
        self.turn = turn

    def add_child(self, child_state, turn):
        child = Node(child_state, turn, parent=self)
        self.children.append(child)
        return child

    def update(self, score):
        self.visits += 1
        self.score += score

    def fully_expanded(self):
        return len(self.children) == len(get_all_board_moves(self.state, self.turn))

    def best_child(self, c=1.4):
        choices_weights = [(c.score / c.visits) + (c.visits**0.5) * math.sqrt(math.log(self.visits) / c.visits) for c in self.children]
        return self.children[choices_weights.index(max(choices_weights))]

class MCTS:
    def __init__(self, board, color1, color2, time_budget=1000):
        self.time_budget = time_budget
        self.color1 = color1
        self.color2 = color2
        self.board = board

    def search(self):
        root = Node(self.board, self.color1)

        for i in range(self.time_budget):
            node = root

            while not node.state.winner() != None and node.fully_expanded():
                node = node.best_child()

            if not node.state.winner() != None:
                node = node.add_child(random.choice(get_all_board_moves(node.state, self.color1)), self.color1)

            score = self.simulate(node.state)
            while node is not None:
                node.update(score)
                node = node.parent

        return root.best_child(c=0)

    def simulate(self, state):

        while not state.winner() != None:
            move = random.choice(get_all_board_moves(state, self.color1))
            state = move

        if state.winner() == self.color1:
            return 1
        elif state.winner() == self.color2:
            return 0
        else:
            return 0.5
        
def monteCarlo(board, color1, color2):
    mc = MCTS(board, color1, color2, 20)
    return mc.search().state