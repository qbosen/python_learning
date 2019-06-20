import pygame
from pygame.sprite import Group

import game_functions as gf
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from settings import Settings
from ship import Ship


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(ai_settings.screen_scale)
    pygame.display.set_caption(ai_settings.caption)

    ship = Ship(ai_settings, screen)
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    bullets = Group()
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    stats.reset_stats()
    sb = Scoreboard(ai_settings, screen, stats)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, bullets, aliens)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, stats, sb, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


if __name__ == '__main__':
    run_game()
