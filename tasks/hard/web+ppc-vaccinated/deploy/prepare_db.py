import sqlite3
import os
import random
import secrets

FLAG = os.environ.get('FLAG') or 'Sabantuy{R3ally_noSQLBrut3_m4ster}'
conn = sqlite3.connect('storage.db')

conn.execute(
    'CREATE TABLE IF NOT EXISTS `employees` (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `username` VARCHAR(255), `password` VARCHAR(255), `email` VARCHAR(255), `isVaccinated` TINYINT(1));')
conn.commit()

users = [('Admin', FLAG, 'admin@cbsctf.live', 1)]

names = ['cathryn', 'cathy', 'elberta', 'florance', 'gorde', 'haleigh', 'heather', 'ignacio', 'jasper', 'jonelle',
         'minta', 'otto', 'rhys', 'scott', 'terrie', 'vladimir']

for name in names:
    email = random.choice(['cbsctf.live', 'gmail.com', 'mail.ru', 'ya.ru'])
    users.append((name, secrets.token_hex(20), name + '@' + email, random.randint(0, 1)))

for u in users:
    conn.execute('INSERT INTO employees (username, password, email, isVaccinated) VALUES (?, ?, ?, ?)', u)
conn.commit()
