#Sechs Krieg Pygame

# Imoprts
import pygame
import random
from pygame import constants
from pygame.constants import K_a, K_d, K_s, K_w
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

# initialize pygame and the display
pygame.init()
pygame.display.init()

# CLASS: Player
# PARAMS: Healthpoints/hp (player_hp), Player movement speed(player_speed) 
# ATTRS: RECTANGLE, HP, SPEED
class Player(pygame.sprite.Sprite):
    def __init__(self, player_hp, player_speed):
        super(Player, self).__init__()
        
        # CREATING PLAYER RECTANGLE 
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()

        # Setting HP and movement speed
        self.hp = player_hp
        self.movementSpeed = player_speed

    # movements
    # checks for key press, moves according to players movement speed
    def update(self, pressed_keys):
        centerOfPlayerX = (self.rect.left + self.rect.right)/2
        centerOfPlayerY = (self.rect.top + self.rect.bottom)/2

        # up
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -(self.movementSpeed))
        # down
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.movementSpeed)
        # left
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-(self.movementSpeed), 0)
        # right
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip((self.movementSpeed), 0)
        
        if pressed_keys[K_w]:
            print("x", centerOfPlayerX, ", y", centerOfPlayerY)
            bullet = Bullet(centerOfPlayerX, centerOfPlayerY, (255, 0, 0), -BULLET_SPEED)
            all_sprites.add(bullet)
        if pressed_keys[K_s]:
            bullet = Bullet(centerOfPlayerX, centerOfPlayerY, (0, 255, 0), BULLET_SPEED)
            all_sprites.add(bullet)
        if pressed_keys[K_a]:
            bullet = Bullet(centerOfPlayerX, centerOfPlayerY, (0, 0, 255), BULLET_SPEED)
            all_sprites.add(bullet)
        if pressed_keys[K_d]:
            bullet = Bullet(centerOfPlayerX, centerOfPlayerY, (255, 0, 255), BULLET_SPEED)
            all_sprites.add(bullet)
        # checking that the player cannot escape the display borders
        # left border
        if self.rect.left < 0:
            self.rect.left = 0
        # right border
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        # top border
        if self.rect.top <= 0:
            self.rect.top = 0
        # bottom border
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            
class Bullet(pygame.sprite.Sprite):
    def __init__(self, spawnPosX, spawnPosY, color, speed):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(
            center=(
                spawnPosX,
                spawnPosY
            )
        )

        self.speed = speed

        def update(self):
            # kills the bullet after it has left the screen
            # left border
            if self.rect.left < 0:
                self.kill()
            # right border
            if self.rect.right > WIDTH:
                self.kill()
            # top border
            if self.rect.top <= 0:
                self.kill()
            # bottom border
            if self.rect.bottom >= HEIGHT:
                self.kill()

# WIP
# CLASS: Enemy
# PARAMS: 
# ATTRS: movement speed, rectangle
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(WIDTH+20, WIDTH+100),
                random.randint(0, HEIGHT)
            )
        )
        self.speed = 1

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# declaring the width and height of the display
WIDTH, HEIGHT = 800, 800
BULLET_SPEED = 2
# setting the width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# custom event to add new enemies to the screen
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# creating an instance of the player
player = Player(10, 1)

# creating a group for all enemies to go into
enemies = pygame.sprite.Group()

# creating a sprite group for all sprites
all_sprites = pygame.sprite.Group()
# adding player to the sprites group
all_sprites.add(player)

# MAIN CONTROLLER
running = True
while running:
    for event in pygame.event.get():
        # check if escape is hit to quit
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        # if the quit button top right is clicked
        elif event.type == QUIT:
            running = False
        # creating a new enemy and adding it to the enemies and all_sprites sprite groups
        # elif event.type == ADDENEMY:
        #     new_enemy = Enemy()
        #     enemies.add(new_enemy)
        #     all_sprites.add(new_enemy)
        # if playerhp is <= 0, game over
        elif player.hp <=0:
            running = False

    # set background color to black
    screen.fill((0, 0, 0))
    
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()

    # adding all sprites to the display
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # checking enemy group to see if collision is detected with player
    for enemy in enemies:
        if pygame.Rect.colliderect(enemy.rect, player.rect):
            # removing the enemy that colided
            enemy.kill()
            # reducing the player's hp
            player.hp -=1

    # update display
    pygame.display.flip()
    
# exit pygame
pygame.quit()
