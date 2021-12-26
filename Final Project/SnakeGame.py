from os import DirEntry
from tkinter import *
from PIL import Image, ImageTk


WIDTH = 1000
HEIGHT = 1000
BODY_SIZE = 40
START_DELAY = 200
LENGTH = 3

count_body_width = WIDTH / BODY_SIZE
count_body_height = HEIGHT / BODY_SIZE

x = [0] * int(count_body_width)
y = [0] * int(count_body_height)


class Snake(Canvas):

    head_image = False
    head = False
    body = False
    apple = False
    delay = 0
    direction = "Right"
    loss = False

    def __init__(self):
        Canvas.__init__(self, width=WIDTH, height=HEIGHT, background="black")
        self.focus_get()
        self.bind_all("<Key>", self.on_key_pressed)
        self.load_resources()
        self.start_play()

    def load_resources(self):
        self.head_image = Image.open("images/head_right.png")
        self.head = ImageTk.PhotoImage(self.head_image.resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.body = ImageTk.PhotoImage(Image.open(
            "images/body_horizontal.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))
        self.apple = ImageTk.PhotoImage(Image.open("images/apple.png").resize((BODY_SIZE, BODY_SIZE), Image.ANTIALIAS))

    def start_play(self):
        delay = START_DELAY
        self.direction = "Right"
        self.loss = False

        self.delete(ALL)
        self.spawn_actors()

    def spawn_actors(self):
        x[0] = int(count_body_width / 2) * BODY_SIZE
        y[0] = int(count_body_height / 2) * BODY_SIZE

    def on_key_pressed(self, event):
        pass


root = Tk()
root.title("SnakeGmae")
root.board = Snake()
root.resizable(False, False)

w_width = root.winfo_reqwidth()
w_height = root.winfo_reqheight()

w_user_width = root.winfo_screenwidth()
w_user_height = root.winfo_screenheight()

x = int(w_user_width / 2 - w_width / 2)
y = int(w_user_height / 2 - w_height / 2)

root.geometry(f"+{x}+{y}")

root.mainloop()
