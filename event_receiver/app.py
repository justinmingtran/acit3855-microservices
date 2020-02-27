import connexion
import json
import yaml
from connexion import NoContent
from pykafka import KafkaClient

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    
# Functions
def add_item(itemName):
    client = KafkaClient(hosts="{}:{}".format(app_config['kafka']['server'],app_config['kafka']['port']))
    topic = client.topics[app_config['kafka']['topic']]
    producer = topic.get_sync_producer()
    msg = {
        "type": "item",
        "payload": itemName
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    return NoContent, 201


def add_order(orderInfo):
    client = KafkaClient(hosts="{}:{}".format(app_config['kafka']['server'],app_config['kafka']['port']))
    topic = client.topics[app_config['kafka']['topic']]
    producer = topic.get_sync_producer()
    msg = {
        "type": "order",
        "payload": orderInfo
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    
    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8080)
