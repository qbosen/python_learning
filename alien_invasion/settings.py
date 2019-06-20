class Settings():
    """存储《外星人入侵》的所有设置"""

    def __init__(self):
        # 游戏相关设置
        self.caption = "Alien Invasion"
        self.screen_scale = (1200, 800)
        self.bg_color = (230, 230, 230)
        self.speedup_factor = 1.1
        self.score_factor = 1.5

        # 飞船相关设置
        self.ship_limit = 3

        # 子弹相关设置
        self.bullet_scale = (399, 15)
        self.bullet_color = (60, 60, 60)
        self.bullet_limit = 3

        # 外星人相关设置
        self.fleet_drop_speed = 10
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """动态设置"""
        self.ship_speed_factor = 3
        self.bullet_speed_factor = 4
        self.alien_speed_factor = 2
        # 1表示右移， -1表示左移
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_factor
        self.bullet_speed_factor *= self.speedup_factor
        self.alien_speed_factor *= self.speedup_factor
        self.alien_points = int(self.alien_points * self.score_factor)
