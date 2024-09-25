import json
import os
import random
import time
from kafka import KafkaProducer

_events = []

def _get_random_event():
    random.seed()
    location = random.choice(['Boston', 'New York', 'San Francisco', 'Atlanta', 'Portland'])
    random.seed()
    event = 'Purchase'
    random.seed()
    customer_account = random.randint(9875,15321)
    random.seed()
    product_info = random.choice([('burger', 3.25), ('fries', 1.25), ('coke', 1.50), ('root beer', 1.50)])
    return  \
             {
                "eventType": event,
                "customer": customer_account,
                "amount": product_info[1],
                "product": product_info[0],
                "location": location,
                "pipeline": 'kafka-connect',
                "timestamp": int(time.time()),
                "message": "Customer {} purchased {} for ${}".format(customer_account, product_info[0], product_info[1])
             }




random.seed()
for i in range(random.randint(10, 40)):
    _event = _get_random_event()
    print(_event)
    _events.append(_event)
    time.sleep(1)



producer = KafkaProducer(bootstrap_servers='localhost:9092')
for ev in _events:
    # Put identical payload onto the events and logs topics respectively.
    # You can consume either of these topics with either the events or logs connectors.
    # If you want events written as a custom event use:
    #    connector.class=com.newrelic.telemetry.events.EventsSinkConnector
    # to have them sent as a Log use:
    #    connector.class=com.newrelic.telemetry.logs.LogsSinkConnector
    response = producer.send('nr_events', json.dumps(ev).encode('utf-8'))
    print(response)
    response = producer.send('nr_logs', json.dumps(ev).encode('utf-8'))
    print(response)


producer.flush()