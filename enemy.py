# enemy.py
import pygame
from random import *

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("image/enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.width,self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.rect.left,self.rect.bottom = randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)
        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("image/enemy1_destory1.png").convert_alpha(),\
            pygame.image.load("image/enemy1_destory2.png").convert_alpha(),\
            pygame.image.load("image/enemy1_destory3.png").convert_alpha(),\
            pygame.image.load("image/enemy1_destory4.png").convert_alpha()])
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left,self.rect.bottom = randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)

class MidEnemy(pygame.sprite.Sprite):
    energy = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), randint(-10 * self.height, -self.height)
        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("image/enemy2_destory1.png").convert_alpha(),\
            pygame.image.load("image/enemy2_destory2.png").convert_alpha(),\
            pygame.image.load("image/enemy2_destory3.png").convert_alpha(),\
            pygame.image.load("image/enemy2_destory4.png").convert_alpha()])
        self.energy = MidEnemy.energy
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left,self.rect.bottom = randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)
        self.energy = MidEnemy.energy

class BigEnemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/enemy3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.rect.left, self.rect.bottom = randint(0, self.width - self.rect.width), randint(-15 * self.height, -5*self.height)
        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("image/enemy3_destroy1.png").convert_alpha(),\
            pygame.image.load("image/enemy3_destroy2.png").convert_alpha(),\
            pygame.image.load("image/enemy3_destroy3.png").convert_alpha(),\
            pygame.image.load("image/enemy3_destroy4.png").convert_alpha(),\
            pygame.image.load("image/enemy3_destroy5.png").convert_alpha(),\
            pygame.image.load("image/enemy3_destroy6.png").convert_alpha()])
        self.energy = BigEnemy.energy
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.rect.left,self.rect.bottom = randint(0, self.width - self.rect.width), randint(-5 * self.height, 0)
        self.energy = BigEnemy.energy

