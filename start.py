
import pygame
from pygame.sprite import Group
from setting import Settings
from ship import Ship
from alien import Alien
from star import Star
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard





import game_funcion as gf

def run_game():
    # Инициализирует игру и создает объект экрана.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    star = Star(ai_settings, screen)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    stars = Group()
    aliens = Group()
    gf.create_fleet_star(ai_settings, screen, ship, stars)
    gf.create_fleet(ai_settings, screen, ship, aliens)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
   
                                        
    while True:
        # Отслеживание событий клавиатуры и мыши.
        
        ship.update()
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
                                      
        screen.fill(ai_settings.bg_color)
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        ship.blitme()
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, stars)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, stars, play_button )

        
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()
run_game()