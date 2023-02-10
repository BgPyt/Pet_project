from tkinter import Tk, Label, Button, PhotoImage
import random
from GamePlay import *


class Ship:

    def __init__(self, name, count, color):
        self.name = name
        self.count = count
        self.color = color
        self.bt_lst = []

    def __repr__(self):
        return f'{self.name, self.count}'


class Game_pole:
    row = 10
    column = 10

    def __init__(self, tk, x, y, player):
        self.buttons = [[MyButton(tk, j, i, (player, self), width=3, bg='#33f') for i in range(self.column)] for j in
                        range(self.row)]
        for i in range(self.row):
            for j in range(self.column):
                btn = self.buttons[i][j]
                btn.place(x=i * 29 + x, y=j * 26 + y) # Расположение каждого виджета на окне из перебора матрицы

    def separation_bot(self):
        pass


class Window:

    def __init__(self):
        tk = Tk()
        image = PhotoImage(file='123.png')
        Label(image=image).pack(fill='both')
        tk.iconphoto(False, PhotoImage(file='unnamed.png'))
        tk.title('Морской бой')
        tk.geometry('1000x700')
        tk.resizable(False, False)
        global message_window
        message_window = Label(tk, text='Выставите четыре однопалубных корабля', font=('Bauhaus 93', 18))
        message_window.place(x=0, y=0)
        game_human = Game_pole(tk, 100, 200, 'human')
        game_bot = Game_pole(tk, 600, 200, 'bot')
        tk.mainloop()


def start():
    play = Window()


if __name__ == '__main__':
    start()
