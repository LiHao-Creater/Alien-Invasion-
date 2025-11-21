import sys
from time import sleep
import random
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet, AlienBullet
from alien import Alien

class AlienInvasion:
    """
    游戏核心控制器 (Main Game Controller)
    ------------------------------------
    负责协调游戏资源、管理游戏循环 (Game Loop) 以及处理全局状态转换。
    架构模式：Model-View-Controller (MVC) 的变体，其中本类充当 Controller。
    """

    def __init__(self):
        """初始化游戏资源与环境"""
        pygame.init()
        self.settings = Settings()
        
        # --- 显示层初始化 ---
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion: PhD Edition")

        # --- 资源加载 (Assets Loading) ---
        # 背景图：区分菜单背景与游戏背景
        self.menu_bg_image = pygame.image.load('images/background.png')
        self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (self.settings.screen_width, self.settings.screen_height))
        
        try:
            self.game_bg_image = pygame.image.load('images/background2.png')
        except pygame.error:
            print("Warning: background2.png not found. Fallback to menu bg.")
            self.game_bg_image = self.menu_bg_image
        self.game_bg_image = pygame.transform.scale(self.game_bg_image, (self.settings.screen_width, self.settings.screen_height))

        # 音频系统初始化 (Audio System)
        self._init_audio()

        # 字体系统初始化 (支持中文回退逻辑)
        self.font_name = pygame.font.match_font('simhei, microsoftyahei, fangsong, arialunicode')
        if not self.font_name:
            self.font_name = None

        # --- 实体与组件实例化 ---
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        
        # Sprite Groups (精灵组)：用于批量管理实体
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        
        # --- 状态机配置 ---
        self.last_game_result = None
        self.win_level = 3
        # game_state 状态枚举: "menu", "playing", "paused", "game_win", "game_over"
        self.game_state = "menu"
        
        # UI 按钮实例化
        self._init_buttons()
        
        # 初始舰队生成
        self._create_fleet()
        
        # 播放背景音乐
        if self.sounds_loaded:
            pygame.mixer.music.play(-1)

    def _init_audio(self):
        """初始化混音器与加载音效资源，包含异常处理机制"""
        try:
            pygame.mixer.init()
            pygame.mixer.music.load('sounds/background.flac')
            pygame.mixer.music.set_volume(0.6)
            
            # 预加载音效对象
            self.sound_laser = pygame.mixer.Sound('sounds/laser.flac')
            self.sound_explosion = pygame.mixer.Sound('sounds/explosion.flac')
            self.sound_hit = pygame.mixer.Sound('sounds/hit.flac')
            self.sound_die = pygame.mixer.Sound('sounds/die.flac')
            self.sound_win = pygame.mixer.Sound('sounds/win.flac')
            self.sound_gameover = pygame.mixer.Sound('sounds/gameover.flac')
            
            # 音量平衡
            self.sound_laser.set_volume(0.2)
            self.sound_hit.set_volume(0.3)
            self.sound_explosion.set_volume(0.4)
            
            self.sounds_loaded = True
        except (FileNotFoundError, pygame.error) as e:
            print(f"System Warning: Audio initialization failed ({e}). Running in silent mode.")
            self.sounds_loaded = False
            # 设置为空对象防止后续调用崩溃
            self.sound_laser = None 
            # ... (其余略，保持原有容错逻辑)

    def _init_buttons(self):
        """初始化 UI 交互按钮"""
        self.play_button = Button(self, "开始游戏", y_offset=315, button_color=(0, 200, 0))
        self.btn_restart = Button(self, "重新开始", x_offset=-120, y_offset=250, width=200, height=50, msg_color=(255,255,255), button_color=(0, 200, 0))
        self.btn_return = Button(self, "返回主页", x_offset=120, y_offset=250, width=200, height=50, msg_color=(255,255,255), button_color=(0, 200, 0))

    def run_game(self):
        """
        主游戏循环 (The Main Game Loop)
        -----------------------------
        采用标准的 Input -> Update -> Render 流程。
        注意：通过 game_state 严格控制逻辑更新，实现暂停功能。
        """
        while True:
            self._check_events()  # 输入处理
            
            # 逻辑更新 (仅在游戏进行时执行)
            if self.game_state == "playing":
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen() # 渲染输出

    def _check_events(self):
        """事件监听与分发 (Event Dispatcher)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 根据当前状态路由鼠标点击事件
                if event.button == 1:
                    if self.game_state == "playing":
                        self._fire_bullet()
                    elif self.game_state == "menu":
                        self._check_play_button(mouse_pos)
                    elif self.game_state in ["game_win", "game_over"]:
                        self._check_result_buttons(mouse_pos)
    
    def _check_play_button(self, mouse_pos):
        """处理菜单界面的开始按钮点击"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self._start_game()

    def _check_result_buttons(self, mouse_pos):
        """处理结算界面的按钮点击 (Restart / Return Home)"""
        if self.btn_restart.rect.collidepoint(mouse_pos):
            self._start_game()
        elif self.btn_return.rect.collidepoint(mouse_pos):
            self.game_state = "menu"
            self.last_game_result = None
            pygame.mouse.set_visible(True)
            self._reset_game_state()
            if self.sounds_loaded:
                if self.sound_win: self.sound_win.stop()
                if self.sound_gameover: self.sound_gameover.stop()
                if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play(-1)

    def _start_game(self):
        """
        执行游戏启动序列 (Initialization Sequence)
        重置动态参数、统计数据，并切换状态至 playing。
        """
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.game_state = "playing" 
        self.last_game_result = None 
        self.sb.prep_images()
        self._reset_game_state() 
        pygame.mouse.set_visible(False)
        
        if self.sounds_loaded and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    def _reset_game_state(self):
        """重置场上实体状态 (Entities Reset)"""
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        """处理键盘按下事件"""
        # --- 状态控制：暂停/恢复 ---
        if event.key == pygame.K_ESCAPE:
            if self.game_state == "playing":
                self.game_state = "paused"
                pygame.mouse.set_visible(True)
            elif self.game_state == "paused":
                self.game_state = "playing"
                pygame.mouse.set_visible(False)
            
        # --- 游戏控制 ---
        if self.game_state == "playing":
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.ship.moving_right = True
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet() 
        
        # --- 全局退出 ---
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE and self.game_state == "menu":
            self._start_game()

    def _check_keyup_events(self, event):
        """处理键盘释放事件"""
        if self.game_state == "playing":
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.ship.moving_right = False
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.ship.moving_left = False

    def _fire_bullet(self):
        """实例化并发射一颗子弹"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            if self.sounds_loaded and self.sound_laser:
                self.sound_laser.play()

    def _update_bullets(self):
        """
        更新所有弹道物体的状态。
        包括：位置更新、越界清理、碰撞检测触发。
        """
        self.bullets.update()
        self.alien_bullets.update()
        
        # 内存优化：移除屏幕外的子弹 (Garbage Collection equivalent)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        self._check_bullet_ship_collisions()

    def _check_bullet_alien_collisions(self):
        """处理 [玩家子弹] vs [外星人] 的碰撞"""
        # groupcollide 返回字典，True, True 表示碰撞双方均消失
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            if self.sounds_loaded and self.sound_explosion:
                self.sound_explosion.play()
            # 计分逻辑 (支持一次击穿多个)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # --- 关卡进度检查 ---
        if not self.aliens:
            # 清场逻辑：下一波
            self.bullets.empty()
            self.alien_bullets.empty()
            self.settings.increase_speed() # 难度提升
            self.stats.level += 1
            self.sb.prep_level()

            if self.stats.level > self.win_level:
                self._game_win()
            else:
                self._create_fleet()

    def _game_win(self):
        """处理胜利状态"""
        self.game_state = "game_win"
        self.last_game_result = "win"
        pygame.mouse.set_visible(True)
        
        if self.sounds_loaded:
            pygame.mixer.music.stop()
            if self.sound_win:
                self.sound_win.play()

    def _check_bullet_ship_collisions(self):
        """处理 [敌方子弹] vs [玩家飞船] 的碰撞"""
        collisions = pygame.sprite.spritecollide(
            self.ship, self.alien_bullets, True)
        if collisions:
            self._ship_hit(damage=15)

    def _ship_hit(self, damage=10):
        """
        玩家受击处理逻辑 (Damage Calculation)
        -----------------------------------
        实现了护盾优先的伤害计算模型：
        1. 优先扣除护盾 (Shield)。
        2. 护盾不足时，溢出伤害 (Overflow Damage) 由生命值 (Health) 承担。
        """
        if self.stats.current_shield > 0:
            self.stats.current_shield -= damage
            if self.stats.current_shield < 0:
                # 计算溢出伤害
                overflow = abs(self.stats.current_shield)
                self.stats.current_shield = 0
                self.stats.current_health -= overflow
        else:
            self.stats.current_health -= damage

        if self.sounds_loaded and self.sound_hit:
            self.sound_hit.play()

        # --- 死亡判定 ---
        if self.stats.current_health <= 0:
            if self.stats.ships_left > 0:
                # 复活逻辑
                self.stats.ships_left -= 1
                self.sb.prep_ships()        
                if self.sounds_loaded and self.sound_die:
                    self.sound_die.play()
                self._draw_resurrecting_msg() # 阻塞式绘制复活提示
                
                if self.sounds_loaded and self.sound_die:
                    sleep(self.sound_die.get_length()) 
                else:
                    sleep(1.0) 

                # 状态回滚
                self.stats.current_health = self.settings.max_health
                self.stats.current_shield = self.settings.max_shield
                self._reset_game_state()
                
                sleep(0.5)
            else:
                # 彻底失败逻辑
                if self.sounds_loaded:
                    pygame.mixer.music.stop()
                    if self.sound_gameover:
                        self.sound_gameover.play()
                
                self.game_state = "game_over"
                self.last_game_result = "lose"
                pygame.mouse.set_visible(True)

    def _draw_resurrecting_msg(self):
        """绘制复活过渡帧"""
        self.screen.blit(self.game_bg_image, (0, 0))
        self.aliens.draw(self.screen)
        self.ship.blitme()
        self.sb.show_score()
        
        font = pygame.font.Font(self.font_name, 80) if self.font_name else pygame.font.SysFont(None, 80)
        try:
            msg = font.render("复活中......", True, (255, 50, 50))
        except pygame.error:
            msg = pygame.font.SysFont(None, 80).render("Resurrecting...", True, (255, 50, 50))
            
        rect = msg.get_rect()
        rect.center = self.screen.get_rect().center
        self.screen.blit(msg, rect)
        pygame.display.flip()

    def _update_aliens(self):
        """
        更新外星人集群的行为。
        包含：边缘检测、位置更新、随机射击决策。
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 蒙特卡洛方法模拟射击概率
        for alien in self.aliens.sprites():
            if random.random() < self.settings.alien_fire_probability:
                if len(self.alien_bullets) < 10: 
                    self.alien_bullets.add(AlienBullet(self, alien))

        # 物理碰撞：Ship vs Aliens
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit(damage=50)

        # 物理碰撞：Aliens reach bottom
        self._check_aliens_bottom()

    def _create_fleet(self):
        """算法生成外星人矩阵 (Matrix Generation)"""
        sample_alien = Alien(self)
        alien_width, alien_height = sample_alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """实例化单个外星人并定位"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        # 记录行索引，用于行级控制
        alien.row_index = row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """
        高级集群控制算法：
        检测哪些行触边，并只反转触边的行，而非整体反转。
        这增强了外星人行为的不可预测性。
        """
        rows_to_change = set()
        for alien in self.aliens.sprites():
            if alien.check_edges():
                rows_to_change.add(getattr(alien, "row_index", 0))

        for row_index in rows_to_change:
            self._change_row_direction(row_index)

    def _change_row_direction(self, row_index):
        """改变特定行的移动方向并下沉"""
        for alien in self.aliens.sprites():
            if getattr(alien, "row_index", None) == row_index:
                alien.rect.y += self.settings.fleet_drop_speed
                alien.row_direction *= -1

    def _check_aliens_bottom(self):
        """检查是否有外星人突破防线 (Reach Bottom)"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit(damage=100) # 致命伤害
                break

    def _update_screen(self):
        """
        渲染管线 (Render Pipeline)
        ------------------------
        根据当前 game_state 选择性地绘制图层。
        Drawing Order: Background -> Sprites -> HUD -> Overlays
        """
        # 背景层渲染
        if self.game_state == "playing" or self.game_state == "paused":
            self.screen.blit(self.game_bg_image, (0, 0))
        else: # menu, game_win, game_over
            self.screen.blit(self.menu_bg_image, (0, 0))
        
        # 实体层渲染
        self.aliens.draw(self.screen)
        self.ship.blitme()

        if self.game_state == "playing" or self.game_state == "paused":
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.alien_bullets.sprites():
                bullet.draw_bullet()
            
            # HUD 层渲染
            self.sb.show_score()
            
            # UI 覆盖层 (Overlay)
            if self.game_state == "paused":
                self._draw_pause_message()

        elif self.game_state == "menu":
            self._draw_menu()
        elif self.game_state in ["game_win", "game_over"]:
            self._draw_result_screen()

        # 双缓冲交换 (Double Buffering Flip)
        pygame.display.flip()

    def _draw_pause_message(self):
        """绘制暂停状态下的半透明遮罩与提示"""
        font = pygame.font.Font(self.font_name, 100) if self.font_name else pygame.font.SysFont(None, 100)
        try:
            msg = font.render("游戏暂停", True, (255, 255, 255))
        except pygame.error:
            msg = pygame.font.SysFont(None, 100).render("PAUSED", True, (255, 255, 255))
            
        rect = msg.get_rect()
        rect.center = self.screen.get_rect().center
        
        # 创建 Alpha 通道表面实现半透明效果
        s = pygame.Surface((self.settings.screen_width, self.settings.screen_height), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128)) # RGBA, Alpha=128
        self.screen.blit(s, (0, 0))
        
        self.screen.blit(msg, rect)
        
    def _draw_menu(self):
        """绘制主菜单"""
        self.ship.update() # 在背景中保持动态
        self.aliens.update()
        
        self.play_button.draw_button()
        pygame.mouse.set_visible(True)

    def _draw_result_screen(self):
        """绘制结算屏幕 (Win/Loss)"""
        font_msg = pygame.font.Font(self.font_name, 60) if self.font_name else pygame.font.SysFont(None, 60)
        
        if self.last_game_result == "win":
            try:
                msg_text = font_msg.render("胜利！地球活下来了！", True, (0, 200, 0))
            except pygame.error:
                msg_text = pygame.font.SysFont(None, 60).render("Victory! Earth survived!", True, (0, 200, 0))
                
        elif self.last_game_result == "lose":
            try:
                msg_text = font_msg.render("游戏结束！地球沦陷了！", True, (200, 0, 0))
            except pygame.error:
                msg_text = pygame.font.SysFont(None, 60).render("Game Over! Earth fell!", True, (200, 0, 0))
                
        msg_rect = msg_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 - 50))
        self.screen.blit(msg_text, msg_rect)
        self.btn_restart.draw_button()
        self.btn_return.draw_button()
        pygame.mouse.set_visible(True)

if __name__ == '__main__':
    # 程序入口点
    ai = AlienInvasion()
    ai.run_game()