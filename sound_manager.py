"""Sound manager module for Alien Invasion"""
import pygame


class SoundManager:
    """A class to manage sound effects for the game."""

    def __init__(self):
        """Initialize the sound manager."""
        try:
            pygame.mixer.init()
            self.sounds_enabled = True
        except:
            self.sounds_enabled = False
        
        # Create simple sound effects using pygame.mixer.Sound
        # We'll generate simple tones for different actions
        if self.sounds_enabled:
            self._create_sounds()

    def _create_sounds(self):
        """Create simple sound effects."""
        try:
            # Create a simple shooting sound (using a generated tone)
            self.shoot_sound = self._generate_tone(440, 0.1)
            # Create a simple explosion sound
            self.explosion_sound = self._generate_tone(220, 0.2)
            # Create a simple hit sound
            self.hit_sound = self._generate_tone(330, 0.15)
        except:
            # If sound generation fails, disable sounds
            self.sounds_enabled = False

    def _generate_tone(self, frequency, duration):
        """Generate a simple tone for sound effects."""
        try:
            sample_rate = 22050
            n_samples = int(round(duration * sample_rate))
            
            # Generate a simple square wave
            import numpy as np
            buf = np.zeros((n_samples, 2), dtype=np.int16)
            max_sample = 2**(16 - 1) - 1
            
            for s in range(n_samples):
                t = float(s) / sample_rate
                value = int(round(max_sample * 0.3 * 
                          (1 if (int(t * frequency) % 2) == 0 else -1)))
                buf[s][0] = value
                buf[s][1] = value
            
            return pygame.sndarray.make_sound(buf)
        except:
            # Return a dummy sound if generation fails
            return None

    def play_shoot(self):
        """Play shooting sound."""
        if self.sounds_enabled and self.shoot_sound:
            try:
                self.shoot_sound.play()
            except:
                pass

    def play_explosion(self):
        """Play explosion sound."""
        if self.sounds_enabled and self.explosion_sound:
            try:
                self.explosion_sound.play()
            except:
                pass

    def play_hit(self):
        """Play hit sound."""
        if self.sounds_enabled and self.hit_sound:
            try:
                self.hit_sound.play()
            except:
                pass
