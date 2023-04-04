from copy import deepcopy
from collections import defaultdict
import pygame
import random
import numpy as np
from .constants import SQUARE_SIZE, OFFSET, GREY, BLUE, WHITE

DELAY = 0

# def monte_carlo(self, game, position, color1, color2): 
#          """Play a move using Monte Carlo Tree Search.""" 
#          root = TreeNode(position, game, None, None, color1, color2) 
#          return root.best_move() 
      
# class TreeNode: 
#     def _init_(self, position, game, move, parent, color1, color2): 
#         self.game = game
#         self.position = position
#         self.move = move 
#         self.parent = parent 
#         self.children = [] 
#         self.visits = 0 
#         self.color1 = color1
#         self.color2 = color2
#         self._results = defaultdict(int) 
#         self._results[BLUE] = 0 
#         self._results[WHITE] = 0 
#         self.untried_moves = self.untried_moves() 
     
#     def untried_moves(self): 
#         self._untried_moves = get_all_board_moves(self.position, self.color1, self.game)
#         return self._untried_moves 
     
#     def q(self): 
#         """Return the action value (quality) of the node.""" 
#         wins = self._results[self.color1] 
#         loses = self._results[self.color2] 
#         return wins - loses 
     
#     def n(self): 
#         """Return the number of visits of the node.""" 
#         return self.visits 

      
#     def expand(self): 
#         """Expand the tree by adding a child node for each untried move.""" 
#         move = random(self.untried_moves) 
#         copy_game = copy.deepcopy(self.game) 
#         copy_game.move(move[0], move[1]) 
#         child = TreeNode(self.position, copy_game, move, self, self.color1, self.color2) 
#         self.children.append(child) 
#         self.untried_moves.remove(move) 
#         return child 
      
#     def is_terminal(self): 
#         """Return True if the node is a terminal node.""" 
#         return self.position.winner()
      
#     def rollout(self): 
#         """Perform a random rollout from the current node.""" 
#         copy_game = copy.deepcopy(self.game) 
#         while not copy_game.over: 
#             copy_game.move(*random(copy_game.board.get_moves(copy_game.player))) 
#         return copy_game.winner 
  
#     def backpropagate(self, winner): 
#         self.visits += 1 
#         self._results[winner] += 1 
#         if self.parent: 
#             self.parent.backpropagate(winner) 
              
#     def is_full_expanded(self): 
#         """Return True if the node has been fully expanded.""" 
#         return len(self.untried_moves) == 0 
     
#     def best_child(self, c_param): 
#         """Return the child with the highest UCB score.""" 
#         choices_weights = [(c.q() / (c.n())) + c_param * np.sqrt(np.log(self.n()) / (c.n())) for c in self.children] 
#         return self.children[np.argmax(choices_weights)] 
      
#     def _tree_policy(self): 
#         """Return the best child using UCB1.""" 
#         current = self 
#         while not current.is_terminal(): 
#             if not current.is_full_expanded(): 
#                 return current.expand() 
#             else: 
#                 current = current.best_child(self.bot.bot_settings.montecarlo_exploration) 
#         return current 
      
#     def _tree_to_string(self, indent): 
#         s = self.indent_string(indent) + str(self.move) + " " + str(self.q()) + " " + str(self.n()) 
#         for c in self.children: 
#             s += c._tree_to_string(indent+1) 
#         return s 
     
#     def indent_string(self, indent): 
#         s = "\n" 
#         for i in range(1, indent+1): 
#             s += "| " 
#         return s 
     
#     def best_move(self): 
#         """Return the best move""" 
#         simulation_no = self.bot.bot_settings.montecarlo_simulations 
         
#         for i in range(simulation_no): 
#             leaf = self._tree_policy() 
#             winner = leaf.rollout() 
#             leaf.backpropagate(winner) 
#             return self.best_child(self.bot.bot_settings.montecarlo_exploration).move

class MonteCarloTreeSearchNode():
    def __init__(self, position, game, color1, color2, parent=None, parent_action=None):
        self.position = position
        self.game = game
        self.color1 = color1
        self.color2 = color2
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0.1
        self._results[-1] = 0.1
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return
    
    def untried_actions(self):
        self._untried_actions = get_all_board_moves(self.position, self.color1, self.game)
        return self._untried_actions    

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
    
        action = self._untried_actions.pop()
        next_state = action
        child_node = MonteCarloTreeSearchNode(next_state, self.game, self.color1, self.color2, self, action)

        self.children.append(child_node)
        return child_node 

    def is_terminal_node(self):
        return self.position.winner()

    def rollout(self):
        current_rollout_state = self.position
        while not current_rollout_state.winner():    

            possible_moves = get_all_board_moves(current_rollout_state, self.color1, self.game)
            current_rollout_state = self.rollout_policy(possible_moves)

        if current_rollout_state.winner() == self.color1:
            return 1
        elif current_rollout_state.winner() == self.color2:
            return -1
        else:
            return 0    

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=0.1):

        choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):

        return random.choice(possible_moves)

    def _tree_policy(self):

        current_node = self
        while not current_node.is_terminal_node():

            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100
    
    
        for i in range(simulation_no):
        
            v = self._tree_policy()
            reward = v.rollout()
            self.backpropagate(reward)
    
        return self.best_child(c_param=0.)

def main1(position, game, color1, color2):
    root = MonteCarloTreeSearchNode(position, game, color1, color2)
    selected_node = root.best_action()
    return selected_node





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


def get_all_board_moves(board, color, game):
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

