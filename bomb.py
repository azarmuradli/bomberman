import pygame
from explosion import Explosion
from pygame.sprite import Sprite

class Bomb(Sprite):
    def __init__(self, player, row, col, blast_range, explode_time):
        """
        Initialize the Bomb object.

        :param player: The player who placed the bomb.
        :param row: The row position of the bomb on the grid.
        :param col: The column position of the bomb on the grid.
        :param blast_range: The range of the bomb's explosion.
        :param explode_time: The time in milliseconds until the bomb explodes.
        """
        super().__init__()
        self.player = player
        self.image = pygame.image.load("images/bomb_image.png")
        self.rect = self.image.get_rect(topleft=(col * 40, row * 40))  # Modify the size accordingly
        self.clock = pygame.time.Clock()
        self.explodeTime = pygame.time.get_ticks() + explode_time
        self.blast_range = blast_range
        self.is_exploding = False
        self.row = row
        self.col = col
        self.explosion_tiles = []


    def update(self,gameMap,monsters,bombs,explosion_tiles,power_ups,players):
        """
        Update the state of the bomb.

        :param gameMap: The game map containing the layout of the game.
        :param monsters: A list of monsters in the game.
        :param bombs: A list of active bombs in the game.
        :param explosion_tiles: A list of tiles affected by explosions.
        :param power_ups: A list of power-ups available in the game.
        :param players: A list of players in the game.
        """
        if(self.player.has_detonator) :
            pass
            
        else :
            current_time = pygame.time.get_ticks()
            if current_time >= self.explodeTime:
                self.explode(gameMap,monsters,bombs,explosion_tiles,power_ups,players)

        

    def isValidRange(self,x,y):
        """
        Check if the given coordinates are within valid range.

        :param x: The x-coordinate (column).
        :param y: The y-coordinate (row).
        :return: True if the coordinates are within valid range, False otherwise.
        """
        return x>=0 and x<=10 and y>=0 and y<=12

    def activate_bomb(self):
        """
        Activate the bomb, starting its countdown or adding it to the game.
        """
        pass

    def explode(self, game_map, monsters, bombs,explosion_tiles,power_ups,players):
        """
        Handle the bomb explosion logic.

        :param game_map: The game map containing the layout of the game.
        :param monsters: A list of monsters in the game.
        :param bombs: A list of active bombs in the game.
        :param explosion_tiles: A list of tiles affected by explosions.
        :param power_ups: A list of power-ups available in the game.
        :param players: A list of players in the game.
        """
        explosion_delay = 500  # Delay for distance 2 explosions in milliseconds
        self.is_exploding = True

        # Immediate effect on the bomb's tile
        self.check_and_affect_tile(game_map, monsters, bombs, self.row, self.col,explosion_tiles,power_ups,players)
        explosion_tiles.append((self.row,self.col,4500))
        # Explode in each direction up to 2 tiles away
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        for drow, dcol in directions:
            for distance in range(1, self.blast_range+1):  # Up to 2 tiles away
                affected_row, affected_col = self.row + drow * distance, self.col + dcol * distance
                if not self.isValidRange(affected_row, affected_col) or game_map.isWall(affected_row, affected_col):
                    break  # Stop if out of bounds or a wall is encountered
                if game_map.isBrick(affected_row, affected_col):
                    game_map.destroy_brick(affected_row, affected_col,power_ups,self.player)
                    break  # Stop if a brick is encountered and destroyed
                
                self.check_and_affect_tile(game_map, monsters, bombs, affected_row, affected_col,explosion_tiles,power_ups,players)
                explosion_tiles.append((affected_row,affected_col,4500+explosion_delay*distance))

        game_map.unmark_bomb_tile(self.row, self.col)
        self.player.bomb_exploded(self)
        self.kill()

    def check_and_affect_tile(self, game_map, monsters, bombs, row, col,explosion_tiles,power_ups,players):
        """
        Check and affect the specified tile during an explosion.

        :param game_map: The game map containing the layout of the game.
        :param monsters: A list of monsters in the game.
        :param bombs: A list of active bombs in the game.
        :param row: The row position of the tile.
        :param col: The column position of the tile.
        :param explosion_tiles: A list of tiles affected by explosions.
        :param power_ups: A list of power-ups available in the game.
        :param players: A list of players in the game.
        """
        # Check for other bombs and trigger their explosion
        for bomb in bombs:
            if bomb.row == row and bomb.col == col and not bomb.is_exploding:
                bomb.explode(game_map,monsters,bombs,explosion_tiles,power_ups,players)

        # Check for player in the affected tile
        for player in players:
            if player.row == row and player.col == col and not player.is_invincible:
                #print("Player with id ", player.id, " died in bomb explosion!")
                self.player.kill()
                players.remove(player)

        # Check for monsters in the affected tile
        for monster in monsters:
            if monster.row == row and monster.col == col:
                monster.image = pygame.image.load("images/explosion_image.png")
                monster.kill()
        
        
        

    def draw(self, screen):
        """
        Draw the bomb on the given screen.

        :param screen: The screen surface to draw the bomb on.
        """
        screen.blit(self.image, self.rect)