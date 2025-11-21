import pygame.font

class Button:
    """
    UI 按钮控件类 (User Interface Component: Button)
    ---------------------------------------------
    封装了绘制矩形按钮和居中文本的逻辑。
    支持：
    1. 自定义位置偏移 (Offset)。
    2. 中文文本渲染 (Font Fallback)。
    """

    def __init__(self, ai_game, msg, x_offset=0, y_offset=0, width=220, height=50, 
                 button_color=(0, 135, 0), msg_color=(255, 255, 255), font_size=48):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 尺寸与样式配置
        self.width, self.height = width, height
        self.button_color = button_color
        self.msg_color = msg_color
        
        # 字体配置：优先使用游戏主字体，否则回退到系统默认
        self.font_name = ai_game.font_name 
        self.font = pygame.font.Font(self.font_name, font_size) if self.font_name else pygame.font.SysFont(None, font_size)

        # 构建按钮的 Rect 对象
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        # 应用位置偏移
        self.rect.x += x_offset
        self.rect.y += y_offset

        # 预渲染文本图像 (Pre-render text to texture)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        将 msg 字符串渲染为图像，并使其在按钮上居中。
        包含对中文渲染失败的异常处理。
        """
        try:
            self.msg_image = self.font.render(msg, True, self.msg_color, self.button_color)
        except pygame.error:
            # Fallback: 使用默认系统字体
            print(f"Warning: Font render failed for '{msg}'. Using system default.")
            self.msg_image = pygame.font.SysFont(None, self.font.get_height()).render(msg, True, self.msg_color, self.button_color)

        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按钮：先填充背景色，再绘制文本纹理"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)