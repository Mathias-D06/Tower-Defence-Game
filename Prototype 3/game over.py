from pygame import *
font.init()
mixer.init()

class Main:
    def __init__(self):
        self.__exit = False
        self._game_screen = display.set_mode((1288,728))
        self.__big_font = font.Font(None, 70)
        self.__small_font = font.Font(None,45)
        self.__background = image.load("Prototype 3\Prototype 3\Background.png")
    
    def Game_Over(self):
        self.__game_over = self.__big_font.render("Game Over", True, (255,255,255))
        self._game_screen.blit(self.__game_over,(500,224))
  
    def Retry(self):
        self.__retry = self.__small_font.render("Play Again", True, (255,255,255))
        self.__retry_rect = self.__retry.get_rect(topleft=(200, 500))
        self._game_screen.blit(self.__retry,self.__retry_rect)
    
    def ReplayGame(self):
        self.__replay = self.__small_font.render("Play Again", True, (255,255,255))
        self.__replay_rect = self.__retry.get_rect(topleft=(900, 500))
        self._game_screen.blit(self.__replay,self.__replay_rect)

    def MainLoop(self):
        while not self.__exit:
            for e in event.get():
                if e.type == QUIT:
                    self.__exit = True
            self._game_screen.blit(self.__background,(0,0))
            self.Game_Over()
            self.Retry()
            self.ReplayGame()
            display.flip()

system = Main()
system.MainLoop()
