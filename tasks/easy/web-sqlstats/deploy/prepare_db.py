import sqlite3
import os

FLAG = os.environ.get('FLAG') or 'Sabantuy{SqlInj3ction_1s_e4sy_b4t_cr1t1c4l}'

conn = sqlite3.connect('storage.db')
conn.execute(
    'CREATE TABLE IF NOT EXISTS shops (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, city VARCHAR(200), address VARCHAR (1000), img VARCHAR(1000))')
conn.execute('CREATE TABLE IF NOT EXISTS flags (flag VARCHAR(300))')
conn.commit()

fake_data = [
    ('Москва', 'Зеленый пр-т, д. 1с3', 'map1.png'),
    ('Мытищи', 'ул. Троицкая, д. 7', 'map2.png'),
    ('Уфа', 'ул. Пушкина, д. 82', 'map3.png'),
    ('Мытищи', 'ул. Карла Маркса, д. 12', 'map4.png'),
    ('Уфа', 'ул. Карла Маркса, д. 20', 'map5.png')
]

for d in fake_data:
    conn.execute('INSERT INTO shops (city, address, img) VALUES (?, ?, ?)', d)
conn.commit()

conn.execute('INSERT INTO flags (flag) VALUES (?)', (FLAG,))
conn.commit()