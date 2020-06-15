import pygame
from pygame.locals import *
import os
import random

pygame.init()

W, H = 800, 437
win = pygame.display.set_mode((W,H))
pygame.display.set_caption('Side Scroller Game!')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
bgX = 0
bgX2 = bg.get_width()
clock = pygame.time.Clock()

class Player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    fall = pygame.image.load(os.path.join('images', '0.png'))
    def __init__(self, x, width, height):
        self.x = x
        self.y = 313
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slide_count = 0
        self.jump_count = 0
        self.jump_height = 9
        self.run_count = 0
        self.slide_up = False
        self.falling = False
    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, 343))
        elif self.jumping:
            counter = self.jump_count/6 - 9
            if counter >= -9:
                neg = 1 if counter < 0 else -1
            self.y -= counter**2 * 0.11 * neg
            win.blit(self.jump[self.jump_count//18], (self.x, self.y))
            self.jump_count += 1
            if self.jump_count > 108:
                self.jump_count = 0
                self.jumping = False
                self.run_count = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slide_up:
            if self.slide_count < 20:
                self.y += 1
                self.hitbox = (self.x+ 4, self.y, self.width-24, self.height-10)
            elif self.slide_count == 80:
                self.y -= 19
                self.sliding = False
                self.slide_up = True
            elif self.slide_count > 20 and self.slide_count < 80:
                self.hitbox = (self.x, self.y + 3, self.width - 8, self.height - 35)

            if self.slide_count >= 110:
                self.slide_count = 0
                self.slide_up = False
                self.run_count = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slide_count//10], (self.x, self.y))
            self.slide_count += 1
        else:
            if self.run_count > 42:
                self.run_count = 0
            win.blit(self.run[self.run_count//6], (self.x,self.y))
            self.run_count += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)

class Saw(object):
    imgs = [pygame.image.load(os.path.join('images', 'SAW' + str(x) + '.png')) for x in range(4)]
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x, y, width, height)
        self.count = 0
    def draw(self, win):
        self.hitbox = (self.x + 5, self.y + 5, self.width - 10, self.height - 5)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.imgs[self.count//2], (64, 64)), (self.x, self.y))
        self.count += 1
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]: return True
        return False

class Spike(Saw):
    img = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self, win):
        self.hitbox = (self.x + 10, self.y, 28, 315)
        win.blit(self.img, (self.x, self.y))
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

def update_file():
    with open("scores.txt", "r") as f: last = int(f.readline())
    if last < int(score):
        with open("scores.txt", "w") as f:
            f.write(str(score))
            return score
    return last

# Actually this means continue the same game in a different screen
# if you remarked that game gets slow down after certain replays
# this is natural beccause if the number of screens the game gets slower
# Yeah, My Bad, But this is the only way I thought about doing it
def end_screen():
    global pause, objects, speed, score
    pause, objects, speed = 0, [], 30
    run = True
    while run:
        win.blit(bg, (0, 0))
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
                runner.falling = False
                runner.sliding = False
                runner.jumping = False
        huge_font = pygame.font.SysFont("comicsans", 92)
        prev_score = huge_font.render("Max Score: "+ str(update_file()), 1, (255, 255, 255))
        new_score = huge_font.render("Your Score: "+ str(score), 1, (255, 255, 255))
        win.blit(prev_score, (W/2 - prev_score.get_width()/2, 150))
        win.blit(new_score, (W/2 - new_score.get_width()/2, 240))
        pygame.display.update()
    score = 0

def redraw_window():
    font = pygame.font.SysFont("comicsans", 32)
    win.blit(bg, (bgX, 0))
    win.blit(bg, (bgX2, 0))
    runner.draw(win)
    text = font.render("Score: "+str(score), 1, (255, 255, 255))
    for obj in objects: obj.draw(win)
    win.blit(text, (700, 10))
    pygame.display.update()

pygame.time.set_timer(USEREVENT + 1, 500)
pygame.time.set_timer(USEREVENT + 2, 4000)
speed = 30
score = 0
run = True
runner = Player(200, 64, 64)
objects = []
pause = 0
fall_speed = 0
while run:
    keys = pygame.key.get_pressed()
    if pause > 0:
        pause += 1
        if pause > fall_speed * 2: end_screen()

    score = speed//5 - 6
    for obj in objects:
        if obj.collide(runner.hitbox):
            runner.falling = True
            if pause == 0:
                pause = 1
                fall_speed = speed

        if obj.x < -64: objects.pop(objects.index(obj))
        else: obj.x -= 1.4

    bgX -= 1.4
    bgX2 -= 1.4

    if bgX < bg.get_width() * -1: bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1: bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            run = False
        if event.type == USEREVENT + 1: speed += 1
        if event.type == USEREVENT + 2:
            randm = random.randrange(0, 2)
            if randm == 0: objects.append(Saw(810, 310, 64, 64))
            elif randm == 1: objects.append(Spike(810, 0, 48, 310))
    if runner.falling == False:
        if keys[pygame.K_UP]:
            if not runner.jumping: runner.jumping = True
        if keys[pygame.K_DOWN]:
            if not runner.sliding: runner.sliding = True

    clock.tick(speed)
    redraw_window()
