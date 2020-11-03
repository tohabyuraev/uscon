__author__ = 'Anthony Byuraev'


import os
import sqlite3
from typing import NamedTuple
from tkinter import StringVar, Tk
from tkinter import constants
from datetime import datetime
from tkinter.ttk import *


class Mode(NamedTuple):
    insert = 'insert'
    fetchone = 'fetchone'
    fetchall = 'fetchall'


class Uscon(Tk):
    def __init__(self):
        super().__init__()

        self.FONT_MAIN = 'Times 14'
        self.FONT_LABEL = 'Times 12'
        self.NUM_OF_PC = 16
        self.WINDOW_SIZE = '400x350'
        self.WINDOW_TITLE = 'Uscon - учет использования компьютеров'

        self.title(self.WINDOW_TITLE)
        self.geometry(self.WINDOW_SIZE)

        self.notebook = Notebook(self)

        # self.admin_tab = Frame(self.notebook)
        self.recording_tab = Frame(self.notebook, padding=40)
        self.registration_tab = Frame(self.notebook, padding=20)

        self.recording_tab_build()
        self.registration_tab_build()

        self.notebook.add(self.recording_tab, text='Запись')
        self.notebook.add(self.registration_tab, text='Регистрация')
        # self.notebook.add(self.admin_tab, text='Администратор')
        self.notebook.pack(fill=constants.BOTH, expand=1)

        self.bind('<Return>', self.write_recording)
    
    def recording_tab_build(self):
        """
        Builds recording tab in notebook
        """

        RECORDING_MESSAGE = 'Пожалуйста, введите логин и пароль.'

        self.recording_message = StringVar(self.recording_tab)
        self.recording_message.set(RECORDING_MESSAGE)
        Label(
            self.recording_tab, textvar=self.recording_message, font=self.FONT_MAIN
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        Label(self.recording_tab, text="Логин:", font=self.FONT_LABEL)\
            .grid(row=1, column=0, padx=5, pady=5)
        self.recording_login = Entry(self.recording_tab)
        self.recording_login.\
            grid(row=1, column=1, padx=5, pady=5)

        Label(self.recording_tab, text="Пароль:", font=self.FONT_LABEL)\
            .grid(row=2, column=0, padx=5, pady=5)
        self.recording_pass = Entry(self.recording_tab)
        self.recording_pass.\
            grid(row=2, column=1, padx=5, pady=5)

        Label(self.recording_tab, text="Номер компьютера:", font=self.FONT_LABEL)\
            .grid(row=3, column=0, padx=5, pady=5)
        self.recording_pc = StringVar(self.recording_tab, value='1')
        pc_variants = (
            pc_number for pc_number in range(self.NUM_OF_PC)
        )
        OptionMenu(
            self.recording_tab, self.recording_pc, *pc_variants
        ).grid(row=3, column=1, padx=5, pady=5)

        
        self.recording_mode = StringVar(self.recording_tab, value='None')
        Radiobutton(
            self.recording_tab, text='Вход', variable=self.recording_mode, value='Вход'
        ).grid(row=4, column=0, padx=5, pady=5)
        Radiobutton(
            self.recording_tab, text='Выход', variable=self.recording_mode, value='Выход'
        ).grid(row=4, column=1, padx=5, pady=5)
        
        Button(
            self.recording_tab, text="Готово", command=self.write_recording
        ).grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def registration_tab_build(self):
        """
        Builds recording tab in notebook
        """

        REGISTRATION_MESSAGE = (
            'Введите имя, фамилию и номер группы,\n'
            'а также новые логин и пароль.'
        )

        self.registration_message = StringVar(self.registration_tab)
        self.registration_message.set(REGISTRATION_MESSAGE)
        Label(
            self.registration_tab, textvar=self.registration_message, font=self.FONT_MAIN
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        Label(self.registration_tab, text="Имя:", font=self.FONT_LABEL).\
            grid(row=1, column=0, padx=5, pady=5)
        self.registration_name = Entry(self.registration_tab)
        self.registration_name.\
            grid(row=1, column=1, padx=5, pady=5)

        Label(self.registration_tab, text="Фамилия:", font=self.FONT_LABEL).\
            grid(row=2, column=0, padx=5, pady=5)
        self.registration_surname = Entry(self.registration_tab).\
            grid(row=2, column=1, padx=5, pady=5)

        Label(self.registration_tab, text="Номер группы:", font=self.FONT_LABEL).\
            grid(row=3, column=0, padx=5, pady=5)
        self.registration_group = Entry(self.registration_tab).\
            grid(row=3, column=1, padx=5, pady=5)

        Label(self.registration_tab, text="Логин:", font=self.FONT_LABEL).\
            grid(row=4, column=0, padx=5, pady=5)
        self.registration_login = Entry(self.registration_tab).\
            grid(row=4, column=1, padx=5, pady=5)

        Label(self.registration_tab, text="Пароль:", font=self.FONT_LABEL).\
            grid(row=5, column=0, padx=5, pady=5)
        self.registration_pass = Entry(self.registration_tab).\
            grid(row=5, column=1, padx=5, pady=5)

        Button(
            self.registration_tab, text="Готово", command=self.write_registration
        ).grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def write_recording(self, event) -> None:
        """
        Write name, surname and etc. to 'Time_control' table
        """

        mode = self.recording_mode.get()
        login = self.recording_login.get()
        password = self.recording_pass.get()
        pc_number = self.recording_pc.get()

        if self.check_user(login, password):
            SELECT_USER_QUERY = "SELECT * FROM Users WHERE login = ?"
            select_user_data = (login,)
            user_data = Uscon.run_query(SELECT_USER_QUERY, select_user_data, mode=Mode.fetchone)

            now = datetime.now()
            name = user_data['name']
            group = user_data['group_name']
            surname = user_data['surname']

            INSERT_USER_QUERY = "INSERT INTO Time_control VALUES (?,?,?,?,?,?)"
            insert_user_data = (name, surname, group, now, mode, pc_number)
            Uscon.run_query(INSERT_USER_QUERY, insert_user_data, mode=Mode.insert)
        else:
            pass
        return None
    
    def write_registration(self):
        """
        Write name, surname and etc. to 'Users' table
        """
        pass

    def check_user(self, login: str, password: str) -> bool:
        """
        Checks login and password in 'uscon.sqlite' database
        """

        SELECT_USER_QUERY = "SELECT password FROM Users WHERE login = ?"
        SELECT_EXISTS_QUERY = "SELECT EXISTS (SELECT password FROM Users WHERE login = ?)"
        select_user_data = (login,)
        user_exists = Uscon.run_query(
            SELECT_EXISTS_QUERY, select_user_data, mode=Mode.fetchone
        )[0]
        user_data = Uscon.run_query(
            SELECT_USER_QUERY, select_user_data, mode=Mode.fetchone
        )

        if user_exists and password == user_data['password']:
            self.recording_message.set("Вы успешно записаны!")
            return True
        elif user_exists and password != user_data['password']:
            self.recording_message.set("Введен неправильный пароль.")
            return False
        elif not user_exists:
            self.recording_message.set("Зарегистрируйтесь.")
            return False

    @staticmethod
    def run_query(query: str, data: tuple = None, mode: str = None):
        """
        Run query to 'uscon.sqlite' database
        """

        conn = sqlite3.connect('uscon.sqlite')
        curs = conn.cursor()
        curs.row_factory = sqlite3.Row
        if mode == Mode.insert:
            curs.execute(query, data)
            conn.commit()
        elif mode == Mode.fetchone:
            curs.execute(query, data)
            return curs.fetchone()
        elif mode == Mode.fetchall:
            curs.execute(query, data)
            return curs.fetchall()
        else:
            curs.execute(query)
            conn.commit()

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
        insert_train_data = (1, 'ryaba', '1234', 'Гоша', 'Рябушкин', 'ИБМ6-11')
        Uscon.run_query(CREATE_USERS_TABLE)
        Uscon.run_query(CREATE_TIME_CONTROL_TABLE)
        Uscon.run_query(INSERT_TRAIN_QUERY, insert_train_data, mode=Mode.insert)
        return None


if __name__ == "__main__":
    if os.path.isfile('uscon.sqlite') is False:
        Uscon.create_database()
    uscon = Uscon()
    uscon.mainloop()
