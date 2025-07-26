import time
import math


from tkinter import PhotoImage

class VirtualBotController:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x, self.y = 250, 250
        import os
        img_path = os.path.join(os.path.dirname(__file__), "..", "robo.png")
        self.bot_img = PhotoImage(file=img_path).subsample(6, 6)
        self.bot_obj = canvas.create_image(self.x, self.y, image=self.bot_img)
        self.path = []
        self.color = "yellow"

    def move_bot(self, direction, distance=50):
        old_x, old_y = self.x, self.y
        if direction == "forward":
            self.y -= distance
        elif direction == "backward":
            self.y += distance
        elif direction == "left":
            self.x -= distance
        elif direction == "right":
            self.x += distance
        self.path.append((old_x, old_y, self.x, self.y))
        self.update_position()

    def move_bot_diagonal(self, direction, distance=50):
        old_x, old_y = self.x, self.y
        if direction == "forward-left":
            self.x -= distance / 1.414
            self.y -= distance / 1.414
        elif direction == "forward-right":
            self.x += distance / 1.414
            self.y -= distance / 1.414
        elif direction == "backward-left":
            self.x -= distance / 1.414
            self.y += distance / 1.414
        elif direction == "backward-right":
            self.x += distance / 1.414
            self.y += distance / 1.414
        self.path.append((old_x, old_y, self.x, self.y))
        self.update_position()

    def move_bot_bezier(self, x1, y1, x2, y2, x3, y3, steps=20):
        old_x, old_y = self.x, self.y
        for t in [i/steps for i in range(steps+1)]:
            xt = (1-t)**2 * x1 + 2*(1-t)*t*x2 + t**2*x3
            yt = (1-t)**2 * y1 + 2*(1-t)*t*y2 + t**2*y3
            self.path.append((self.x, self.y, xt, yt))
            self.x, self.y = xt, yt
            self.update_position()
            self.canvas.update()
            time.sleep(0.05)

    def reset_bot(self):
        self.x, self.y = 250, 250
        self.path.clear()
        self.color = "yellow"
        self.update_position()
        self.canvas.delete("path_line")

    def change_color(self, color):
        self.color = color
        # Color change is not supported for images, so this is a no-op for image bot

    def update_position(self):
        self.canvas.coords(self.bot_obj, self.x, self.y)
        # Draw path
        if self.path:
            x0, y0, x1, y1 = self.path[-1]
            self.canvas.create_line(x0, y0, x1, y1, fill="blue", tags="path_line")
