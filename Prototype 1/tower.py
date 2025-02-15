from pygame import *
import math
init()
display.set_caption('Frontlines')
font.init()
clock = time.Clock()
import random
mixer.init()
import subprocess

class Tower():                              # creates the tower class
    def __init__(self):
        self.__range = 100                 #sets the tower range and damage to a set number, the position will depend on where the tower is placed.
        self._damage1 = 40
        self._damage2 = 65
        self._type1 = image.load("Prototype 1\Prototype 1 Assets/towerDefense_tile249.png")        # the sprites for the 2 different towers must be loaded as they are pre made images from an asset pack 
        self._type2 = image.load("Prototype 1\Prototype 1 Assets/towerDefense_tile250.png")
        self._type1_cost = 100                                      # initialises the cost for the 2 towers
        self._type2_cost = 200
        self._towers = []                                       # initialsies the towers list
        self._cooldown_times = {}                           # create a dictionary for the cooldown times
        self._money = 250                                # set money to the starting number
        self._projectiles = []
    
    def inRange(self,tower,enemy):
        centre_x = tower[0] + self._type1.get_width() // 2              # check for the centre of the tower image x co-ordinate
        centre_y = tower[1] + self._type1.get_height() // 2         # same for the y
        enemy_centre_x = enemy[0] + self._type1.get_width() // 2        # repeat for the enemy
        enemy_centre_y = enemy[1] + self._type1.get_height() // 2
        distance = math.sqrt((centre_x - enemy_centre_x)**2 + (centre_y - enemy_centre_y)**2)   # find the distance using trig
        return distance <= self.__range                    
    
    def attack(self, enemies):
        current_time = time.get_ticks()
        for tower in self._towers:
            if tower not in self._cooldown_times:
                self._cooldown_times[tower] = 0
            if current_time - self._cooldown_times[tower] >= 100:
                target = self.newTarget(enemies, tower)
                if target:
                    if tower[2] == self._type1:
                        damage = self._damage1 
                    else: 
                        self._damage2
                    projectile = Projectile(tower[0], tower[1], target, damage)
                    self._projectiles.append(projectile)
                    self._cooldown_times[tower] = current_time
        for enemy in enemies:
            if enemy[2] <= 0:
                self._money += 15
        return [enemy for enemy in enemies if enemy[2] > 0]

    def update_projectiles(self, enemies):
        for projectile in self._projectiles[:]:
            projectile.move()
            if projectile.check_collision():
                projectile._enemy_target[2] -= projectile.damage
                self._projectiles.remove(projectile)
    
    def newTarget(self, enemies, tower):
        for enemy in enemies:                   
            if self.inRange(tower, enemy):      
                return enemy
        return None

class TowerSelection(Tower):                            # class specific for the selection of towers by the player
    def __init__(self):
        Tower.__init__(self)                             # makes sure that all attributes are inherited correctly
        self._selected_tower = None                        # set the tower used as none initially
        self._tower1_rect = None                        # sets the initial rect for the 2 towers as None
        self._tower2_rect = None
        self.stamped_surface = Surface((1288,728), SRCALPHA)   # creates a transparent surface and adds a transparent feature to it
        self.stamped_surface.fill((0,0,0,0))       # fills it with transparency
        self._enemies = []
    
    def select_tower(self,mouse_pos):
              if self._tower1_rect and self._tower1_rect.collidepoint(mouse_pos):     # check it see if the mouse is touching the tower rect
                  self._selected_tower = self._type1                                    # set it to type 1
              elif self._tower2_rect and self._tower2_rect.collidepoint(mouse_pos):      # do it for the other tower  
                  self._selected_tower = self._type2
    
    def drawTower_preview(self,game_screen,mouse_pos):
        if self._selected_tower:                                                    # checks to see if there is a selected tower
            self._previewRect = Rect(mouse_pos[0] - 32, mouse_pos[1] - 32, 64, 64)    # creates a rect around the preview tower
            if (mouse_pos[0] >= 32 and mouse_pos[0] <= (1288 - 32) and mouse_pos[1] >= 32 and mouse_pos[1] <= (728 -32)):  # checks if the mouse pos is near the boundary of the screen
                game_screen.blit(self._selected_tower,(mouse_pos[0] - 32, mouse_pos[1] - 32))  # if so then use the mouse position to blit an image of the tower to screen
    
    def pos_valid(self,mouse_pos,enemies):
        self._previewRect = Rect(mouse_pos[0] - 32, mouse_pos[1] - 32, 64, 64)   # creates a rect for the preview tower using the mouse position
        if (mouse_pos[0] < 32 or mouse_pos[0] > 1288 or mouse_pos[1] < 32 or mouse_pos[1] > 728): # checks if the mouse pos is near the boundary of the screen
            return False
        for tower in self._towers:                                          # iterates through the towers array 
            self._currentRect = Rect(tower[0] - 32, tower[1] - 32, 64, 64)       # sets a rect around each existing tower using each of the tower index
            if self._previewRect.colliderect(self._currentRect):                      # checks to see if there is a collision
                return False
        for enemy in enemies:
            self._currentRect = Rect(enemy[0] - 32, enemy[1] - 32, 64, 64)
            if self._previewRect.colliderect(self._currentRect):
                return False 
        return True
    
    def place_tower(self,mouse_pos):
        if self._selected_tower:                                     # checks to see if there is a tower that has been selected
            if self._selected_tower == self._type1 and self._money >= self._type1_cost:   # checks to see if it is the first tower and that the player has enough money
                if self.pos_valid(mouse_pos, self._enemies):                       # checks to see if the current position is valid
                    self.stamped_surface.blit(self._type1, (mouse_pos[0] - 32, mouse_pos[1] - 32))    # blits the current tower to the transparent surface using the mouse positions
                    self._towers.append((mouse_pos[0], mouse_pos[1], self._type1)) # adds the current towers mouse positions and type to the array
                    self._money -= self._type1_cost                                 # deducts the cost
                    self._selected_tower = None                                    # sets it back to none

            elif self._selected_tower == self._type2 and self._money >= self._type2_cost:   # the same is repeated for the second type
                if self.pos_valid(mouse_pos, self._enemies):
                    self.stamped_surface.blit(self._type2, (mouse_pos[0] - 32, mouse_pos[1] - 32))
                    self._towers.append((mouse_pos[0], mouse_pos[1], self._type2))
                    self._money -= self._type2_cost
                    self._selected_tower = None

class Projectile:
    def __init__(self, x, y, target, damage):
        self._x = x
        self._y = y
        self._enemy_target = target
        self._image = image.load("Prototype 1\Prototype 1 Assets/towerDefense_tile251.png")
        self.__speed = 5
        self.damage = damage

    def move(self):
        dx = self._enemy_target[0] - self._x
        dy = self._enemy_target[1] - self._y
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            self._x += self.__speed * dx / distance
            self._y += self.__speed * dy / distance

    def check_collision(self):
        dx = self._enemy_target[0] - self._x
        dy = self._enemy_target[1] - self._y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < 5 

    def draw(self, game_screen):
        game_screen.blit(self._image, (self._x - 16, self._y - 16))

class EnemyGroup:    
    def __init__(self):
        self._image = image.load("Prototype 1\Prototype 1 Assets/towerDefense_tile248.png") # the sprite of the enemies are pre set like the tower images
        self._health = 40                                   # the health is set to be a constant
        self._round = 0                                          # sets the number of rounds to 0
        self._speed = 0                                         # the enemy speed is set to 0
        self._enemies = []                  # the enemy list is initialised
        self._number = 3
        self._spawn = True                                                   
    
    def take_damage(self,damage):       
        self._health -= damage          # will reduce the health by the damage inflicted
        return self._health <= 0        # returns whether the enemy is alive or not
    
    def spawn_enemy(self):
        self._number += 1
        self.__numEnemies = self._number      # increases the number of enemies each round                    
        self._speed = 0.3                       # sets the initial speed to 0.3
        spacing = 25                        # creates a 25px spacing between the enemies
        self.__numEnemies = min(self._number, 20)  # limit to 20 enemies per round
        for _ in range(self.__numEnemies):             # for the number of current enemies it will repeat the below code
            start_x = 0 - (_ * spacing)             # the x co-ordinates to allow for spacing between the enemies
            random_y = random.randint(379,409)          # choses a random y co-ordinate for the enemies between set values
            self._health += (self._round * 2)                         # increase the health 
            self._enemy = [start_x,random_y,self._health]             # the positions of the enemies will be stored in an array
            self._enemies.append(self._enemy)             # the position of the enemies will be stored in a list
    
    def updateEnemies(self,game_screen):
        alive_enemies = []                    # this is the list that only holds the alive enemies, it holds the x and y positions of the enemies
        for self._enemy in self._enemies:             # iterates though the original list
            if self._enemy[2] > 0:                   # checks the enemies that are alive 
                alive_enemies.append(self._enemy)       # adds it to the list
        self._enemies = alive_enemies          # it then updates the older list
        for self._enemy in self._enemies:                 # iterates through the current enemies
            self.movement()                            # calls the movement function for the alive ones
            game_screen.blit(self._image,(self._enemy[0],self._enemy[1]))       # updates the screen removing "dead" enemies
    
    def movement(self):
        for enemy in self._enemies:                                        # iterates through the alive enemies
            if enemy[0] < 390:                                          # checks the x position of the enemies
                enemy[0] += self._speed                                        # if the x poisition is less than 390 it will move the enemy to the right
            elif enemy[0] >= 390 and enemy[0] <= 395 and enemy[1] > 280:            
                enemy[1] -= self._speed                                     # The enemy will move up by the set speed
            elif enemy[1] <= 280 and enemy[0] < 830:
                enemy[0] += self._speed
            elif enemy[0] >= 830 and enemy[0] <= 835 and enemy[1] < 395:        # its mostly self explanatory
                enemy[1] += self._speed
            else:
                enemy[0] += self._speed
        if enemy[0] > 1288:
            self._spawn = False
                                 
class MainLoop:
    def __init__(self):
        self.__exit_game = False                                  # the exit game variable is set to false initially 
        self._game_screen = display.set_mode((1288,728))             # the game screen is set to a certain size
        self.__map = image.load("Prototype 1\Prototype 1 Assets\map.png")                            # the map is loaded with an image
        self.__font = font.Font(None,36)                              # the font is set to a size of 36
        self.__tower_selection = TowerSelection()                     # will inherit from the TowerSelection class for its attributes
        self.__select_rect = Rect(400,575,488,153)                   # this is the black rectangle which will be the background for the selection (it will be at the bottom)
        self.__tower1 = image.load("Prototype 1\Prototype 1 Assets/towerDefense_tile249.png")
        self.__tower2 = image.load("Prototype 1\Prototype 1 Assets/towerDefense_tile250.png")
        self.__tower1_rect = Rect(450,600,64,64)                    # this is the outline for the towers in the tower selection box
        self.__tower2_rect = Rect(750,600,64,64)
        self.__tower_selection._tower1_rect = self.__tower1_rect        # makes it so that the TowerSelection class can use it for selection
        self.__tower_selection._tower2_rect = self.__tower2_rect
        self.__enemyGroup = EnemyGroup() 
        mixer.music.load("Prototype 1\Prototype 1 Assets\loop3.ogg")
        mixer.music.play(-1)

    def displayStats(self):
        self._display_money = self.__font.render("Money:" + str(self.__tower_selection._money), True, (255,255,255))
        self._game_screen.blit(self._display_money, (100,25))
        self._display_round = self.__font.render("Round:" + str(self.__enemyGroup._round), True, (255,255,255))
        self._game_screen.blit(self._display_round, (1100,25))

    def drawTowerbox(self):
        draw.rect(self._game_screen, (0,0,0), self.__select_rect)     # this draws the black rectangle
        draw.rect(self._game_screen, (255, 255, 255), self.__tower1_rect)  # this is the white rectangle for the outline
        draw.rect(self._game_screen, (255, 255, 255), self.__tower2_rect)
        self._game_screen.blit(self.__tower1, self.__tower1_rect)     # this blits it to the screen
        self._game_screen.blit(self.__tower2, self.__tower2_rect)
        cost1 = self.__font.render("Cost: " + str(self.__tower_selection._type1_cost), True, (255,255,255))  # this draws the cost of each tower to the screen
        cost2 = self.__font.render("Cost: " + str(self.__tower_selection._type2_cost), True, (255,255,255))
        self._game_screen.blit(cost1, (430,685))
        self._game_screen.blit(cost2, (730,685))
       
    def gameOver(self):
        if self.__enemyGroup._spawn == False:
            subprocess.Popen(['python', 'Prototype 3/game over.py'])
            self.__exit_game = True
       
    def gamescreen(self):
        while not self.__exit_game:
            mouse_pos = mouse.get_pos()  # gets the mouse position constantly while the game is running
            for e in event.get():
                if e.type == QUIT:
                    self.__exit_game = True   # will quit the game
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        if self.__tower_selection._selected_tower: # checks to see if there is a tower that has been selected
                            self.__tower_selection.place_tower(mouse_pos)  # this will run the code to then place the tower onto the game map
                        else:                                                   # if not
                            self.__tower_selection.select_tower(mouse_pos)  # will run the select tower function if the left mouse button is pressed
                elif e.type == KEYDOWN:
                    if e.key == K_ESCAPE:
                        self.__tower_selection._selected_tower = None  # will cancel the selection if the escape button is pressed
            
            if not self.__enemyGroup._enemies:          # if there are no more enemies in the array
                self.__enemyGroup.spawn_enemy()         # spawn in the next wave of enemies
                self.__enemyGroup._round+=1           
            
            for projectile in self.__tower._projectiles:
                projectile.draw(self._game_screen) 
                       
            self.__enemyGroup._enemies = self.__tower_selection.attack(self.__enemyGroup._enemies)
            self.__tower.update_projectiles(self.__enemyGroup._enemies)
            self._game_screen.blit(self.__map,(0,0))              # will blit the map to the screen
            self.drawTowerbox()                                 # will run the tower box function
            self._game_screen.blit(self.__tower_selection.stamped_surface, (0, 0))
            self.__tower_selection._enemies = self.__enemyGroup._enemies
            self.__tower_selection.drawTower_preview(self._game_screen,mouse_pos) # will run the tower box function using the screen and pos as parameters
            self.__enemyGroup.updateEnemies(self._game_screen)
            self.Projectile(self._game_screen)           
            self.displayStats()
            self.gameOver()
            display.flip()
            clock.tick(60)                                  # sets the refresh rate to 60hz

loop = MainLoop()
loop.gamescreen()


