import unittest
from unittest.mock import Mock, patch
import pygame
from bomb import Bomb
from map import Map
from player import Player
from monster import Monster
from explosion import Explosion

class TestBomb(unittest.TestCase):
    def setUp(self):
        pygame.init()
        
        # Mocking image loading
        patcher = patch('pygame.image.load', Mock(return_value=pygame.Surface((40, 40))))
        self.mock_image_load = patcher.start()
        self.addCleanup(patcher.stop)
        
        # Set up a simple map mock
        self.mock_map = Mock(spec=Map)
        self.mock_map.width = 13
        self.mock_map.height = 11
        self.mock_map.isFloor.side_effect = lambda x, y: True
        self.mock_map.isWall.side_effect = lambda x, y: False
        self.mock_map.isBrick.side_effect = lambda x, y: False
        self.mock_map.destroy_brick.side_effect = lambda x, y, z, w: None
        self.mock_map.unmark_bomb_tile.side_effect = lambda x, y: None
        self.mock_map.mark_bomb_tile.side_effect = lambda x, y: None
        
        # Create a Player mock
        self.mock_player = Mock(spec=Player)
        self.mock_player.row = 5
        self.mock_player.col = 5
        self.mock_player.blast_range = 2
        self.mock_player.has_detonator = False
        self.mock_player.can_place_bomb.return_value = True
        self.mock_player.bomb_exploded.side_effect = lambda bomb: None
        self.mock_player.is_invincible = False  # Add the missing attribute
        self.mock_player.id = 1  # Add the missing attribute
        
        # Create a Bomb instance
        self.bomb = Bomb(self.mock_player, 5, 5, self.mock_player.blast_range, 3000)
        
        # Mock for Explosion
        self.mock_explosion = Mock(spec=Explosion)
        
        # Create groups
        self.monsters = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group(self.bomb)
        self.explosion_tiles = []
        self.power_ups = pygame.sprite.Group()
        self.players = pygame.sprite.Group(self.mock_player)
        
    def test_bomb_creation(self):
        # Check bomb's initial position and state
        self.assertEqual(self.bomb.row, 5, "Bomb initial row is incorrect")
        self.assertEqual(self.bomb.col, 5, "Bomb initial col is incorrect")
        self.assertFalse(self.bomb.is_exploding, "Bomb should not be exploding initially")
        
    def test_bomb_update_no_explode(self):
        # Simulate update before explosion time
        self.bomb.explodeTime = pygame.time.get_ticks() + 5000  # Set future explode time
        self.bomb.update(self.mock_map, self.monsters, self.bombs, self.explosion_tiles, self.power_ups, self.players)
        self.assertFalse(self.bomb.is_exploding, "Bomb should not explode before its time")
        
    def test_bomb_explode(self):
        # Simulate bomb explosion
        self.bomb.explodeTime = pygame.time.get_ticks()  # Set current time to explode
        self.bomb.update(self.mock_map, self.monsters, self.bombs, self.explosion_tiles, self.power_ups, self.players)
        self.assertTrue(self.bomb.is_exploding, "Bomb should be exploding")
        self.assertIn((5, 5, 4500), self.explosion_tiles, "Bomb explosion not registered correctly")
        
    def test_bomb_chain_explosion(self):
        # Simulate chain reaction with another bomb
        another_bomb = Bomb(self.mock_player, 5, 6, 2, 3000)
        self.bombs.add(another_bomb)
        
        self.bomb.explodeTime = pygame.time.get_ticks()  # Set current time to explode
        self.bomb.update(self.mock_map, self.monsters, self.bombs, self.explosion_tiles, self.power_ups, self.players)
        
        self.assertTrue(self.bomb.is_exploding, "Bomb should be exploding")
        self.assertTrue(another_bomb.is_exploding, "Another bomb should be triggered to explode")
        
    def test_bomb_kills_player(self):
        # Simulate player being in bomb's explosion range
        self.mock_player.row = 5
        self.mock_player.col = 5
        self.mock_player.is_invincible = False
        
        self.bomb.explode(self.mock_map, self.monsters, self.bombs, self.explosion_tiles, self.power_ups, self.players)
        self.mock_player.kill.assert_called_once_with()
        
    def test_bomb_kills_monster(self):
        # Add a monster in the bomb's explosion range
        monster = Mock(spec=Monster)
        monster.row = 5
        monster.col = 5
        self.monsters.add(monster)
        
        self.bomb.explode(self.mock_map, self.monsters, self.bombs, self.explosion_tiles, self.power_ups, self.players)
        monster.kill.assert_called_once_with()
        
    def test_bomb_destroys_brick(self):
        # Simulate bomb explosion destroying a brick
        self.mock_map.isBrick.side_effect = lambda x, y: (x, y) == (5, 6)
        
        self.bomb.explode(self.mock_map, self.monsters, self.bombs, self.explosion_tiles, self.power_ups, self.players)
        self.mock_map.destroy_brick.assert_any_call(5, 6, self.power_ups, self.mock_player)
        
    def test_bomb_valid_range(self):
        self.assertTrue(self.bomb.isValidRange(0, 0), "Bomb valid range check failed for (0, 0)")
        self.assertFalse(self.bomb.isValidRange(-1, 0), "Bomb valid range check failed for (-1, 0)")
        self.assertFalse(self.bomb.isValidRange(11, 0), "Bomb valid range check failed for (11, 0)")
        self.assertFalse(self.bomb.isValidRange(0, 13), "Bomb valid range check failed for (0, 13)")
        
if __name__ == '__main__':
    unittest.main()
