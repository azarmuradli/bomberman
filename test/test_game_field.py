import unittest
import pygame
from game import Player
from map import Map
from gameField import GameField

class TestGameField(unittest.TestCase):
    def setUp(self):
        self.player1 = Player(1, 0, 0, 2, 2, [])
        self.player2 = Player(2, 10, 12, 3, 3, [])
        self.players = pygame.sprite.Group()
        self.players.add(self.player1) 
        self.players.add(self.player2)
        self.game_map = Map('map1.txt', 30)
        self.game_field = GameField(self.game_map)

    def test_is_valid_move_up(self):
        # Movement up, when the tile above is a valid tile and in-bounds
        self.assertTrue( self.game_field.is_valid_move((1,2), (-1, 0),False,self.players) ) 
        # Movement up, when the tile above is not a valid tile but in-bounds
        self.assertFalse( self.game_field.is_valid_move((2,1), (-1, 0),False,self.players) ) 
        # Movement up is out of bounds
        self.assertFalse( self.game_field.is_valid_move((0,0), (-1, 0), False,self.players) ) 

    def test_is_valid_move_down(self):
        # Movement down, when the tile is a valid tile and in-bounds
        self.assertTrue( self.game_field.is_valid_move((0,0), (1, 0),False,self.players) ) 
        # Movement down, when the tile below is not a valid tile but in-bounds
        self.assertFalse( self.game_field.is_valid_move((0,1), (1, 0),False,self.players) ) 
        # Movement down is out of bounds
        self.assertFalse( self.game_field.is_valid_move((10,12), (1, 0), False,self.players) ) 

    def test_is_valid_move_right(self):
        # Movement right, when the tile to the right is a valid tile and in-bounds
        self.assertTrue(self.game_field.is_valid_move((0, 0), (0, 1), False, self.players))
        # Movement right, when the tile to the right is not a valid tile but in-bounds
        self.assertFalse(self.game_field.is_valid_move((1, 0), (0, 1), False, self.players))
        # Movement right is out of bounds (testing the last column)
        self.assertFalse(self.game_field.is_valid_move((10, 12), (0, 1), False, self.players))

    def test_is_valid_move_left(self):
        # Movement left, when the tile to the left is a valid tile and in-bounds
        self.assertTrue(self.game_field.is_valid_move((0, 2), (0, -1), False, self.players))
        # Movement left, when the tile to the left is not a valid tile but in-bounds
        self.assertFalse(self.game_field.is_valid_move((1, 2), (0, -1), False, self.players))
        # Movement left is out of bounds (testing the first column)
        self.assertFalse(self.game_field.is_valid_move((0, 0), (0, -1), False, self.players))

    def test_is_valid_move_player_collision(self):
        # Movement when there is no player, and is a valid tile
        self.assertTrue(self.game_field.is_valid_move((0, 2), (0, -1), False, self.players))
        # Movement when there is a player on the tile we want to move
        self.assertFalse(self.game_field.is_valid_move((1,0), (-1, 0), False, self.players))

if __name__ == '__main__':
    unittest.main()
