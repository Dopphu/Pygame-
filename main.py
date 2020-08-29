# main.py
import pygame
import sys
import traceback
import myplane
import bullet
import enemy
#import supply
from pygame.locals import *
from random import *

pygame.init()
bg_size = 480, 700
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战 demo")
background = pygame.image.load("image/bg.png").convert()
#载入游戏音乐
pygame.mixer.music.load("sound/game_music.mp3")
pygame.mixer.music.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/bullet.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/e3fly.wav")
enemy3_fly_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/e3down.wav")
enemy3_down_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/e1down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/e2down.wav")
enemy2_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def main():
    pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    e1_destory_index = 0
    e2_destory_index = 0
    e3_destory_index = 0
    me_destory_index = 0
    delay = 100
    running = True
    me = myplane.Myplane(bg_size)
    
    #游戏暂停
    paused = False
    paused_nor_image = pygame.image.load("image/paused_nor.png")
    paused_pressed_image = pygame.image.load("image/paused_pressed.png")
    resume_nor_image = pygame.image.load("image/resume_nor.png")
    resume_pressed_image = pygame.image.load("image/resume_pressed.png")
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left, paused_rect.top = bg_size[0] - paused_rect.width -10, 10
    #默认显示这个
    paused_image = paused_nor_image
    #分数字体
    score = 0
    score_font = pygame.font.Font("font/font.TTF",36)

    enemies = pygame.sprite.Group()
    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies,20)
    #生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,8)
    #生成敌方大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,4)
    #生成子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    #用于阻止重复打开记录文件
    recorded = False
    game_over_font = pygame.font.Font("font/font.TTF",48)
    again_image = pygame.image.load("image/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("image/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = paused_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = paused_nor_image

        if not paused:
            screen.blit(background,(0,0))
            #绘制得分
            #大，中，小 飞机毁灭时分别得到 10000，6000，1000 分
            score_text = score_font.render("Score:%s"%str(score),True,WHITE)
            screen.blit(score_text,(10,5))
            if not(delay%10):
                bullet1[bullet1_index].reset(me.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM
            #检测用户键盘的操作
            key_pressed = pygame.key.get_pressed()
            #移动我方飞机
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight() 
            #绘制我方飞机#screen.blit(me.image, me.rect)
            if me.active:
                screen.blit(me.image,me.rect)
            else:
                #毁灭
                me_down_sound.play()
                if not(delay % 3):
                    screen.blit(me.destory_images[me_destory_index],me.rect)
                    me_destory_index = (me_destory_index + 1) % 4
                    if me_destory_index == 0:
                        print("GAME OVER!")                                        # # # # # # ###
                        running = False##################################################################
            #绘制子弹                                                               # # # # # # ###
            for b in bullet1:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                #if b.rect.top < 0:
                #     b.reset(me.rect.midtop)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
                                score += 1000 #################################################################################
            #绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    #毁灭
                    if not(delay % 3):
                        if e1_destory_index == 1:
                            enemy1_down_sound.play()
                    #       print("e1down",each.rect)
                        screen.blit(each.destory_images[e1_destory_index],each.rect)
                        e1_destory_index = (e1_destory_index + 1) % 4
                        if e1_destory_index == 1:
                            enemy1_down_sound.stop()
                    #       print("e1stop",each.rect)
                            each.reset()
                            
            #绘制中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    #毁灭
                    if not(delay % 3):
                        if e2_destory_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destory_images[e1_destory_index],each.rect)
                        e2_destory_index = (e1_destory_index + 1) % 4
                        if e2_destory_index == 0:
                            enemy2_down_sound.stop()
                            each.reset()
                            score += 6000
                pygame.draw.line(screen,BLACK,(each.rect.left, each.rect.top - 5),(each.rect.right, each.rect.top - 5),2)
                energy_remain = each.energy/ enemy.MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5), (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),2)
            #绘制大型飞机
            for each in big_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                    #即将出现在画面中，播放音效
                    if each.rect.bottom >= -50:
                        enemy3_fly_sound.play(-1)
                else:
                    #毁灭
                    if not(delay % 3):
                        if e3_destory_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destory_images[e3_destory_index],each.rect)
                        e3_destory_index = (e3_destory_index + 1) % 6
                        if e3_destory_index == 0:
                            enemy3_down_sound.stop()
                            each.reset()
                            score += 10000
                pygame.draw.line(screen,BLACK,(each.rect.left, each.rect.top - 5),(each.rect.right, each.rect.top - 5),2)
                energy_remain = each.energy/ enemy.MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5), (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),2)

            #检测我方飞机是否被碰撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down:
                me.active = False
                for e in enemies_down:
                    e.active = False
        #绘制暂停图标
        screen.blit(paused_image, paused_rect)
        #screen.blit(background,(0,0))
        if not running:
            #背景音乐停止
            pygame.mixer.music.stop()
            #停止全部音效
            pygame.mixer.stop()
            if not recorded:
                recorded = True
                #读取历史最高分
                with open("record/recorded.txt",'r') as f:
                    record_score = int(f.read())
                #如果分数超记录则覆盖录入最高分数
                if score > record_score:
                    with open("record/recorded.txt",'w') as f:
                        f.write(str(score))
            #绘制结束画面
            record_score_text = score_font.render("Best: %d" % record_score, True, (255,255,255))
            screen.blit(background,(0,0))
            screen.blit(record_score_text,(50,50))
            gameover_text1 = game_over_font.render("Your Score", True, (255,255,255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (bg_size[0] - gameover_text1_rect.width)//2, bg_size[1] // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            gameover_text2 = game_over_font.render(str(score), True, (255,255,255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (bg_size[0] - gameover_text2_rect.width)//2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)
            again_rect.left, again_rect.top = (bg_size[0] - again_rect.width)//2, gameover_text2_rect.bottom + 50
            screen.blit(again_image,again_rect)
            gameover_rect.left, gameover_rect.top = (bg_size[0] - gameover_rect.width)//2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)
            pygame.display.flip()
            while True:
                #检测用户鼠标操作
                #如果按下鼠标左键
                if pygame.mouse.get_pressed()[0]:
                    #获取鼠标坐标
                    pos = pygame.mouse.get_pos()
                    #如果用户选择重新开始
                    if again_rect.left < pos[0] < again_rect.right and again_rect.top < pos[1] < again_rect.bottom:
                        #调用main()函数重新开始游戏
                        main()
                    #如果用户选择结束游戏
                    elif gameover_rect.left < pos[0] < gameover_rect.right and gameover_rect.top < pos[1] < gameover_rect.bottom:
                        pygame.quit()
                        sys.exit()
                    

        pygame.display.flip()
        delay += 1
        
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()



