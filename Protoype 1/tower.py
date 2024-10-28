from pygame import *
import math
init()
display.set_caption('Frontlines')
font.init()

class Tower:                              # creates a tower class
    def __init__(self,pos):
        self.range = 10                 #sets the tower range and damage to a set number, the position will depend on where the tower is placed.
        self.damage = 20
        self.pos = pos
        self.target = None     # initialy the targeted enemy is set to none as it will be changed when an enemy is near
        self.type1 = image.load("towerDefense_tile249.png")        # the sprites for the 2 different towers must be loaded as they are pre made images from an asset pack 
        self.type2 = image.load("towerDefense_tile250.png")
        self.projectile = image.load("towerDefense_tile251.png")      # the same for the projectile
        self.type1_cost = 100
        self.type2_cost = 150
    
    def inRange(self,enemy):
        centre_x = self.tower.pos[0] + self.type1.get_height()//2          # to calculate the the centre of the images we take the bottom left corner co-ordinates and add in the height and width
        centre_y = self.tower.pos[1] + self.type2.get_width()//2
        enemy_centre_x = self.enemy.x + self.enemy.image.get_height()//2        # do the same for the enemy centre
        enemy_centre_y = self.enemy.y + enemy.image.get_width()//2
        distance = math.sqrt((centre_x - enemy_centre_x)**2 + (centre_y - enemy_centre_y)**2)       # using triganometry to calucate the distance between the enemy and tower
        return distance <= self.range
    def attack(self,enemy,inRange):                       # using the inRange() fucntion attack the nearest tower 
        self.willhit = inRange(self,target,enemy[target])
        if self.target and self.willhit:                                 # if an enemy has been found and it's in range then deal damage
            self.target.take_damage(self.damage)
            if self.target.health <= 0:                            # if an enemy is killed then set the target back to 0
                self.target = None
        else:
            self.new_target = newTarget(self,enemies)

            if self.new_target is not None:                                       # when there is no target set the target to the new one
                self.target = self.new_target
                self.target = self.take_damage(self.damage)                     # that target will then take damage
            else:
                self.target = None
    def newTarget(self,):                                                    # a function to assign a new enemy as the target
        self.area = inRange(self,enemy)
        for enemy in enemies:                                           # by checking a valid enemy within the group of enemies it will return the nearest enemy 
            if self.area:
                return enemy
        return None

class TowerSelection:                            # class specific for the selection of towers by the player
    def __init__(self):
        self.selected_tower = None                        # set the tower used as none initially
        self.money = 250                                # set money to the starting number
        self.tower1_rect = None
        self.tower2_rect = None
    
    def selected_tower(self,pos):
        if self.tower1_rect and self.tower1_rect.collidepoint(pos):# if the tower type selected is the first tower then the seleted tower is set as the first tower
            self.selected_tower = self.type1                   
        elif self.tower2_rect and self.tower2_rect.collidepoint(pos):# else use the second tower
            self.selected_tower = self.type2                      
    
    def place_tower(self):
        if self.selected_tower == self.type1:                        # if the first tower will be set as type 1
            if self.money >= self.type1_cost:
                if self.game_map.pos_valid(pos) == True:                  # it will use the validation function to check the position that is selected by the user
                    self.game_map.add_tower(selected_tower,pos)
                    self.money -= self.type1_cost                      #  it will then take the cost away from the money owned
                    self.selected_tower.draw()
                    selected_tower = None                            # it will reset the selected tower back to none
        elif self.selected_tower == self.type2:                           
            if self.money >= self.type2_cost:                           
                if self.game_map.pos_valid(pos) == True:
                    self.game_map.add_tower(selected_tower,pos)             # this code is repeated for the second type of tower
                    self.money -= self.type2_cost
                    self.selected_tower.draw()
                    selected_tower = None
    

                    
class Enemy:
    def __init__(self,image):
        self.image = image.load("towerDefense_tile248.png")
        self.health = 40
        self.number = 4
        self.speed = 6
        self.pos = []
        self.round = round

                    


    


class MainLoop:
    def __init__(self):
        font.init()
        self.exit_game = False
        self.game_screen = display.set_mode((1288,728))
        self.map = image.load("map.png")
        self.font = font.Font(None,36)
        self.tower_selection = TowerSelection()
        self.select_rect = Rect(1000,0,288,728)
        self.tower1 = image.load("towerDefense_tile249.png")
        self.tower2 = image.load("towerDefense_tile250.png")
        self.tower1_rect = Rect(1050,50,64,64)
        self.tower2_rect = Rect(1050,150,64,64)
        self.tower_selection.tower1_rect = self.tower1_rect
        self.tower_selection.tower2_rect = self.tower2_rect

    def drawTowerbox(self):
        draw.rect(self.game_screen, (0,0,0), self.select_rect)
        self.game_screen.blit(self.tower1, self.tower1_rect)
        self.game_screen.blit(self.tower2, self.tower2_rect)
        cost1 = font.render("Cost: " + str(self.tower_selection.type1_cost), True, (255,255,255))
        cost2 = font.render("Cost: " + str(self.tower_selection.type2_cost), True, (255,255,255))
        self.game_screen.blit(cost1, (1150,65))
        self.game_screen.blit(cost2, (1150,165))

    def gamescreen(self):
        while not self.exit_game:
            for e in event.get():
                if e.type == QUIT:
                    self.exit_game = True
                elif e.type == MOUSEBUTTONDOWN:
                    mouse_pos = mouse.get_pos()
                    if e.button == 1:
                        self.tower_selection.selected_tower(mouse_pos)
                
                self.game_screen.blit(self.map,(0,0))
                self.drawTowerbox()
                display.flip()

loop = MainLoop()
loop.gamescreen()


