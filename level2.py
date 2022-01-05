#Ben Wilson
#May 10
#File for level 2 of "Spaced Out"

import pygame, os, random, time,Util
from pygame.locals import *

WIDTH = 800 #Games width
HEIGHT = 600 #Games height
BOSS = "boss2.png"  #Image for the boss sprite
ENEMY ="enemy2.png" #Image for the enemy sprite's



class Mobs(pygame.sprite.Sprite):
    """An instance of a second level enemy"""
    def __init__(self):
        """ Constructor. Create all attributes and initialize the enemy. """
        pygame.sprite.Sprite.__init__(self)
        mobimage = Util.load_image(ENEMY)
        self.image = mobimage   #The sprite image  
        self.rect = self.image.get_rect() #The sprites rectangle
        self.rect.centerx = random.randrange(WIDTH)
        self.rect.bottom = -5
        self.speed = 8 #The speed
        self.health = 4  #The enemy's health
        
    def update(self):
        """Updates the enemy's movement"""
        self.rect.bottom += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Boss2(pygame.sprite.Sprite):
    """An instance of the second level boss"""
    def __init__(self,player):
        """ Constructor. Create all attributes and initialize the boss """

        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(BOSS)  #The sprite image  
        self.rect = self.image.get_rect()  #The sprites rectangle
        self.rect.centerx = WIDTH/2
        self.health = 50  #The boss's health
        self.rect.bottom = -20 
        self.speed = 3 #The boss's speed 
        self.player = player
    def update(self):
        """Updates the boss's movement"""
        if self.rect.centery < 0:
            self.rect.centery += self.speed
            self.health = 50
        else:
            if self.rect.centerx < self.player.rect.centerx and self.rect.right != WIDTH:
                self.rect.centerx += self.speed
            elif self.rect.left > 0:
                self.rect.centerx -= self.speed
            if self.rect.centery < self.player.rect.centery and self.rect.bottom != HEIGHT:
                self.rect.centery += self.speed
            elif self.rect.top > 0:
                self.rect.centery -= self.speed



class Level2():
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self,points,lives):
        """ Constructor. Create all our attributes and initialize
        the game. The stats provided customize the game. """
        self.points = points  #The points
        self.lives = lives   #The lives

        self.level_over = False  #Boolean that controls whether the level is over or not

        self.bossspawn = False #Boolean that contorls whether the boss has spawned
        self.startboss = 40 #Time untill the boss spawns

        self.startmobtime = time.time()   #The timer for when new enemies spawn
        self.bosstimer = time.time()   #The timer for when the boss will spawn
                      
        
        self.newmob = 0.8  #The time until new enemeies spawn
        self.initialmobs = 3    #The initial amount of enemies


        
        self.mobs = pygame.sprite.Group()  #Group containing the enemies
        
    def run_logic(self,player,shots,musicPlaying,impact,damage,all_sprites):
        """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
        if not self.level_over:
            
            if not self.bossspawn:
                endmobtime = time.time() #Ends the timer for new enemies to spawn
                if endmobtime - self.startmobtime >= self.newmob:
                    for i in range(self.initialmobs):
                        amob = Mobs()
                        if pygame.sprite.spritecollide(amob, self.mobs, False):
                            while pygame.sprite.spritecollide(amob, self.mobs, False):
                                amob = Mobs() #A single mob  
                        self.mobs.add(amob)
                        all_sprites.add(amob)
                    self.startmobtime = time.time()
                    
            if not self.bossspawn:
                mob_hit_list = pygame.sprite.groupcollide(self.mobs,shots, False,impact) #List of collisions between enemies and the player's shots
                for amob in mob_hit_list:
                    Util.eplo(musicPlaying,all_sprites,amob)
                    amob.health -= damage
                    if amob.health <= 0:
                        amob.kill()
                        self.points += 300
                playerhits = pygame.sprite.spritecollide(player, self.mobs, True)   #List of collisions between the player and the enemies

                endbosstime = time.time()   #Ends the timer for the boss to spawn
                if endbosstime - self.bosstimer>= self.startboss:
                    self.bossspawn = True
                    self.boss = Boss2(player)  #The boss
                    shots.empty()
                    self.mobs.empty()
                    all_sprites.empty()
                    all_sprites.add(player)
                    all_sprites.add(self.boss)
                    pygame.time.wait(500)

                
            else:
                playerhits = pygame.sprite.collide_rect(player, self.boss) #List of collisions between the player and the boss
                
                boss_hit_list = pygame.sprite.spritecollide(self.boss,shots,True) #List of collisions between the boss and the player's shots
                if boss_hit_list:
                    self.boss.health -= damage
                    self.points += 100
                    Util.eplo(musicPlaying,all_sprites,self.boss)
                if self.boss.health <= 0:
                    self.points += 1000
                    self.boss.kill()
                    all_sprites.empty()
                    all_sprites.add(player)
                    self.level_over = True  
    
            if playerhits:
                Util.eplo(musicPlaying,all_sprites,player)
                self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
    def display_frame(self, windowSurface,red):
        """ Display everything to the screen for the game. """
        if self.bossspawn and self.boss.health > 0:
            pygame.draw.rect(windowSurface,red,(50,50,20,4*self.boss.health),0)        




