# myplane.py
import pygame

class Myplane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/me.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size[0], bg_size[1]
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        #初始化飞机位于下方中间位置
        #下方预留约60像素位置作为"状态栏"
        self.rect.left, self.rect.top = (self.width - self.rect.width)/2,self.height - self.rect.height - 60
        self.speed = 10
        self.destory_images = []
        self.destory_images.extend([\
            pygame.image.load("image/me_destroy1.png").convert_alpha(),\
            pygame.image.load("image/me_destroy2.png").convert_alpha(),\
            pygame.image.load("image/me_destroy3.png").convert_alpha(),\
            pygame.image.load("image/me_destroy4.png").convert_alpha()])
        

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.top = 0
    def moveDown(self):
        if self.rect.bottom<self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60
    def moveLeft(self):
        if self.rect.left>0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
    #def reset(self):



