from random import randint
from typing import Any
import pygame

HEIGHT = 700
WIDTH = 1200
SIZE = (WIDTH, HEIGHT)
FPS = 60

lost = 0
score = 0
monsters_num = 5

window = pygame.display.set_mode(SIZE)

clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load("galaxy.jpg"), SIZE)

pygame.mixer.init()
pygame.mixer.music.load("space.ogg")
pygame.mixer.music.play()

fire_sfx = pygame.mixer.Sound("fire.ogg")

pygame.font.init()
font_big = pygame.font.Font(None, 70)
font_medium = pygame.font.Font(None, 70)
font_small = pygame.font.Font(None, 70)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, coords: tuple[int,int], speed:int, size:tuple[int, int]):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (size))
        self.rect = self.image.get_rect()
        self.rect.center = coords 
        self.speed = speed

    def reset(self):
        window.blit(self.image, self.rect.topleft)

class Player(GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if self.rect.x < WIDTH:
                self.rect.x += self.speed
            else:
                self.rect.x = WIDTH

        if keys[pygame.K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
            else:
                self.rect.x = WIDTH

    def fire(self):
            new_bullet = Bullet("bullet.png", (self.rect.centerx, self.rect.top), 7, (10, 15))
            bullets.add(new_bullet)
            fire_sfx.play()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom >= HEIGHT:
            self.rect.y = 0
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

player = Player('rocket.png', (WIDTH/2, HEIGHT - 50), 10, (75, 100))
#test_enemy = Enemy("ufo.png", (randint(50, WIDTH-50), 0), 4, (75, 50))
monsters = pygame.sprite.Group()

for i in range(monsters_num):
    new_enemy = Enemy("ufo.png", (randint(50, WIDTH-50), 0), randint(2, 5), (75, 50))
    monsters.add(new_enemy)

bullets = pygame.sprite.Group()


game = True
finish = False

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()
    if not finish:
        window.blit(background, (0, 0))
        player.reset()
        player.update()    
        monsters.update()
        monsters.draw(window)  
        bullets.update()
        bullets.draw(window)
        text_lost = font_medium.render("Пропущено: " + str(lost), True, (255, 255, 255))
        text_score = font_medium.render("Збито: " + str(score), True, (255, 255, 255))
        
        window.blit(text_score, (0, 0))
        window.blit(text_lost, (0, 40))



    pygame.display.update()
    clock.tick(FPS)