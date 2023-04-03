import pygame
from code25.constants import WIDTH, HEIGHT, SQUARE_SIZE, OFFSET, RED, BLACK, WHITE, ROWS, BLUE
from code25.game import Game, State
from code25.bot import minimax, randomPlay, main1

pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Code25')


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
            pos = None
            if game.winner() != None:
                print(game.winner())
                game.reset()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.reset()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
            if game.turn == game.ai1_color:
                # pygame.time.wait(1000)
                if game.ai1_diff == 0:
                    new_board = main1(game.board, game, game.p1_color, game.p2_color)  #easy mode
                elif game.ai1_diff == 1:
                    eval, new_board = minimax(game.board, 2, True, game.p1_color, game.p2_color, game)  #medium mode
                elif game.ai1_diff == 2:
                    eval, new_board = minimax(game.board, 4, True, game.p1_color, game.p2_color, game)  #hard mode -> use monte carlo
                #print(f"eval : {eval} | dist : {1/eval}")
                game._move_ai(new_board)
            elif game.turn == game.ai2_color:
                # pygame.time.wait(1000)
                if game.ai2_diff == 0:
                    new_board = main1(game.board, game, game.p2_color, game.p2_color) #easy mode
                elif game.ai2_diff == 1:
                    eval, new_board = minimax(game.board, 2, True, game.p2_color, game.p1_color, game)  #medium mode
                elif game.ai2_diff == 2:
                    eval, new_board = minimax(game.board, 4, True, game.p2_color, game.p1_color, game)  #hard mode
                #print(f"eval : {eval} | dist : {1/eval}")
                game._move_ai(new_board)
            else:
                if pos != None:
                    row, col = get_row_col_from_mouse(pos)
                    if row < ROWS and row >= 0 and col < ROWS and col >= 0:
                        game.select(row, col)
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
                            game.game_state = State.SETTINGS_MENU_STATE
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
                        elif game.selected_player_menu_opts == 1:
                            game.selected_player2_menu_type = (game.selected_player2_menu_type - 1) % len(game.player_menu_opts[1]["type"])
                    elif event.key == pygame.K_RIGHT:
                        if game.selected_player_menu_opts == 0:
                            game.selected_player1_menu_type = (game.selected_player1_menu_type + 1) % len(game.player_menu_opts[0]["type"])
                        elif game.selected_player_menu_opts == 1:
                            game.selected_player2_menu_type = (game.selected_player2_menu_type + 1) % len(game.player_menu_opts[1]["type"])
                    elif event.key == pygame.K_RETURN:
                        if game.selected_player_menu_opts == 2:
                            game.game_state = game.set_players()
        elif game.game_state == State.SETTINGS_MENU_STATE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.reset()
        game.update()
    
    pygame.quit()

main()