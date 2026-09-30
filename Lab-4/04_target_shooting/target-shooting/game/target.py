"""
Target: a circular target that moves around the play area.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70), speed_x=2, speed_y=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self, width, height):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x - self.radius <= 0 or self.x + self.radius >= width:
            self.speed_x *= -1

        if self.y - self.radius <= 0 or self.y + self.radius >= height:
            self.speed_y *= -1

    def get_bounding_rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )
