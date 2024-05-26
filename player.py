


import pygame
from pygame.sprite import Sprite
from brick import Obstacle

class Player(Sprite):

    """
    Represents a player in the game.

    Attributes:
        id (int): The player's ID.
        row (int): The current row position of the player.
        col (int): The current column position of the player.
        bombs_limit (int): The maximum number of bombs the player can place.
        active_bombs (int): The current number of active bombs placed by the player.
        bomb_list (list): List of bombs placed by the player.
        blast_range (int): The blast range of the bombs placed by the player.
        control_keys (list): List of control keys for the player.
        has_detonator (bool): Whether the player has a detonator.
        ghost_mode (bool): Whether the player is in ghost mode.
        ghost_timer (int): The timer for ghost mode duration.
        ghost_duration (int): The duration of the ghost mode in milliseconds.
        is_invincible (bool): Whether the player is invincible.
        invincibility_timer (int): The timer for invincibility duration.
        invincibility_duration (int): The duration of the invincibility in milliseconds.
        obstacles_limit (int): The maximum number of obstacles the player can place.
        active_obstacles (int): The current number of active obstacles placed by the player.
        alive (bool): Whether the player is alive.
    """

    def __init__(self, id, row, col, bombs, blast_range, control_keys):

        """
        Initializes the Player with the given parameters.

        Args:
            id (int): The player's ID.
            row (int): The initial row position.
            col (int): The initial column position.
            bombs (int): The initial bomb limit.
            blast_range (int): The initial blast range.
            control_keys (list): The control keys for the player.
        """

        super().__init__()
        self.image = pygame.image.load("images/player_image.png")
        self.rect = self.image.get_rect(topleft=(col * 40, row * 40))  # Assuming each tile is 32x32 pixels
        self.id = id
        self.row = row
        self.col = col
        self.bombs_limit = bombs  # Maximum number of active bombs
        self.active_bombs = 0  # Currently active bombs
        self.bomb_list = []
        self.blast_range = blast_range
        self.control_keys =  control_keys
        self.has_detonator = False
        self.ghost_mode = False
        self.ghost_timer = 0
        self.ghost_duration = 5000  # 5000 milliseconds (5 seconds)
        self.is_invincible = False
        self.invincibility_timer = 0
        self.invincibility_duration = 5000  # 5000 milliseconds (5 seconds)
        self.obstacles_limit = 0  # Start with a capacity to place 0 obstacles
        self.active_obstacles = 0  # List to track placed obstacles
        self.alive = True

    def place_obstacle(self, map, x, y):

        """
        Places an obstacle at the given position if within the obstacle limit.

        Args:
            map (Map): The game map.
            x (int): The x position.
            y (int): The y position.

        Returns:
            bool: True if the obstacle was placed, False otherwise.
        """

        if self.active_obstacles < self.obstacles_limit:
            obstacle = Obstacle()
            obstacle.rect.x = x * map.tile_size
            obstacle.rect.y = y * map.tile_size
            map.set_tile(x, y, obstacle)
            self.active_obstacles+=1
            return True
        return False

    def increase_obstacle_capacity(self):
        """
        Increases the player's obstacle placement capacity by 3.
        """
        self.obstacles_limit += 3  # Increase the limit by 3 for each Obstacle power-up picked up

    def activate_invincibility(self):

        """
        Activates invincibility mode for the player.
        """
        self.is_invincible = True
        self.invincibility_timer = pygame.time.get_ticks() + self.invincibility_duration
        self.image = pygame.image.load("images/invincible_player_image.png")  # Change to invincibility visual

    def activate_ghost_mode(self):
        """
        Activates ghost mode for the player.
        """
        self.ghost_mode = True
        self.ghost_timer = pygame.time.get_ticks() + self.ghost_duration
        self.image = pygame.image.load("images/ghost_player_image.png")  # Change to ghost visual

    def update(self,map,players):
        """
        Updates the player's state, checking for expiration of ghost mode and invincibility.

        Args:
            map (Map): The game map.
            players (pygame.sprite.Group): The group of players.
        """
        current_time = pygame.time.get_ticks()
        if self.ghost_mode and current_time > self.ghost_timer:
            self.ghost_mode = False
            self.image = pygame.image.load("images/player_image.png")  # Revert to normal visual
            # Check if the player ends on a non-passable tile
            if map.isBrick(self.row,self.col) | map.isWall(self.row,self.col):
                players.remove(self)
                print("Player died because it was in brick or wall after ghost mode")

        if self.is_invincible and current_time > self.invincibility_timer:
            self.is_invincible = False
            self.image = pygame.image.load("images/player_image.png")  # Revert to normal visual
                

    def move(self, drow, dcol):
        """
        Moves the player by the given delta row and column.

        Args:
            drow (int): Delta row.
            dcol (int): Delta column.
        """
        self.row += drow
        self.col += dcol
        self.rect.topleft = (self.col * 40, self.row * 40)  # Assuming each tile is 32x32 pixels

    def get_coordinates(self):

        """
        Gets the player's current coordinates.

        Returns:
            tuple: The current (row, col) coordinates of the player.
        """
        return (self.row, self.col)

    def draw(self, screen):
        """
        Draws the player on the given screen.

        Args:
            screen (pygame.Surface): The game screen.
        """
        screen.blit(self.image, self.rect)


    def placed_bomb(self,bomb):

        """ Call this method when the player places a bomb. """
        self.active_bombs += 1
        self.bomb_list.append(bomb)
        print('placed bomb',self.active_bombs)
    
    def can_place_bomb(self):
        """ Check if the player can place a bomb. """
        return self.active_bombs < self.bombs_limit and not self.ghost_mode
    
    def bomb_exploded(self,bomb):
        print('exploded',self.active_bombs)
        """ Call this method when a bomb placed by the player explodes. """
        if self.active_bombs > 0:
            self.active_bombs -= 1
            self.bomb_list.remove(bomb)

    def kill(self):
        self.alive = False