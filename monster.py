import pygame
from pygame.sprite import Sprite
import random
from collections import deque

class Monster(Sprite):
    """
    Represents a basic monster in the game, capable of moving randomly across the game field.

    Attributes:
        game_field (GameField): The game field on which the monster operates.
        row (int): Current row position of the monster on the grid.
        col (int): Current column position of the monster on the grid.
        speed (float): Speed factor for the monster.
        move_delay (int): Time delay between moves in milliseconds.
    """
    def __init__(self, game_field, row, col, speed, move_delay=1000):  # move_delay in milliseconds
        """
        Initializes a Monster instance with specified position and movement characteristics.

        Parameters:
            game_field (GameField): The game field object containing game logic and state.
            row (int): Starting row position on the game field.
            col (int): Starting column position on the game field.
            speed (float): Movement speed of the monster.
            move_delay (int): Delay between moves in milliseconds.
        """
        super().__init__()
        self.game_field = game_field
        self.image = pygame.image.load("images/monster_image.png")  # Make sure the image path is correct
        self.rect = self.image.get_rect(topleft=(col * 40, row * 40))  # Assuming tile size is 40x40
        self.row = row
        self.col = col
        self.speed = speed  # Speed attribute for future use
        self.move_delay = move_delay
        self.next_move_time = pygame.time.get_ticks() + self.move_delay
        self.move_timer = pygame.time.get_ticks()

    def update(self, game_map, monsters, players):
        """
        Updates the monster's state. This includes managing movement timing and triggering moves.

        Parameters:
            game_map (Map): The current game map.
            monsters (Group): Group containing all monster sprites.
            players (Group): Group containing all player sprites.
        """
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_move_time:
            self.move(game_map, monsters)
            self.next_move_time = current_time + self.move_delay

    def draw(self, screen):
        """
        Draws the monster on the given screen.

        Parameters:
            screen (Surface): Pygame surface where the monster is to be drawn.
        """
        screen.blit(self.image, self.rect)

    def move(self, game_map, monsters):
        """
        Handles the logic for moving the monster on the game map.

        Parameters:
            game_map (Map): The game map where the monster is located.
            monsters (Group): Group containing all monster sprites to check for collisions.
        """
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Possible directions
        random.shuffle(directions)  # Shuffle directions for more unpredictability

        for drow, dcol in directions:
            new_row = self.row + drow
            new_col = self.col + dcol

            if 0 <= new_row < game_map.height and 0 <= new_col < game_map.width  and game_map.isFloor(new_row, new_col):  # Check bounds
                if is_monster_move_valid(game_map, monsters, new_row, new_col):
                    self.row = new_row
                    self.col = new_col
                    self.rect.topleft = (self.col * 40, self.row * 40)  # Update position
                    break

    def catches(self, player):
        """
        Determines if the monster catches a player.

        Parameters:
            player (Player): The player to check against the monster's position.

        Returns:
            bool: True if the monster catches the player, otherwise False.
        """
        return self.rect.colliderect(player.rect)

    def get_coordinates(self):
        """
        Retrieves the current coordinates of the monster.

        Returns:
            tuple: The (row, col) position of the monster.
        """
        return self.row, self.col


    def kill(self):
        """
        Removes this monster instance from all Pygame groups it belongs to.
        """
        self.kill()

    def kill(self):
        """
        Removes this monster instance from all Pygame groups it belongs to.
        """
        pygame.sprite.Sprite.kill(self)  # Correctly call the kill method from the parent class


def is_monster_move_valid(game_map, monsters, new_row, new_col):
    """
    Determines if a monster can move to a specified position on the game map.

    This function checks whether the proposed new position for a monster is within the game's map boundaries,
    not already occupied by another monster, and not blocked by walls, bricks, or bombs. This helps ensure that
    monster movements are valid within the constraints of the game environment.

    Parameters:
        game_map (Map): The game map object that contains information about walls, bricks, and other obstacles.
        monsters (pygame.sprite.Group): A group containing all the monsters in the game to check for collisions.
        new_row (int): The row index of the new position to check.
        new_col (int): The column index of the new position to check.

    Returns:
        bool: True if the move is valid (the space is free of obstacles and other monsters), False otherwise.
    """
    # Check if the proposed move is onto a wall or brick
    # Check if the proposed move is within the game borders
    if new_row < 0 or new_row >= game_map.height or new_col < 0 or new_col >= game_map.width:
        return False
    # Check for collisions with other monsters
    for monster in monsters:
        if monster.row == new_row and monster.col == new_col:
            return False
    return not game_map.isWall(new_row, new_col) and not game_map.isBrick(new_row, new_col) and not game_map.isBomb(new_row,new_col)  # The move is valid

class WallPassingMonster(Monster):
    """
    A specific type of monster that can pass through walls. Inherits from Monster.

    Attributes:
        move_delay (int): Time delay between moves in milliseconds, set higher for slower movement.
    """
    def __init__(self, game_field, row, col, speed=0.75):
        """
        Initializes a WallPassingMonster with a modified image and move delay.

        Parameters:
            game_field (GameField): The game field object.
            row (int): Starting row position on the game field.
            col (int): Starting column position on the game field.
            speed (float): Movement speed of the monster.
        """
        super().__init__(game_field, row, col, speed)
        self.image = pygame.image.load("images/monster_brown_image.png")
        self.move_delay = 2000  # Set a higher delay for slower movement, 2000 milliseconds (2 seconds)
        

    def update(self, game_map, monsters, players):
        """
        Overrides the update method to enable movement through walls.

        Parameters:
            game_map (Map): The current game map.
            monsters (Group): Group containing all monster sprites.
            players (Group): Group containing all player sprites.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.move_timer > self.move_delay:  # Use move_delay to control update frequency
            self.move_through_walls(game_map, monsters)
            self.move_timer = current_time

    def move_through_walls(self, game_map, monsters):
        """
        Moves the monster through walls until a free space or obstacle is encountered.

        Parameters:
            game_map (Map): The game map where the monster is located.
            monsters (Group): Group containing all monster sprites to check for collisions.
        """
        direction = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])  # Choose initial direction
        next_row = self.row + direction[0]
        next_col = self.col + direction[1]

        while game_map.isWall(next_row, next_col) or game_map.isBrick(next_row, next_col):
            if game_map.isBomb(next_row, next_col):
                return  # Stop moving if a bomb is encountered
            next_row += direction[0]
            next_col += direction[1]

            # Ensure the monster does not go out of bounds
            if not (0 <= next_row < game_map.height and 0 <= next_col < game_map.width):
                return

        if game_map.isFloor(next_row, next_col):
            self.row = next_row
            self.col = next_col
            self.rect.topleft = (self.col * 40, self.row * 40)



class PathfindingMonster(Sprite):
    """
    A monster that uses pathfinding algorithms to chase players within the game. This class
    extends the Sprite class from pygame, allowing it to be managed within pygame's sprite system.

    Attributes:
        game_field (GameField): The game field where the monster moves and interacts.
        row (int): The row index on the game field grid where the monster is currently located.
        col (int): The column index on the game field grid where the monster is currently located.
        speed (float): The speed factor of the monster, influencing its movement.
        move_delay (int): The delay in milliseconds between each move to simulate speed.
        paused (bool): Indicates whether the monster is paused (not allowed to move).
        pause_timer (int): The time at which the monster can resume movement.
        pause_duration (int): The duration in milliseconds for which the monster is paused.
    """
    def __init__(self, game_field, row, col, speed, move_delay=400, image_path='images/monster_green_image.png'):
        """
        Initializes a PathfindingMonster with given attributes and an image.

        Parameters:
            game_field (GameField): The field on which the monster moves.
            row (int): The initial row position of the monster.
            col (int): The initial column position of the monster.
            speed (float): Speed factor affecting how fast the monster moves.
            move_delay (int): The delay in milliseconds between moves.
            image_path (str): Path to the image file representing the monster.
        """
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(col * 40, row * 40))
        self.game_field = game_field
        self.row = row
        self.col = col
        self.speed = speed
        self.move_delay = move_delay
        self.next_move_time = pygame.time.get_ticks() + self.move_delay
        self.paused = False
        self.pause_timer = 0
        self.pause_duration = 5000  # 5000 milliseconds (5 seconds)

    def pause(self):
        """
        Pauses the monster's movement for a defined duration.
        """
        self.paused = True
        self.pause_timer = pygame.time.get_ticks() + self.pause_duration

    def update(self, game_map, monster, players):
        """
        Updates the monster's position and state at each frame. Checks if the monster is paused,
        finds paths to players using BFS, and moves towards them or randomly if no path is found.

        Parameters:
            game_map (Map): The game map containing terrain information.
            monster (Monster): Reference to self, passed if needed in the context.
            players (Group): The group of player sprites currently active in the game.
        """
        current_time = pygame.time.get_ticks()
        if self.paused:
            if current_time > self.pause_timer:
                print("paused")
                self.paused = False
            else:
                return 
        if pygame.time.get_ticks() >= self.next_move_time:
            target = self.find_closest_player(players)
            path = self.bfs(game_map, target)
            if not path:
                self.random_move(game_map)
            else:
                self.move_towards_player(game_map, players)
            self.next_move_time = pygame.time.get_ticks() + self.move_delay

    def is_blocked(self, game_map):
        """
        Checks if the monster is completely surrounded by impassable objects.

        Parameters:
            game_map (Map): The game map containing terrain and obstacle information.

        Returns:
            bool: True if all adjacent spaces are impassable, otherwise False.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for drow, dcol in directions:
            new_row = self.row + drow
            new_col = self.col + dcol
            if game_map.is_passable(new_row, new_col):
                return False
        return True

    def move_towards_player(self, game_map, players):
        """
        Directs the monster towards the closest player using a calculated path.

        Parameters:
            game_map (Map): The map where the game takes place.
            players (Group): The group of player sprites.
        """
        target = self.find_closest_player(players)
        # print('Target is ', target)
        path = self.bfs(game_map, target)
        print('Path is', path)
        if path and len(path) > 1:
            next_step = path[1]  # Skip the first element as it's the monster's current position
            self.row, self.col = next_step
            self.rect.topleft = (self.col * 40, self.row * 40)

    def find_closest_player(self, players):
        """
        Identifies the closest player based on Euclidean distance.

        Parameters:
            players (Group): A group of player sprites from which to find the closest.

        Returns:
            tuple: The grid coordinates (row, col) of the closest player.
        """
        closest_player = min(players, key=lambda player: (player.row - self.row)**2 + (player.col - self.col)**2)
        return (closest_player.row, closest_player.col)

    def bfs(self, game_map, target):
        """
        Performs a breadth-first search (BFS) to find the shortest path to a target location.

        Parameters:
            game_map (Map): The map where the game takes place.
            target (tuple): The (row, col) coordinates of the target position.

        Returns:
            list: A list of tuples representing the path from the monster's current location to the target, or None if no path is found.
        """
        queue = deque([(self.row, self.col)])
        visited = set([(self.row, self.col)])
        paths = {(self.row, self.col): [(self.row, self.col)]}
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        while queue:
            current = queue.popleft()
            if current == target:
                return paths[current]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < game_map.height and 0 <= neighbor[1] < game_map.width:  # Boundary check
                    if game_map.is_passable(neighbor[0], neighbor[1]) and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
                        paths[neighbor] = paths[current] + [neighbor]

        return None

    def random_move(self, game_map):
        """
        Moves the monster in a random direction that is passable.

        Parameters:
            game_map (Map): The map where the game takes place.
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)  # Shuffle directions to ensure randomness
        for drow, dcol in directions:
            new_row = self.row + drow
            new_col = self.col + dcol
            if game_map.is_passable(new_row, new_col):
                self.row = new_row
                self.col = new_col
                self.rect.topleft = (self.col * 40, self.row * 40)
                break  # Move in the first available direction

class DecisionMakingMonster(PathfindingMonster):
    """
    A specialized monster that randomly chooses between a pathfinding move and a random move.
    This class inherits from PathfindingMonster, adding the capability to make strategic decisions at forks.

    Attributes:
        Inherits all attributes from the PathfindingMonster class.
    """
    def __init__(self, game_field, row, col, speed, move_delay=1000):  # Same speed as basic
        """
        Initializes a DecisionMakingMonster with specified attributes and an overridden image.

        Parameters:
            game_field (GameField): The field on which the monster moves.
            row (int): The initial row position of the monster.
            col (int): The initial column position of the monster.
            speed (float): Speed factor affecting how fast the monster moves.
            move_delay (int): The delay in milliseconds between moves, set higher to simulate more thoughtful movement.
        """
        super().__init__(game_field, row, col, speed, move_delay)
        self.image = pygame.image.load("images/monster_red_image.png")

    def move(self, game_map, monsters):
        """
        Overrides the move method to incorporate decision-making capability, allowing the monster
        to choose between following a pathfinding algorithm towards a player or making a random move.

        Parameters:
            game_map (Map): The game map providing terrain and obstacle context.
            monsters (Group): The group of monster sprites used for collision detection.
        """
        # Moves like the PathfindingMonster but makes random 'wrong' decisions at forks
        if random.choice([True, False]):  # Random chance to make a wrong decision
            super().move(game_map, monsters)  # Wrong decision: random move
        else:
            self.move_towards_player(game_map, monsters)  # Correct decision
    
