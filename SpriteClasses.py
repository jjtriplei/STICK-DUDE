from Utils import *
from tkinter import PhotoImage
import time

class Coords:
        def __init__(self, x1=0, y1=0, x2=0, y2=0):
                self.x1 = x1
                self.y1 = y1
                self.x2 = x2
                self.y2 = y2

class Sprite:
        def __init__(self, game):
                self.game = game
                self.endgame = False
                self.coordinates = None

        def move(self):
                pass
        def coords(self):
                return self.coordinates

class PlatformSprite(Sprite):
        def __init__(self, game, photo_image, x, y, width, height):
                Sprite.__init__(self, game)
                self.photo_image = photo_image
                self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
                self.coordinates = Coords(x, y, x + width, y + height)

class StickFigureSprite(Sprite):
        def __init__(self, game):
                Sprite.__init__(self, game)
                self.images_left = [
                        PhotoImage(file="assets\L1.gif"),
                        PhotoImage(file="assets\L2.gif"),
                        PhotoImage(file="assets\L3.gif"),
                        PhotoImage(file="assets\L4.gif"),
                        PhotoImage(file="assets\L5.gif"),
                        PhotoImage(file="assets\L6.gif")
                ]
                self.images_right = [
                        PhotoImage(file="assets\R1.gif"),
                        PhotoImage(file="assets\R2.gif"),
                        PhotoImage(file="assets\R3.gif"),
                        PhotoImage(file="assets\R4.gif"),
                        PhotoImage(file="assets\R5.gif"),
                        PhotoImage(file="assets\R6.gif")
                ]
                self.image_idle_left = PhotoImage(file="assets\Lidle.gif")
                self.image_idle_left = PhotoImage(file="assets\Ridle.gif")
                self.image = game.canvas.create_image(200, 470, \
                        image=self.images_left[0], anchor='nw')
                self.x = 0
                self.y = 0
                self.current_image = 0
                self.current_image_add = 1
                self.jump_count = 0
                self.last_time = time.time()
                self.coordinates = Coords()
                self.canvas = game.canvas
                game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
                game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
                game.canvas.bind_all('<space>', self.jump)

        def turn_left(self, evt):
                if self.y == 0:
                        self.x = -2

        def turn_right(self, evt):
                if self.y == 0:
                        self.x = 2

        def jump(self, evt):
                if self.y == 0:
                        self.y = -4
                        self.jump_count = 0

        def animate(self):
                if self.x != 0 and self.y == 0:
                        if time.time() - self.last_time > 0.1:
                                self.last_time = time.time()
                                self.current_image += self.current_image_add
                                if self.current_image >= 2:
                                        self.current_image_add = -1
                                if self.current_image <= 0:
                                        self.current_image_add = 1
                if self.x < 0:
                        if self.y != 0:
                                self.game.canvas.itemconfig(self.image, \
                                        image=self.images_left[2])
                        else:
                                self.game.canvas.itemconfig(self.image, \
                                        image=self.images_left[self.current_image])
                elif self.x > 0:
                        if self.y != 0:
                                self.game.canvas.itemconfig(self.image, \
                                        image=self.images_right[2])
                        else:
                                self.game.canvas.itemconfig(self.image, \
                                        image=self.images_right[self.current_image])

        def coords(self):
                xy = self.game.canvas.coords(self.image)
                self.coordinates.x1 = xy[0]
                self.coordinates.y1 = xy[1]
                self.coordinates.x2 = xy[0] + 57
                self.coordinates.y2 = xy[1] + 63
                return self.coordinates

        def move(self):
                self.animate()
                if self.y < 0:
                        self.jump_count += 1
                        if self.jump_count > 20:
                                self.y = 4
                if self.y > 0:
                        self.jump_count -= 1
                co = self.coords()
                left = True
                right = True
                top = True
                bottom = True
                falling = True
                if self.y > 0 and co.y2 >= self.game.canvas_height:
                        self.y = 0
                        bottom = False
                elif self.y < 0 and co.y1 <= 0:
                        self.y = 0
                        top = False
                if self.x > 0 and co.x2 >= self.game.canvas_width:
                        self.x = 0
                        right = False
                elif self.x < 0 and co.x1 <= 0:
                        self.x = 0
                        left = False
                for sprite in self.game.sprites:
                        if sprite == self:
                                continue
                        sprite_co = sprite.coords()
                        if top and self.y < 0 and collided_top(co, sprite_co):
                                self.y = -self.y
                                top = False
                        if bottom and self.y > 0 and collided_bottom(self.y, \
                                        co, sprite_co):
                                self.y = sprite_co.y1 - co.y2
                                if self.y < 0:
                                        self.y = 0
                                bottom = False
                                top = False
                        if bottom and falling and self.y == 0 \
                                        and co.y2 < self.game.canvas_height \
                                        and collided_bottom(1, co, sprite_co):
                                falling = False
                        if left and self.x < 0 and collided_left(co, sprite_co):
                                self.x = 0
                                left = False
                                if sprite.endgame:
                                        self.game.running = False
                        if right and self.x > 0 and collided_right(co, sprite_co):
                                self.x = 0
                                right = False
                                if sprite.endgame:
                                        self.game.running = False
                if falling and bottom and self.y == 0 \
                                and co.y2 < self.game.canvas_height:
                        self.y = 4
                self.game.canvas.move(self.image, self.x, self.y)

        def debug(self):
                self.canvas.create_text(10, 10, text=self.current_image)

class DoorSprite(Sprite):
        def __init__(self, game, photo_image, x, y, width, height):
                Sprite.__init__(self, game)
                self.photo_image = photo_image
                self.image = game.canvas.create_image(x, y, \
                        image=self.photo_image, anchor='nw')
                self.coordinates = Coords(x, y, x + (width / 2), y + height)
                self.endgame = True