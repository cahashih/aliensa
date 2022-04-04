class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self):
        """Инициализирует настройки игры."""
        # Параметры экрана
        self.screen_width = 1500
        self.screen_height = 1000
        self.bg_color = (0, 0, 0)
        self.ship_limit = 3

        
        self.bullet_width = 4
        self.bullet_height = 10
        self.bullet_color = 250, 250, 250
        self.bullets_allowed = 10
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.2
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
    def initialize_dynamic_settings(self):
# """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.alien_points = 50
        self.ship_speed_factor = 1.6
        self.bullet_speed_factor = 5
        self.alien_speed_factor = 2
# fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

    def increase_speed(self):
# """Увеличивает настройки скорости."""
        self.alien_points = int(self.alien_points * self.score_scale)
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
