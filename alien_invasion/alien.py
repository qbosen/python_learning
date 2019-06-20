import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """外星人"""

    def __init__(self, ai_settings, screen):
        """初始化外星人，设置初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 初始化在屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储准确位置
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人处于屏幕边缘 返回 TRUE"""
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
