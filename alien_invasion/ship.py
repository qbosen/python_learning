import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船，设置初始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载图像，获取外矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        # 初始坐标
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 浮点坐标
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # 移动flag，用于连续移动
        self.moving_flag = {'up': False, 'down': False, 'left': False, 'right': False}

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据flag调整飞船位置"""
        for direction, flag in self.moving_flag.items():
            if flag:
                if direction == 'up' and self.bottom > self.rect.height:
                    self.bottom -= self.ai_settings.ship_speed_factor
                if direction == 'down' and self.bottom < self.screen_rect.bottom:
                    self.bottom += self.ai_settings.ship_speed_factor
                if direction == 'right' and self.center < self.screen_rect.right:
                    self.center += self.ai_settings.ship_speed_factor
                if direction == 'left' and self.center > 0:
                    self.center -= self.ai_settings.ship_speed_factor
        # 更新为整数坐标
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom
