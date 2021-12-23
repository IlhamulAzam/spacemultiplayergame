"""""
# another space game
import pygame
import sys

screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
background = pygame.image.load('backgroundSpace_01.1.png')

class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load('ship5.png')
        self.image = pygame.transform.scale(self.image, (90, 110))

        self.rect = self.image.get_rect(center=(screen_width/2, screen_height-200))

    def update(self):
        pygame.event.get()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.rect.y>0:

            self.rect.y-=2

        if keys[pygame.K_DOWN] and self.rect.y<650:
            self.rect.y+=2

        if keys[pygame.K_RIGHT] and self.rect.x<700:

            self.rect.x+=2

        if keys[pygame.K_LEFT] and self.rect.x>0:

            self.rect.x-=2

    def create_bullet(self):

        return Enemy_Bullet(self.rect.centerx, self.rect.centery)





class Enemy(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load('spiked ship 3. small.blue_.png')
        self.image = pygame.transform.scale(self.image, (90, 110))
        self.rect = self.image.get_rect(center = (screen_width/2, screen_height-600))

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def create_bullet(self):
        return Spaceship_Bullet(self.rect.centerx+11, self.rect.centery+15 )
        #return Spaceship_Bullet(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])




class Spaceship_Bullet(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image,(30, 50 ))

        self.rect = self.image.get_rect(center= (pos_x, pos_y))

    def update(self):
        self.rect.y+=5

        if self.rect.y>800:
            self.kill()

class Enemy_Bullet(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):

        super().__init__()

        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect(center= (pos_x, pos_y))

    def update(self):

        self.rect.y -= 5

        #if self.rect.y<0:
            # self.kill()


enemy = Enemy()
enemy_group = pygame.sprite.Group()


spaceship = Spaceship()

spaceship_group = pygame.sprite.Group()
enemy_bullet_group = pygame.sprite.Group()
another_bullet_group = pygame.sprite.Group()

spaceship_group.add(spaceship)
enemy_group.add(enemy)

pygame.mouse.set_visible(False)

keys = pygame.key.get_pressed()
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            enemy_bullet_group.add(enemy.create_bullet())

        








    screen.blit(background, (0, 0))
    spaceship_group.draw(screen)
    enemy_group.draw(screen)
    enemy_bullet_group.draw(screen)
    




    spaceship_group.update()
    enemy_group.update()
    enemy_bullet_group.update()
    

    pygame.display.flip()
"""''



import pygame, sys, random
from pygame import mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

explosion_sound = pygame.mixer.Sound('NenadSimic - Muffled Distant Explosion.wav')
laser_sound = pygame.mixer.Sound('laser1.wav')
laser_sound_enemy = pygame.mixer.Sound('laser1.wav')

explosion_sound.set_volume(5)
laser_sound.set_volume(0.1)
laser_sound_enemy.set_volume(0.01)

red = (255, 0, 0)
green = (0, 255, 0)

# SPACESHIP AND BULLELTS
class Player(pygame.sprite.Sprite):

    def __init__(self, health):
        super().__init__()

        self.image = pygame.image.load('DurrrSpaceShip.png')
        self.image = pygame.transform.scale(self.image, (50, 30))

        self.rect = self.image.get_rect(center = (screen_width/2 , screen_height/2))
        self.health_at_the_beginning = health
        self.health_remaining = health

    def update(self):
        # movements
        self.rect.center = pygame.mouse.get_pos()

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # health_bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 5), self.rect.width, 15))

        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 5), int(self.rect.width * (self.health_remaining / self.health_at_the_beginning)), 15))
        if self.health_remaining <=0:
            animation = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(animation)
            self.kill()


    def create_bullet(self):

        laser_sound.play()


        #return Bullets( pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1] )
        return Bullets(self.rect.centerx+11.5, self.rect.centery)



class Bullets(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))



    def update(self):

        self.rect.y -= 5

        if self.rect.y <0:

            self.kill()

        if pygame.sprite.spritecollide(self, object_group, True):
            self.kill()
            explosion_sound.play()

            #explosion_sound.play()
            animation = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(animation)

# TARGETS


class Objects(pygame.sprite.Sprite):

    def __init__(self, picture_path, pos_x, pos_y, health):
        super().__init__()

        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image, (30, 20))

        self.rect =  self.image.get_rect(center = (pos_x, pos_y))

        self.health_at_the_beginning = health
        self.health_remaining = health

    def update(self ):


        self.rect.y += 2

        if self.rect.y>800:
            self.rect.y = 0

        if self.rect.x>800:

            self.rect.x = 0

        if self.health_remaining == 0:
             animation = Explosion(self.rect.x, self.rect.y)
             explosion_group.add(animation)

             self.kill()




# enemy bullets
class Enemy_Bullets(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y):
        super().__init__()

        self.image = pygame.image.load('laserBullet.png')
        self.image = pygame.transform.scale(self.image, (30, 20))
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self):
        #laser_sound_enemy.play()
        self.rect.y += 10
        killing = False

        if self.rect.y > 800:

            self.kill()

        if pygame.sprite.spritecollide(self, player_group, killing):
            self.kill()
            explosion_sound.play()
            player.health_remaining -= 0.1

            animation = Explosion(self.rect.x, self.rect.y)
            explosion_group.add(animation)


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


bullet_group = pygame.sprite.Group()
bullets = Bullets( pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
screen_width, screen_height = 800, 800



screen = pygame.display.set_mode((screen_width, screen_height))
#background = pygame.image.load('space1.png')


player = Player(3)
player_group = pygame.sprite.Group()
player_group.add(player)

#enemy_bullets = pygame.sprite.Group()



#explosion_group = pygame.sprite.Group()
#object_group = pygame.sprite.Group()


# enemy spaceships

"""""
for objects in range(3):

    enemy = Objects('DurrrSpaceShipcopy.png', random.randint(0, screen_width),random.randint(0, screen_height), 3)
    Giant = Objects('Transforming fighter ship 1_061.png' , random.randint(0, screen_width), random.randint(0, screen_height),3)
    giant = Objects('Transforming fighter ship 1_001.png', random.randint(0, screen_width), random.randint(0, screen_width), 3)
    giant1 = Objects('Transforming fighter ship 1_027.png', random.randint(0, screen_width), random.randint(0, screen_height),3)
    object_group.add(enemy)
    object_group.add(Giant)
    object_group.add(giant)
    object_group.add(giant1)
"""""


pygame.mouse.set_visible(False)



frame_rate = pygame.time.Clock()
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet_group.add(player.create_bullet())
        """""
        if True:

            attacking_ship = random.choice(object_group.sprites())
            alien_bullet = Enemy_Bullets(attacking_ship.rect.centerx +9, attacking_ship.rect.bottom)
            enemy_bullets.add(alien_bullet)
        """""
    screen.blit(background, (0, 0))


    object_group.draw(screen)

    player_group.draw(screen)
    bullet_group.draw(screen)
    enemy_bullets.draw(screen)
    explosion_group.draw(screen)


    player_group.update()
    bullet_group.update()
    object_group.update()
    enemy_bullets.update()
    explosion_group.update()



    frame_rate.tick(200)
    pygame.display.flip()






