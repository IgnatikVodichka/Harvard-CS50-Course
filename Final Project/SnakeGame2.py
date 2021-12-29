import random
from tkinter import *
from typing import KeysView
from PIL import Image, ImageTk


WIDTH = 1000
HEIGHT = 1000
BODY_SIZE = 40
START_DELAY = 1000
LENGTH = 8

count_body_width = WIDTH / BODY_SIZE
count_body_height = HEIGHT / BODY_SIZE

x = [0] * int(count_body_width)
y = [0] * int(count_body_width)


class Snake(Canvas):

    head_image = False
    head = False
    body = False
    tail = False
    apple = False
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
        self.head_image = Image.open("images/head.png")
        self.head = ImageTk.PhotoImage(self.head_image.resize(
            (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open(
            "images/body_horizontal.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open(
            "images/apple.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.tail = ImageTk.PhotoImage(Image.open(
            "images/tail.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))

    def start_play(self):
        self.delay = START_DELAY
        self.direction = "Right"
        self.loss = False

        self.delete(ALL)
        self.spawn_actors()
        self.after(self.delay, self.timer)

    def spawn_actors(self):
        self.apple_spawn()
        x[0] = int(count_body_width / 2) * BODY_SIZE
        y[0] = int(count_body_height / 2) * BODY_SIZE
        for i in range(1, LENGTH):
            x[i] = x[0] - BODY_SIZE * i
            y[i] = y[0]
        self.create_image(x[0], y[0], image=self.head, anchor="nw", tag="head")
        for i in range(LENGTH - 1, 0, -1):
            if i == LENGTH - 1:
                self.create_image(x[i], y[i], image=self.tail,
                                  anchor="nw", tag="tail")
            else:
                self.create_image(x[i], y[i], image=self.body,
                                  anchor="nw", tag="body")

    def apple_spawn(self):
        apple = self.find_withtag("apple")
        if apple:
            self.delete(apple[0])
        apple_x = random.randint(0, count_body_width - 1)
        apple_y = random.randint(0, count_body_height - 1)
        self.create_image(apple_x * BODY_SIZE, apple_y *
                          BODY_SIZE, image=self.apple, anchor="nw", tag="apple")

    def on_key_pressed(self, event):
        key = event.keysym
        if key == "Left" and self.direction != "Right":
            self.direction_temp = key
        if key == "Right" and self.direction != "Left":
            self.direction_temp = key
        if key == "Up" and self.direction != "Down":
            self.direction_temp = key
        if key == "Down" and self.direction != "Up":
            self.direction_temp = key

    def update_direction(self):
        self.direction = self.direction_temp
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        tail = self.find_withtag("tail")
        head_x, head_y = self.coords(head)
        tail_x, tail_y = self.coords(tail)
        self.delete(head)
        self.delete(body)
        self.delete(tail)

        rotate_directions = {"Right": 0, "Up": 90, "Down": -90}
        if self.direction == "Left":
            self.head = ImageTk.PhotoImage(self.head_image.transpose(Image.FLIP_LEFT_RIGHT).resize(
                (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            self.create_image(head_x, head_y, image=self.head,
                              anchor="nw", tag="head")
            self.tail = ImageTk.PhotoImage(Image.open(
                "images/tail.png").transpose(Image.FLIP_LEFT_RIGHT).resize(
                (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            self.create_image(tail_x, tail_y, image=self.tail,
                              anchor="nw", tag="tail")

        else:
            self.head = ImageTk.PhotoImage(self.head_image.rotate(rotate_directions[self.direction]).resize(
                (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            self.create_image(head_x, head_y, image=self.head,
                              anchor="nw", tag="head")
            self.tail = ImageTk.PhotoImage(Image.open(
                "images/tail.png").rotate(rotate_directions[self.direction]).resize(
                (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            self.create_image(tail_x, tail_y, image=self.tail,
                              anchor="nw", tag="tail")
            # for i in range(LENGTH - 1, 0, -1):
            #     body_x, body_y = self.coords(body)
            # self.body = ImageTk.PhotoImage(Image.open(
            #     "images/body_horizontal.png").rotate(rotate_directions[self.direction]).resize(
            #     (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
            # for i in range(LENGTH - 1, 0, -1):
            #     self.create_image(x[i], y[i], image=self.body,
            #                       anchor="nw", tag="body")

    def timer(self):
        if not self.loss:
            self.update_direction()
            self.move_snake()
            self.after(self.delay, self.timer)

    def move_snake(self):
        head = self.find_withtag("head")
        body = self.find_withtag("body")
        tail = self.find_withtag("tail")
        items = tail+body+head
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
