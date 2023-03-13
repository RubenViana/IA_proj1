import pygame
from code25.constants import WIDTH, HEIGHT, SQUARE_SIZE, OFFSET, RED, BLACK, WHITE, ROWS, BLUE
from code25.game import Game, State

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Code25')

# Set up the font
FONT = pygame.font.SysFont("Arial", 40, bold=True)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = (y - OFFSET) // SQUARE_SIZE
    col = (x - OFFSET) // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if game.game_state == State.PLAY_STATE:
            if game.winner() != None:
                print(game.winner())
                game.reset()
            if game.turn == game.ai1_color:
                # ai_move(turn, game, ai1_diff)  ->  make an ai move
                game._move_ai()
            elif game.turn == game.ai2_color:
                # ai_move(turn, game, ai2_diff)  ->  make an ai move 
                game._move_ai()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = get_row_col_from_mouse(pos)
                        if row < ROWS and row >= 0 and col < ROWS and col >= 0:
                            game.select(row, col)
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            game.reset()
        elif game.game_state == State.P2COLORSIDE_STATE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.board.rotate_board()
                    elif event.key == pygame.K_s:
                        if game.turn == WHITE:
                            game.set_turn(BLUE)
                        else:
                            game.set_turn(WHITE)
                    elif event.key == pygame.K_SPACE:
                        game.set_turn(game.p1_color)
                        game.game_state = State.PLAY_STATE
                    elif event.key == pygame.K_ESCAPE:
                        game.reset()
        elif game.game_state == State.MENU_STATE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        game.selected_main_menu_item = (game.selected_main_menu_item - 1) % len(game.main_menu_items)
                    elif event.key == pygame.K_DOWN:
                        game.selected_main_menu_item = (game.selected_main_menu_item + 1) % len(game.main_menu_items)
                    elif event.key == pygame.K_RETURN:
                        if game.selected_main_menu_item == 0:
                            game.game_state = State.PLAY_MENU_STATE
                        elif game.selected_main_menu_item == 1:
                            print("Rules")
                        elif game.selected_main_menu_item == 2:
                            run = False
        elif game.game_state == State.PLAY_MENU_STATE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.reset()
                    if event.key == pygame.K_UP:
                        game.selected_player_menu_opts = (game.selected_player_menu_opts - 1) % len(game.player_menu_opts)
                    elif event.key == pygame.K_DOWN:
                        game.selected_player_menu_opts = (game.selected_player_menu_opts + 1) % len(game.player_menu_opts)
                    elif event.key == pygame.K_LEFT:
                        if game.selected_player_menu_opts == 0:
                            game.selected_player1_menu_type = (game.selected_player1_menu_type - 1) % len(game.player_menu_opts[0]["type"])
                        elif game.selected_player_menu_opts == 1 and game.player_menu_opts[0]["type"][game.selected_player1_menu_type] == "Machine":
                            game.selected_player1_menu_diff = (game.selected_player1_menu_diff - 1) % len(game.player_menu_opts[1]["type"])
                        elif game.selected_player_menu_opts == 2:
                            game.selected_player2_menu_type = (game.selected_player2_menu_type - 1) % len(game.player_menu_opts[2]["type"])
                        elif game.selected_player_menu_opts == 3 and game.player_menu_opts[2]["type"][game.selected_player2_menu_type] == "Machine":
                            game.selected_player2_menu_diff = (game.selected_player2_menu_diff - 1) % len(game.player_menu_opts[3]["type"])
                    elif event.key == pygame.K_RIGHT:
                        if game.selected_player_menu_opts == 0:
                            game.selected_player1_menu_type = (game.selected_player1_menu_type + 1) % len(game.player_menu_opts[0]["type"])
                        elif game.selected_player_menu_opts == 1 and game.player_menu_opts[0]["type"][game.selected_player1_menu_type] == "Machine":
                            game.selected_player1_menu_diff = (game.selected_player1_menu_diff + 1) % len(game.player_menu_opts[1]["type"])
                        elif game.selected_player_menu_opts == 2:
                            game.selected_player2_menu_type = (game.selected_player2_menu_type + 1) % len(game.player_menu_opts[2]["type"])
                        elif game.selected_player_menu_opts == 3 and game.player_menu_opts[2]["type"][game.selected_player2_menu_type] == "Machine":
                            game.selected_player2_menu_diff = (game.selected_player2_menu_diff + 1) % len(game.player_menu_opts[3]["type"])
                    elif event.key == pygame.K_RETURN:
                        if game.selected_player_menu_opts == 4:
                            game.game_state = game.set_players()
        game.update()
    
    pygame.quit()

main()