
from pickle import TRUE
import sys
import pygame
from bullet import Bullet
from alien import Alien
from star import Star
from random import randint
from time import sleep
from pygame.sprite import Group


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, stars, play_button):
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    # Все пули выводятся позади изображений корабля и пришельцев.
    stars.draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
        
    ship.blitme()
    
    
        # Удаление пуль, вышедших за край экрана.
    aliens.draw(screen)
    

    #Отоюражение последнего прорисованного экрана.
    pygame.display.flip()





# Звезды
def get_number_stars_x(ai_settings, star_width):
# """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * star_width
    number_stars_x = int(available_space_x / (2 * star_width))
    return number_stars_x

def get_number_rowsstar(ai_settings, star_height):
# """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (2 * star_height))
    number_rowsstar = int(available_space_y / (2 * star_height))
    return number_rowsstar

def create_stars(ai_settings, screen, stars, star_number, row_number_star):
# """Создает пришельца и размещает его в ряду."""
    star = Star(ai_settings, screen)
    star_width = star.rect.width * 3
    star.x = star_width + 2 * star_width * star_number
    star.rect.x = star.x + randint(-100 ,100)
    star.rect.y = star.rect.height + 2 * star.rect.height * row_number_star * 2 + randint(-100 ,100)
    stars.add(star)

def create_fleet_star(ai_settings, screen, ship, stars):
# """Создает флот пришельцев."""
# Создание пришельца и вычисление количества пришельцев в ряду.
    star = Star(ai_settings, screen)
    number_stars_x = get_number_stars_x(ai_settings, star.rect.width)
    number_rowsstar = get_number_rowsstar(ai_settings, star.rect.height)
    for row_number_star in range(number_rowsstar):
        for star_number in range(number_stars_x):
            create_stars(ai_settings, screen, stars, star_number, row_number_star)










# пришельцы

def get_number_aliens_x(ai_settings, alien_width):
# """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
# """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (4 * alien_height ) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
# """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    

def create_fleet(ai_settings, screen, ship, aliens):
# """Создает флот пришельцев."""
# Создание пришельца и вычисление количества пришельцев в ряду.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                    row_number)
# Создание первого ряда пришельцев.

def check_fleet_edges(ai_settings, aliens):
#"""Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break
def change_fleet_direction(ai_settings, aliens):
# """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
#"""Обрабатывает столкновение корабля с пришельцем."""
# Уменьшение ships_left.
    if stats.ships_left > 0:
# Уменьшение ships_left.
        stats.ships_left -= 1

# Пауза.
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    stats.ships_left -= 1
    sb.prep_ships()
    
# Очистка списков пришельцев и пуль.
    aliens.empty()
    bullets.empty()
# Создание нового флота и размещение корабля в центре.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
# Пауза.
    sleep(0.5)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
#"""Проверяет, добрались ли пришельцы до нижнего края экрана."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
# Происходит то же, что при столкновении с кораблем.
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            
            break


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
# """Обновляет позиции всех пришельцев во флоте."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens,
                            bullets)
    


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, stars):
# """Обработка коллизий пуль с пришельцами."""
# Удаление пуль и пришельцев, участвующих в коллизиях.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
            
    if len(aliens) == 0:
# Уничтожение существующих пуль и создание нового флота.
        bullets.empty()
        stars.empty()
        stats.level += 1
        sb.prep_level()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        create_fleet_star(ai_settings, screen, ship, stars)


# Обновляет позиции пуль и уничтожает старые пули.
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets, stars):
    # Обновление позиций пуль.
    bullets.update()
    
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets, stars)


def check_high_score(stats, sb):
# """Проверяет, появился ли новый рекорд."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        with open ('highscore.txt', 'w') as f:
            f.write(str(stats.high_score ))

def fire_bullet(ai_settings, screen, ship, bullets):
    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

# Реагирует на нажатие клавиши.
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_q:
        sys.exit()

# реагирует на отпуск клавишши.
def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship,aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
# """Запускает новую игру при нажатии кнопки Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.game_active = True
        # Сброс игровой статистики.
        sb.prep_score()
        sb.prep_ships()
        sb.prep_high_score()
        sb.prep_level()
# Очистка списков пришельцев и пуль.
        aliens.empty()
        bullets.empty()
# Создание нового флота и размещение корабля в центре.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

