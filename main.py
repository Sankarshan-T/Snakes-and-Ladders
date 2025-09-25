import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

snakes = {40: 3, 27: 5, 43: 18, 54: 31, 66: 45, 99: 41, 76: 58, 91: 53}
ladders = {4: 25, 13: 46, 33: 49, 50: 69, 42: 63, 62: 81, 74: 92, 71: 91, 80: 100}

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snakes and Ladders")

        self.board_img = Image.open("board.jpg")
        self.board_tk = ImageTk.PhotoImage(self.board_img)
        self.canvas = tk.Canvas(root, width=self.board_img.width, height=self.board_img.height)
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor="nw", image=self.board_tk)

        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Roll.TButton',
                        font=('Helvetica', 16, 'Bold'),
                        foreground='white',
                        background="#B40519",
                        padding='10')