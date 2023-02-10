from game_to import *
import tkinter.messagebox as mb


class MyButton(Button):
    init_pole_human = 20
    prev = None
    Message_window = None

    def __init__(self, master, x, y, player, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.config(command=lambda x=self.__class__: self.click(x))
        self.x = x
        self.y = y
        self.player = player
        self.is_ship = False  # есть ли тут корабль
        self.ship = None  # ссылка на объект корабля
        self.shoot_down = False

    def click(self, cls):
        if cls.init_pole_human > 0:
            self.separation_human(cls)

    def call_error(self):
        mb.showwarning('Невозможно', 'Нужно ставить в один ряд за следующим')

    def location(self):
        if (self.x, self.y) in [(self.prev.x + 1, self.prev.y), (self.prev.x - 1, self.prev.y),
                                (self.prev.x, self.prev.y + 1), (self.prev.x, self.prev.y - 1)]:
            return True

    def is_validator(self, deck=None):
        lst = self.player[1].buttons
        x, y = self.x, self.y
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
                        print(t[1] - (self.prev.x - x))
                        bt.ship = self.prev.ship
                        bt.is_ship = True
                        bt.ship.bt_lst.append(bt)
                        bt.config(bg='violet')
                        return True
                    else:
                        return False

            if deck and self.location():
                t = ('y', y) if x == self.prev.x else ('x', x)
                if 2 <= t[1] <= 7:
                    select_y = t[1] - (self.prev.y - y)
                    select_x = t[1] - (self.prev.x - x)
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
                else:
                    return False

    def separation_human(self, cls):
        if self.player[0] == 'human' and self.ship is None:
            self.message_player(cls)
            if cls.init_pole_human > 16:
                self.ship = Ship('single_deck', 1, 'red')
                cls.init_pole_human = cls.init_pole_human - 1
                self.is_ship = True
                self.ship.bt_lst.append(self)
                self.config(bg='red')
            elif cls.init_pole_human > 10:
                if not cls.prev:
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
                else:
                    self.call_error()
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
            elif cls.init_pole_human > 1 and self.is_validator(True):
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
        else:
            mb.showwarning('Предупреждение', 'Что-то пошло ни так')

    def message_player(self, cls):
        if cls.init_pole_human == 17:
            Message_window.place_forget()
            cls.Message_window = Label(self.master, text='Выставите три двухпалубных корабля', font=('Bauhaus 93', 18))
            cls.Message_window.place(x=0, y=0)

        elif cls.init_pole_human == 11:
            cls.Message_window.place_forget()
            cls.Message_window.config(text='Выставите два трехпалубных корабля')


        elif cls.init_pole_human == 6:
            pass




    def __repr__(self):
        return f'Button({self.ship},{self.x}, {self.y})'
