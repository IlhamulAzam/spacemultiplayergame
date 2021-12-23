
import pygame
import sys
import random
from pygame import mixer
# really significant
pygame.init()

# sound settings
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
explosion_sound = pygame.mixer.Sound('NenadSimic - Muffled Distant Explosion.wav')
laser_sound = pygame.mixer.Sound('laser1.wav')
laser_sound_enemy = pygame.mixer.Sound('laser1.wav')
explosion_sound.set_volume(5)
laser_sound.set_volume(0.1)
laser_sound_enemy.set_volume(0.01)

# screen and background settings
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('backgroundSpace_01.1.png')

# colors for health bar
red = (255, 0, 0)
green = (0, 255, 0)

# creating classes for objects
class Player1(pygame.sprite.Sprite):

    def __init__(self, health):
        super().__init__()

        self.image = pygame.image.load('ship5.png')
        self.image = pygame.transform.scale(self.image, (50, 30))

        self.rect = self.image.get_rect(center = (screen_width/2 , screen_height/2))

        self.health_at_the_start = health
        self.health_remaining = health


    def update(self):
        # movements
        self.rect.center = pygame.mouse.get_pos()

        self.mask = pygame.mask.from_surface(self.image)


        # health_bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 5), self.rect.width, 15))
        print(self.health_remaining)
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 5), int(self.rect.width * (
                        self.health_remaining / self.health_at_the_start)), 15))
        if self.health_remaining <= 0:
            explosion_sound.play()
            self.kill()

    def create_bullet(self):

        return Bullets(self.rect.centerx+11.5, self.rect.centery)


class Bullets(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):

        self.rect.y -= 5

        if pygame.sprite.spritecollide(self, player2_group, False, pygame.sprite.collide_mask):
            self.kill()
            animation = Explosion(self.rect.centerx, self.rect.top)
            explosion_group.add(animation)
            player2.health_remaining -= 0.1

        if pygame.sprite.spritecollide(self, companions2_group, True, pygame.sprite.collide_mask):
            animation = Explosion(self.rect.centerx, self.rect.top)
            explosion_group.add(animation)
            self.kill()

        if self.rect.y <0:
            self.kill()


# player 2  settings

class Player2(pygame.sprite.Sprite):

    def __init__(self, health):
        super().__init__()

        self.image = pygame.image.load('spiked ship 3. small.blue_.png')
        self.image = pygame.transform.scale(self.image, (50, 30))

        self.rect = self.image.get_rect(center = (screen_width/2 , screen_height/2))
        self.health_at_the_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()



    def update(self):
        self.mask = pygame.mask.from_surface(self.image)
        if pygame.sprite.spritecollide(self, player1_group, False, pygame.sprite.collide_mask):
            animation = Explosion(self.rect.centerx, self.rect.bottom)
            explosion_group.add(animation)
            player2.health_remaining -= 0.01
            player1.health_remaining-=0.01

        # movements
        cooldown = 100
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y>5:
            self.rect.y -=5

        if keys[pygame.K_DOWN] and self.rect.y<800:
            self.rect.y +=5

        if keys[pygame.K_RIGHT] and self.rect.x<800:

            self.rect.x +=5

        if keys[pygame.K_LEFT] and self.rect.x>0:

            self.rect.x-=5
        self.mask = pygame.mask.from_surface(self.image)

        # health_bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.top - 20), self.rect.width, 15))

        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.top - 20), int(self.rect.width * (
                    self.health_remaining / self.health_at_the_start)), 15))
        if self.health_remaining <= 0:
            explosion_sound.play()
            self.kill()

        time_now = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            bullet2 = Bullets2(self.rect.centerx+12, self.rect.bottom)
            laser_sound.play()
            bullet2_group.add(bullet2)
            self.last_shot = time_now

    def creating_bullets(self):
        return Bullets2(self.rect.centerx+11.5, self.rect.centery)


class Bullets2(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):

        self.rect.y +=5

        if pygame.sprite.spritecollide(self, player1_group, False, pygame.sprite.collide_mask):
            self.kill()
            animation = Explosion(self.rect.centerx, self.rect.bottom)
            explosion_group.add(animation)
            player1.health_remaining -= 0.1

        if pygame.sprite.spritecollide(self, companions1_group, True, pygame.sprite.collide_mask):
            animation = Explosion(self.rect.centerx, self.rect.bottom)
            companion1.health_remaining -= 1
            explosion_group.add(animation)
            self.kill()

        if self.rect.y > 800:
            self.kill()

# player 1 companions

class Player1_team(pygame.sprite.Sprite):

    def __init__(self, picture_path, pos_x, pos_y, health):
        super().__init__()

        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (30, 20))

        self.rect =  self.image.get_rect(center = (pos_x, pos_y))
        self.health_at_the_beginning = health
        self.health_remaining = health

    def update(self):

        self.rect.y -= 0.0000000000001

        if self.rect.y==0:

            self.rect.y = 800

        if self.health_remaining <= 0:
            self.kill()

        if pygame.sprite.spritecollide(self, player2_group, False, pygame.sprite.collide_mask):
            player2.health_remaining -= 0.5
            animation = Explosion(self.rect.centerx, self.rect.top)
            explosion_group.add(animation)
            self.kill()

# player 2 companions

class Player2_team(pygame.sprite.Sprite):

    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()

        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (30, 20))

        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        self.rect.y += 1

        if self.rect.y == 800:
            self.rect.y = 0

        if pygame.sprite.spritecollide(self, player1_group, False, pygame.sprite.collide_mask):
            player1.health_remaining -= 0.5
            animation = Explosion(self.rect.centerx, self.rect.bottom)
            explosion_group.add(animation)

            self.kill()


# companions1 bullets

class Companion1_bullets(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):

        self.rect.y -= 10

        if pygame.sprite.spritecollide(self, player2_group, False):
            self.kill()
            animation = Explosion(self.rect.centerx, self.rect.bottom)
            explosion_group.add(animation)

            player2.health_remaining -= 0.1

        if pygame.sprite.spritecollide(self, companions2_group, True):

            animation = Explosion(self.rect.centerx, self.rect.bottom)
            explosion_group.add(animation)

            self.kill()

        if self.rect.y < 0:
            self.kill()

# companion 2 bullets
class Companion2_bullets(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):

        self.rect.y += 10

        if pygame.sprite.spritecollide(self, player1_group, False):
            self.kill()
            animation = Explosion(self.rect.centerx, self.rect.top)
            explosion_group.add(animation)

            player1.health_remaining -= 0.1

        if pygame.sprite.spritecollide(self, companions1_group, True):

            animation = Explosion(self.rect.centerx, self.rect.top)
            explosion_group.add(animation)

            self.kill()

        if self.rect.y > 800:
            self.kill()

# explosion class
class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        self.explosions = []

        for num in range(1, 3):

            img = pygame.image.load('explo_tiao1_img4.png')
            img2 = pygame.image.load('explo_tiao1_img10.png')

            self.explosions.append(img)
            self.explosions.append(img2)

            self.index = 0

            self.image = self.explosions[self.index]
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.counter = 0


    def update(self):

        explosion_speed = 3

        # updating explosion animation

        self.counter+=1

        if self.counter >= explosion_speed and self.index< len(self.explosions)-1:

            self.counter = 0
            self.index+=1
            self.image = self.explosions[self.index]

        if self.counter>= explosion_speed and self.index>= len(self.explosions)-1:
            self.kill()

pygame.init()
player1 = Player1(3)
player1_group = pygame.sprite.Group()
player1_group.add(player1)
bullet1_group = pygame.sprite.Group()
pygame.mouse.set_visible(False)

player2 = Player2(3)
player2_group = pygame.sprite.Group()
player2_group.add(player2)
bullet2_group = pygame.sprite.Group()

# companion groups
companions1_group = pygame.sprite.Group()
companions2_group = pygame.sprite.Group()

# companion bullet groups

companion1bullet_group = pygame.sprite.Group()
companion2bullet_group = pygame.sprite.Group()


# explosion group

explosion_group = pygame.sprite.Group()

# conditions

running1 = 'True'
running2 = 'True'
# making small spaceships
for objects in range(20):
    companion1 = Player1_team('ship3.png', random.randint(0, screen_width), random.randint(600, screen_height), 3)
    companions1_group.add(companion1)

for objects in range(20):
    companion2 = Player2_team('ship2.png', random.randint(0, screen_width), random.randint(0, 800))
    companions2_group.add(companion2)


going = 'True'
keys = pygame.key.get_pressed()

while True:
    if len(companions1_group) == 0:
        running1 = 'False'

    if len(companions2_group) == 0:
        running2 = 'False'

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            laser_sound.play()
            bullet1_group.add(player1.create_bullet())

        if running1 == 'True':
            companion1_ship = random.choice(companions1_group.sprites())
            companion1_bullet = Companion1_bullets(companion1_ship.rect.centerx + 9, companion1_ship.rect.top)
            companion1bullet_group.add(companion1_bullet)

        if running2 == 'True':

            companion2_ship = random.choice(companions2_group.sprites())
            companion2_bullet = Companion2_bullets(companion2_ship.rect.x+23, companion2_ship.rect.bottom)
            companion2bullet_group.add(companion2_bullet)

    screen.blit(background, (0, 0))
    player1_group.draw(screen)
    bullet1_group.draw(screen)
    player2_group.draw(screen)
    bullet2_group.draw(screen)
    companions1_group.draw(screen)
    companions2_group.draw(screen)
    companion1bullet_group.draw(screen)
    companion2bullet_group.draw(screen)
    explosion_group.draw(screen)

    player1_group.update()
    player2_group.update()
    bullet1_group.update()
    bullet2_group.update()
    companions1_group.update()
    companions2_group.update()
    companion1bullet_group.update()
    companion2bullet_group.update()
    explosion_group.update()

    pygame.display.update()
    pygame.display.flip()








