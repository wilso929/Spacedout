#Ben Wilson
#May 3
#File for level 1 of "Spaced Out"
import pygame, os, random, time,Util
from pygame.locals import *

WIDTH = 800 #Games width
HEIGHT = 600 #Games height


BOSS = "boss1.png"  #Image for the boss sprite
LASER ="energy.png" #Image for the boss's shots
ENEMY ="enemy.png"  #Image for the enemy sprite's


    
class Mobs(pygame.sprite.Sprite):
    """An instance of a first level enemy"""
    def __init__(self):
        """ Constructor. Create all attributes and initialize the enemy. """
        pygame.sprite.Sprite.__init__(self)
        self.image =Util.load_image(ENEMY) #The sprite image  
        self.rect = self.image.get_rect()  #The sprites rectangle
        self.rect.centerx = random.randrange(WIDTH)
        if self.rect.centerx <= 0 or self.rect.centerx >= WIDTH:
            while self.rect.centerx <= 0 or self.rect.centerx >= WIDTH:
                self.rect = self.image.get_rect()
        self.rect.bottom = -5
        self.speed = random.randrange(5,10)     #The speed
        
    def update(self):
        """Updates the enemy's movement"""
        self.rect.bottom += self.speed
        if self.rect.top > HEIGHT:
            self.kill()



class Boss1(pygame.sprite.Sprite):
    """An instance of the first level boss"""
    def __init__(self):
        """ Constructor. Create all attributes and initialize the boss """
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(BOSS)  #The sprite image
        self.rect = self.image.get_rect()  #The sprite rectangle
        self.rect.centerx = WIDTH/2
        self.health = 40                  #The boss's health
        self.rect.bottom = -20
        self.speedy = 2         #The boss's y speed
        self. speedx = 5      #The boss's x speed
    def update(self):
        """Updates the boss's movement"""
        if self.rect.top < 0:
            self.rect.top += self.speedy
            self.health = 40
        else:
            if self.rect.x <= 0 or self.rect.x >= WIDTH:
                self.rect.y += self.speedy
                self.speedx*=-1;
            self.rect.x += self.speedx;

        

class BossShoot(pygame.sprite.Sprite):
    """An instance of the boss's shots"""
    def __init__(self, x, y):
        """ Constructor. Create all attributes and initialize the shot """
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(LASER)   #The sprite image
        self.rect = self.image.get_rect()  #The sprite rectangle
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 5         #The shot's y speed
        self.speedx = random.randrange(-5,5)   #The shot's x speed
    def update(self):
        """Updates the shots movements"""
        self.rect.y += self.speedy
        self.rect.x += self.speedx

class Level1():
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self,points,lives):
        """ Constructor. Create all our attributes and initialize the level. """
        self.points = points     #The points
        self.lives = lives     #The lives

        self.level_over = False    #Boolean that controls whether the level is over or not
        self.bossspawn = False      #Boolean that contorls whether the boss has spawned
        self.bosstimer = time.time()    #The timer for when the boss will spawn
        self.startboss = 20             #Time untill the boss spawns

        self.startmobtime = time.time() #The timer for when new enemies spawn
        self.newmob = 1              #The time until new enemeies spawn
        self.initialmobs = 10      #The initial amount of enemies
        
        self.mobs = pygame.sprite.Group()   #Group containing all th enemies
 
        self.bossshots = pygame.sprite.Group()   #Group containing all the boss's shots
                      
    def run_logic(self,player,shots,musicPlaying,impact,damage,all_sprites):
        """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
        
        if not self.level_over:
            endmobtime = time.time()   #Ends the timer for new enemies to spawn
            if endmobtime - self.startmobtime >= self.newmob:
            #Spawns the enemy or boss shots when the timer runs out
                if not self.bossspawn:
                    for i in range(self.initialmobs):
                        amob = Mobs()   #A single mob
                        self.mobs.add(amob)
                        all_sprites.add(amob)
                    self.startmobtime = time.time()
                else:   
                    for i in range(self.initialmobs):
                        bshot = BossShoot(self.boss.rect.centerx,self.boss.rect.centery)
                        self.bossshots.add(bshot)
                        all_sprites.add(bshot)
                    self.startmobtime = time.time()

                    
            if not self.bossspawn:
                mob_hit_list = pygame.sprite.groupcollide(shots, self.mobs,impact,True)   #List of collisions between enemies and the player's shots
                for amob in mob_hit_list:
                #Damagest the enemies when hit
                    self.points += 100
                    Util.eplo(musicPlaying,all_sprites,amob)
                    
                playerhits = pygame.sprite.spritecollide(player, self.mobs, True) #List of collisions between the player and the enemies
                if playerhits:
                #Damages the player when hit
                    Util.eplo(musicPlaying,all_sprites,player)
                    self.lives -= 1

                endbosstime = time.time()   #Ends the timer for the boss to spawn
                if endbosstime - self.bosstimer>= self.startboss:
                    self.initialmobs = 3
                    self.bossspawn = True
                    self.boss = Boss1()  #The boss
                    shots.empty()
                    self.mobs.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(self.boss)
                    pygame.time.wait(500)

            else:
                playerhits = pygame.sprite.collide_rect(player, self.boss)      #List of collisions between the player and the boss
                playerhits2 = pygame.sprite.spritecollide(player, self.bossshots,True)  #List of collisions between the player and the boss's shots
                if playerhits or playerhits2:
                #Damages the player when hit
                    Util.eplo(musicPlaying,all_sprites,player)
                    self.lives -= 1

    
                boss_hit_list = pygame.sprite.spritecollide(self.boss,shots,True)  #List of collisions between the boss and the player's shots
                if boss_hit_list:
                #Damages the boss when hit
                    self.boss.health -= damage
                    self.points += 100
                    Util.eplo(musicPlaying,all_sprites,self.boss)
                if self.boss.health <= 0:
                #Kills the boss when it's health hits zero
                    self.points += 1000
                    self.boss.kill()
                    all_sprites.empty()
                    all_sprites.add(player)
                    self.level_over = True


            if self.lives <= 0:
                self.game_over = True

    def display_frame(self, windowSurface,red):
        """ Display everything to the screen for the game. """
        if self.bossspawn and self.boss.health > 0:
        #Displays the boss's health bar
            pygame.draw.rect(windowSurface,red,(50,50,20,4*self.boss.health),0)        




