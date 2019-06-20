import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """飞船发出的子弹"""

    def __init__(self, ai_settings, screen, ship):
        """在飞船的头部创建一个子弹对象"""
        super().__init__()
        self.screen = screen
        # 子弹没有图像，所以我们创建了一个矩形，定义坐标位置和矩形大小
        self.rect = pygame.Rect(0, 0, *ai_settings.bullet_scale)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 子弹的垂直位置，用小数表示
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
