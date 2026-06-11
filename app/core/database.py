import sqlite3

from sqlite3 import Connection, Cursor

from app.core.paths import DB_PATH, DB_DIR
from app.core.hashing import hash_password, compare_hash_password

from app.models.car_model import Car
from app.models.user_model import User


def check_user(user_name: str, user_password: str) -> bool:
    user = get_user(user_name = user_name)

    if not user:
        return False

    stored_hash = user.password_hash

    return compare_hash_password(
        stored = stored_hash, user_password = user_password
    )

def connect_database() -> Connection:
    return sqlite3.connect(DB_PATH)

def create_database() -> None:
    DB_DIR.mkdir(parents = True, exist_ok = True)

    if DB_PATH.exists():
        return

    with connect_database() as con:
        cur: Cursor = con.cursor()

        _ = cur.execute("""
            CREATE TABLE IF NOT EXISTS cars (
                car_id INTEGER PRIMARY KEY AUTOINCREMENT,
                car_name TEXT,
                car_price REAL NOT NULL,
                car_quantity INTEGER NOT NULL
            )
        """)

        _ = cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT UNIQUE,
                user_password TEXT NOT NULL,
                user_role TEXT DEFAULT 'user'
            )
        """)

        _ = cur.executemany("""
            INSERT INTO cars (car_name, car_price, car_quantity)
            VALUES (?, ?, ?)
        """, [
            ("Bugatti Bolide", 12.99, 100),
            ("Mazda MX-5", 2.99, 160),
            ("Nissan GT-R", 14.99, 40)
        ])

        users = [
            ("utilizador", hash_password("1234"), "user"),
            ("administrador", hash_password("A12B34c56!"),
            "admin")
        ]

        _ = cur.executemany("""
            INSERT INTO users (user_name, user_password, user_role)
            VALUES (?, ?, ?)
        """, users)

def fetch_all_cars():
    with connect_database() as con:
        cur: Cursor = con.cursor()
        _ = cur.execute(
            "SELECT car_id, car_name, car_price, car_quantity FROM cars"
        )
        rows = cur.fetchall()

    return [
        Car(
            car_id = r[0],
            car_name = r[1],
            car_price = r[2],
            car_quantity = r[3]
        )
        for r in rows
    ]

def get_user(user_name: str) -> User | None:
    with connect_database() as con:
        cur: Cursor = con.cursor()
        _ = cur.execute("""SELECT user_id, user_name, user_password, user_role
        FROM users WHERE user_name = ?""", (user_name,))
        r = cur.fetchone()

    if r is None:
        return None

    return User(
        user_id = r[0],
        user_name = r[1],
        password_hash = r[2],
        user_role = r[3]
    )

def update_car_quantity(car_id: int, new_quantity: int) -> None:
    with connect_database() as con:
        cur: Cursor = con.cursor()
        _ = cur.execute("""
            UPDATE cars
            SET car_quantity = ?
            WHERE car_id = ?
        """, (new_quantity, car_id))

def retrieve_info(car_id: int):
    with connect_database() as con:
        cur: Cursor = con.cursor()
        _ = cur.execute("""
            SELECT car_id, car_name, car_price,car_quantity
            FROM cars WHERE car_id = ?""", (car_id,)
        )
        r = cur.fetchone()

    if r is None:
        return None

    return Car(
        car_id = r[0],
        car_name = r[1],
        car_price = r[2],
        car_quantity = r[3]
    )