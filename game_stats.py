class GameStats:
    """跟踪游戏的统计数据"""
    def __init__(self, ai_game):
        """初始化统计数据"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能发生变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1