import pygame
from pygame.sprite import Group
from brick import Brick, Obstacle
from wall import Wall
from floor import Floor
from powerUp import BombPowerUp, RangePowerUp,DetonatorPowerUp,GhostPowerUp, InvincibilityPowerUp, ObstaclePowerUp, MonsterPowerUp
import random 

class Map:
    def __init__(self, filename, tile_size):
        self.tile_size = tile_size
        self.tiles_group = pygame.sprite.Group()  # Assuming use of pygame for sprite management
        self.bomb_tiles = set()
        self.load_map(filename)

    def load_map(self, filename):
        with open(f'maps/{filename}', 'r') as file:
            lines = file.readlines()
            self.width = len(lines[0].strip())
            self.height = len(lines)
            self.tile_matrix = [[None for _ in range(self.width)] for _ in range(self.height)]

            for row, line in enumerate(lines):
                for col, char in enumerate(line.strip()):
                    if char == '0':
                        tile = Floor()
                    elif char == '1':
                        tile = Wall()
                    elif char == '2':
                        tile = Brick()
                    self.set_tile(row, col, tile)

    def set_tile(self, row, col, tile):
        self.tile_matrix[row][col] = tile
        tile.rect.x = col * self.tile_size
        tile.rect.y = row * self.tile_size
        self.tiles_group.add(tile)

    def is_passable(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            tile = self.tile_matrix[row][col]
            return tile.is_passable
        return False

    def can_pass(self, row, col, ignore_walls=False):
        """Checks if the specified tile can be passed, optionally ignoring walls."""
        if 0 <= row < self.height and 0 <= col < self.width:
            tile = self.tile_matrix[row][col]
            if isinstance(tile, Floor):
                return True
            elif ignore_walls and isinstance(tile, Wall):
                return True
            elif isinstance(tile, Brick):
                return tile.is_passable  # assuming Brick might sometimes be passable
            return False
        return False

    def mark_occupied(self, row, col, occupant):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.occupancy_grid[row][col] = occupant

    def mark_unoccupied(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            self.occupancy_grid[row][col] = None

    def is_tile_type(self, row, col, tile_type):
        if 0 <= row < len(self.tile_matrix) and 0 <= col < len(self.tile_matrix[row]):
            return isinstance(self.tile_matrix[row][col], tile_type)
        return False
    def destroy_brick(self, row, col,power_ups,player):
        # Replace the brick tile with a floor tile, or simply remove the brick.
        # Make sure you have a way to update the visual representation as well.
            # Assuming you have a way to set a floor tile in place of a brick
        if self.isObstacle(row,col):
            player.active_obstacles-= 1  # Remove from the player's list
        else:
            if random.random() < 0.3:
                power_up_type = random.choice([MonsterPowerUp,ObstaclePowerUp,DetonatorPowerUp,BombPowerUp, RangePowerUp,GhostPowerUp,InvincibilityPowerUp])#
                power_up = power_up_type(col, row)
                power_ups.add(power_up)
        self.set_tile(row, col, Floor())
            

    def mark_bomb_tile(self, x, y):
        """ Mark the tile at (x, y) as containing a bomb. """
        self.bomb_tiles.add((x, y))

    def unmark_bomb_tile(self, x, y):
        """ Remove the mark from the tile at (x, y) after a bomb has exploded. """
        self.bomb_tiles.discard((x, y))  # Safe to call even if the tile is not in the set

    def isBomb(self, row, col):
        """ Check if the tile at (x, y) has a bomb on it. """
        return (row, col) in self.bomb_tiles


    def isBrick(self, row, col):
        return isinstance(self.tile_matrix[row][col], Brick) 
    
    def isObstacle(self, row, col):
        return isinstance(self.tile_matrix[row][col], Obstacle) 
    
    def isFloor(self, row, col):
        return isinstance(self.tile_matrix[row][col], Floor) 

    def isWall(self, row, col):
        return self.is_tile_type(row, col, Wall)

    def isBrick(self, row, col):
        return self.is_tile_type(row, col, Brick)

    def isFloor(self, row, col):
        return self.is_tile_type(row, col, Floor)


    def draw(self, screen):
        self.tiles_group.draw(screen)