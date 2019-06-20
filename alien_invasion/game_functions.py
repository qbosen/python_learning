import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet

direction_keys = {pygame.K_UP: 'up', pygame.K_DOWN: 'down', pygame.K_LEFT: 'left', pygame.K_RIGHT: 'right'}


def check_events(ai_settings, screen, stats, sb, play_button, ship, bullets, aliens):
    """响应按键和鼠标事件"""
    # 定义按键映射关系
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            __check_key_down(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            __check_key_up(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            __check_play_button(ai_settings, screen, ship, aliens, bullets, stats, sb, play_button, mouse_x, mouse_y)


def __check_play_button(ai_settings, screen, ship, aliens, bullets, stats, sb, play_button, mouse_x, mouse_y):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        # 重制记分板
        sb.prep_high_score()
        sb.prep_score()
        sb.prep_level()
        ai_settings.initialize_dynamic_settings()
        __reset_game_elements(ai_settings, screen, ship, aliens, bullets)


def __check_key_down(event, ai_settings, screen, ship, bullets):
    if event.key in direction_keys.keys():
        ship.moving_flag[direction_keys[event.key]] = True
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_SPACE:
        # 发射子弹，添加编组
        if len(bullets) < ai_settings.bullet_limit:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


def __check_key_up(event, ship):
    if event.key in direction_keys.keys():
        ship.moving_flag[direction_keys[event.key]] = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕图像，重绘图像"""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    # 绘制所有子弹
    # 没有image属性，无法直接使用 draw(screen)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 如果游戏没有激活，绘制 play 按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让重绘的屏幕可见
    pygame.display.flip()


def update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """更新子弹位置，删除界外子弹"""
    # 对编组调用update会自动调用每个元素的update方法
    bullets.update()
    # 删除所有屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 碰撞检测
    __check_bullet_alien_collisions(ai_settings, stats, sb, aliens, bullets, screen, ship)


def __check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def __check_bullet_alien_collisions(ai_settings, stats, sb, aliens, bullets, screen, ship):
    """碰撞检测,碰撞后删除对应的子弹和外星人"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        collision_number = 0
        for collision_alien in collisions.values():
            collision_number += len(collision_alien)
        stats.score += ai_settings.alien_points * collision_number
        sb.prep_score()
        __check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = int(ai_settings.screen_scale[0] / (2 * alien.rect.width)) - 1
    number_aliens_y = int((ai_settings.screen_scale[1] - ship.rect.height) / (2 * alien.rect.height)) - 1

    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            __create_alien(ai_settings, screen, aliens, alien_number, row_number)


def __create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """根据位置创建一个外星人"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    __check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens) or __check_aliens_bottom(screen, aliens):
        __lose_life(ai_settings, stats, sb, screen, ship, aliens, bullets)


def __check_aliens_bottom(screen, aliens):
    """检查是否有外星人到了最底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            return True
    return False


def __change_fleet_direction(ai_settings, aliens):
    """将外星人整体下移一排，改变水平移动方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def __check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            # 只要有一个外星人到达边缘，便整体移动一次
            __change_fleet_direction(ai_settings, aliens)
            break


def __lose_life(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """外星人撞击到飞船"""
    if stats.ship_lives <= 0:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    else:
        stats.ship_lives -= 1
        sb.prep_ships()
        __reset_game_elements(ai_settings, screen, ship, aliens, bullets)
        sleep(0.5)


def __reset_game_elements(ai_settings, screen, ship, aliens, bullets):
    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()
