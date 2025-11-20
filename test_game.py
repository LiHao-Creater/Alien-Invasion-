"""Simple test script for Alien Invasion game components"""
import pygame
import sys

# Initialize pygame
pygame.init()

# Test imports
print("Testing game component imports...")
try:
    from settings import Settings
    from game_stats import GameStats
    from ship import Ship
    from bullet import Bullet, AlienBullet
    from alien import Alien
    from shield import Shield, ShieldBlock
    from button import Button
    from scoreboard import Scoreboard
    from sound_manager import SoundManager
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import failed: {e}")
    sys.exit(1)

# Test settings
print("\nTesting Settings...")
try:
    settings = Settings()
    assert settings.screen_width == 1200
    assert settings.screen_height == 800
    assert settings.ship_speed > 0
    assert settings.bullets_allowed > 0
    print("✓ Settings initialized correctly")
except Exception as e:
    print(f"✗ Settings test failed: {e}")
    sys.exit(1)

# Test game initialization
print("\nTesting game initialization...")
try:
    screen = pygame.display.set_mode((800, 600))
    
    # Create a minimal game-like object for testing
    class TestGame:
        def __init__(self):
            self.settings = Settings()
            self.screen = screen
            self.stats = GameStats(self)
    
    test_game = TestGame()
    
    # Test ship
    test_game.ship = Ship(test_game)
    assert test_game.ship.rect is not None
    print("✓ Ship created successfully")
    
    # Test alien
    alien = Alien(test_game)
    assert alien.rect is not None
    print("✓ Alien created successfully")
    
    # Test bullet
    bullet = Bullet(test_game)
    assert bullet.rect is not None
    print("✓ Bullet created successfully")
    
    # Test alien bullet
    alien_bullet = AlienBullet(test_game, alien)
    assert alien_bullet.rect is not None
    print("✓ Alien bullet created successfully")
    
    # Test shield
    shield = Shield(100, 100, 100, 20)
    assert len(shield.blocks) > 0
    print("✓ Shield created successfully")
    
    # Test button
    button = Button(test_game, "Test")
    assert button.rect is not None
    print("✓ Button created successfully")
    
    # Test scoreboard
    sb = Scoreboard(test_game)
    assert sb.score_image is not None
    print("✓ Scoreboard created successfully")
    
    # Test sound manager
    sound_mgr = SoundManager()
    print("✓ Sound manager initialized")
    
except Exception as e:
    print(f"✗ Game component test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)
print("\nGame is ready to play!")
print("Run: python alien_invasion.py")

pygame.quit()
