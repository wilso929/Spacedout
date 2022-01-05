#Ben Wilson
#May 16, 2019
#This file conatains all the classes and functions used by each of the other files

import pygame
from pygame.locals import *

EXPLOSOUND ='Explosion.wav' #The explosion sound effect 


def load_image(filename):
    """ Load an image from a file.  Return the image and corresponding rectangle """
    image = pygame.image.load(filename)
    image = image.convert_alpha()   #Not as fast as .convert(), but works with transparent backgrounds
    return image


class Explosion(pygame.sprite.Sprite):
    """Creates an explosion effet"""
    def __init__(self,center):
        """Constructor. Create all our attributes and initialize the explosion"""
        pygame.sprite.Sprite.__init__(self)
        self.explo = [] #List of anmation frames
        for b in range(8):
            filename = 'regularExplosion0{}.png'.format(b)
            img = load_image(filename)  #One frame of the animation
            img = pygame.transform.scale(img,((50,52)))
            self.explo.append(img)
        self.image = self.explo[0]#First frame of the animaition
        self.rect = self.image.get_rect() #The explsoion's rectangle
        self.rect.center = center
        self.frame = 0  #The current fraem
        self.rate = 60   #The frame rate
        self.last_update = pygame.time.get_ticks()  #The time since the last update
    def update(self):
        """Updates the animation"""
        now = pygame.time.get_ticks()  #The current time
        if now - self.last_update > self.rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.explo):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.explo[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def eplo(musicPlaying,all_sprites,ob):
    """Creates and explosion effect at an objects location"""
    explo_sound = pygame.mixer.Sound(EXPLOSOUND) #Load the explosion sound effect
    if musicPlaying:
        explo_sound.play()
    ex = Explosion(ob.rect.center)  #The explosion itself
    all_sprites.add(ex)
    return
