"""Shield module for Alien Invasion"""
import pygame
from pygame.sprite import Sprite


class ShieldBlock(Sprite):
    """A class to represent a single block of a shield."""

    def __init__(self, x, y, width, height):
        """Initialize a shield block."""
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 255, 0)
        self.hits = 3  # Number of hits the block can take

    def hit(self):
        """Handle a hit to the shield block."""
        self.hits -= 1
        if self.hits == 2:
            self.color = (200, 255, 0)
        elif self.hits == 1:
            self.color = (255, 200, 0)
        return self.hits <= 0

    def draw(self, screen):
        """Draw the shield block."""
        pygame.draw.rect(screen, self.color, self.rect)


class Shield:
    """A class to manage a shield structure."""

    def __init__(self, x, y, width, height):
        """Initialize the shield with blocks."""
        self.blocks = pygame.sprite.Group()
        block_width = width // 10
        block_height = height // 3
        
        # Create shield blocks in a defensive structure
        for row in range(3):
            for col in range(10):
                # Skip corners for a more interesting shape
                if (row == 0 and (col < 2 or col > 7)) or \
                   (row == 1 and (col < 1 or col > 8)):
                    continue
                block_x = x + col * block_width
                block_y = y + row * block_height
                block = ShieldBlock(block_x, block_y, block_width, block_height)
                self.blocks.add(block)

    def draw(self, screen):
        """Draw all blocks in the shield."""
        for block in self.blocks:
            block.draw(screen)

    def check_collision_with_bullet(self, bullets):
        """Check for collisions between bullets and shield blocks."""
        for bullet in bullets:
            collisions = [block for block in self.blocks if block.rect.colliderect(bullet.rect)]
            if collisions:
                bullet.kill()
                for block in collisions:
                    if block.hit():
                        self.blocks.remove(block)
                return True
        return False
