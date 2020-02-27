import connexion
import json
import yaml

from connexion import NoContent
from pykafka import KafkaClient

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    
def get_item_by_offset(offset):
    client = KafkaClient(hosts="{}:{}".format(app_config['kafka']['server'], app_config['kafka']['port']))
    topic = client.topics[app_config['kafka']['topic']]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)
    item_list = []
    for message in consumer:
        msg_str = message.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'item':
            item_list.append(msg)

    if offset >= len(item_list):
        return NoContent, 404
    return item_list[offset], 201

def get_order_by_quantity(quantity, ordered_item):
    client = KafkaClient(hosts="{}:{}".format(app_config['kafka']['server'], app_config['kafka']['port']))
    topic = client.topics[app_config['kafka']['topic']]
    
    consumer = topic.get_simple_consumer(reset_offset_on_start=True, consumer_timeout_ms=100)
    
    order_list = []
    for message in consumer:
        msg_str = message.value.decode('utf-8')
        msg = json.loads(msg_str)
        if msg['type'] == 'order' and msg['payload']['quantity'] >= quantity and msg['payload']['ordered_item']:
            order_list.append(msg)
    if len(order_list) == 0:
        return NoContent, 404
    return order_list, 201
    

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")

if __name__ == "__main__":
    app.run(port=8200)