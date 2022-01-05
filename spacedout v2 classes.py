#Ben Wilson
#May 6, 2019
#The main game file for my game "Spaced Out"

import pygame, os, random, time,level1,level2,level3,Util,math
from pygame.locals import *

WIDTH = 800 #Game's width
HEIGHT = 600 #Game's height

#Sets colors of the game
BLACK= (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Set up the frame rate
FRAMERATE = 60


#Set up images to be used
LASER = "laser-blast-png.png" #The playes laser sprite

#The ship the player can select
PLAYERIMGS = ["ship.png","ship2.png","ship3.png"]

#The versions of the player images that will be displayed in the ship select
DISPLAYER = ["dship.png","dship2.png","dship3.png"]

BACK = "space.png" #The background
WIN = "win.png"  #The win screen
INSTRUCTIONS = ["insutruction.png","objective.png" ]   #The instructions screen pages
INTRO = "intro.png"     #The intro screen
GO = "go screen.png"    #The game over screen
GAT = "gattling.png"    #The gattling gun power-up sprite
SPREAD = "spread.png"   #The spread shot power-up sprite
CHARGE ="charge.png"    #The charge shot power-up sprite
CHARGESHOT = "chargeshot.png"   #What the shot sprite changes to when the player gets the charge shot
ANGLE = 90  #The angle the player starts at

SHOOTSOUND = 'Laser_Shoot4.wav' #The sound effect for the player's shots
BACKGROUND = 'tgfcoder-FrozenJam-SeamlessLoop.ogg' #The backgorund music

NUMSCORES = 5 #The number of possilbe highscores
SCORES = "highscore.txt"    #The file containing the highscores
NAMES = "names.txt"          #The file containing the highscore names

def terminate():
    """ This function is called when the user closes the window or presses ESC """
    pygame.quit()
    os._exit(1)
    return

def drawText(text, font, surface, x, y, textcolour):
    """ Draws the text on the surface at the location specified """
    textobj = font.render(text, 1, textcolour)  #The text itself
    textrect = textobj.get_rect()   #The textès rectangle
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return

def score(windowSurface,count,lives,txt):
    """Displays the current score, lives, and highscore""" 
    font = pygame.font.SysFont(None, 25) #The font
    text = font.render("Points: "+str(count), True, WHITE) #The current points
    windowSurface.blit(text,(0,0))
    text = font.render("Lives: "+str(lives), True, WHITE)#The current lives
    windowSurface.blit(text,(WIDTH-100,0))
    text = font.render("High Score: "+txt, True, WHITE)#The current highscore
    windowSurface.blit(text,(WIDTH/2-100,0))
    return

def level_display(levelnum,windowSurface):
    """Displayes the current level"""
    largeText = pygame.font.SysFont("Stencil",115)  #The font
    drawText("Level "+str(levelnum), largeText, windowSurface, WIDTH*0.25, HEIGHT*0.40, WHITE)
    pygame.display.update()
    pygame.time.wait(1000)
    return

def intro(windowSurface):
    """Displays the intro screen"""
    screen = Util.load_image(INTRO) #The image of the screen itself
    windowSurface.fill(BLACK)
    windowSurface.blit(screen,(0,0))
    pygame.display.update()
    intro = True    #The boolian that controlls howlong the screen is displayed
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                elif event.key == pygame.K_x:
                    instructions(windowSurface)
        windowSurface.fill(BLACK)
        windowSurface.blit(screen,(0,0))
        pygame.display.update()
    return

def instructions(windowSurface):
    """Displays the instructions screen"""
    read = True #The boolian that controlls howlong the screen is displayed
    pagenum = 0 #The current page
    intruct = Util.load_image(INSTRUCTIONS[pagenum])  #The image of the screen itself
    while read:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    read = False
                if event.key == K_LEFT or event.key == ord('a'):
                    if pagenum != 0:
                        pagenum -= 1
                        intruct = Util.load_image(INSTRUCTIONS[pagenum])  #The image of the screen itself
                elif event.key == K_RIGHT or event.key == ord('d'):
                    if pagenum != len(INSTRUCTIONS)-1:
                        pagenum += 1
                        intruct = Util.load_image(INSTRUCTIONS[pagenum])  #The image of the screen itself
                if event.key == K_ESCAPE:
                    terminate()
        windowSurface.fill(BLACK)
        windowSurface.blit(intruct,(0,0))
        pygame.display.update()
    return

def show_go_screen(windowSurface):
    """Displays the game over screen"""
    screen = Util.load_image(GO)    #The image of the screen itself
    largeText = pygame.font.SysFont("Stencil",70)   #The font
    windowSurface.fill(BLACK)
    windowSurface.blit(screen,(0,0))
    height =150     #The height of the text
    scores = open(SCORES, "r")  #The opened score file
    names = open(NAMES, "r")    #The opened name file
    score = scores.readline().strip()   #The current score
    name = names.readline().strip()     #The current name
    while score != "":
         drawText(name, largeText,windowSurface,100,height,BLACK)
         drawText(score, largeText,windowSurface,550,height,BLACK)
         score = scores.readline().strip()
         name = names.readline().strip()
         height += 75
    names.close()
    scores.close()
    pygame.display.update()
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    again = False  
    return

def enter_socre(windowSurface):
    """Allows the player to enter their with their score"""
    typing = True   #The boolian that controls how long the screen is displayed
    name = ""   #The player's name
    while typing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    if len(name) > 0:
                        name = name[:-1]
                else:
                    if len(name) < 3:
                        name += event.unicode
        pygame.draw.rect(windowSurface, BLUE ,(0,100,WIDTH,300))
        largeText = pygame.font.SysFont("Stencil",40)   #The font
        drawText("Enter Your Name And Press Space", largeText,windowSurface,65,100,BLACK)
        largeText = pygame.font.SysFont("Stencil",200)    
        drawText(name, largeText,windowSurface,210,200,BLACK)
        pygame.display.update()
    return(name)

def sort_score(name,score):
    """Sorts the highscores"""
    scores = open(SCORES, "r")  #The opened score file
    names = open(NAMES, "r")    #The opened name file
    scorelist = []  #The list of the highscores
    namelist = []   #The list of the names
    for x in range(NUMSCORES):
        curscore = scores.readline().strip()    #the current score
        scorelist.append(int(curscore))
        curname = names.readline().strip()  #The current name
        namelist.append(curname)
    scorelist.append(score)
    namelist.append(name)
    names.close()
    scores.close()
    sort = True     #The boolian that controls how long the porgram trys to sort
    passed = 0      #the number of passes
    while sort:
        passed = passed + 1
        switch = 0  #The number of switches
        for y in range(len(scorelist)-passed):
            if scorelist[y] < scorelist[y+1]:
                temps = scorelist[y+1]
                scorelist[y+1] = scorelist[y]
                scorelist[y] = temps
                tempn = namelist[y+1]
                namelist[y+1] = namelist[y]
                namelist[y] = tempn
                switch = switch + 1
        if switch== 0:
            sort = False
    scores = open(SCORES, "w")
    names = open(NAMES, "w")
    for z in range(NUMSCORES):
        scores.write(str(scorelist[z])+"\n")
        names.write(namelist[z]+"\n")
    names.close()
    scores.close()
    return
        
            
def ship_select(windowSurface,back):
    """Lets the player select their ship"""
    x = 0  #The current place in the list
    select = False  #The boolian that controls how long the player is selecting
    current = Util.load_image(PLAYERIMGS[x])    #The current ship
    display = Util.load_image(DISPLAYER[x])     #The curretn ship displayed
    while not select:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    if x != 0:
                        x -=1
                        current = Util.load_image(PLAYERIMGS[x])    #The current ship selected
                        display = Util.load_image(DISPLAYER[x])     #The curretn ship displayed
                elif event.key == K_RIGHT or event.key == ord('d'):
                    if x != len(PLAYERIMGS)-1:
                        x += 1
                        current = Util.load_image(PLAYERIMGS[x])    #The current ship selected
                        display = Util.load_image(DISPLAYER[x])     #The curretn ship displayed
                elif event.key == K_SPACE:
                    return(current)

        windowSurface.fill(BLACK)
        windowSurface.blit(back,(0,0))
        pygame.draw.rect(windowSurface, BLUE ,(0,HEIGHT*0.05,WIDTH,100))
        pygame.draw.rect(windowSurface, BLUE ,(0,HEIGHT*0.8,WIDTH,100))
        largeText = pygame.font.SysFont("Stencil",50)   #The font
        drawText("Press Space To Select A Ship", largeText,windowSurface,10,HEIGHT*0.85,BLACK)
        largeText = pygame.font.SysFont("Stencil",40)
        drawText("Use Left And Right To Change Ships", largeText,windowSurface,30,HEIGHT*0.1,BLACK)
        windowSurface.blit(display, (WIDTH/2-110,HEIGHT/2-100))
        pygame.display.update()

class Player(pygame.sprite.Sprite):
    """Creates and instacne of the player"""
    def __init__(self,img):
        """Constructor. Create all attributes and initialize the player."""
        pygame.sprite.Sprite.__init__(self) 
        self.origin = img  #The original images
        self.image = img    #The image that will be diplayed on the screen
        self.rect = self.image.get_rect()   #the player's rectangle
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-30
        self.angle = ANGLE #The current angle the player is at
        
        # set up movement variables
        self.moveLeft = False
        self.moveRight = False
        self.moveup = False
        self.movedown = False
        
        self.movespeed = 5 #The player's move speed
        
    def update(self):
        """Change the position of the player's rectangle""" 
        mouse = pygame.mouse.get_pos()  #The location of the mouse
        xdif =  mouse[0]- self.rect.centerx #The x diffrence between the player and mouse
        ydif =  mouse[1]-self.rect.centery  #The y diffrence between the player and mouse
        self.angle  = (180 / math.pi) * -math.atan2(ydif, xdif) - 90 #The angle the player turns
        self.image = pygame.transform.rotate(self.origin,self.angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx,self.rect.centery))

        if self.moveLeft and self.rect.left > 0:
            self.rect.left -= self.movespeed
        elif self.moveRight and self.rect.right < WIDTH:
            self.rect.right += self.movespeed
        if self.moveup and self.rect.top > 0:
            self.rect.top -= self.movespeed
        elif self.movedown and self.rect.bottom < HEIGHT:
            self.rect.bottom += self.movespeed



class Shoot(pygame.sprite.Sprite):
    """Creates an instace of the player's shot"""
    def __init__(self, x, y,angle,img):
        """ Constructor. Create all attributes and initialize the shot."""
        pygame.sprite.Sprite.__init__(self)
        self.image = Util.load_image(img) #The sprite image
        self.angle = angle + ANGLE  #The current angle the player is at
        self.rect = self.image.get_rect() #The sprites rectangle
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = 10 #The shots speed
        self.speedy = -self.speed*math.sin(self.angle*(math.pi/180))
        if self.angle >= 180:
            self.speedx = -self.speed*math.cos(self.angle*(math.pi/180))
        else:
            self.speedx = self.speed*math.cos(self.angle*(math.pi/180))
    def update(self):
        """Change the position of the shot""" 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.y < 0:
            self.kill()
        elif self.rect.y > HEIGHT:
            self.kill()
        elif self.rect.x < 0:
            self.kill()
        elif self.rect.x > WIDTH:
            self.kill()

class Gattling(pygame.sprite.Sprite):
     """Creates an instace of the gattling gun power-up"""
     
     def __init__(self):
         """ Constructor. Create all attributes and initialize the power-up. """
         pygame.sprite.Sprite.__init__(self)
         self.image = Util.load_image(GAT)  #The sprite image
         self.rect = self.image.get_rect()  #The sprite's rectangle
         self.rect.centerx = random.randrange(WIDTH)
         self.rect.centery = random.randrange(HEIGHT)
         self.dur = 3  #How long the power-up lasts
         self.rate = 0.05   #The fire rate
         self.impact = True         #The booliean that controls wheither the shots are killed on impact
         self.damage = 0.5          #The damage
         self.img = LASER           #The image for the shot
         self.time = time.time()    #Starts the timer for the power-up
     def update(self):
        """Kills the power-up if the time is up"""
        endtime= time.time()    #End time for the power-up
        if endtime - self.time >= self.dur:
            self.kill()
            
class Spread(pygame.sprite.Sprite):
     """Creates an instace of the spread shot power-up"""
     def __init__(self):
         """ Constructor. Create all attributes and initialize the power-up. """
         pygame.sprite.Sprite.__init__(self)
         self.image = Util.load_image(SPREAD)  #The sprite image
         self.rect = self.image.get_rect()  #The sprite's rectangle
         self.rect.centerx = random.randrange(WIDTH)
         self.rect.centery = random.randrange(HEIGHT)
         self.dur = 5  #How long the power-up lasts
         self.rate = 0.2  #The fire rate
         self.angles = [-180,-90,-45,0,45,90,135,180,225,270] #The angles the spread shot fires at
         self.impact = True   #The booliean that controls wheither the shots are killed on impact
         self.damage = 1   #The damage
         self.time = time.time() #Starts the timer for the power-up
         self.img = LASER  #The image for the shot 
     def update(self):
        """Kills the power-up if the time is up"""
        endtime= time.time()  #End time for the power-up
        if endtime - self.time >= self.dur:
            self.kill()
            
class Charge(pygame.sprite.Sprite):
     """Creates an instace of the chargeshot power-up"""
     def __init__(self):
         """ Constructor. Create all attributes and initialize the power-up. """
         pygame.sprite.Sprite.__init__(self)
         self.image =Util.load_image(CHARGE)  #The sprite image
         self.rect = self.image.get_rect() #The sprite's rectangle
         self.rect.centerx = random.randrange(WIDTH)
         self.rect.centery = random.randrange(HEIGHT)
         self.dur = 5  #How long the power-up lasts
         self.rate = 0.4  #The fire rate
         self.impact = False  #The booliean that controls wheither the shots are killed on impact
         self.damage = 4  #The damage
         self.img = CHARGESHOT  #The image for the shot 
         self.time = time.time() #Starts the timer for the power-up
     def update(self):
        """Kills the power-up if the time is up"""
        endtime= time.time() #End time for the power-up
        if endtime - self.time >= self.dur:
            self.kill()


class Game():
    """ This class represents an instance of the game"""
 
    def __init__(self,img,windowSurface):
        """ Constructor. Create all attributes and initialize the game. """

        self.game_over = False  #The boolian that controls whether the game is over or not
        self.points = 0  #The points
        self.lives = 5  #The lives
        in_file = open(SCORES, "r") #The open score file
        self.highscore = in_file.readline().strip() #The current highscore
        in_file.close()
        self.powerspawn = False #The boolean that controls whether a power-up has spawned
        self.powered = False  #The boolean that controls whether the player has a power up
        self.surface = windowSurface   #The display surface
      
        
        self.all_sprites = pygame.sprite.Group()#The group containing all sprites in the game
        self.player = Player(img)       #The player 
        self.all_sprites.add(self.player)
     
        self.shots = pygame.sprite.Group() #The group containing the player's shots
        self.shoot = False      #The boolian that controls whether the player is shooting
        self.shoottime = time.time()    #The time for the player's shots
        self.newshot = 0.2      #The shot rate
        self.impact = True   #The booliean that controls wheither the shots are killed on impact
        self.damage = 1     #The damage
        self.shotimg = LASER    #The shots sprite image
        self.spread = False     #The boolina that controls whether the spread shto power-up it active

         
        self.levelnum = 1  #The surrent level number
        self.displayed = False  #The boolean that controls wheter the level number has been displayed
        self.level = level1.Level1(self.points,self.lives)  #the level 


        # Set up music
        pygame.mixer.music.load(BACKGROUND )  #Load the background music
        self.shootsound = pygame.mixer.Sound(SHOOTSOUND) #Load the sound effect for the player's shots
        # Play the background music
        pygame.mixer.music.play(-1, 0.0)
        self.musicPlaying = True
        

    def process_events(self):
        """ Process all of the keyboard."""
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    self.player.moveRight = False
                    self.player.moveLeft = True
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.player.moveLeft = False
                    self.player.moveRight = True
                elif event.key == K_UP or event.key == ord('w'):
                    self.player.movedwon = False
                    self.player.moveup = True
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.player.moveup = False
                    self.player.movedown = True
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_LEFT or event.key == ord('a'):
                    self.player.moveLeft = False
                elif event.key == K_RIGHT or event.key == ord('d'):
                    self.player.moveRight = False
                elif event.key == K_UP or event.key == ord('w'):
                    self.player.moveup = False
                elif event.key == K_DOWN or event.key == ord('s'):
                    self.player.movedown = False
                elif event.key == ord('m'):
                    # toggles the sound music
                    if self.musicPlaying:
                        pygame.mixer.music.stop()
                    else:
                        pygame.mixer.music.play(-1, 0.0)
                    self.musicPlaying = not self.musicPlaying
            elif event.type == MOUSEBUTTONUP:
                self.shoot = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot = True

                      
    def run_logic(self):
        """ This method is run each time through the frame. It
        updates positions and checks for collisions. """
        
        
        if not self.game_over:

            endshootime = time.time() #The end time for the player's shots
            if self.shoot:
                if endshootime - self.shoottime >= self.newshot:
                    if self.spread:
                    #Fires the spread shot if the power-up is active
                        for x in range(len(self.powerup.angles)):
                            ashot = Shoot(self.player.rect.centerx,self.player.rect.centery,self.powerup.angles[x],self.shotimg)#A single shot
                            self.shots.add(ashot)
                            self.all_sprites.add(ashot)
                    else:
                    #Fires the normal shot
                        ashot = Shoot(self.player.rect.centerx,self.player.rect.centery,self.player.angle,self.shotimg)
                        self.shots.add(ashot)
                        self.all_sprites.add(ashot)
                    if self.musicPlaying:
                        self.shootsound.play()
                    self.shoottime = time.time()
                            
                        
            if not self.powerspawn:
                spawn = random.randrange(0,10)  #The random number genorator that determines is a power-up is spawned
                if spawn == 1:
                    self.powertype = random.randrange(0,3) #The random number genorator that determines which power-up is spwaned
                    #Creates of power-up of the determined type
                    if self.powertype == 1:
                     self.powerup = Gattling()
                    elif self.powertype == 2:
                        self.powerup = Spread()
                    else:
                        self.powerup = Charge()
                    self.all_sprites.add(self.powerup)
                    self.powerspawn = True
            else:
                if pygame.sprite.collide_rect(self.player, self.powerup):
                    #Sets up the variables for the power-up
                    if self.powertype == 2:
                        self.spread = True
                    self.newshot = self.powerup.rate
                    self.powertime = time.time()
                    self.powerdur = self.powerup.dur
                    self.powered = True
                    self.impact = self.powerup.impact
                    self.damage = self.powerup.damage
                    self.shotimg = self.powerup.img
                    self.powerup.kill()
                if self.powered:
                    endpowertime = time.time()
                    if endpowertime- self.powertime >= self.powerdur:
                        #Rests the variable when the time is up
                        self.impact = True
                        self.damage = 1
                        self.newshot = 0.2
                        self.shotimg = LASER
                        self.powered = False
                        self.powerspawn = False
                        self.spread = False
                        
            if self.levelnum == 1:
                if self.level.level_over:
                    #Sets up the variabels for the second level
                    self.lives = 5
                    self.level = level2.Level2(self.points,self.lives)
                    self.player.rect.centerx = WIDTH/2
                    self.player.rect.bottom = HEIGHT-30
                    self.levelnum += 1
                    self.displayed = False
                else:
                    #Runs the logic for the first level
                    self.level.run_logic(self.player,self.shots,self.musicPlaying,self.impact,self.damage,self.all_sprites)
            elif self.levelnum == 2:
                if self.level.level_over:
                    #Sets up the variabels for the thrid level
                    self.lives = 5
                    self.level = level3.Level3(self.all_sprites,self.points,self.lives,self.player)
                    self.player.rect.centerx = WIDTH/2
                    self.player.rect.bottom = HEIGHT-30
                    self.levelnum += 1
                    self.displayed = False
                else:
                    #Runs the logic for the first level
                    self.level.run_logic(self.player,self.shots,self.musicPlaying,self.impact,self.damage,self.all_sprites)
                
            else:
                if self.level.level_over:
                    #Ends the game when the thrid level is over
                    self.surface.fill(BLACK)
                    win = Util.load_image(WIN)  
                    self.surface.blit(win,(0,0))
                    pygame.display.update()
                    pygame.time.wait(500)
                    self.game_over = True
                else:
                    #Runs the logic for the first level
                    self.level.run_logic(self.shots,self.musicPlaying,self.impact,self.damage,self.all_sprites)
            self.points = self.level.points 
            self.lives = self.level.lives
            
            if self.lives <= 0:
                #Ends the game if the player's lives hit zero
                pygame.time.wait(1000)
                self.game_over = True
            
            
            #update
            self.all_sprites.update()
  
    def display_frame(self,back):
        """ Display everything to the screen for the game. """
        
        # draw the frame.
        self.surface.fill(BLACK)
        self.surface.blit(back,(0,0))
        score(self.surface,self.points,self.lives,self.highscore)
        self.all_sprites.draw(self.surface)
        self.level.display_frame(self.surface,RED)
        if self.displayed == False:
            level_display(self.levelnum,self.surface)
            self.displayed = True
 
        # draw the window onto the screen
        pygame.display.update()




def main():
    """ Mainline for the program """
    
    pygame.init()
    mainClock = pygame.time.Clock()     #The main game clock

    windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32) #The main game surface
    pygame.display.set_caption('Spaced Out')    
    back = Util.load_image(BACK)    #The backgorund
    back = pygame.transform.scale(back,((WIDTH,HEIGHT)))
    windowSurface.blit(back,(0,0))
    

    #Display a menu and select a ship
    intro(windowSurface)
    ship = ship_select(windowSurface,back) #The ship selected by the player
    game = Game(ship,windowSurface)     #The game itself
        
    # run the game loop until the user quits
    while True:
        #Check if the game is over
        if game.game_over:
            windowSurface.blit(back,(0,0))
            name = enter_socre(windowSurface)
            sort_score(name,int(game.points))
            show_go_screen(windowSurface)
            game = Game(ship,windowSurface)
        # Process events
        game.process_events()

        # Update object positions, check for collisions
        game.run_logic()
        
        # Draw the current frame
        game.display_frame(back)        
        
        mainClock.tick(FRAMERATE)
        
main()

            

