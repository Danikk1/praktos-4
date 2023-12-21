import sqlite3

class Database:
    def __init__(self, db_name="store.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        ''')

        self.connection.commit()

    def add_user(self, username, password, role):
        self.cursor.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password, role))
        self.connection.commit()

    def get_user(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        return self.cursor.fetchone()

    def add_product(self, name, price, quantity):
        self.cursor.execute('INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)', (name, price, quantity))
        self.connection.commit()

    def get_products(self):
        self.cursor.execute('SELECT * FROM products')
        return self.cursor.fetchall()

    def add_order(self, user_id, product_id, quantity):
        self.cursor.execute('INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
        self.connection.commit()

    def get_orders_by_user(self, user_id):
        self.cursor.execute('SELECT * FROM orders WHERE user_id = ?', (user_id,))
        return self.cursor.fetchall()

# Класс пользователя
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role

# Класс товара
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

# Класс заказа
class Order:
    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity

def main():
    db = Database()

    # Регистрация пользователя

    username = input("Введите ваш логин: ")
    password = input("Введите ваш пароль: ")
    role = "client"  
    db.add_user(username, password, role)
    print("Регистрация успешна!")

    # Авторизация пользователя
    auth_username = input("Введите ваш логин для авторизации: ")
    auth_password = input("Введите ваш пароль для авторизации: ")
    user_data = db.get_user(auth_username)
    if user_data and auth_password == user_data[2]:
        print(f"Добро пожаловать, {auth_username}!")
        user = User(auth_username, auth_password, user_data[3])

    
        if user.role == "client":
            products = db.get_products()
            print("Список товаров:")
            for product in products:
                print(f"{product[0]}. {product[1]} - {product[2]} рублей, количество: {product[3]}")

            # Добавление товара в заказ
            product_id = int(input("Введите номер товара, который вы хотите добавить в заказ: "))
            quantity = int(input("Введите количество товара: "))
            db.add_order(user_data[0], product_id, quantity)
            print("Товар добавлен в заказ!")

            # Просмотр заказов пользователя
            orders = db.get_orders_by_user(user_data[0])
            print("Ваши заказы:")
            for order in orders:
                print(f"Заказ {order[0]}: Товар {order[2]}, количество {order[3]}")

    else:
        print("Неверный логин или пароль.")

if __name__ == "__main__":
    main()
