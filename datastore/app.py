import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from item import Item
from order import Order
from flask_cors import CORS, cross_origin
import datetime
import yaml
import json

import logging
import logging.config
from threading import Thread
from pykafka import KafkaClient
# Functions

try:
    with open('/config/app_config.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except IOError:
    with open('app_conf.yml', 'r') as f:
        app_config = yaml.safe_load(f.read())

with open('log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

DB_ENGINE = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(app_config['datastore']['user'], app_config['datastore']['password'],
                                                                  app_config['datastore']['hostname'], app_config['datastore']['port'], app_config['datastore']['db'], app_config['datastore']['auth_plugin']))

Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def process_messages():
    client = KafkaClient(hosts="{}:{}".format(
        app_config['kafka']['server'], app_config['kafka']['port']))
    topic = client.topics[app_config['kafka']['topic']]

    consumer = topic.get_simple_consumer()

    for msg in consumer:

        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)

        if msg['type'] == 'item':
            add_item(msg['payload'])
            logger.info('consumed item message')
        elif msg['type'] == 'order':
            add_order(msg['payload'])
            logger.info('consumed order info')


def add_item(payload):

    session = DB_SESSION()

    item = Item(payload['item_name'])

    session.add(item)

    session.commit()
    session.close()

    return NoContent, 201


def get_item(startDate, endDate):
    try:
        start = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        bad_request = {
            "detail": "startDate or endDate must be in this format '2020-01-22T20:00:00'",
            "status": 400,
            "title": "Bad Request",
            "type": "about:blank"
        }
        logger.error("Bad Request when trying to retrieve item data")
        return bad_request, 400

    results_list = []

    session = DB_SESSION()

    results = (session.query(Item).filter(
        Item.date_created.between(start, end)))

    for result in results:
        results_list.append(result.to_dict())
        # print(result.to_dict())

    session.close()

    return results_list, 201


def add_order(payload):
    session = DB_SESSION()
    order = Order(payload['order_id'],
                  payload['ordered_item'],
                  payload['quantity'])

    session.add(order)
    session.commit()
    session.close()

    return NoContent, 201


def get_order(startDate, endDate):

    try:
        start = datetime.datetime.strptime(startDate, "%Y-%m-%dT%H:%M:%S")
        end = datetime.datetime.strptime(endDate, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        bad_request = {
            "detail": "startDate or endDate must be in this format '2020-01-22T20:00:00'",
            "status": 400,
            "title": "Bad Request",
            "type": "about:blank"
        }
        return bad_request, 400

    results_list = []

    session = DB_SESSION()

    results = (session.query(Order).filter(
        Order.date_created.between(start, end)))

    for result in results:
        results_list.append(result.to_dict())
        # print(result.to_dict())

    session.close()

    return results_list, 201


app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
