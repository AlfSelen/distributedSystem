import pygame


# from utilities import *


class Player:
    def __init__(self, start_position, width, height, color=(255, 0, 0)):
        self.x, self.y = start_position
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x, self.y, width, height)
        self.velocity = 3

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.velocity
        if keys[pygame.K_UP]:
            self.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.y += self.velocity
        self.x += 1
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
