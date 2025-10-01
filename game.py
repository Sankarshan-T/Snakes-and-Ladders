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
                        font=('Helvetica', 16, 'bold'), 
                        foreground='white', 
                        background='#B40519',
                        padding=10)
        style.map('Roll.TButton',
                  background=[('active', '#45a049')])

        self.positions = [0, 0]
        self.current_player = 0

        self.dice_images = [ImageTk.PhotoImage(Image.open(f"dicefaces/{i}.png").resize((50, 50))) for i in range(1,7)]

        self.roll_btn = ttk.Button(root, text="Roll Dice", style='Roll.TButton', command=self.roll_dice)
        self.roll_btn.pack(pady=10)

        self.status = tk.Label(root, text="Player 1's turn", font=('Helvetica', 14))
        self.status.pack()

        self.dice_label = tk.Label(root)
        self.dice_label.pack(pady=5)

        self.draw_tokens()

    def get_coords(self, square):
        if square < 1 or square > 100:
            return None
        num = square - 1
        row = 9 - (num // 10)
        col = num % 10 if row % 2 != 0 else 9 - (num % 10)
        cell_size = self.board_img.width // 10
        x = col * cell_size + cell_size // 2
        y = row * cell_size + cell_size // 2
        return x, y

    def draw_tokens(self):
        self.canvas.delete("token")
        colors = ["#0003c2", "#ff0062"]
        for i, pos in enumerate(self.positions):
            if pos == 0:
                continue
            x, y = self.get_coords(pos)
            r = 15
            self.canvas.create_oval(x - r + i * 10, y - r, x + r + i * 10, y + r, fill=colors[i], tags="token")

    def animate_dice(self, callback):
        rolls = 10
        def roll_animation(count=0):
            if count < rolls:
                face = random.randint(1, 6)
                self.dice_label.config(image=self.dice_images[face-1])
                self.root.after(100, roll_animation, count + 1)
            else:
                callback()
        roll_animation()

    def roll_dice(self):
        self.roll_btn.config(state="disabled")
        self.status.config(text=f"Player {self.current_player + 1} is rolling...")
        self.animate_dice(self.after_dice_roll)

    def after_dice_roll(self):
        dice = random.randint(1, 6)
        self.dice_label.config(image=self.dice_images[dice-1])
        self.status.config(text=f"Player {self.current_player + 1} rolled a {dice}")
        self.move_player_smooth(dice)
        

    def move_player_smooth(self, dice):
        start = self.positions[self.current_player]
        path = []

        for step in range(1, dice + 1):
            next_pos = start + step
            if next_pos > 100:
                next_pos = start
                break
            path.append(next_pos)

        def move_step(i=0):
            if i < len(path):
                pos = path[i]
                self.positions[self.current_player] = pos
                self.draw_tokens()
                self.root.after(300, move_step, i+1)
            else:
                self.check_snake_ladder()

        move_step()

    def check_snake_ladder(self):
        pos = self.positions[self.current_player]
        if pos in snakes:
            self.status.config(text=f"Player {self.current_player + 1} bitten by snake! Going down...")
            self.positions[self.current_player] = snakes[pos]
            self.draw_tokens()
            self.root.after(700, self.finish_turn)
        elif pos in ladders:
            self.status.config(text=f"Player {self.current_player + 1} climbs a ladder! Going up...")
            self.positions[self.current_player] = ladders[pos]
            self.draw_tokens()
            self.root.after(700, self.finish_turn)
        else:
            self.finish_turn()

    def finish_turn(self):
        pos = self.positions[self.current_player]
        if pos == 100:
            self.status.config(text=f"Player {self.current_player + 1} wins!")
            self.roll_btn.config(state="disabled")
            return
        self.current_player = 1 - self.current_player
        self.status.config(text=f"Player {self.current_player + 1}'s turn")
        self.roll_btn.config(state="normal")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x700")
    game = SnakeLadderGame(root)
    root.mainloop()
