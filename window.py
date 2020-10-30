__author__ = 'Anthony Byuraev'


import os
import sqlite3
import tkinter as tk
from tkinter import constants
from tkinter.ttk import Notebook


class Uscon(tk.Tk):
    def __init__(self):
        super().__init__()

        self.FONT_SIZE = 14
        self.WINDOW_SIZE = '400x300'
        self.WINDOW_TITLE = 'Uscon - учет использования компьютеров'

        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_SIZE)

        self.notebook = Notebook(self)

        self.frame_top = tk.Frame(self.notebook)
        self.frame_login = tk.Frame(self.notebook)
        self.frame_password = tk.Frame(self.notebook)
        self.frame_bottom = tk.Frame(self.notebook)

        self.label = tk.Label(self.frame_top, text="Пожалуйста, введите логин и пароль.")

        self.label_login = tk.Label(self.frame_top, text="Логин: ")
        self.entry_login = tk.Entry(self.frame_top)

        self.label_password = tk.Label(self.frame_top, text="Пароль: ")
        self.entry_password = tk.Entry(self.frame_top)

        self.label_pc_number = tk.Label(self.frame_top, text="Номер компьютера: ")
        self.entry_pc_number = tk.Entry(self.frame_top)

        self.notebook.add(self.frame_top, text='Запись')
        self.notebook.add(self.frame_login, text='Запись')
        self.notebook.add(self.frame_login, text='Регистрация')
        self.notebook.add(self.frame_password, text='Администратор')
        self.notebook.pack(fill=constants.BOTH, expand=1)

        # self.frame_top.pack()
        # self.frame_login.pack()
        # self.frame_password.pack()
        # self.frame_bottom.pack()

        self.label.pack(padx=10, pady=10)

        self.label_login.pack(padx=5, pady=5, side=constants.TOP)
        self.entry_login.pack(padx=5, pady=5, side=constants.TOP)

        self.label_password.pack(padx=5, pady=5, side=constants.TOP)
        self.entry_password.pack(padx=5, pady=5, side=constants.TOP)

        self.label_pc_number.pack(padx=5, pady=5, side=constants.TOP)
        self.entry_pc_number.pack(padx=5, pady=5, side=constants.TOP)

        self.bind("<Return>", self.check_user)

    def write_to_database(self, event) -> None:
        """
        Write name, surname and etc. to 'Time_control' table
        """
        INSERT_USER_QUERY = (
            """
            INSERT INTO Time_control
            VALUES (?,?,?,?,?,?) 
            """
        )
        # insert_user_data = (name, surname, group, now, 1, pc_number)
        # self.run_query(INSERT_USER_QUERY, insert_user_data)
        return None

    def check_user(self, event):
        """
        Checks login and password in 'uscon.sqlite' database
        """
        login, password = self.entry_login.get(), self.entry_password.get()

        SELECT_USER_QUERY = 'SELECT password FROM Users WHERE login = ?'
        select_user_data = (login,)
        user_data = Uscon.run_query(
            SELECT_USER_QUERY, select_user_data, receive=True)[0]

        if user_data is not None \
           and password == user_data['password']:
            print('ok')
            return True
        elif user_data is not None:
            print('Введен неправильный пароль')
            self.label_log.config(text='Введен неправильный пароль')
            self.frame_bottom.pack(padx=10, pady=10, side=const.BOTTOM)
            return False
        else:
            print('Такого пользователя не существует')
            return None

    @staticmethod
    def run_query(query: str, data: tuple = None, receive: bool = False):
        """
        Run query to 'uscon.sqlite' database
        """
        conn = sqlite3.connect('uscon.sqlite')
        curs = conn.cursor()
        curs.row_factory = sqlite3.Row
        if data is not None:
            curs.execute(query, data)
        else:
            curs.execute(query)
        if receive is True:
            return curs.fetchall()
        else:
            conn.commit()
        conn.close()

    @staticmethod
    def create_database() -> None:
        """
        Creates 'uscon.sqlite' database with two tables:
            1) users;
            2) time_control.

        'Users' table:
            The table contains login, password, names, surnames
            and group number of students.

        'Time_control' table:
            The table contains names, surnames and group number
            of students, login and loguot time, PC number.
        """

        CREATE_USERS_TABLE = (
            """
            CREATE TABLE Users
            (
                id INTEGER NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                group_name TEXT NOT NULL
            )
            """
        )
        CREATE_TIME_CONTROL_TABLE = (
            """
            CREATE TABLE Time_control
            (
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                group_name TEXT NOT NULL,
                login_time TEXT,
                logout_time TEXT,
                pc_number INTEGER NOT NULL
            )
            """
        )
        INSERT_TRAIN_QUERY = 'INSERT INTO Users VALUES (?,?,?,?,?,?)'
        insert_train_data = (1, 'toha', '1234', 'Антон', 'Бюраев', 'СМ6-92')
        Uscon.run_query(CREATE_USERS_TABLE)
        Uscon.run_query(CREATE_TIME_CONTROL_TABLE)
        Uscon.run_query(INSERT_TRAIN_QUERY, insert_train_data)
        return None


if __name__ == "__main__":
    if os.path.isfile('uscon.sqlite') is False:
        Uscon.create_database()
    uscon = Uscon()
    uscon.mainloop()
