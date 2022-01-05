#Ben Wilson
#May 17
#The file for level 3 of "Spaced Out"


import pygame, os, random, time,Util,math
from pygame.locals import *


WIDTH = 800 #Games width
HEIGHT = 600 #Games height

BOSS = "boss3.png"   #Image for the boss
LASER ="enemyshot.png"  #Image for the enemi
ENEMY ="enemy3.png"     #image for the enemies


    
class Mobs(pygame.sprite.Sprite):
     """An instance of a third level enemy"""
     def __init__(self,player):
        """ Constructor. Create all attributes and initialize the enemy. """
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(ENEMY)  #The sprite image  
        self.rect = self.image.get_rect()    #The sprites rectangle
        self.rect.centerx = random.randrange(WIDTH)
        self.rect.top = -10
        self.player = player  #The player
        self.rect.bottom = -5
        self.health = 10  #The enemy's health
     def update(self):
        """Updates the enemy's movement"""
        #Sets the enemis speed
        if self.player.rect.centerx - self.rect.centerx > 2 or self.player.rect.centerx - self.rect.centerx < -2:
             self.speed = 3
        else:
             self.speed = 1
             
        if self.rect.top < 30:
            self.health = 10
            self.rect.y += self.speed
        if self.rect.centerx < self.player.rect.centerx:
            self.rect.centerx += self.speed
        elif self.rect.centerx > self.player.rect.centerx:
            self.rect.centerx -= self.speed
            
class Mobshots(pygame.sprite.Sprite):
    """An instacne of the enemy's shot"""
    def __init__(self, x, y,player):
        """ Constructor. Create all attributes and initialize the shot. """
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(LASER)  #The sprite image 
        self.rect = self.image.get_rect()  #The sprites rectangle
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10  #The shot's y speed
        self.player = player  #The
        #Determines the shot's x speed
        if self.rect.centerx < self.player.rect.centerx:
            self.speedx = 2
        elif self.rect.centerx > self.player.rect.centerx:
            self.speedx = -2
        else:
            self.speedx = 0
    def update(self):
        """Updates the shot's movement"""
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx
        if self.rect.y > HEIGHT:
            self.kill()

class Boss3(pygame.sprite.Sprite):
    """An instance of the third level boss"""
    def __init__(self,player):
        """ Constructor. Create all attributes and initialize the boss """ 
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(BOSS)  #The sprite image  
        self.rect = self.image.get_rect() #The sprites rectangle
        self.rect.centerx = WIDTH/2
        self.health = 60    #The boss's health
        self.rect.bottom = -20
        self.speed = 3 #The boss's speed
        self.player = player #The player
    def update(self):
        """Updates the boss's movement"""
        if self.rect.centery < 0:
            self.rect.centery += self.speed
            self.health = 60
        else:
            if self.rect.centerx < self.player.rect.centerx and self.rect.right != WIDTH:
                self.rect.centerx += self.speed
            elif self.rect.left > 0:
                self.rect.centerx -= self.speed
            if self.rect.centery < self.player.rect.centery and self.rect.bottom != HEIGHT:
                self.rect.centery += self.speed
            elif self.rect.top > 0:
                self.rect.centery -= self.speed


class Bossshots(pygame.sprite.Sprite):
    """An instacne of the boss's shot"""
    def __init__(self, x, y,player):
        """ Constructor. Create all attributes and initialize the shot. """
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(LASER)  #The sprite image  
        self.rect = self.image.get_rect() #The sprites rectangle
        self.rect.centery = y
        self.rect.centerx = x
        speed = 10  #The shot's speed
        xdif = player.rect.centerx - x  #The diffrene between the player and boss's x values
        ydif = player.rect.centery - y #The diffrene betweent the player and boss's y values
        self.angle  = (180 / math.pi) * -math.atan2(ydif, xdif)  #The boss's shooting angle 
        self.speedy = -speed*math.sin(self.angle*(math.pi/180)) #The Y speed of the shot
        #Determines the x speed of the shot
        if self.angle >= 180:
            self.speedx = -speed*math.cos(self.angle*(math.pi/180))
        else:
            self.speedx = speed*math.cos(self.angle*(math.pi/180))  
    def update(self):
        """Updates the shot's movement"""
        self.rect.centery += self.speedy
        self.rect.centerx += self.speedx
        if self.rect.y > HEIGHT:
            self.kill()
        elif self.rect.y < 0:
            self.kill()
        elif self.rect.x > WIDTH:
            self.kill()
        elif self.rect.x < 0:
            self.kill()


class Level3():
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """
 
    def __init__(self,all_sprites,points,lives,player):
        """ Constructor. Create all our attributes and initialize
        the game. The stats provided customize the game. """
        self.points = points  #The points
        self.lives = lives  #The lives
        self.player = player   #the player
        self.level_over = False   #Boolean that controls whether the level is over or not
        self.bossspawn = False   #Boolean that contorls whether the boss has spawned
        self.startboss = 60   #Time untill the boss spawns

        self.startmobtime = time.time()  #The timer for when new enemies spawn
        self.newshot = 0.4     #The time the enemies and boss shoot
        self.bosstimer = time.time()   #The timer for when the boss will spawn

        self.amob = Mobs(player) #A single mob             
        all_sprites.add(self.amob)


        self.mobshots = pygame.sprite.Group()     #Group containing the enemies 
        self.bossshots = pygame.sprite.Group()  #Group containing the boss's shots

    def run_logic(self,shots,musicPlaying,impact,damage,all_sprites):
        """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
        
        if not self.level_over:
            endmobtime = time.time()  #Ends the timer for new enemies to spawn
            if endmobtime - self.startmobtime >= self.newshot:
            #Spawns the boss or enemy shots when the timer runs out
                if not self.bossspawn:
                    ashot = Mobshots(self.amob.rect.centerx,self.amob.rect.centery,self.player) #A shot
                    self.mobshots.add(ashot)
                    all_sprites.add(ashot)
                else:
                    ashot = Bossshots(self.boss.rect.centerx,self.boss.rect.centery,self.player)  #a shot
                    self.bossshots.add(ashot)
                    all_sprites.add(ashot)
                self.startmobtime = time.time()
                    
            if not self.bossspawn:
                mob_hit_list = pygame.sprite.spritecollide(self.amob,shots,impact)    #List of collisions between enemies and the player's shots
                if mob_hit_list:
                #Damages the enemies when hit
                    Util.eplo(musicPlaying,all_sprites,self.amob)
                    self.amob.health -= damage
                    if self.amob.health <= 0:
                        self.amob.kill()
                        self.points += 500
                        if not self.bossspawn:
                            self.amob = Mobs(self.player)   
                            all_sprites.add(self.amob)
                    else:
                        self.amob.health -= 1
                playerhits = pygame.sprite.spritecollide(self.player, self.mobshots, True)  #List of collisions between the player and  and the enemy's shots
                playerhits2 = pygame.sprite.collide_rect(self.player, self.amob) #List of collisions between the player and the enemies
                    
                endbosstime = time.time() #Ends the timer for the boss to spawn
                if endbosstime - self.bosstimer>= self.startboss:
                #Spawns the boss when the timer runs out
                    self.amob.kill()
                    self.boss = Boss3(self.player)
                    shots.empty()
                    all_sprites.empty()
                    all_sprites.add(self.player)
                    all_sprites.add(self.boss)
                    pygame.time.wait(500)
                    self.bossspawn = True    

            else:
                playerhits = pygame.sprite.collide_rect(self.player, self.boss) #List of collisions between the player and the boss
                playerhits2 = pygame.sprite.spritecollide(self.player, self.bossshots,True) #List of collisions between the player and  and the boss'sshots

                boss_hit_list = pygame.sprite.spritecollide(self.boss,shots,True)  #List of collisions between the boss and the player's shots

                if boss_hit_list:
                #Damages the boss when hit
                    self.boss.health -= damage
                    self.points += 100
                    Util.eplo(musicPlaying,all_sprites,self.boss)
                if self.boss.health <= 0:
                    self.points += 1000
                    self.boss.kill()
                    all_sprites.empty()
                    self.level_over = True

            if playerhits or playerhits2:
            #Damages the player when hit
               Util.eplo(musicPlaying,all_sprites,self.player)
               self.lives -= 1
            if self.lives <= 0:
            #Kills the boss when it's life reaches zero
                self.game_over = True
                                  
  
    def display_frame(self, windowSurface,red):
        """ Display everything to the screen for the game. """
        if self.bossspawn and self.boss.health > 0:
        #Displays the boss's health bar
            pygame.draw.rect(windowSurface,red,(50,50,20,4*self.boss.health),0)        




