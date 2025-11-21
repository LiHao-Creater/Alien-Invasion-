import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """
    玩家飞船类 (Player Ship Entity)
    -------------------------------
    继承自 Pygame Sprite 类。
    负责管理玩家飞船的资源加载、位置计算 (Kinematics) 和渲染 (Blitting)。
    """

    def __init__(self, ai_game):
        """初始化飞船并设置初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # --- 资源加载与异常处理 ---
        try:
            self.image = pygame.image.load('images/ship.png').convert_alpha()
        except FileNotFoundError:
            # 容错机制：若资源丢失，使用色块代替
            print("Error: images/ship.png not found. Loading fallback.")
            self.image = pygame.Surface((60, 50))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        
        # 初始化位置：屏幕底部中央
        self.center_ship()

        # --- 运动状态标志位 (Movement Flags) ---
        # 这种设计允许处理持续按键事件 (Continuous Key Press)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """
        根据运动标志位调整飞船位置。
        包含边界检查逻辑，防止飞船移出可视区域。
        """
        # 更新 x 坐标而非 rect 对象，以支持浮点数精度的速度值
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # 同步物理坐标到渲染坐标
        self.rect.x = self.x

    def center_ship(self):
        """将飞船复位至屏幕底部中央 (用于关卡重置或复活)"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """在指定位置绘制飞船图像"""
        self.screen.blit(self.image, self.rect)