from pygame import *
import subprocess
import sys
import os
init()
mixer.init()
font.init()
clock = time.Clock()
display.set_caption("Frontlines")

class MenuLoop:
   def __init__(self):
       self.__exit = False      # sets the exit condition to false
       self._main_screen = display.set_mode((1285,700))  # sets the screen size
       self._background = image.load("Prototype 2\Prototype 2 Assets\image_fx_ (1) downscale.jpg") # loads the background image
       mixer.music.load("Prototype 2\Prototype 2 Assets\menu_chill.wav")  # loads the background music
       mixer.music.play(-1) # plays the background music in a continuous loop
       self.__font = font.Font(None,50) # sets the font and size of the text
       self.__start = False
   
   def Buttons(self):
       self.__start_button = self.__font.render("Start", True, (255,255,255)) # sets the text and colour of the text
       self.__settings_button = self.__font.render("Settings", True, (255,255,255)) # same for this
       self.__start_rect = self.__start_button.get_rect(topleft=(300,550)) # sets the position of the text using the top left corner
       self.__settings_rect = self.__settings_button.get_rect(topleft=(850,550)) # same for this
       self._main_screen.blit(self.__start_button, self.__start_rect) # displays the text on the screen
       self._main_screen.blit(self.__settings_button, self.__settings_rect) # same for this
   
   def Collision(self, mouse_pos):    
       if self.__start_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]: # checks for mouse collision and mouse click
           mixer.music.stop() # stops the music
           self.__start = True
           subprocess.Popen(['python', 'Prototype 1/tower.py'])
       elif self.__settings_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]: # same as above
           print("Opening Settings") # currently a placeholder
   
   def SystemLoop(self):
       while not self.__start and not self.__exit: # checks if the exit conditions is false
           mouse_pos = mouse.get_pos() # gets the mouse position constantly
           for e in event.get(): # checks for events
               if e.type == QUIT:  # if the user closes the window
                   self.__exit = True  # sets exit to true                   

           self._main_screen.blit(self._background,(0,0)) # blits the background image at the top left corner
           self.Buttons() # runs the buttons function
           self.Collision(mouse_pos) # checks for collision using the mouse position as a parameter
           display.flip() 
           clock.tick(60) # sets the frame rate to 60

system = MenuLoop() # creates an instance of the class
system.SystemLoop() # runs the main loop