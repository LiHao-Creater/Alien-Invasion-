"""Alien module for Alien Invasion"""
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.Surface((50, 40))
        self.image.fill((0, 255, 0))
        # Draw a simple alien shape
        pygame.draw.ellipse(self.image, (100, 255, 100), 
                          pygame.Rect(5, 5, 40, 30))
        pygame.draw.circle(self.image, (50, 200, 50), (15, 15), 8)
        pygame.draw.circle(self.image, (50, 200, 50), (35, 15), 8)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien right or left."""
        self.x += (self.settings.alien_speed *
                   self.settings.fleet_direction)
        self.rect.x = self.x
