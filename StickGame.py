from tkinter import *
import random
import time
from SpriteClasses import Sprite, PlatformSprite, StickFigureSprite, DoorSprite

class Game:
        def __init__(self):
                self.tk = Tk()
                self.tk.title("Stick Man Races")
                self.tk.resizable(0, 0)
                self.tk.wm_attributes("-topmost", 1)
                self.canvas = Canvas(self.tk, width=1600, height=900, highlightthickness=0)
                self.canvas.pack()
                self.tk.update()
                self.canvas_height = 900
                self.canvas_width = 1600
                self.bg = PhotoImage(file="assets/background3.gif")
                w = self.bg.width()
                h = self.bg.height()
                for x in range(0, 33):
                        for y in range(0, 20):
                                self.canvas.create_image(x * w, y * h, image=self.bg, anchor='nw')
                self.sprites = []
                self.running = True

        def mainloop(self):
                while 1:
                        if self.running == True:
                                for sprite in self.sprites:
                                        sprite.move()
                        self.tk.update_idletasks()
                        self.tk.update()
                        time.sleep(0.01)


g = Game()
# platform1 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 0, 480, 100, 10)
# platform2 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 150, 440, 100, 10)
# platform3 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 400, 100, 10)
# platform4 = PlatformSprite(g, PhotoImage(file="platform1.gif"), 300, 160, 100, 10)
# platform5 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 175, 350, 66, 10)
# platform6 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 50, 300, 66, 10)
# platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 170, 120, 66, 10)
# platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"), 45, 60, 66, 10)
# platform9 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 170, 250, 32, 10)
# platform10 = PlatformSprite(g, PhotoImage(file="platform3.gif"), 230, 200, 32, 10)
# g.sprites.append(platform1)
# g.sprites.append(platform2)
# g.sprites.append(platform3)
# g.sprites.append(platform4)
# g.sprites.append(platform5)
# g.sprites.append(platform6)
# g.sprites.append(platform7)
# g.sprites.append(platform8)
# g.sprites.append(platform9)
# g.sprites.append(platform10)
# door = DoorSprite(g, PhotoImage(file="door1.gif"), 45, 30, 40, 35)
# g.sprites.append(door)
sf = StickFigureSprite(g)
g.sprites.append(sf)
sf.debug()
g.mainloop()