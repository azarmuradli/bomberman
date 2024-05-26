import pygame
from pygame.sprite import Sprite

class Brick(Sprite):
    def __init__(self):
        """
        Initialize the Brick object.

        This class represents a brick in the game. Bricks are not passable by default.

        Attributes:
            image (Surface): The image representing the brick.
            rect (Rect): The rectangular area of the brick.
            is_passable (bool): A flag indicating if the brick is passable.
        """
        super().__init__()
        self.image = pygame.image.load('images/brick_image.png')  # Ensure you have a valid path
        self.rect = self.image.get_rect()
        self.is_passable = False

class Obstacle(Brick):  
    def __init__(self):
        """
        Initialize the Obstacle object.

        This class represents an obstacle in the game. Obstacles inherit from bricks but have a different image.

        Attributes:
            image (Surface): The image representing the obstacle.
            rect (Rect): The rectangular area of the obstacle.
        """
        super().__init__()
        self.image = pygame.image.load("images/obstacle_image.png") 
        self.rect = self.image.get_rect()
