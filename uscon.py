__author__ = 'Anthony Byuraev'


import typing
import sqlite3
import datetime


class Message(typing.NamedTuple):
    WELCOME = '\t\t\tПожалуйста введите логин и пароль'
    REGESTRATION = (
        'Зарегистрируйтесь.'
        'Укажите логин и пароль, а также номер вашей группы.'
    )
    PC_NUMBER = (
        '\tВедите номер компьютера. Он указан на верхней панели корпуса.'
    )


def main() -> None:
    print(Message.WELCOME)
    login, password = input('Login: '), input('Password: ')
    if check_user_input(login, password) is True:
        write_to_time_control(login)
    elif check_user_input(login, password) is False:
        # input_login_password()
        pass


def write_to_time_control(login: str) -> None:
    print(Message.PC_NUMBER)
    pc_number = input('Номер компьютера: ')
    now = datetime.datetime.now()
    curs.execute("SELECT * FROM users WHERE login = ?", (login,))
    user = curs.fetchone()
    name, surname, group = user['name'], user['surname'], user['group_name']
    curs.execute(
        "INSERT INTO time_control VALUES (?,?,?,?,?,?)",
        (name, surname, group, now, 1, pc_number)
    )
    conn.commit()
    return None


def check_user_input(login: str, password: str) -> bool:
    curs.execute("SELECT password FROM users WHERE login = ?", (login,))
    data_from_database = curs.fetchone()
    if data_from_database is not None \
       and password == data_from_database['password']:
        return True
    elif data_from_database is not None:
        print('Введен неправильный пароль')
        return False
    else:
        print('Такого пользователя не существует')
        return None


if __name__ == "__main__":
    conn = sqlite3.connect('uscon.sqlite')
    curs = conn.cursor()
    curs.row_factory = sqlite3.Row

    main()
    conn.close()
