import pygame
import random
from map import Map
from player import Player
from gameField import GameField
from monster import Monster, WallPassingMonster, PathfindingMonster, DecisionMakingMonster
from bomb import Bomb
from powerUp import PowerUp
from explosion import Explosion

class Game:
   """
    The main game class for managing game interactions, drawing, and game state.

    Attributes:
        screen (pygame.Surface): The display surface for rendering the game.
        tile_size (int): Size of the tiles in pixels.
        screen_width (int): Width of the game screen in pixels.
        screen_height (int): Height of the game screen in pixels.
        clock (pygame.time.Clock): Clock for managing frame rate.
        game_map (Map): The game map containing tiles.
        bombs (pygame.sprite.Group): Group of bomb sprites.
        powerUps (pygame.sprite.Group): Group of power-up sprites.
        explosions (pygame.sprite.Group): Group of explosion sprites.
        explosion_tiles (list): List of explosion effect details.
        players (pygame.sprite.Group): Group of player sprites.
        monsters (pygame.sprite.Group): Group of monster sprites.

    Parameters:
        screen (pygame.Surface): The display surface where the game will be rendered.
        map_number (int): The map number to load for this game session.
        player_mode (int): The mode of the game determining the number of players.
        num_of_rounds (int): Number of rounds to be played.
    """ 
   def __init__(self, screen, map_number, player_mode, num_of_rounds):
        self.screen = screen
        self.tile_size = 40
        self.screen_width = self.tile_size * 13
        self.screen_height = self.tile_size * 11
        self.clock = pygame.time.Clock()

        # Load the map
        if map_number == 1:
            map_filename = 'map1.txt'
        elif map_number == 2:
            map_filename = 'map2.txt'
        else:
            map_filename = 'map3.txt'

        self.game_map = Map(map_filename, self.tile_size)
        self.bombs = pygame.sprite.Group()
        self.powerUps = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.explosion_tiles = []

        # Initialize the game field
        self.game_field = GameField(self.game_map)

        # Player Group - Single for now
        self.players = pygame.sprite.Group()
        self.players.add(Player(1, 0, 0, 2, 2, [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d,pygame.K_RETURN,pygame.K_o])) 
        self.players.add(Player(2, 10, 12, 3, 3, [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT,pygame.K_m,pygame.K_n]))
        if player_mode == 3:
            self.players.add(Player(3, 10, 0, 3, 3, [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l,pygame.K_v,pygame.K_c]))

        self.monsters = pygame.sprite.Group()
        # Adding different types of monsters
        monster_types = [Monster, WallPassingMonster, PathfindingMonster, DecisionMakingMonster]
        for monster_class in monster_types:
            row, col = self.get_random_position(self.game_map)
            monster = monster_class(self.game_field, row, col, 1)  # Speed parameter is set to 1
            self.monsters.add(monster)

   def play(self, end_game_callback):
       """
        Handles the main game loop, processing events, updating game objects, and rendering them on the screen.

        This method continuously processes events such as player input and system signals (e.g., quit events),
        updates the positions and states of all game objects (players, monsters, bombs, etc.), and renders
        the current state of the game to the display. The game loop runs until a stopping condition is met,
        such as a player winning or all monsters being eliminated. Upon termination, it calls the provided
        `end_game_callback` with the winner(s) as its argument.

        Parameters:
            end_game_callback (function): A callback function that is called with the list of winning player IDs
                                        when the game ends, either through all other players being eliminated or all
                                        monsters being killed.

        Note:
            This method is intended to be called once to start the game after all initial setup is completed.
            It manages the game's frame rate, player interactions, and drawing the game state to the screen.
        """
       running = True
       while running:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   running = False
               elif event.type == pygame.KEYDOWN:
                   for player in self.players:
                        if event.key in player.control_keys:
                            player_coords = player.get_coordinates()
                            if event.key == player.control_keys[0]:  # Move up
                                if self.game_field.is_valid_move(player_coords, (-1, 0),player.ghost_mode,self.players):
                                    player.move(-1, 0)
                            elif event.key == player.control_keys[1]:  # Move down
                                if self.game_field.is_valid_move(player_coords, (1, 0),player.ghost_mode,self.players):
                                    player.move(1, 0)
                            elif event.key == player.control_keys[2]:  # Move left
                                if self.game_field.is_valid_move(player_coords, (0, -1),player.ghost_mode,self.players):
                                    player.move(0, -1)
                            elif event.key == player.control_keys[3]:  # Move right
                                if self.game_field.is_valid_move(player_coords, (0, 1),player.ghost_mode,self.players):
                                    player.move(0, 1) 
                            elif event.key == player.control_keys[4]:  # If the Enter key is pressed
                                if player.can_place_bomb():
                                    #bomb = Bomb(game_field, row, col, 1)
                                    bomb = Bomb(player,player.row, player.col, player.blast_range, 3000)
                                    self.bombs.add(bomb)
                                    self.game_map.mark_bomb_tile(bomb.row, bomb.col)
                                    player.placed_bomb(bomb)
                                elif (player.can_place_bomb()==False) and player.has_detonator:
                                    for bomb in player.bomb_list:
                                        bomb.explode(self.game_map,self.monsters,self.bombs,self.explosion_tiles,self.powerUps,self.players)
                                    print('detonator should work')
                                    player.has_detonator = False
                                else:
                                    print("Can't place bomb! Either you run out of bombs or there is a active bomb!")

                            elif event.key == player.control_keys[5]: # place obstacle 
                                placed = player.place_obstacle(self.game_map, player.row, player.col)

           for monster in self.monsters:
               monster.update(self.game_map, self.monsters, self.players)

           for bomb in self.bombs:
                bomb.update(self.game_map,self.monsters,self.bombs,self.explosion_tiles,self.powerUps,self.players)
                
           for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1 and event.monster:
                    event.monster.paused = False  # Unpause the monster

           for effect in self.explosion_tiles:
                current_time = pygame.time.get_ticks()
                row, col , activation_time = effect
                explosion = Explosion(self.game_field,row,col,activation_time)
                self.explosions.add(explosion)
                self.explosion_tiles.remove(effect)
                #explosion.add(self.explosions,explosion_tiles,effect)
                
           if len(self.explosion_tiles)==0:
                for explosion in list(self.explosions):  # Iterate over a copy to safely remove items
                    if explosion.is_expired():
                        self.explosions.remove(explosion)  # Remove the explosion if it has expired

           for player in self.players:
                player.update(self.game_map,self.players)
                for power_up in self.powerUps:
                    if pygame.sprite.collide_rect(player, power_up):
                        print('tema bahalasdi')
                        power_up.apply_effect(player,self.monsters)
                        power_up.kill()  # This removes the power-up from all groups it belongs to

                if player.is_invincible:
                    remaining_time = max(0, player.invincibility_timer - pygame.time.get_ticks())
                    if remaining_time < 1000:  # Less than 1 second remaining
                        # Blink the player sprite or change color to indicate ending
                        if (remaining_time // 200) % 2 == 0:
                            player.image.set_alpha(128)  # Make player semi-transparent
                        else:
                            player.image.set_alpha(255)  # Normal visibility

                if player.ghost_mode:
                    remaining_time = max(0, player.ghost_timer - pygame.time.get_ticks())
                    if remaining_time < 1000:  # Less than 1 second remaining
                        # Blink the player sprite or change color to indicate ending
                        if (remaining_time // 200) % 2 == 0:
                            player.image.set_alpha(128)  # Make player semi-transparent
                        else:
                            player.image.set_alpha(255)  # Normal visibility

            # Check for collisions between players and monsters
           for player in self.players:
                collisions = pygame.sprite.spritecollide(player, self.monsters, False)
                if collisions:
                    if(not player.is_invincible) :
                        print("Player with id ", player.id, " was caught by a monster!")
                        self.players.remove(player)
                        player.kill()
                    else:
                        print("You are invincible!!!")

            # Drawing
           self.screen.fill((0, 0, 0))  # Clear the screen

            # Render the map
           self.game_map.draw(self.screen)

            # Draw the monsters
           self.monsters.draw(self.screen)

            # Draw the player
           self.players.draw(self.screen)

            # draw the bombs

           self.bombs.draw(self.screen)

            # draw the explosions

           self.explosions.draw(self.screen)

            # draw the powerups 

           self.powerUps.draw(self.screen)

            # Update the display
           pygame.display.update()

            # Cap the frame rate
           self.clock.tick(60)

           if len(self.players) == 1:
               winner = self.players.sprites()[0]
               running = False
               end_game_callback([winner.id])

           # Check if all monsters are killed
           if len(self.monsters) == 0:
               print("All players were caught by monsters!")
               winners = [player.id for player in self.players.sprites()]
               running = False
               end_game_callback(winners)

   def get_random_position(self, game_map):
       """
        Generates a random position on the game map that is a floor tile.

        This method randomly selects coordinates within the dimensions of the provided game map,
        continuously retrying until it finds a position that corresponds to a floor tile. This ensures
        that the position is suitable for placing game entities such as monsters or power-ups.

        Parameters:
            game_map (Map): The game map instance which contains tile information and dimensions.

        Returns:
            tuple: A tuple (row, col) representing a valid floor tile position on the map.
        """
       while True:
           row = random.randint(0, game_map.height - 1)
           col = random.randint(0, game_map.width - 1)
           if game_map.isFloor(row, col):  # Checks if the tile is a floor
               return row, col


