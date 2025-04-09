import logging
import json
import requests

from service_comunications.microservices import connectors

def get_connector(connector_id):
    response = requests.get(f"{connectors}/connection?id={connector_id}")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(response.text)
