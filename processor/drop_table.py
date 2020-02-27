import sqlite3

conn = sqlite3.connect('inventory.sqlite')

c = conn.cursor()
c.execute('''
          DROP TABLE items
          ''')

c.execute('''DROP TABLE orders''')

conn.commit()
conn.close()
