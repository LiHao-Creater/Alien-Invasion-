import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    玩家子弹类 (Player Projectile)
    ----------------------------
    继承自 Sprite，管理飞船发射的子弹。
    """
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 在 (0,0) 处创建子弹矩形，再将其对齐到飞船顶部
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        
        # 存储浮点数位置以实现精确移动
        self.y = float(self.rect.y)

    def update(self):
        """
        更新子弹位置 (Kinematic Update)
        方向：垂直向上 (y 轴负方向)
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """在屏幕上渲染子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class AlienBullet(Sprite):
    """
    外星人子弹类 (Enemy Projectile - PhD Extension)
    ---------------------------------------------
    扩展功能：允许敌方单位进行反击。
    """
    def __init__(self, ai_game, alien):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.alien_bullet_color

        # 初始化位置：发射该子弹的外星人底部
        self.rect = pygame.Rect(0, 0, self.settings.alien_bullet_width,
            self.settings.alien_bullet_height)
        self.rect.midbottom = alien.rect.midbottom
        self.y = float(self.rect.y)

    def update(self):
        """
        更新子弹位置
        方向：垂直向下 (y 轴正方向)
        """
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)