import pygame
from .constants import BLUE_WHITE, WHITE, BLUE, SQUARE_SIZE, GREY, OFFSET, WIDTH, BLACK, ROWS, BTN, BTN_HOVER, BACKGROUND
from code25.board import Board
from enum import Enum

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
            # choose random color to p2(ai2) and rotate board randomly aswell
            self.set_turn(BLUE)
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

    def color_changes(self, piece, row, col):
        piece.row_ = piece.row
        piece.col_ = piece.col
        color_changes = 0
        intermediate_pos = self.get_intermediate_positions((piece.row, piece.col), (row, col))
        self.board.board[ROWS//2][ROWS//2].set_color(self.turn)
        for int_pos in intermediate_pos:
            row_int, col_int = int_pos
            if (piece.color != self.board.board[row_int][col_int].get_color()) or (self.board.board[piece.row_][piece.col_].get_color() != self.board.board[row_int][col_int].get_color()):
                color_changes += 1
                piece.row_ = row_int
                piece.col_ = col_int
        self.board.board[ROWS//2][ROWS//2].set_color(BLUE_WHITE)
        return color_changes
    
    def stop_movement(self, piece, row, col):
        intermediate_pos = self.get_intermediate_positions((piece.row, piece.col), (row, col))

        for int_pos in intermediate_pos:
            row_int, col_int = int_pos
            if (self.board.get_piece(row_int, col_int) != 0 or (row_int == ROWS//2 and col_int == ROWS//2)) and (row_int != row or col_int != col):
                return True

    def get_valid_moves(self, piece):
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
                if self.board.get_piece(row, col) == 0 or (self.board.get_piece(row, col).color != self.turn and self.board.get_piece(row, col).goal == False):
                    if self.color_changes(piece, row, col) < 2 and not(self.stop_movement(piece, row, col)):
                        valid_moves.add(move)
                            
        return valid_moves

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn and piece.goal == False:
            self.selected = piece
            self.valid_moves = self.get_valid_moves(piece)
            return True
            
        return False

    def _move_ai(self):             # implement from here AI monte carlo and minimax
        pygame.time.wait(1000)
        self.change_turn()

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and (row, col) in self.valid_moves and piece != 0 and piece.color != self.turn:
            self.board.remove(piece)
        if self.selected and (row, col) in self.valid_moves:
            self.move(self.selected, row, col)
            self.change_turn()
        else:
            return False

        return True
    
    def move(self, piece, row, col):
        self.board.pieces[piece.row][piece.col], self.board.pieces[row][col] = self.board.pieces[row][col], self.board.pieces[piece.row][piece.col]
        piece.move(row, col)

        if (row == ROWS - 1 and piece.color == WHITE and self.p1_color == WHITE) or (row == 0 and piece.color == WHITE and self.p1_color == BLUE) or (row == 0 and piece.color == BLUE and self.p1_color == WHITE) or (row == ROWS - 1 and piece.color == BLUE and self.p1_color == BLUE):
            piece.make_goal()
            if piece.color == WHITE:
                self.board.white_goal += 1
            else:
                self.board.blue_goal += 1 

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
        
