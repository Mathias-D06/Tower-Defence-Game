from pygame import *
import subprocess
init()
mixer.init()
font.init()
clock = time.Clock()
display.set_caption("Frontlines")

class VolumeSlider:
    def __init__(self, pos:tuple, size:tuple, initial:float, min:int, max:int):
        self.__pos = pos
        self.__size = size
        self._slider_left = self.__pos[0] - (size[0]//2)
        self._slider_right = self.__pos[0] + (size[0]//2)
        self._slider_top = self.__pos[1] - (size[1]//2)
        self.min = min
        self.max = max
        self._initial = (self._slider_right - self._slider_left) * initial
        self._box_rect = Rect(self._slider_left, self._slider_top, self.__size[0], self.__size[1])
        self._button_rect = Rect(self._slider_left + (self._initial - 5), self._slider_top, 10, self.__size[1])

    def moveSlider(self, mouse_pos):
        self._button_rect.centerx = mouse_pos[0]
        self.volumeChange()

    def drawSlider(self, screen):
        draw.rect(screen, (0, 0, 0), self._box_rect)
        draw.rect(screen, (255, 0, 0), self._button_rect)
    
    def getValue(self):
        self.range = self._slider_right - self._slider_left - 1
        self.button_value = self._button_rect.centerx - self._slider_left
        return (self.button_value/self.range)*(self.max-self.min)+self.min
    
    def volumeChange(self):
        self.volume = (self.getValue() / 100)
        mixer.music.set_volume(self.volume)
        self.current_volume = mixer.music.get_volume()
        print(self.volume * 100)

class MenuLoop:
    def __init__(self):
        self.__exit = False
        self._main_screen = display.set_mode((1285,700))
        self._background = image.load("Prototype 2\Prototype 2 Assets\image_fx_ (1) downscale.jpg")
        mixer.music.load("Prototype 2\Prototype 2 Assets\menu_chill.wav")
        mixer.music.play(-1)
        self.__font = font.Font(None,50)
        self.__start = False
        self.__settings = False

    def Buttons(self):
        self.__start_button = self.__font.render("Start", True, (255,255,255))
        self.__settings_button = self.__font.render("Settings", True, (255,255,255))
        self.__start_rect = self.__start_button.get_rect(topleft=(300,550))
        self.__settings_rect = self.__settings_button.get_rect(topleft=(850,550))
        self._main_screen.blit(self.__start_button, self.__start_rect)
        self._main_screen.blit(self.__settings_button, self.__settings_rect)

    def Collision(self, mouse_pos):
        if self.__start_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
            mixer.music.stop()
            self.__start = True
            subprocess.Popen(['python', 'Prototype 1/tower.py'])
        elif self.__settings_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
            self.__settings = True

    def SystemLoop(self):
        while not self.__start and not self.__exit and not self.__settings:
            mouse_pos = mouse.get_pos()
            for e in event.get():
                if e.type == QUIT:
                    self.__exit = True
            self._main_screen.blit(self._background, (0, 0))
            self.Buttons()
            self.Collision(mouse_pos)
            if self.__settings:
                return SettingsScreen().ScreenLoop()
            display.flip()
            clock.tick(60)

class SettingsScreen(MenuLoop):
    def __init__(self):
        MenuLoop.__init__(self)
        self.__font = font.Font(None, 40)
        self._settingsScreen = self._main_screen
        self.__settings = True
        self.__exit = False
        self.slider = VolumeSlider((642, 400), (500, 40), 1, 0, 100)
        self._screen = image.load("Prototype 2\Prototype 2 Assets\image_fx_ (1).jpg")

    def Return(self, mouse_pos):
        self.__back_button = self.__font.render("Back", True, (255,255,255))
        self.__back_rect = self.__back_button.get_rect(topleft=(50, 600))
        self._settingsScreen.blit(self.__back_button, self.__back_rect)
        if self.__back_rect.collidepoint(mouse_pos) and mouse.get_pressed()[0]:
            self.__settings = False
            print("pressed return")
            print("going back to main menu")
            return "menu"
    
    def Text(self):
        self.__volume_text = self.__font.render("Volume", True, (255,255,255))
        self._settingsScreen.blit(self.__volume_text, (590,500))

    def drawSlider(self, mouse_pos, mouse_click):
        self.slider.drawSlider(self._settingsScreen)
        if self.slider._box_rect.collidepoint(mouse_pos) and mouse_click[0]:
            self.slider.moveSlider(mouse_pos)

    def ScreenLoop(self):
        while self.__settings and not self.__exit:
            mouse_pos = mouse.get_pos()
            mouse_click = mouse.get_pressed()
            for e in event.get():
                if e.type == QUIT:
                    self.__exit = True
            self._settingsScreen.blit(self._screen, (0, 0))
            self.drawSlider(mouse_pos, mouse_click)
            self.Text()
            switch = self.Return(mouse_pos)
            if switch == "menu":
                return MenuLoop().SystemLoop()
            display.flip()
            clock.tick(60)

system = MenuLoop()
system.SystemLoop()


