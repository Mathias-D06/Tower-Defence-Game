from pygame import *
font.init()
import subprocess

class Main:
    def __init__(self):
        self.__exit = False
        self._game_screen = display.set_mode((1288,728))
        self.__big_font = font.Font(None, 70)
        self.__small_font = font.Font(None,45)
        self.__background = image.load("Prototype 3\Prototype 3 Assets\Background.png")
        self.__retry = False
    
    def Game_Over(self):
        self.__game_over = self.__big_font.render("Game Over", True, (255,255,255))
        self._game_screen.blit(self.__game_over,(500,224))

    def Retry(self):
        self.__retry = self.__small_font.render("Play Again", True, (255,255,255))
        self.__retry_rect = self.__retry.get_rect(topleft=(200, 500))
        self._game_screen.blit(self.__retry,self.__retry_rect)
    
    def ReplayGame(self):
        self.__replay = self.__small_font.render("Replay", True, (255,255,255))
        self.__replay_rect = self.__retry.get_rect(topleft=(900, 500))
        self._game_screen.blit(self.__replay,self.__replay_rect)

    def Collision(self,mouse_pos):
        if self.__retry_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
            self.__retry = True
            subprocess.Popen(['python', 'Prototype 1/tower.py'])

    def MainLoop(self):
        while not self.__exit:
            mouse_pos = mouse.get_pos()
            for e in event.get():
                if e.type == QUIT:
                    self.__exit = True
            self._game_screen.blit(self.__background,(0,0))
            self.Game_Over()
            self.Retry()
            self.ReplayGame()
            self.Collision(mouse_pos)
            display.flip()

system = Main()
system.MainLoop()
