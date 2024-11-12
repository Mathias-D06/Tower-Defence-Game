from pygame import *
import math
init()
display.set_caption('Frontlines')
font.init()
clock = time.Clock()

class Tower:                              # creates the tower class
    def __init__(self):
        self.__range = 10                 #sets the tower range and damage to a set number, the position will depend on where the tower is placed.
        self.__damage = 20
        self.__target = None     # initialy the targeted enemy is set to none as it will be changed when an enemy is near
        self._type1 = image.load("towerDefense_tile249.png")        # the sprites for the 2 different towers must be loaded as they are pre made images from an asset pack 
        self._type2 = image.load("towerDefense_tile250.png")
        self._projectile = image.load("towerDefense_tile251.png")      # the same for the projectile
        self._type1_cost = 100
        self._type2_cost = 150
        self._towers = []
    
    def inRange(self):
        self._image_height = self._type1.get_height()
        self._image_width = self._type1.get_width()
        centre_x = self._tower.pos[0] + self._image_height//2          # to calculate the the centre of the images we take the bottom left corner co-ordinates and add in the height and width
        centre_y = self._tower.pos[1] + self._image_width//2
        enemy_centre_x = self._enemy.x + self._enemy.image.get_height()//2        # do the same for the enemy centre
        enemy_centre_y = self._enemy.y + self._enemy.image.get_width()//2
        distance = math.sqrt((centre_x - enemy_centre_x)**2 + (centre_y - enemy_centre_y)**2)       # using triganometry to calucate the distance between the enemy and tower
        return distance <= self.__range
    def attack(self,enemy,inRange):                       # using the inRange() fucntion attack the nearest tower 
        self._willhit = inRange(self,target,enemy[target])
        if self.__target and self._willhit:                                 # if an enemy has been found and it's in range then deal damage
            self.__target.take_damage(self.__damage)
            if self.__target.health <= 0:                            # if an enemy is killed then set the target back to 0
                self.__target = None
        else:
            self.__new_target = newTarget(self,enemies)
            if self.__new_target is not None:                                       # when there is no target set the target to the new one
                self.__target = self.__new_target
                self.__target = self._take_damage(self.__damage)                     # that target will then take damage
            else:
                self.__target = None
    def newTarget(self):                                                    # a function to assign a new enemy as the target
        self.__area = inRange(self,enemy)
        for enemy in enemies:                                           # by checking a valid enemy within the group of enemies it will return the nearest enemy 
            if self.__area:
                return enemy
        return None

class TowerSelection(Tower):                            # class specific for the selection of towers by the player
    def __init__(self):
        Tower.__init__(self)                             # makes sure that all attributes are inherited correctly
        self._selected_tower = None                        # set the tower used as none initially
        self._money = 250                                # set money to the starting number
        self._tower1_rect = None                        # sets the initial rect for the 2 towers as None
        self._tower2_rect = None
    
    def select_tower(self, mouse_pos):
              if self._tower1_rect and self._tower1_rect.collidepoint(mouse_pos):     # check it see if the mouse is touching the tower rect
                  self._selected_tower = self._type1                                    # set it to type 1
              elif self._tower2_rect and self._tower2_rect.collidepoint(mouse_pos):      # do it for the other tower
                  self._selected_tower = self._type2
    
    def drawTower_preview(self,game_screen,mouse_pos):
        if self._selected_tower:                                                            # checks to see if there is a selected tower
            game_screen.blit(self._selected_tower,(mouse_pos[0] - 32, mouse_pos[1] - 32))  # if so then use the mouse position to blit an image of the tower to screen
    
    def pos_valid(self,mouse_pos):
        self._previewRect = Rect(mouse_pos[0] - 32, mouse_pos[1] - 32, 64, 64)   # creates a rect for the preview tower using the mouse position
        for tower in self._towers:                                          # iterates through the towers array 
            self._currentRect = Rect(tower[0] - 32, tower[1] - 32, 64, 64)       # sets a rect around each existing tower using each of the tower index
            if self._previewRect.colliderect(self._currentRect):                      # checks to see if there is a collision
                return False
        return True
    
    def place_tower(self,mouse_pos,game_screen):
        for e in event.get():    
            if e.type == MOUSEBUTTONDOWN:        
                if self._selected_tower == self._type1:                        # if the first tower will be set as type 1
                    if self._money >= self._type1_cost:                         # checks if the player has enough money
                        if self.pos_valid(mouse_pos) == True:                  # it will use the validation function to check the position that is selected by the user
                            if e.button == 1: 
                                game_screen.blit(self._selected_tower,(mouse_pos[0] - 32, mouse_pos[1] - 32))
                                self._towers.append((mouse_pos[0], mouse_pos[1], self._type1))
                                self._money -= self._type1_cost                      #  it will then take the cost away from the money owned
                                self._selected_tower = None                            # it will reset the selected tower back to none
            elif self._selected_tower == self._type2:                           # this block of code is repeated for the second type of tower
                if self._money >= self._type2_cost:                           
                    if self.pos_valid(mouse_pos) == True:            
                            if e.button == 1:
                                game_screen.blit(self._selected_tower,(mouse_pos[0] - 32, mouse_pos[1] - 32))
                                self._towers.append((mouse_pos[0], mouse_pos[1], self._type2))
                                self._money -= self._type2_cost
                                self._selected_tower = None

class Enemy:
    def __init__(self,image):
        self._image = image.load("towerDefense_tile248.png")         # the sprite of the enemies are pre set like the tower images
        self._health = 40                                           # the health is set to be a constant
        self._number = 4                                             # the number and speed are to be vaiable as they will change as the round goes on
        self._speed = 6
        self._pos = []                                              # the positions of the enemies will be stored in an array
        self._round = 1                                          # currently a place holder for the round variable

class MainLoop:
    def __init__(self):
        self.__exit_game = False                                  # the exit game variable is set to false initially
        self.__game_screen = display.set_mode((1288,728))             # the game screen is set to a certain size
        self.__map = image.load("map.png")                            # the map is loaded with an image
        self.__font = font.Font(None,36)                              # the font is set to a size of 36
        self.__tower_selection = TowerSelection()                     # will inherit from the TowerSelection class for its attributes
        self.__select_rect = Rect(400,575,488,153)                   # this is the black rectangle which will be the background for the selection (it will be at the bottom)
        self.__tower1 = image.load("towerDefense_tile249.png")
        self.__tower2 = image.load("towerDefense_tile250.png")
        self.__tower1_rect = Rect(450,600,64,64)                    # this is the outline for the towers in the tower selection box
        self.__tower2_rect = Rect(750,600,64,64)
        self.__tower_selection._tower1_rect = self.__tower1_rect        # makes it so that the TowerSelection class can use it for selection
        self.__tower_selection._tower2_rect = self.__tower2_rect    

    def drawTowerbox(self):
        draw.rect(self.__game_screen, (0,0,0), self.__select_rect)     # this draws the black rectangle
        draw.rect(self.__game_screen, (255, 255, 255), self.__tower1_rect)  # this is the white rectangle for the outline
        draw.rect(self.__game_screen, (255, 255, 255), self.__tower2_rect)
        self.__game_screen.blit(self.__tower1, self.__tower1_rect)     # this blits it to the screen
        self.__game_screen.blit(self.__tower2, self.__tower2_rect)
        cost1 = self.__font.render("Cost: " + str(self.__tower_selection._type1_cost), True, (255,255,255))  # this draws the cost of each tower to the screen
        cost2 = self.__font.render("Cost: " + str(self.__tower_selection._type2_cost), True, (255,255,255))
        self.__game_screen.blit(cost1, (430,685))
        self.__game_screen.blit(cost2, (730,685))

    def gamescreen(self):
        while not self.__exit_game:
            mouse_pos = mouse.get_pos()  # gets the mouse position constantly while the game is running
            for e in event.get():
                if e.type == QUIT:
                    self.__exit_game = True   # will quit the game
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.__tower_selection._selected_tower: # checks to see if there is a tower that has been selected
                            self.__tower_selection.place_tower(mouse_pos,self.__game_screen)  # this will run the code to then place the tower onto the game map
                        else:                                                   # if not
                            self.__tower_selection.select_tower(mouse_pos)  # will run the select tower function if the left mouse button is pressed
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.__tower_selection._selected_tower = None  # will cancel the selection if the escape button is pressed
                
            self.__game_screen.blit(self.__map,(0,0))              # will blit the map to the screen
            self.drawTowerbox()                                 # will run the tower box function
            self.__tower_selection.drawTower_preview(self.__game_screen,mouse_pos) # will run the tower box function using the screen and pos as parameters
            display.flip()
            clock.tick(60)                                  # sets the refresh rate to 60hz

loop = MainLoop()
loop.gamescreen()


