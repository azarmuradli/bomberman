import pygame, sys
from button import Button
from game import Game

pygame.init()

SCREEN_WIDTH = 13*40
SCREEN_HEIGHT = 11*40

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("./assets/Background.png")

chosen_map = 1
player_mode = 2
chosen_round = 3
current_round = 1

scoreboard = {
    "player1": 0,
    "player2": 0,
    "player3": 0,
}

def get_font(size): # Returns Press-Start-2P in the desired size
    """
    Returns the Press-Start-2P font in the desired size.

    :param size: The size of the font.
    :return: The font object.
    """
    return pygame.font.Font("assets/font.ttf", size)

def reset_scoreboard():
    """
    Resets the scoreboard for all players.
    """
    global scoreboard
    for key in scoreboard.keys():
        scoreboard[key] = 0

def end_game(winners):
    """
    Handles the end game logic, updates scores, and displays the results.

    :param winners: A list of winner player indices.
    """
    global current_round
    global chosen_round

    for winner in winners:
        player_key = f"player{winner}"  
        if player_key in scoreboard:
            scoreboard[player_key] += 1
    
    while True:
        SCREEN.blit(BG, (0, 0))

        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH * 7/8 - 30, SCREEN_HEIGHT * 1/8), 
                            text_input="Settings", font=get_font(20), base_color="Gray", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        if(current_round != chosen_round):
            CONTINUE_BUTTON = Button(image=None, pos=(SCREEN_WIDTH * 1/8 + 30, SCREEN_HEIGHT * 1/8), 
                            text_input="Continue", font=get_font(20), base_color="Gray", hovering_color="Green")
            CONTINUE_BUTTON.changeColor(OPTIONS_MOUSE_POS)
            CONTINUE_BUTTON.update(SCREEN)

        WINNER_TEXT = get_font(20).render("Round "+ str(current_round) +" results ", True, "White")
        WINNER_RECT = WINNER_TEXT.get_rect(center=(SCREEN_WIDTH * 1/2, SCREEN_HEIGHT * 3/8))
        SCREEN.blit(WINNER_TEXT, WINNER_RECT)

        SCORE1_TEXT = get_font(15).render("Player 1: " + str(scoreboard["player1"]) + "p", True, "White")
        SCORE1_RECT = SCORE1_TEXT.get_rect(center=(SCREEN_WIDTH * 2/8, SCREEN_HEIGHT * 6/10))
        SCREEN.blit(SCORE1_TEXT, SCORE1_RECT)

        SCORE2_TEXT = get_font(15).render("Player 2: " + str(scoreboard["player2"]) + "p", True, "White")
        SCORE2_RECT = SCORE2_TEXT.get_rect(center=(SCREEN_WIDTH * 2/8, SCREEN_HEIGHT * 7/10))
        SCREEN.blit(SCORE2_TEXT, SCORE2_RECT)

        if(player_mode == 3):
            SCORE3_TEXT = get_font(15).render("Player 3: " + str(scoreboard["player3"]) + "p", True, "White")
            SCORE3_RECT = SCORE3_TEXT.get_rect(center=(SCREEN_WIDTH * 2/8, SCREEN_HEIGHT * 8/10))
            SCREEN.blit(SCORE3_TEXT, SCORE3_RECT)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    current_round = 1
                    reset_scoreboard()
                    main_menu()
                if current_round != chosen_round :
                    if CONTINUE_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                        current_round = current_round + 1
                        game = Game(SCREEN, chosen_map, player_mode, chosen_round)
                        game.play(end_game)

        pygame.display.update()

def play():
    """
    Starts the game after choosing the number of rounds.
    """
    choose_rounds()
    game = Game(SCREEN, chosen_map, player_mode, chosen_round)
    game.play(end_game)
    current_round = current_round + 1

def choose_rounds():
    """
    Displays the screen for choosing the number of rounds.
    """
    global chosen_round
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BG, (0, 0))

        OPTIONS_TEXT = get_font(20).render("CHOOSE ROUNDS: ", True, "White")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH * 2/7 + 30, SCREEN_HEIGHT * 1/6))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        MAP1_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/6), 
                            text_input="3", font=get_font(20), base_color="White", hovering_color="GREEN")
        MAP2_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/6), 
                            text_input="5", font=get_font(20), base_color="White", hovering_color="GREEN")
        MAP3_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 4/6), 
                            text_input="7", font=get_font(20), base_color="White", hovering_color="GREEN")
        
        for button in [MAP1_BUTTON, MAP2_BUTTON, MAP3_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAP1_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    chosen_round = 3
                    return
                if MAP2_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    chosen_round = 5
                    return
                if MAP3_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    chosen_round = 7
                    return

        pygame.display.update()
    
def choose_map():
    """
    Displays the screen for choosing the map.
    """
    global chosen_map
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("GREY")

        OPTIONS_TEXT = get_font(20).render("CHOOSE MAP: ", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH * 1/4, SCREEN_HEIGHT * 1/6))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH * 7/8, SCREEN_HEIGHT * 1/6), 
                            text_input="BACK", font=get_font(20), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        MAP1_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/6), 
                            text_input="MAP 1", font=get_font(20), base_color="BLACK", hovering_color="GREEN")
        MAP2_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/6), 
                            text_input="MAP 2", font=get_font(20), base_color="BLACK", hovering_color="GREEN")
        MAP3_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 4/6), 
                            text_input="MAP 3", font=get_font(20), base_color="BLACK", hovering_color="GREEN")
        
        for button in [MAP1_BUTTON, MAP2_BUTTON, MAP3_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if MAP1_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    chosen_map = 1
                    main_menu()
                if MAP2_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    chosen_map = 2
                    main_menu()
                if MAP3_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    chosen_map = 3
                    main_menu()

        pygame.display.update()

def choose_player_number():
    """
    Displays the screen for choosing the number of players.
    """
    global player_mode
    while True:
        PLAYERS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("GREY")

        OPTIONS_TEXT = get_font(20).render("PLAYER NUMBER: ", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH * 1/3, SCREEN_HEIGHT * 1/6))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH * 7/8, SCREEN_HEIGHT * 1/6), 
                            text_input="BACK", font=get_font(20), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(PLAYERS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        SINGLEPLAYER_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/6), 
                            text_input="2-PLAYER", font=get_font(20), base_color="BLACK", hovering_color="GREEN")
        MULTIPLAYER_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/6), 
                            text_input="3-PLAYER", font=get_font(20), base_color="BLACK", hovering_color="GREEN")
        
        for button in [SINGLEPLAYER_BUTTON, MULTIPLAYER_BUTTON]:
            button.changeColor(PLAYERS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(PLAYERS_MOUSE_POS):
                    main_menu()
                if SINGLEPLAYER_BUTTON.checkForInput(PLAYERS_MOUSE_POS):
                    player_mode = 2
                    main_menu()
                if MULTIPLAYER_BUTTON.checkForInput(PLAYERS_MOUSE_POS):
                    player_mode = 3
                    main_menu()

        pygame.display.update()

def main_menu():
    """
    Displays the main menu of the game, with options to Play, Choose Map, Choose Players, or Quit the game.
    Handles user interactions with the menu buttons.
    """
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 1/6))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 2/6), 
                            text_input="PLAY", font=get_font(20), base_color="White", hovering_color="#d7fcd4")
        MAP_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 3/6), 
                            text_input="CHOOSE MAP", font=get_font(20), base_color="White", hovering_color="#d7fcd4")
        PLAYER_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 4/6), 
                            text_input="PLAYERS", font=get_font(20), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Options Rect1.png"), pos=(SCREEN_WIDTH/2, SCREEN_HEIGHT * 5/6), 
                            text_input="QUIT", font=get_font(20), base_color="White", hovering_color="#d7fcd4")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, MAP_BUTTON, PLAYER_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if MAP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choose_map()
                if PLAYER_BUTTON.checkForInput(MENU_MOUSE_POS):
                    choose_player_number()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()