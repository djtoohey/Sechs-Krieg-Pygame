#Sechs Krieg
# Python Game Basic
import pygame
import random
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from pygame.sprite import spritecollideany
pygame.init()
pygame.display.init()

class Player(pygame.sprite.Sprite):
    def __init__(self, player_hp, player_speed):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()

        self.hp = player_hp
        self.speed = player_speed

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -(self.speed))
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
            # print("DOWN")
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-(self.speed), 0)
            # print("LEFT")
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip((self.speed), 0)
            # print("RIGHT")

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, id):
        super(Enemy, self).__init__()
        self.id = id
        self.surf = pygame.Surface((20,10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH+20, WIDTH+100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = random.randint(1,5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

WIDTH, HEIGHT = 800, 800

screen = pygame.display.set_mode((WIDTH, HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

player1 = Player(10, 1)

enemies = pygame.sprite.Group()
enemy_counter = 0

all_sprites = pygame.sprite.Group()
all_sprites.add(player1)

# MAIN CONTROLLER
running = True
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy(enemy_counter)
            enemy_counter+=1
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    
    screen.fill((0, 0, 0))
    
    pressed_keys = pygame.key.get_pressed()
    player1.update(pressed_keys)
    enemies.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # UP TO HERE IT WORKS
    for enemy in enemies:
        if pygame.Rect.colliderect(enemy.rect, player1):
            enemy.kill()
    # if pygame.sprite.spritecollideany(player1, enemies):
        
    #     player1.hp -= 1
       
    #     running = False

    pygame.display.flip()
    
pygame.quit()
