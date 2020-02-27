import sqlite3

conn = sqlite3.connect('inventory.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)

c = conn.cursor()

c.execute('''
        CREATE TABLE items
        (item_id INTEGER PRIMARY KEY ASC,
        item_name VARCHAR(250) NOT NULL,
        date_created VARCHAR(100) NOT NULL)
            ''')

c.execute('''CREATE TABLE orders
        (id INTEGER PRIMARY KEY ASC,
        order_id VARCHAR(250) NOT NULL,
        ordered_item VARCHAR(500) NOT NULL,
        quantity INTEGER NOT NULL,
        date_created VARCHAR(100) NOT NULL)''')

conn.commit()
conn.close()