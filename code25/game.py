import pygame
from .constants import BLUE_WHITE, WHITE, BLUE, SQUARE_SIZE, GREY, OFFSET, WIDTH, BLACK, ROWS, BTN, BTN_HOVER, BACKGROUND
from code25.board import Board
from enum import Enum
import random

class State(Enum):
    MENU_STATE = 0
    PLAY_STATE = 1
    P2COLORSIDE_STATE = 2
    PLAY_MENU_STATE = 3


class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.font = pygame.font.SysFont("arial", 35, bold=True)
        self.font_mm = pygame.font.SysFont("arial", 40, bold=True)
        self.font_opt = pygame.font.SysFont("arial", 30, bold=False)
        self.btn_font = pygame.font.SysFont("arial", 20, bold=True)
        self.main_menu_items = [
                {"text": "Play", "position": (WIDTH // 2, 400)},
                {"text": "Rules", "position": (WIDTH // 2, 500)},
                {"text": "Quit", "position": (WIDTH // 2, 600)}
            ]
        self.player_menu_opts = [
                {"text": "Player1", "type": ["Human", "Machine"], "pos1": (WIDTH // 3 + 20, 280), "pos2": (WIDTH*2 // 3 - 20, 280)},
                {"text": "Difficulty1", "type": ["Easy", "Medium", "Hard"], "pos1": (WIDTH // 3 + 20, 350), "pos2": (WIDTH*2 // 3 - 20, 350)},
                {"text": "Player2", "type": ["Human", "Machine"], "pos1": (WIDTH // 3 + 20, 480), "pos2": (WIDTH*2 // 3 - 20, 480)},
                {"text": "Difficulty2", "type": ["Easy", "Medium", "Hard"], "pos1": (WIDTH // 3 + 20, 550), "pos2": (WIDTH*2 // 3 - 20, 550)},
                {"text": "START", "pos1": (WIDTH // 2, 670)}
            ]
    
    def update(self):
        if self.game_state == State.PLAY_MENU_STATE:
            self.win.fill(BACKGROUND)
            esc_text = self.btn_font.render("[ESC] Back", True, BTN)
            self.win.blit(esc_text, (10, 10))

            for i, item in enumerate(self.player_menu_opts):
                if i == self.selected_player_menu_opts:
                    if i == 4:
                        text = self.font.render(item["text"], True, BTN_HOVER)
                    else:
                        text = self.font.render(item["text"], True, BTN_HOVER)
                        texto = self.font.render("<", True, BTN_HOVER)
                        texto_rect = texto.get_rect()
                        texto_rect.center = (item["pos2"][0] - 70, item["pos2"][1])
                        self.win.blit(texto, texto_rect)
                        texto = self.font.render(">", True, BTN_HOVER)
                        texto_rect = texto.get_rect()
                        texto_rect.center = (item["pos2"][0] + 70, item["pos2"][1])
                        self.win.blit(texto, texto_rect)
                else:
                    text = self.font.render(item["text"], True, BTN)
                text_rect = text.get_rect()
                text_rect.center = item["pos1"]
                self.win.blit(text, text_rect)

                if item["text"] == "Player1":
                    texto = self.font_opt.render(item["type"][self.selected_player1_menu_type], True, BTN)
                    texto_rect = texto.get_rect()
                    texto_rect.center = item["pos2"]
                    self.win.blit(texto, texto_rect)
                elif item["text"] == "Difficulty1" and self.selected_player1_menu_type == 1:
                    texto = self.font_opt.render(item["type"][self.selected_player1_menu_diff], True, BTN)
                    texto_rect = texto.get_rect()
                    texto_rect.center = item["pos2"]
                    self.win.blit(texto, texto_rect)
                elif item["text"] == "Player2":
                    texto = self.font_opt.render(item["type"][self.selected_player2_menu_type], True, BTN)
                    texto_rect = texto.get_rect()
                    texto_rect.center = item["pos2"]
                    self.win.blit(texto, texto_rect)
                elif item["text"] == "Difficulty2" and self.selected_player2_menu_type == 1:
                    texto = self.font_opt.render(item["type"][self.selected_player2_menu_diff], True, BTN)
                    texto_rect = texto.get_rect()
                    texto_rect.center = item["pos2"]
                    self.win.blit(texto, texto_rect)

        if self.game_state == State.MENU_STATE:
            # Draw the background
            self.win.fill(BACKGROUND)

            # Draw the menu items
            for i, item in enumerate(self.main_menu_items):
                if i == self.selected_main_menu_item:
                    text = self.font_mm.render(item["text"], True, BTN_HOVER)
                else:
                    text = self.font_mm.render(item["text"], True, BTN)
                text_rect = text.get_rect()
                text_rect.center = item["position"]
                self.win.blit(text, text_rect)
            
        if self.game_state == State.PLAY_STATE or self.game_state == State.P2COLORSIDE_STATE:
            self.win.fill(BACKGROUND)
            self.board.draw(self.win)
            self.draw_valid_moves(self.valid_moves)

            esc_text = self.btn_font.render("[ESC] Back", True, BTN)
            self.win.blit(esc_text, (10, 10))

            p1_text = self.font.render("PLAYER 1", True, BLACK)
            p1_text_rect = p1_text.get_rect()
            p1_text_rect.center = (OFFSET + (ROWS*SQUARE_SIZE) // 2, OFFSET - 50)
            self.win.blit(p1_text, p1_text_rect)
            p2_text = self.font.render("PLAYER 2", True, BLACK)
            p2_text_rect = p2_text.get_rect()
            p2_text_rect.center = (OFFSET + (ROWS*SQUARE_SIZE) // 2, OFFSET + (ROWS*SQUARE_SIZE) + 50)
            self.win.blit(p2_text, p2_text_rect)
        
        if self.game_state == State.PLAY_STATE:
            if self.turn == self.p1_color:
                pygame.draw.polygon(self.win, (255,215,0), ((110, 80),(125, 95),(110, 110)))
            elif self.turn == self.p2_color:
                pygame.draw.polygon(self.win, (255,215,0), ((110, 680),(125, 695),(110, 710)))

        if self.game_state == State.P2COLORSIDE_STATE:
            rotate_text = self.btn_font.render("[R] Rotate", True, BTN)
            self.win.blit(rotate_text, (OFFSET + ROWS*SQUARE_SIZE // 2 - 240, OFFSET + (ROWS*SQUARE_SIZE) + 90))
            s_select_text = self.btn_font.render("[S] Switch Color", True, BTN)
            self.win.blit(s_select_text, (OFFSET + ROWS*SQUARE_SIZE // 2 - 115, OFFSET + (ROWS*SQUARE_SIZE) + 90))
            sp_select_text = self.btn_font.render("[Space] Start Game", True, BTN)
            self.win.blit(sp_select_text, (OFFSET + ROWS*SQUARE_SIZE // 2 + 60, OFFSET + (ROWS*SQUARE_SIZE) + 90))


        pygame.display.update()

    def _init(self):
        self.game_state = State.MENU_STATE
        self.board = Board()
        self.selected = None
        self.turn = WHITE
        self.p1_color = WHITE
        self.p2_color = BLUE
        self.ai1_color = None
        self.ai2_color = None
        self.ai1_diff = None
        self.ai2_diff = None
        self.board.set_pieces(WHITE, BLUE)
        self.valid_moves = set()
        self.selected_main_menu_item = 0
        self.selected_player_menu_opts = 0
        self.selected_player1_menu_type = 0
        self.selected_player1_menu_diff = 0
        self.selected_player2_menu_type = 0
        self.selected_player2_menu_diff = 0

    def set_turn(self, color):
        self.p1_color = color
        if color == WHITE:
            self.p2_color = BLUE
        else:
            self.p2_color = WHITE

        if self.ai2_diff != None:
            self.ai2_color = self.p2_color
        if self.ai1_diff != None:
            self.ai1_color = self.p1_color

        self.board.set_pieces(self.p1_color, self.p2_color)

        self.turn = self.p1_color

    def set_players(self):
        if self.selected_player1_menu_type != 0:
            self.ai1_diff = self.selected_player1_menu_diff
        if self.selected_player2_menu_type != 0:
            self.ai2_diff = self.selected_player2_menu_diff
            n_rotations = random.randrange(0,4)
            n_side = random.randrange(0,1)
            for r in range(n_rotations):
                self.board.rotate_board()
            if n_side == 0:
                self.set_turn(BLUE)
            elif n_side == 1:
                self.set_turn(WHITE)
            return State.PLAY_STATE
        return State.P2COLORSIDE_STATE

    def winner(self):
        if self.board.winner() != None:
            if self.board.winner() == self.p1_color:
                winner = "PLAYER 1"
            else:
                winner = "PLAYER 2"
            pygame.draw.rect(self.win, (10, 10, 10), (50, OFFSET, WIDTH - 100, 100), 0)
            text = self.font_mm.render(f"{winner} WON", True, BTN_HOVER)
            text_rect = text.get_rect()
            text_rect.center = (50 + (WIDTH-100) // 2, OFFSET + 50)
            self.win.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(2000)
            return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn and piece.goal == False:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, self.turn)
            return True
            
        return False

    def _move_ai(self, new_board):             # implement from here AI monte carlo and minimax
        self.board = new_board
        self.change_turn()

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves and piece != 0 and piece.color != self.turn:
            self.board.remove(piece)
        if self.selected and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False

        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, GREY, (col * SQUARE_SIZE + SQUARE_SIZE//2 + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE//2 + OFFSET), SQUARE_SIZE//8)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = WHITE
        else:
            self.turn = BLUE
        
