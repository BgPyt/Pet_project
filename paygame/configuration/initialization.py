from functionality import *
from tkinter import Tk, Label, PhotoImage
from random import randint, choice


class Ship:

    def __init__(self, name, count, color):
        self.name = name
        self.count = count
        self.color = color
        self.bt_lst = []  # список виджетов
        self.attempts = set()  # множество ходов
        self.lst_button = []  # Список всех найденных кораблей

    def __repr__(self):
        return f'{self.name, self.count}'


class Game_pole:
    row = 10
    column = 10
    players = []
    button = None  # значение ссылки на виджет, предоставляемый последний искомый
    unfinished = []
    lb = None
    Message_window = None

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        cls.players.append(obj)
        return obj

    def __init__(self, tk, x, y, player):
        self.buttons = [[MyButton(tk, j, i, (player, self), width=3, bg='#B0E0E6') for i in range(self.column)] for j in
                        range(self.row)]
        self.counter_ships = 20
        for i in range(self.row):
            for j in range(self.column):
                btn = self.buttons[i][j]
                btn.place(x=i * 29 + x, y=j * 26 + y)  # Расположение каждого виджета на окне из перебора матрицы
        if player == 'human':
            self.message_window = Label(tk, text='Выставите четыре однопалубных корабля', foreground="#B71C1C",
                                        background="#FFCDD2", font=('Bauhaus 93', 18))
            self.message_window.place(x=0, y=0)

    @classmethod
    def damage_bot(cls, category):
        if not cls.unfinished:
            while True:
                button = choice(choice(cls.players[0].buttons)) if cls.button is None else cls.button
                if button.shoot_down is False or button == cls.button:
                    break
        else:
            button = choice(cls.unfinished)
        while button.is_ship is True:
            vessel = button.ship
            if button.shoot_down is False:
                vessel.lst_button.append(button)
                cls.button = button
                cls.unfinished.append(cls.button)
                ship = button.ship
                ship.count -= 1
                cls.players[0].counter_ships -= 1
                button.shoot_down = True
                button.config(bg=ship.color, text='☠')
                button['state'] = 'disable'
                cls.game_state(category)
                if ship.count == 0:
                    for vd in ship.bt_lst:
                        vd.config(bg='red', text='X', fg='#696969')
                        cls.unfinished.remove(vd)
                        cls.button = None
                    if not cls.unfinished:
                        while True:
                            button = choice(choice(cls.players[0].buttons))
                            if button.shoot_down is False:
                                break
                    else:
                        button = choice(cls.unfinished)
                    continue
            cls.game_state(category)
            if len(vessel.lst_button) == 1:
                x = button.x
                y = button.y
                while True:
                    button = choice(
                        [cls.players[0].buttons[
                             choice((x + 1, x - 1)) if 1 <= x <= 8 else (x + 1, x - 1)[0 if x <= 8 else 1]][y],
                         cls.players[0].buttons[x][
                             choice((y + 1, y - 1)) if 1 <= y <= 8 else (y + 1, y - 1)[0 if y <= 8 else 1]]])
                    if button.shoot_down is False:
                        break
                continue
            elif len(vessel.lst_button) == 2:
                if vessel.lst_button[0].x == vessel.lst_button[1].x:  # Если равны по x
                    obj = max(vessel.lst_button, key=lambda el: int(str(el).split()[1]))
                    if obj.y < 9 and cls.players[0].buttons[obj.x][obj.y + 1] not in vessel.attempts \
                            and cls.players[0].buttons[obj.x][obj.y + 1].shoot_down is False:
                        button = cls.players[0].buttons[obj.x][obj.y + 1]
                        vessel.attempts.add(button)
                        continue
                    elif obj.y > 1:
                        button = cls.players[0].buttons[obj.x][obj.y - 2]
                        vessel.attempts.add(button)
                        continue
                else:
                    obj = max(vessel.lst_button, key=lambda el: int(str(el).split()[0]))
                    if obj.x < 9 and cls.players[0].buttons[obj.x + 1][obj.y] not in vessel.attempts \
                            and cls.players[0].buttons[obj.x + 1][obj.y].shoot_down is False:
                        button = cls.players[0].buttons[obj.x + 1][obj.y]
                        vessel.attempts.add(button)
                        continue
                    elif obj.x > 1 and cls.players[0].buttons[obj.x - 2][obj.y] not in vessel.attempts:
                        button = cls.players[0].buttons[obj.x - 2][obj.y]
                        vessel.attempts.add(button)
                        continue
            elif len(vessel.lst_button) == 3:
                if vessel.lst_button[0].x == vessel.lst_button[1].x == vessel.lst_button[2].x:
                    obj = max(vessel.lst_button, key=lambda el: int(str(el).split()[1]))
                    if obj.y < 9 and cls.players[0].buttons[obj.x][obj.y + 1] not in vessel.attempts \
                            and cls.players[0].buttons[obj.x][obj.y + 1].shoot_down is False:
                        button = cls.players[0].buttons[obj.x][obj.y + 1]
                        vessel.attempts.add(button)
                        continue
                    elif obj.y > 3 and cls.players[0].buttons[obj.x][obj.y - 3] not in vessel.attempts:
                        button = cls.players[0].buttons[obj.x][obj.y - 3]
                        vessel.attempts.add(button)
                        continue
                else:
                    obj = max(vessel.lst_button, key=lambda el: int(str(el).split()[0]))
                    if obj.x < 9 and cls.players[0].buttons[obj.x + 1][obj.y] not in vessel.attempts \
                            and cls.players[0].buttons[obj.x + 1][obj.y].shoot_down is False:
                        button = cls.players[0].buttons[obj.x + 1][obj.y]
                        vessel.attempts.add(button)
                        continue
                    elif obj.x > 3 and cls.players[0].buttons[obj.x - 3][obj.y] not in vessel.attempts:
                        button = cls.players[0].buttons[obj.x - 3][obj.y]
                        vessel.attempts.add(button)
                        continue
        button.config(text='⊗')
        button.shoot_down = True
        button['state'] = 'disable'

    @classmethod
    def game_state(cls, category):
        """Состояние игры"""
        if cls.players[0].counter_ships == 0:  # Побеждает противник
            for i in range(10):
                for j in range(10):
                    cls.players[0].buttons[i][j]['state'] = 'disable'
                    cls.players[1].buttons[i][j]['state'] = 'disable'
            category.Message_window.destroy()
            cls.Message_window = Label(text='Вы проиграли!(ಥ﹏ಥ)', bg='#B22222', font=('Bauhaus 93', 48, "bold"))
            cls.Message_window.place(x=180, y=0)
            category.Message_window = None

        elif cls.players[1].counter_ships == 0:  # Выигрывает пользаватель
            for i in range(10):
                for j in range(10):
                    cls.players[0].buttons[i][j]['state'] = 'disable'
                    cls.players[1].buttons[i][j]['state'] = 'disable'
            category.Message_window.destroy()
            cls.Message_window = Label(text='Вы победили!', bg='#B22222', font=("Bauhaus 93", 48, "bold"))
            cls.Message_window.place(x=250, y=0)
            category.Message_window = None

    def separation_bot(self):
        """Инициализация игрового поля ИИ"""
        pole_ship = 20
        Ships = [(Ship('double_deck', 2, 'orange'), Ship('double_deck', 2, 'orange'), Ship('double_deck', 2, 'orange')),
                 (Ship('three_deck', 3, 'violet'), Ship('three_deck', 3, 'violet')),
                 Ship('four_deck', 4, 'black')
                 ]
        for x in range(10):
            for y in range(10):
                band = self.buttons[randint(0, 9)][randint(0, 9)]
                if pole_ship > 16 and band.is_ship is False:
                    band.is_ship = True
                    band.ship = Ship('single_deck', 1, '#8B4513')
                    band.ship.bt_lst.append(band)
                    pole_ship -= 1
                    continue
                elif pole_ship > 10 and band.is_ship is False:
                    band.is_ship = True
                    band.ship = Ships[0][0 if pole_ship > 14 else [1, 2][0 if pole_ship > 12 else 1]]
                    band.ship.bt_lst.append(band)
                    band_2 = choice(list(filter(None, (self[band.x - 1, band.y], self[band.x + 1, band.y],
                                                       self[band.x, band.y - 1], self[band.x + 1, band.y]))))
                    band_2.is_ship = True
                    band_2.ship = Ships[0][0 if pole_ship > 14 else [1, 2][0 if pole_ship > 12 else 1]]
                    band_2.ship.bt_lst.append(band_2)
                    pole_ship -= 2
                elif pole_ship > 4 and band.is_ship is False:
                    if band.x <= 7 and self.buttons[band.x + 1][band.y].is_ship is False and \
                            self.buttons[band.x + 2][band.y].is_ship is False:
                        for ind in [band.x, band.x + 1, band.x + 2]:
                            self.buttons[ind][band.y].is_ship = True
                            self.buttons[ind][band.y].ship = Ships[1][0 if pole_ship > 7 else 1]
                            self.buttons[ind][band.y].ship.bt_lst.append(self.buttons[ind][band.y])
                        pole_ship -= 3
                    elif band.x >= 2 and self.buttons[band.x - 1][band.y].is_ship is False and self.buttons[band.x - 2][
                         band.y].is_ship is False:
                        for ind in [band.x, band.x - 1, band.x - 2]:
                            self.buttons[ind][band.y].is_ship = True
                            self.buttons[ind][band.y].ship = Ships[1][0 if pole_ship > 7 else 1]
                            self.buttons[ind][band.y].ship.bt_lst.append(self.buttons[ind][band.y])
                        pole_ship -= 3
                    elif band.y <= 7 and self.buttons[band.x][band.y + 1].is_ship is False and self.buttons[band.x][
                         band.y + 2].is_ship is False:
                        for ind in [band.y, band.y + 1, band.y + 2]:
                            self.buttons[ind][band.y].is_ship = True
                            self.buttons[ind][band.y].ship = Ships[1][0 if pole_ship > 7 else 1]
                            self.buttons[ind][band.y].ship.bt_lst.append(self.buttons[ind][band.y])
                        pole_ship -= 3
                    elif band.y >= 2 and self.buttons[band.x][band.y - 1].is_ship is False and self.buttons[band.x][
                         band.y - 2].is_ship is False:
                        for ind in [band.y, band.y - 1, band.y - 2]:
                            self.buttons[ind][band.y].is_ship = True
                            self.buttons[ind][band.y].ship = Ships[1][0 if pole_ship > 7 else 1]
                            self.buttons[ind][band.y].ship.bt_lst.append(self.buttons[ind][band.y])
                        pole_ship -= 3
                elif pole_ship > 1 and band.is_ship is False:
                    if band.x <= 6 and self.buttons[band.x + 1][band.y].is_ship is False and \
                            self.buttons[band.x + 2][band.y].is_ship is False \
                            and self.buttons[band.x + 3][band.y].is_ship is False:
                        for ind in [band.x, band.x + 1, band.x + 2, band.x + 3]:
                            self.buttons[ind][band.y].is_ship = True
                            self.buttons[ind][band.y].ship = Ships[2]
                            self.buttons[ind][band.y].ship.bt_lst.append(self.buttons[ind][band.y])
                        pole_ship -= 4
                    elif band.x >= 3 and self.buttons[band.x - 1][band.y].is_ship is False and \
                            self.buttons[band.x - 2][band.y].is_ship is False \
                            and self.buttons[band.x - 3][band.y].is_ship is False:
                        for ind in [band.x, band.x - 1, band.x - 2, band.x - 3]:
                            self.buttons[ind][band.y].is_ship = True
                            self.buttons[ind][band.y].ship = Ships[2]
                            self.buttons[ind][band.y].ship.bt_lst.append(self.buttons[ind][band.y])
                        pole_ship -= 4
                    elif band.y <= 6 and self.buttons[band.x][band.y + 1].is_ship is False and self.buttons[band.x][
                         band.y + 2].is_ship is False and self.buttons[band.x][band.y + 3].is_ship is False:
                        for ind in [band.y, band.y + 1, band.y + 2, band.y + 3]:
                            self.buttons[band.x][ind].is_ship = True
                            self.buttons[band.x][ind].ship = Ships[2]
                            self.buttons[band.x][ind].ship.bt_lst.append(self.buttons[band.x][ind])
                        pole_ship -= 4
                    elif band.y >= 3 and self.buttons[band.x][band.y - 1].is_ship is False and self.buttons[band.x][
                         band.y - 2].is_ship is False and self.buttons[band.x][band.y - 3].is_ship is False:
                        for ind in [band.y, band.y - 1, band.y - 2, band.y - 3]:
                            self.buttons[band.x][ind].is_ship = True
                            self.buttons[band.x][ind].ship = Ships[2]
                            self.buttons[band.x][ind].ship.bt_lst.append(self.buttons[band.x][ind])
                        pole_ship -= 4

    def __getitem__(self, item):
        if 0 <= item[0] <= 9 and 0 <= item[1] <= 9 and self.buttons[item[0]][item[1]].is_ship is False:
            return self.buttons[item[0]][item[1]]
        return None


class Window:

    def __init__(self):
        tk = Tk()
        image = PhotoImage(file='123.png')
        Label(image=image).pack(fill='both')
        Button(text='Начать заново', font=("Bauhaus 93", 20, "bold"),
               command=lambda root=tk: self.restart(root)).place(x=0, y=650)
        Button(text='Выйти', font=("Bauhaus 93", 20, "bold"),
               command=tk.quit).place(x=890, y=650)
        tk.iconphoto(False, PhotoImage(file='unnamed.png'))
        tk.title('Морской бой')
        tk.geometry('1000x700')
        tk.resizable(False, False)
        Game_pole(tk, 100, 200, 'human')
        game_bot = Game_pole(tk, 600, 200, 'bot')
        game_bot.separation_bot()
        tk.mainloop()

    @staticmethod
    def restart(tk) -> None:
        MyButton.init_pole_human = 20
        MyButton.prev = None
        if MyButton.Message_window:
            MyButton.Message_window.destroy()
        if Game_pole.Message_window:
            Game_pole.Message_window.destroy()
            Game_pole.Message_window = None
        MyButton.Message_window = None
        Game_pole.players = []
        Game_pole.button = None
        Game_pole.unfinished = []
        Game_pole(tk, 100, 200, 'human')
        game_bot = Game_pole(tk, 600, 200, 'bot')
        game_bot.separation_bot()


def start():
    Window()


if __name__ == '__main__':
    start()
