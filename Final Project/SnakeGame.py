from os import DirEntry
import random
from tkinter import *
from PIL import Image, ImageTk
import random


WIDTH = 1000
HEIGHT = 1000
BODY_SIZE = 40
START_DELAY = 200
LENGTH = 2

count_body_width = WIDTH / BODY_SIZE
count_body_height = HEIGHT / BODY_SIZE

x = [0] * int(count_body_width)
y = [0] * int(count_body_height)


class Snake(Canvas):

    head_image = False
    head = False
    body = False
    tail = False
    apple = False
    delay = 0
    direction = "Right"
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
        self.head_image = Image.open("images/head_right.png")
        self.head = ImageTk.PhotoImage(self.head_image.resize(
            (BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open(
            "images/body_horizontal.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open(
            "images/apple.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.tail = ImageTk.PhotoImage(Image.open(
            "images/tail_left.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))

    def start_play(self):
        delay = START_DELAY
        self.direction = "Right"
        self.loss = False

        self.delete(ALL)
        self.spawn_actors()

    def spawn_actors(self):
        self.apple_spawn()
        x[0] = int(count_body_width / 2) * BODY_SIZE
        y[0] = int(count_body_height / 2) * BODY_SIZE
        for i in range(1, LENGTH):
            x[i] = x[0] - BODY_SIZE * i
            y[i] = y[0]
        self.create_image(x[0], y[0], image=self.head, anchor="nw", tag="head")
        for i in range(LENGTH - 1, 0, -1):
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
        pass


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
