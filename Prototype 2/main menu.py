from pygame import *
init()
clock = time.Clock()
display.set_caption("Frontlines")


class MenuLoop:
    def __init__(self):
        self.__exit = False
        self.__start = False
        self._main_screen = display.set_mode((1285,700))
        self._background = image.load("Prototype 2\Prototype 2 Assets\image_fx_ (1) downscale.jpg")
    
    def mainLoop(self):
        while not self.__start and not self.__exit:
            for e in event.get():
                if e.type == QUIT:
                    self.__exit = True
                elif e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        break
            



            self._main_screen.blit(self._background,(0,0))                    
            display.flip()
            clock.tick(60)

system = MenuLoop()
system.mainLoop()