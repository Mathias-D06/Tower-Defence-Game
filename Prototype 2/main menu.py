from pygame import *
init()
mixer.init()
font.init()
clock = time.Clock()
display.set_caption("Frontlines")

class MenuLoop:
   def __init__(self):
       self.__exit = False
       self.__start = False
       self._main_screen = display.set_mode((1285,700))
       self._background = image.load("Prototype 2\Prototype 2 Assets\image_fx_ (1) downscale.jpg")
       mixer.music.load("Prototype 2\Prototype 2 Assets\menu_chill.wav")
       mixer.music.play(-1)
       self.__font = font.Font(None,50)
   
   def Buttons(self):
       self.__start_button = self.__font.render("Start", True, (255,255,255))
       self.__settings_button = self.__font.render("Settings", True, (255,255,255))
       self.__start_rect = self.__start_button.get_rect(topleft=(300,550))
       self.__settings_rect = self.__settings_button.get_rect(topleft=(850,550))
       self._main_screen.blit(self.__start_button, self.__start_rect)
       self._main_screen.blit(self.__settings_button, self.__settings_rect)
   
   def Collision(self, mouse_pos):    
       if self.__start_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
           self.__start = True
       elif self.__settings_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
           print("Opening Settings")
   
   def MainLoop(self):
       while not self.__start and not self.__exit:
           mouse_pos = mouse.get_pos()
           for e in event.get():
               if e.type == QUIT:
                   self.__exit = True

           self._main_screen.blit(self._background,(0,0))
           self.Buttons()
           self.Collision(mouse_pos)
           display.flip()
           clock.tick(60)
       
       return self.__start

system = MenuLoop()
system.MainLoop()