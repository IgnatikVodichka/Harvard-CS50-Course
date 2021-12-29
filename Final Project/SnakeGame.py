import random
from tkinter import *
from typing import KeysView
from PIL import Image, ImageTk


WIDTH = 1000
HEIGHT = 1000
BODY_SIZE = 40
START_DELAY = 400
LENGTH = 3

count_body_width = WIDTH / BODY_SIZE
count_body_height = HEIGHT / BODY_SIZE


class Snake(Canvas):
    x = False
    y = False
    head_image = False
    head = False
    body = False
    cat = False
    delay = 0
    direction = "Right"
    direction_temp = "Right"
    loss = False

    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT,
                        background="black", highlightthickness=0)
        self.focus_get()
        self.bind_all("<Key>", self.on_key_pressed)
        self.load_resources()
        self.start_play()
        self.pack()

    def load_resources(self):
        self.head_image = Image.open("images/ducky.png")
        self.head = ImageTk.PhotoImage(self.head_image.resize(
            (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open(
            "images/duckling.png").resize((BODY_SIZE - 10, BODY_SIZE - 10), Image.ANTIALIAS))
        self.cat = ImageTk.PhotoImage(Image.open(
            "images/cat.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))

    def start_play(self):
        self.delay = START_DELAY
        self.direction = "Right"
        self.loss = False
        self.x = [0] * int(count_body_width)
        self.y = [0] * int(count_body_height)
        self.delete(ALL)
        self.spawn_actors()
        self.after(self.delay, self.timer)

    def timer(self):
        self.check_collision()
        if not self.loss:
            self.check_cat()
            self.update_direction()
            self.move_snake()
            self.after(self.delay, self.timer)
        else:
            self.game_over()

    def spawn_actors(self):
        self.cat_spawn()
        self.x[0] = int(count_body_width / 2) * BODY_SIZE
        self.y[0] = int(count_body_height / 2) * BODY_SIZE
        for i in range(1, LENGTH):
            self.x[i] = self.x[0] - BODY_SIZE * i
            self.y[i] = self.y[0]
        self.create_image(self.x[0], self.y[0], image=self.head,
                          anchor="se", tag="head")
        for i in range(LENGTH - 1, 0, -1):
            self.create_image(self.x[i], self.y[i], image=self.body,
                              anchor="se", tag="body")

    def cat_spawn(self):
        cat = self.find_withtag("cat")
        if cat:
            self.delete(cat[0])
        apple_x = random.randint(0, count_body_width - 5)
        apple_y = random.randint(0, count_body_height - 5)
        self.create_image(apple_x * BODY_SIZE, apple_y *
                          BODY_SIZE, image=self.cat, anchor="nw", tag="cat")

    def check_cat(self):
        cat = self.find_withtag("cat")[0]
        head = self.find_withtag("head")
        body_last_part = self.find_withtag("body")[-1]
        x1, y1, x2, y2 = self.bbox(head)
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for actor in overlaps:
            if actor == cat:
                tempx, tempy = self.coords(body_last_part)
                self.cat_spawn()
                self.create_image(
                    tempx, tempy, image=self.body, anchor="se", tag="body")
                if self.delay > 100:
                    self.delay -= 20

    def check_collision(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        x1, y1, x2, y2 = self.bbox(head)
        overlaps = self.find_overlapping(x1, y1, x2, y2)
        for b in body:
            for actor in overlaps:
                if actor == b:
                    self.loss = True
        if x1 < 0 or x2 > WIDTH:
            self.loss = True
        if y1 < 0 or y2 > HEIGHT:
            self.loss = True

    def on_key_pressed(self, event):
        key = event.keysym
        if key == "Left" and self.direction != "Right":
            self.direction_temp = key
        elif key == "Right" and self.direction != "Left":
            self.direction_temp = key
        elif key == "Up" and self.direction != "Down":
            self.direction_temp = key
        elif key == "Down" and self.direction != "Up":
            self.direction_temp = key
        elif key == "space" and self.loss:
            self.start_play()

    def update_direction(self):
        self.direction = self.direction_temp
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        head_x, head_y = self.coords(head)
        self.delete(head)
        rotate_directions = {"Right": 0, "Up": 90, "Down": -90}
        if self.direction == "Left":
            self.head = ImageTk.PhotoImage(self.head_image.transpose(Image.FLIP_LEFT_RIGHT).resize(
                (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            self.create_image(head_x, head_y, image=self.head,
                              anchor="se", tag="head")
            self.body = ImageTk.PhotoImage(Image.open(
                "images/duckling.png").transpose(Image.FLIP_LEFT_RIGHT).resize((BODY_SIZE - 10, BODY_SIZE - 10), Image.ANTIALIAS))
            for i in range(len(body)):
                body_x, body_y = self.coords(body[i])
                self.delete(body[i])
                self.create_image(body_x, body_y, image=self.body,
                                  anchor="se", tag="body")
        else:
            self.head = ImageTk.PhotoImage(self.head_image.rotate(rotate_directions[self.direction]).resize(
                (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            self.create_image(head_x, head_y, image=self.head,
                              anchor="se", tag="head")
            self.body = ImageTk.PhotoImage(Image.open(
                "images/duckling.png").rotate(rotate_directions[self.direction]).resize((BODY_SIZE - 10, BODY_SIZE - 10), Image.ANTIALIAS))
            for i in range(len(body)):
                body_x, body_y = self.coords(body[i])
                self.delete(body[i])
                self.create_image(body_x, body_y, image=self.body,
                                  anchor="se", tag="body")

    def move_snake(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        items = body+head
        for i in range(len(items) - 1):
            current_x_y = self.coords(items[i])
            next_x_y = self.coords(items[i+1])
            self.move(items[i], next_x_y[0] - current_x_y[0],
                      next_x_y[1] - current_x_y[1])
        if self.direction == "Left":
            self.move(head, -BODY_SIZE, 0)
        elif self.direction == "Right":
            self.move(head, BODY_SIZE, 0)
        elif self.direction == "Up":
            self.move(head, 0, -BODY_SIZE)
        elif self.direction == "Down":
            self.move(head, 0, BODY_SIZE)

    def game_over(self):
        self.delete(ALL)
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 - 60,
                         text="Game Over", fill="red", font="Tahoma 40", tag="text")
        self.create_text(self.winfo_width() / 2, self.winfo_height() / 2 + 30,
                         text="Press space to try again", fill="white", font="Tahoma 25", tag="text")


root = Tk()
root.title("SnakeGmae")
root.board = Snake()
root.resizable(False, False)

w_user_width = root.winfo_screenwidth()
w_user_height = root.winfo_screenheight()

x = int(w_user_width / 2 - WIDTH / 2)
y = int(w_user_height / 2 - HEIGHT / 2)

root.geometry(f"+{x}+{y}")

root.mainloop()
