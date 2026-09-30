"""
GameEngine: owns the targets and handles player clicks.

Starter version: a few static targets that respawn elsewhere when
clicked (correctly or not, depending on the hit-detection bug) - no
movement, no score/combo, no timer yet. That's Tasks 2-4.
"""

import random
import pygame

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT

NUM_TARGETS = 3
TARGET_RADIUS = 28


class GameEngine:
    def __init__(self):
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 0
        self.time_limit = 30
        self.time_left = 30
        self.round_active = True
        self.round_start_time = pygame.time.get_ticks()

    

    def _random_target(self):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)
        speed = random.choice([1, 3, 5])
        direction_x = random.choice([-1, 1])
        direction_y = random.choice([-1, 1])

        return Target(
        x,
        y,
        radius=TARGET_RADIUS,
        speed_x=speed * direction_x,
        speed_y=speed * direction_y
)

    def handle_click(self, pos):
        if not self.round_active:
            return
        target = check_hit(self.targets, pos)
        
        if target is not None:
            self.hits += 1

    # Increase combo first, then award points
            self.combo += 1
            self.score += 10 * self.combo

            self.targets.remove(target)
            self.targets.append(self._random_target())

        else:
            self.misses += 1

            # A miss breaks the combo
            self.combo = 0

    def update(self):
        if not self.round_active:
            return

        for target in self.targets:
            target.update(WIDTH, HEIGHT)

        elapsed = pygame.time.get_ticks() - self.round_start_time
        self.time_left = max(0, self.time_limit - elapsed / 1000)

        if self.time_left <= 0:
            self.time_left = 0
            self.round_active = False

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)
        renderer.draw_text(    
    surface,
    font,
    f"{self.score}  Combo: x{max(1, self.combo)}  Time: {int(self.time_left)}",
    (10, 10))

        if not self.round_active:
            renderer.draw_text(
                surface,
                font,
                f"ROUND OVER! Final Score: {self.score}",
                (200, 250)
        )
            renderer.draw_text(
            surface,
            font,
            "Press R to start a new round",
            (200, 290)
)

    def restart_round(self):
        self.targets = [self._random_target() for _ in range(NUM_TARGETS)]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.combo = 0
        self.time_left = self.time_limit
        self.round_active = True
        self.round_start_time = pygame.time.get_ticks()