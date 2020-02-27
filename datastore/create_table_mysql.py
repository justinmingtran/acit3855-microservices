import mysql.connector
import yaml

with open('app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())


db_conn = mysql.connector.connect(host=app_config['datastore']['hostname']
                                  ,user=app_config['datastore']['user']
                                  ,password=app_config['datastore']['password']
                                  ,database=app_config['datastore']['db'])

db_cursor = db_conn.cursor()

db_cursor.execute('''
                  CREATE TABLE items
                  ( item_id INT NOT NULL AUTO_INCREMENT,
                  item_name VARCHAR(250) NOT NULL,
                  date_created VARCHAR(100) NOT NULL,
                  CONSTRAINT item_id_pk PRIMARY KEY (item_id))
                  ''')

db_cursor.execute('''
                  CREATE TABLE orders
                  ( id INT NOT NULL AUTO_INCREMENT,
                  order_id VARCHAR(250) NOT NULL,
                  ordered_item VARCHAR(500) NOT NULL,
                  quantity INT NOT NULL,
                  date_created VARCHAR(100) NOT NULL,
                  CONSTRAINT orders_pk PRIMARY KEY (id))
                  ''')

db_conn.commit()
db_conn.close()
