import unittest
from unittest.mock import Mock, patch
import pygame
from powerUp import BombPowerUp, RangePowerUp, DetonatorPowerUp, GhostPowerUp, InvincibilityPowerUp, ObstaclePowerUp, MonsterPowerUp
from player import Player
from monster import PathfindingMonster

class TestPowerUp(unittest.TestCase):
    def setUp(self):
        pygame.init()
        
        # Mocking image loading
        patcher = patch('pygame.image.load', Mock(return_value=pygame.Surface((40, 40))))
        self.mock_image_load = patcher.start()
        self.addCleanup(patcher.stop)
        
        # Create a Player mock
        self.mock_player = Mock(spec=Player)
        self.mock_player.bombs_limit = 1
        self.mock_player.blast_range = 1
        self.mock_player.has_detonator = False
        self.mock_player.activate_ghost_mode = Mock()
        self.mock_player.activate_invincibility = Mock()
        self.mock_player.increase_obstacle_capacity = Mock()

        # Create a PathfindingMonster mock
        self.mock_monster = Mock(spec=PathfindingMonster)
        self.mock_monster.pause = Mock()

        # Create a monsters group containing the mock monster
        self.monsters = pygame.sprite.Group(self.mock_monster)
        
    def test_bomb_powerup(self):
        powerup = BombPowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.assertEqual(self.mock_player.bombs_limit, 2, "Bomb limit did not increase correctly")
        
    def test_range_powerup(self):
        powerup = RangePowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.assertEqual(self.mock_player.blast_range, 2, "Blast range did not increase correctly")
        
    def test_detonator_powerup(self):
        powerup = DetonatorPowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.assertTrue(self.mock_player.has_detonator, "Player did not acquire detonator")
        
    def test_ghost_powerup(self):
        powerup = GhostPowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.mock_player.activate_ghost_mode.assert_called_once_with()
        
    def test_invincibility_powerup(self):
        powerup = InvincibilityPowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.mock_player.activate_invincibility.assert_called_once_with()
        
    def test_obstacle_powerup(self):
        powerup = ObstaclePowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.mock_player.increase_obstacle_capacity.assert_called_once_with()
        
    def test_monster_powerup(self):
        powerup = MonsterPowerUp(1, 1)
        powerup.apply_effect(self.mock_player, self.monsters)
        self.mock_monster.pause.assert_called_once_with()

if __name__ == '__main__':
    unittest.main()
