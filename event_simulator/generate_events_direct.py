import json
import os
import random
import requests
import time
from kafka import KafkaProducer




class NRInsertAPI:
  def __init__(self, account_id):
    self.account_id = account_id
    self.headers = {
      'Content-Type': 'application/json',
      'Api-Key': '{}'.format(os.getenv('NR_INSERT_KEY'))
      }
    self.insert_url = 'https://insights-collector.newrelic.com/v1/accounts/{}/events'.format(account_id)


  def insert(self, events):
    return requests.post(self.insert_url, data=json.dumps(events), headers=self.headers)



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
                "pipeline": 'direct',
                "timestamp": int(time.time()),
                "message": "Customer {} purchased {} for ${}".format(customer_account, product_info[0], product_info[1])
             }




random.seed()
for i in range(random.randint(10, 40)):
    _event = _get_random_event()
    print(_event)
    _events.append(_event)
    time.sleep(1)


nr_insert_api = NRInsertAPI(2760049)
response = nr_insert_api.insert(_events)

print(response.status_code)
print(response.text)
