import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top
        if self.y < 0:
            self.y = 0
            self.velocity_y *= -1

        # Bounce off bottom
        if self.y + self.height > self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
            self.velocity_y += random.choice([-1, 0, 1])
            return "paddle"
        elif self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            self.velocity_y += random.choice([-1, 0, 1])
            return "paddle"
        return None

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)
