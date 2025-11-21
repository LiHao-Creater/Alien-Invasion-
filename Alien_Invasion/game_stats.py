class GameStats:
    """
    游戏统计信息跟踪类 (Runtime Statistics Tracker)
    ---------------------------------------------
    负责维护游戏运行时的状态数据。
    包括：
    1. 会话级数据：如最高分 (High Score)，需全生命周期保持。
    2. 局级数据：如当前得分、剩余飞船、护盾值，需在 restart 时重置。
    """

    def __init__(self, ai_game):
        """初始化统计跟踪器"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 游戏活跃状态标志 (State Flag)
        # 启动时默认为 False，处于非活跃状态（菜单界面）
        self.game_active = False

        # 最高分记录 (Session Persistence)
        # 任何情况下都不应被重置，除非关闭程序
        self.high_score = 0

    def reset_stats(self):
        """
        重置局级统计信息。
        在开始新游戏 (New Game) 或复活 (Respawn) 时调用。
        """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        
        # [PhD Extension] 扩展属性：引入 RPG 元素的血量与护盾机制
        self.current_health = self.settings.max_health
        self.current_shield = self.settings.max_shield