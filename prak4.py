import sqlite3
import os
import time

conn_users = sqlite3.connect('users.db')
cursor_users = conn_users.cursor()

cursor_users.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT UNIQUE,
        password TEXT
    )
''')
conn_users.commit()

conn_order = sqlite3.connect('orders.db')
cursor_order = conn_order.cursor()

cursor_order.execute('''
    CREATE TABLE IF NOT EXISTS basket_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        stop_list BOOLEAN DEFAULT 0
    )
''')
conn_order.commit()

basket = []

def jober(login: str, password: str):
    cursor_users.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, password))
    conn_users.commit()

def showuser(login: str, password: str):
    cursor_users.execute("SELECT * FROM users WHERE login=? AND password=?", (login, password))
    return cursor_users.fetchone() is not None

def add_to_basket(item_name):
    global basket

    stop_list_items = ["Сырные колечки", "Биг спешиал"]

    if item_name in stop_list_items:
        stop_list = 1
        print(f"Эта позиция ({item_name}) находится в стоп-листе!")
    else:
        stop_list = 0

    basket.append(item_name)

    cursor_order.execute('''
    INSERT INTO basket_items (item_name, stop_list) VALUES (?, ?)
    ''', (item_name, stop_list))
    conn_order.commit()


def display_basket():
    print("Текущая корзина:", basket)

def save_credentials(login, password):
    with open('credentials.txt', 'w') as file:
        file.write(f'{login}\n{password}')

def register_user():
    print('Введите логин:')
    login = input()

    print('Введите пароль:')
    password = input()

    print('Повторите пароль:')
    password_repeat = input()

    if password != password_repeat:
        print('Пароли не совпадают!')
    else:
        result = jober(login, password)
        if not result:
            print('Пользователь с таким логином уже существует')
        else:
            print('Регистрация прошла успешно!')
            login_user()

def login_user():
    while True:
        print('Введите логин:')
        login = input()

        print('Введите пароль:')
        password = input()

        result = showuser(login, password)

        if result:
            print('Вы вошли в оформление заказа Вкусно и Точка')
            save_credentials(login, password) 
            VIT()
            break
        else:
            print('Неверный логин или пароль. Попробуйте снова.')

def login_or_register():
    while True:
        print('Выберите действие (1 - Вход, 2 - Регистрация, 3 - Вход для клиента, 4 - Выход): ')
        action = input()

        if action == '1':
            login_user()
            break
        elif action == '2':
            register_user()
            break
        elif action == '4':
            print('До свидания')
            exit()
        else:
            print('Некорректный выбор, пожалуйста, повторите.')


def introduction():
    print("Добро пожаловать во Вкусно и Точка")

    if os.path.exists('credentials.txt'):
        with open('credentials.txt', 'r') as file:
            login = file.readline().strip()
            password = file.readline().strip()
        result = showuser(login, password)
        if result:
            print(f'Автоматическая авторизация для админа {login}')
            VIT()
        else:
            print('Невозможно автоматически войти. Введите учетные данные вручную.')
            login_or_register()
    else:
        login_or_register()

def VIT():
    while True:
        time.sleep(1)

        choice = input('''
            Выберите категорию:
                1. Новинки
                2. Популярное
                3. Напитки
                4. Картошка и стартеры
            ''')

        if choice == "1":
            choice2 = input(''' Выберите что-то из этого:
                   1. Скандинавский бургер 
                   2. Биг спешиал 
                   3. Кидз комбо
                    :''')
            if choice2 == '1':
                add_to_basket("Скандинавский бургер")
                print("Скандинавский бургер добавлен в корзину!")
            elif choice2 == '2':
                add_to_basket("Биг спешиал")
                display_basket()
                print("Эта позиция находится в стоп-листе. Выберите другую.")
                return VIT()
            elif choice2 == '3':
                add_to_basket("Кидз комбо")
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        elif choice == "2":
            choice3 = input('''Выберите что-то из этого:
                1. Биг хит
                2. Гранд
                3. Гранд де люкс
                : ''')
            if choice3 == '1':
                add_to_basket("Биг хит")
                display_basket()
            elif choice3 == '2':
                add_to_basket("Гранд")
                display_basket()
            elif choice3 == '3':
                add_to_basket("Гранд де люкс")
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        elif choice == "3":
            choice4 = input('''Выберите что-то из этого:
                1. Добрый кола
                2. Добрый апельсин
                3. Молочный коктейль Ванильный
                : ''')
            if choice4 == '1':
                add_to_basket("Добрый кола")
                display_basket()
            elif choice4 == '2':
                add_to_basket("Добрый апельсин")
                display_basket()
            elif choice4 == '3':
                add_to_basket("Молочный коктейль Ванильный")
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        elif choice == "4":
            choice5 = input('''Выберите что-то из этого:
                1. Сырные колечки
                2. Гранд фри
                3. Снэк бокс
                : ''')
            if choice5 == '1':
                add_to_basket("Сырные колечки")
                display_basket()
                print("Эта позиция находится в стоп-листе. Выберите другую.")
                return choice
            elif choice5 == '2':
                add_to_basket("Гранд фри")
                display_basket()
            elif choice5 == '3':
                add_to_basket("Снэк бокс")
                display_basket()
            else:
                print("Некорректный выбор, пожалуйста, повторите.")
                continue

        else:
            print("Некорректный выбор, пожалуйста, повторите.")
            continue

        proceed = input("Желаете добавить еще что-то в корзину? (Да/Нет): ").lower()
        if proceed != 'да':
            break

def welcome():
    print("Добро пожаловать во Вкусно и Точка")

    if os.path.exists('credentials.txt'):
        with open('credentials.txt', 'r') as file:
            login = file.readline().strip()
            password = file.readline().strip()
        result = showuser(login, password)
        if result:
            print(f'Автоматическая авторизация для админа {login}')
            VIT()
        else:
            print('Невозможно автоматически войти. Введите учетные данные вручную.')
            login_user()
    else:
        login_user()

def main():
    welcome()

main()

conn_users.close()
conn_order.close()