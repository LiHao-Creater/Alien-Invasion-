import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """
    记分板与 HUD 管理类 (Heads-Up Display System)
    -------------------------------------------
    负责渲染游戏界面上的所有统计信息，包括：
    1. 文本信息：得分、最高分、当前关卡。
    2. 图标信息：剩余飞船数。
    3. 进度条信息 (PhD Feature)：生命值与护盾值可视化。
    """

    def __init__(self, ai_game):
        """初始化记分板属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 样式配置
        self.text_color = (30, 30, 30)
        self.font_name = ai_game.font_name
        self.font = pygame.font.Font(self.font_name, 48) if self.font_name else pygame.font.SysFont(None, 48)
        
        # 初始化静态图像资源
        self.prep_images()

    def prep_images(self):
        """准备所有初始的 HUD 图像资源"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将得分转换为渲染图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(f"Score: {score_str}", True, self.text_color, self.settings.bg_color)
        
        # 布局：右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分转换为渲染图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(f"High: {high_score_str}", True, self.text_color, self.settings.bg_color)
        
        # 布局：顶部居中
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """将等级转换为渲染图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(f"Lvl: {level_str}", True, self.text_color, self.settings.bg_color)
        
        # 布局：得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示剩余飞船数 (Lives)"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def draw_health_bars(self):
        """
        绘制专业级状态条 (Health & Shield Bars)
        ------------------------------------
        逻辑：
        1. 绘制背景槽 (深色)。
        2. 计算当前值与最大值的比例。
        3. 绘制前景条 (根据血量百分比动态变色：绿->黄->红)。
        4. 叠加 Shield 护盾条 (蓝色)。
        """
        bar_width = 200
        bar_height = 15
        x_pos = 10
        y_pos_health = 70
        y_pos_shield = 95
        
        # --- 1. 生命条 (Health Bar) ---
        health_bg = pygame.Rect(x_pos, y_pos_health, bar_width, bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), health_bg)
        
        health_pct = max(0, self.stats.current_health / self.settings.max_health)
        health_fg = pygame.Rect(x_pos, y_pos_health, int(bar_width * health_pct), bar_height)
        
        # 动态颜色逻辑
        color = (0, 200, 0) if health_pct > 0.5 else (200, 200, 0) if health_pct > 0.2 else (200, 0, 0)
        pygame.draw.rect(self.screen, color, health_fg)

        # --- 2. 护盾条 (Shield Bar) ---
        shield_bg = pygame.Rect(x_pos, y_pos_shield, bar_width, bar_height)
        pygame.draw.rect(self.screen, (50, 50, 50), shield_bg)

        shield_pct = max(0, self.stats.current_shield / self.settings.max_shield)
        shield_fg = pygame.Rect(x_pos, y_pos_shield, int(bar_width * shield_pct), bar_height)
        pygame.draw.rect(self.screen, (0, 100, 255), shield_fg)
        
        # --- 3. 文本标签 ---
        small_font = pygame.font.SysFont(None, 20)
        h_label = small_font.render("HP", True, (255, 255, 255))
        s_label = small_font.render("SHIELD", True, (255, 255, 255))
        
        self.screen.blit(h_label, (x_pos + bar_width + 5, y_pos_health + bar_height/4))
        self.screen.blit(s_label, (x_pos + bar_width + 5, y_pos_shield + bar_height/4))


    def show_score(self):
        """统一绘制所有 HUD 元素"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
        # 实时绘制动态血条
        self.draw_health_bars()

    def check_high_score(self):
        """检查是否诞生了新的最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()