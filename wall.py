import pygame
from pygame.sprite import Sprite

class Wall(Sprite):
    def __init__(self):
        """
        Initialize the Wall object.

        This class represents a wall in the game. Walls are not passable by default.

        Attributes:
            image (Surface): The image representing the wall.
            rect (Rect): The rectangular area of the wall.
            is_passable (bool): A flag indicating if the wall is passable.
        """
        super().__init__()
        self.image = pygame.image.load("images/wall_image.png")
        self.rect = self.image.get_rect()
        self.is_passable = False  # Walls are not passable