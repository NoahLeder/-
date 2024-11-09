class Settings:
    def __init__(self):
        """初始化游戏设置"""
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #速度
        self.ship_speed = 15
        self.ship_limit = 3

        #子弹设置
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 60

        #外星人
        self.alien_speed = 1.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        #加快游戏节奏
        self.speedup_scale = 1.5
        self.initialize_dynamic_settings()
    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 10
        self.bullet_speed = 3
        self.alien_speed = 3
        self.fleet_direction = 1
        #设置积分
        self.alien_points = 50
    def increase_speed(self):
        """提高速度的值"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)
