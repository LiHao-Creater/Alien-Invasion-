import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """
    外星人实体类 (Alien Enemy Entity)
    -------------------------------
    表示舰队中的单个外星人。包含位置初始化、资源加载及自主移动逻辑。
    """

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # --- 资源加载 ---
        try:
            self.image = pygame.image.load('images/alien.png').convert_alpha()
        except FileNotFoundError:
            print("Error: images/alien.png not found. Using fallback surface.")
            self.image = pygame.Surface((50, 40))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()
        # 初始位置设置：左上角附近，留出边距
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

        # --- 智能体状态属性 ---
        # row_direction: 该实体所在行的移动方向 (1: Right, -1: Left)
        # 这一设计解耦了不同行的移动逻辑，允许更复杂的队形变换
        self.row_direction = 1
        
        # row_index: 标识该实体属于哪一行，用于批量控制
        self.row_index = 0

    def check_edges(self):
        """
        边界检测 (Collision Detection - Boundaries)
        如果外星人触碰到屏幕边缘，返回 True。
        """
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        """
        更新外星人位置。
        逻辑：x = x + (speed * direction)
        """
        self.x += self.settings.alien_speed * self.row_direction
        self.rect.x = self.x