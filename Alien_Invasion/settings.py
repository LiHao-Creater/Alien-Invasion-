class Settings:
    """
    游戏配置类 (Configuration Class)
    --------------------------------
    集中管理《外星人入侵》的所有静态设置与动态参数。
    采用分离设计：
    1. __init__: 初始化游戏启动时固定的静态参数（如屏幕分辨率、资源上限）。
    2. initialize_dynamic_settings: 初始化随游戏进程重置的动态参数（如速度、难度）。
    """

    def __init__(self):
        """初始化游戏的静态设置 (Static Settings)"""
        # --- 屏幕与显示设置 ---
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # --- 飞船实体设置 (Ship Configuration) ---
        self.ship_limit = 3       # 生命值：玩家拥有的飞船总数
        self.max_health = 100     # 生命条上限
        self.max_shield = 100     # 护盾条上限
        self.shield_regen_rate = 0.0  # 预留接口：护盾自然恢复率

        # --- 玩家投射物设置 (Projectile: Player) ---
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 255, 0)  # 绿色高亮显示
        self.bullets_allowed = 5         # 限制同屏最大子弹数以平衡性能与难度

        # --- 外星人实体设置 (Alien Configuration) ---
        self.fleet_drop_speed = 10       # 触边后的下沉步长

        # --- 敌方投射物设置 (Projectile: Enemy) ---
        self.alien_bullet_width = 4
        self.alien_bullet_height = 15
        self.alien_bullet_color = (0, 255, 0)
        self.alien_fire_probability = 0.0005  # 射击概率模型 (Monte Carlo approach per frame)

        # --- 难度迭代参数 (Difficulty Scaling) ---
        self.speedup_scale = 1.1  # 速度递增因子 (几何级数增长)
        self.score_scale = 1.5    # 分数奖励递增因子

        # 初始化动态变量
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        初始化随游戏状态变化的动态设置。
        在由菜单进入新游戏或重置关卡时调用。
        """
        self.ship_speed = 1.0          # 飞船横向移动速度
        self.bullet_speed = 4.0        # 玩家子弹初速度
        self.alien_speed = 0.4         # 外星人巡航速度
        self.alien_bullet_speed = 1.0  # 敌方弹幕速度
        
        # 舰队移动方向标志位 (1: 向右, -1: 向左)
        self.fleet_direction = 1
        
        # 计分权重
        self.alien_points = 50

    def increase_speed(self):
        """
        执行难度升级逻辑。
        在清理完一波外星人后调用，按比例提升所有实体速度与奖励分值。
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)