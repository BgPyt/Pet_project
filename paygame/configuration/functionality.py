from paygame.configuration.initialization.py import Ship, Label
import tkinter.messagebox as mb
from tkinter import Button
import time

first_time = None
game_time = None


class MyButton(Button):
    init_pole_human = 20
    prev = None
    Message_window = None

    def __init__(self, master, x, y, player, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.config(command=lambda cls=self.__class__: self.click(cls))
        self.x = x
        self.y = y
        self.player = player
        self.is_ship = False  # есть ли тут корабль
        self.ship = None  # ссылка на объект корабля
        self.shoot_down = False

    def click(self, cls):
        if cls.init_pole_human > 0:
            self.separation_human(cls)
        if cls.init_pole_human == 0 and self.player[0] == 'bot':
            self.damage_human()

    def damage_human(self):
        if self.is_ship:
            ship = self.ship
            ship.count -= 1
            self.player[1].counter_ships -= 1
            self.shoot_down = True
            self.config(bg=ship.color)
            self['state'] = 'disable'
            self.player[1].game_state(self.__class__)
            if ship.count == 0:
                for vd in ship.bt_lst:
                    vd.config(text='☠', bg='red')

        else:
            self['state'] = 'disable'
            self.config(text='⊗', fg='#000000')
            self.player[1].damage_bot(self.__class__)

    def __call__(self, *args, **kwargs):
        mb.showwarning('Невозможно', 'Нужно ставить в один ряд за следующим')

    def location(self):
        """Проверка, что последующий клик будет по рядом по горизонтали или вертикали относительно первого нажатия
        выставленной кнопки """
        if (self.x, self.y) in [(self.prev.x + 1, self.prev.y), (self.prev.x - 1, self.prev.y),
                                (self.prev.x, self.prev.y + 1), (self.prev.x, self.prev.y - 1)]:
            return True

        else:
            self()

    def is_validator(self, deck=None):
        """Проверка валидации и конфигарция виджетов на то, что они не выходят за границу и нету ли занимаемым им
        полем других кораблей """
        lst = self.player[1].buttons
        x, y = self.x, self.y
        if self.init_pole_human > 10 and self.prev is None:
            if x <= 8 and not lst[x + 1][y].is_ship:
                return True
            if x >= 1 and not lst[x - 1][y].is_ship:
                return True
            if y <= 8 and not lst[x][y + 1].is_ship:
                return True
            if y >= 1 and not lst[x][y - 1].is_ship:
                return True
            mb.showwarning('Пользовательская ошибка', 'Нельзя тут выставить')
            return False

        if self.prev is None and deck:
            if x <= 6 and not lst[x + 1][y].is_ship and not lst[x + 2][y].is_ship and not lst[x + 3][y].is_ship:
                return True
            if x >= 3 and not lst[x - 1][y].is_ship and not lst[x - 2][y].is_ship and not lst[x - 3][y].is_ship:
                return True
            if y <= 6 and not lst[x][y + 1].is_ship and not lst[x][y + 2].is_ship and not lst[x][y + 3].is_ship:
                return True
            if y >= 3 and not lst[x][y - 1].is_ship and not lst[x][y - 2].is_ship and not lst[x][y - 3].is_ship:
                return True
            mb.showwarning('Пользовательская ошибка', 'Нельзя тут выставить')
            return False

        if self.prev is None:
            if x <= 7 and not lst[x + 1][y].is_ship and not lst[x + 2][y].is_ship:
                return True
            if x >= 2 and not lst[x - 1][y].is_ship and not lst[x - 2][y].is_ship:
                return True
            if y <= 7 and not lst[x][y + 1].is_ship and not lst[x][y + 2].is_ship:
                return True
            if y >= 2 and not lst[x][y - 1].is_ship and not lst[x][y - 2].is_ship:
                return True
            mb.showwarning('Пользовательская ошибка', 'Нельзя тут выставить')
            return False
        else:
            if not deck and self.location():
                t = ('y', y) if x == self.prev.x else ('x', x)
                if 1 <= t[1] <= 8:
                    select_y = t[1] - (self.prev.y - y)
                    select_x = t[1] - (self.prev.x - x)
                    if 'y' in t and not lst[x][select_y].is_ship:
                        bt = lst[x][select_y]
                        bt.ship = self.prev.ship
                        bt.is_ship = True
                        bt.ship.bt_lst.append(bt)
                        bt.config(bg='violet')
                        return True
                    if 'x' in t and not lst[select_x][y].is_ship:
                        bt = lst[select_x][y]
                        bt.ship = self.prev.ship
                        bt.is_ship = True
                        bt.ship.bt_lst.append(bt)
                        bt.config(bg='violet')
                        return True
                    else:
                        return False

            if deck and self.location():
                t = ('y', y) if x == self.prev.x else ('x', x)
                select_y = t[1] - (self.prev.y - y)
                select_x = t[1] - (self.prev.x - x)
                if (select_y > 0 and t[0] == 'y') or (select_x > 0 and t[0] == 'x'):
                    if 'y' in t and not lst[x][select_y].is_ship and not lst[x][select_y - (self.prev.y - y)].is_ship:
                        for bt in (lst[x][select_y], lst[x][select_y - (self.prev.y - y)]):
                            bt.ship = self.prev.ship
                            bt.is_ship = True
                            bt.ship.bt_lst.append(bt)
                            bt.config(bg='black')
                        return True
                    if 'x' in t and not lst[select_x][y].is_ship and not lst[select_x - (self.prev.x - x)][y].is_ship:
                        for bt in (lst[select_x][y], lst[select_x - (self.prev.x - x)][y]):
                            bt.ship = self.prev.ship
                            bt.is_ship = True
                            bt.ship.bt_lst.append(bt)
                            bt.config(bg='black')
                        return True
                    else:
                        return False

    def separation_human(self, cls):
        if self.player[0] == 'human' and self.ship is None:
            self.message_player(cls)
            if cls.init_pole_human > 16:
                self.ship = Ship('single_deck', 1, '#8B4513')
                cls.init_pole_human = cls.init_pole_human - 1
                self.is_ship = True
                self.ship.bt_lst.append(self)
                self.config(bg='#8B4513')
            elif cls.init_pole_human > 10:
                if not cls.prev and self.is_validator():
                    self.ship = Ship('double_deck', 2, 'orange')
                    self.is_ship = True
                    self.ship.bt_lst.append(self)
                    self.config(bg='orange')
                    cls.prev = self
                    cls.init_pole_human = cls.init_pole_human - 1
                elif cls.prev and self.location():
                    self.ship = self.prev.ship
                    self.is_ship = True
                    self.ship.bt_lst.append(self)
                    self.config(bg='orange')
                    cls.init_pole_human = cls.init_pole_human - 1
                    cls.prev = None
            elif cls.init_pole_human > 4 and self.is_validator():
                if not self.prev:
                    self.ship = Ship('three_deck', 3, 'violet')
                    self.is_ship = True
                    self.ship.bt_lst.append(self)
                    self.config(bg='violet')
                    cls.prev = self
                    cls.init_pole_human = cls.init_pole_human - 1
                elif cls.prev:
                    self.ship = self.prev.ship
                    self.is_ship = True
                    self.ship.bt_lst.append(self)
                    self.config(bg='violet')
                    cls.init_pole_human = cls.init_pole_human - 2
                    cls.prev = None
                    self.message_player(cls)
            elif cls.init_pole_human <= 4 and self.is_validator(True):
                if not self.prev:
                    self.ship = Ship('four_deck', 4, 'black')
                    self.is_ship = True
                    self.ship.bt_lst.append(self)
                    self.config(bg='black')
                    cls.prev = self
                    cls.init_pole_human = cls.init_pole_human - 2
                elif cls.prev:
                    self.ship = self.prev.ship
                    self.is_ship = True
                    self.ship.bt_lst.append(self)
                    self.config(bg='black')
                    cls.init_pole_human = cls.init_pole_human - 2
                    cls.prev = None
                    self.message_player(cls)
        else:
            mb.showwarning('Предупреждение', 'Что-то пошло ни так')

    def message_player(self, cls):
        if cls.init_pole_human == 17:
            self.player[1].message_window.place_forget()
            cls.Message_window = Label(self.master, text='Выставите три двухпалубных корабля', foreground="#B71C1C",
                                       background="#FFCDD2", font=('Bauhaus 93', 18))
            cls.Message_window.place(x=0, y=0)

        elif cls.init_pole_human == 11:
            cls.Message_window.config(text='Выставите два трехпалубных корабля')

        elif cls.init_pole_human == 4:
            cls.Message_window.config(text='Выставите один четырехпалубный корабль')

        elif cls.init_pole_human == 0:
            cls.Message_window.place_forget()
            cls.Message_window = Label(self.master, text='Игра началась', foreground="#1E90FF",
                                       background="#FFEBCD", font=('TkTooltipFont:', 18))
            cls.Message_window.place(x=400, y=0)
            self.movement_time(cls)

    def movement_time(self, cls):
        start_time = time.time()
        global first_time
        if first_time is None:
            first_time = time.time()
        global game_time
        game_time = time.gmtime(start_time - first_time)
        if cls.Message_window is None:
            first_time = None
            game_time = None
        current_timer = f'{str(game_time.tm_min).rjust(2, "0")}:{str(game_time.tm_sec).rjust(2, "0")}'
        self.master.after(1000, lambda clap=cls: self.movement_time(clap))
        cls.Message_window.config(text=f'ИГРА НАЧАЛАСЬ\n{current_timer}')

    def __str__(self):
        return f'{self.x} {self.y}'
