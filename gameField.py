from floor import Floor

class GameField:
    def __init__(self, game_map):
        self.map = game_map

    def is_valid_move(self, player_coords, movement,ghost_mode,players):
        """
        Determines if a move is valid based on the game map and current game conditions.

        This method evaluates whether a proposed movement from a current position results in a valid new
        position on the game map. It takes into account boundary limits, collisions with other players,
        and whether the player is in ghost mode, which allows passing through obstacles.

        Parameters:
            player_coords (tuple): The current (x, y) coordinates of the player.
            movement (tuple): The proposed (x, y) change in position.
            ghost_mode (bool): Indicates if the player can move through obstacles.
            players (pygame.sprite.Group): Group of all player sprites to check for potential collisions.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        # Get the new coordinates after movement
        new_x = player_coords[0] + movement[0]
        new_y = player_coords[1] + movement[1]

        # Check if the new coordinates are out of bounds
        if new_x < 0 or new_x > 10 or new_y < 0 or new_y > 12:
            return False  
        
        # Check if two players will stand on the same tile
        for player in players:
            if player.get_coordinates() == (new_x, new_y):
                return False

        if ghost_mode:
            return True
        else:
            # Check if the new coordinate is of floor type, if yes it is suitable
            if self.map.isFloor(new_x, new_y) and not self.map.isBomb(new_x,new_y):
                return True  

        return False  
