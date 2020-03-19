import connexion
from connexion import NoContent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS, cross_origin

import yaml
import logging
import logging.config
import apscheduler
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import json
import datetime
import os
# Function

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


def populate_stats():

    logger.info('Started Periodic Processing')
    json_data = get_inventory_stats()[0]

    new_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
    parameters = {
        "startDate": json_data['updated_timestamp'],
        "endDate": new_timestamp
    }
    
    num_orders = requests.get(url='http://acit3855-docker-lab.eastus.cloudapp.azure.com:8090/order', params=parameters)
    num_items = requests.get(url='http://acit3855-docker-lab.eastus.cloudapp.azure.com:8090/item', params=parameters)
    
    if json_data.get('updated_timestamp'):
        json_data['updated_timestamp'] = new_timestamp
    else:
        json_data['updated_timestamp'] = new_timestamp

    if json_data.get('num_item'):
        json_data['num_item'] = json_data['num_item'] + len(num_items.json())
    else:
        json_data['num_item'] = len(num_items.json())

    if json_data.get('num_order'):
        json_data['num_order'] = json_data['num_order'] + \
            len(num_orders.json())
    else:
        json_data['num_order'] = len(num_orders.json())

    with open(app_config['datastore']['filename'], 'w') as new_json:
        json.dump(json_data, new_json)
        logger.debug("Recevied %d new orders" % len(num_orders.json()))
        logger.debug("Recevied %d new items" % len(num_items.json()))
        logger.info("Ended Periodic Processing")

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(populate_stats, 'interval',
                  seconds=app_config['scheduler']['period_sec'])
    sched.start()


def get_inventory_stats():
    logger.info("/event/stats Processing Request")
    if os.path.exists(app_config['datastore']['filename']):
        with open(app_config['datastore']['filename'], 'r') as json_data:
            data = json.load(json_data)
            logger.debug(data)
            logger.info("/event/stats Request completed")
            return data, 200
    else:
        logger.error(
            "No file found. Creating new data.json with default values")
        with open('data.json', 'w') as f:
            new_dict = {
                "num_item": 0,
                "num_order": 0,
                "updated_timestamp": ""
            }
            json.dump(new_dict, f)
        return 404

app = connexion.FlaskApp(__name__, specification_dir='')
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'
app.add_api("openapi.yaml")

if __name__ == "__main__":
    init_scheduler()
    app.run(port=8100)

