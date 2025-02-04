from pygame import *
font.init()

class Main:
    def __init__(self):
        self.__exit = False
        self._game_screen = display.set_mode((1288,728))
        self.__font = font.Font(None, 70)
    
    def Text(self):
        self.__game_over = self.__font.render("Game Over", True, (255,255,255))
        self._game_screen.blit(self.__game_over,(500,224))
  
    def MainLoop(self):
        while not self.__exit:
            for e in event.get():
                if e.type == QUIT:
                    self.__exit = True
            self._game_screen.fill((128,128,128))
            self.Text()
            display.flip()

system = Main()
system.MainLoop()
