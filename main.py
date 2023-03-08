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

def draw_menu(selected_item, menu_items):
        # Draw the background
        WIN.fill((215, 171, 170))

        # Draw the menu items
        for i, item in enumerate(menu_items):
            if i == selected_item:
                text = FONT.render(item["text"], True, (255,215,0))
            else:
                text = FONT.render(item["text"], True, BLACK)
            text_rect = text.get_rect()
            text_rect.center = item["position"]
            WIN.blit(text, text_rect)

        # Update the screen
        pygame.display.update()

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    selected_item = 0
    menu_items = [
            {"text": "Play", "position": (WIDTH // 2, 400)},
            {"text": "Rules", "position": (WIDTH // 2, 500)},
            {"text": "Quit", "position": (WIDTH // 2, 600)}
        ]
    
    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            game.game_state = State.MENU_STATE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_state == State.PLAY_STATE:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if row < ROWS and row >= 0 and col < ROWS and col >= 0:
                    game.select(row, col)
            elif event.type == pygame.KEYDOWN and game.game_state == State.PLAY_STATE:
                if event.key == pygame.K_ESCAPE:
                    game.reset()
            elif event.type == pygame.KEYDOWN and game.game_state == State.P2COLORSIDE_STATE:
                if event.key == pygame.K_r:
                    game.board.rotate_board()
                elif event.key == pygame.K_s:
                    if game.turn == WHITE:
                        game.set_turn(BLUE)
                    else:
                        game.set_turn(WHITE)
                elif event.key == pygame.K_SPACE:
                    game.game_state = State.PLAY_STATE
                elif event.key == pygame.K_ESCAPE:
                    game.reset()
            elif event.type == pygame.KEYDOWN and game.game_state == State.MENU_STATE:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        game.game_state = State.P2COLORSIDE_STATE
                    elif selected_item == 1:
                        print("Rules")
                    elif selected_item == 2:
                        run = False
                
        if game.game_state == State.MENU_STATE:
            draw_menu(selected_item, menu_items)
        elif game.game_state == State.PLAY_STATE or game.game_state == State.P2COLORSIDE_STATE:
            game.update()
    
    pygame.quit()

main()