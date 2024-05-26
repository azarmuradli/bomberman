import pygame
from pygame.sprite import Sprite

class Floor(Sprite):
    def __init__(self):
        """
        Initialize the Floor object.

        This class represents a floor tile in the game. Floor tiles are passable by default.

        Attributes:
            image (Surface): The image representing the floor tile.
            rect (Rect): The rectangular area of the floor tile.
            is_passable (bool): A flag indicating if the floor tile is passable.
        """
        super().__init__()
        self.image = pygame.image.load("images/floor_image.png")
        self.rect = self.image.get_rect()
        self.is_passable = True  # Floors are passable