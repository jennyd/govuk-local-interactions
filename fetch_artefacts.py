#!/usr/env/python3

from csv import DictReader
import json
import os
import requests
from time import sleep

# Fetch and cache all local transaction artefacts, with Lambeth's snac.


with open('govuk-local-transactions.csv', 'r', encoding='ascii') as f:
    govuk_local_transactions_csv = DictReader(f)
    govuk_local_transactions_data = [row for row in govuk_local_transactions_csv]


DIRECTORY = 'artefacts'

os.makedirs(DIRECTORY, exist_ok=True)


for local_transaction in govuk_local_transactions_data:
    slug = local_transaction['slug']
    url = 'https://www.gov.uk/api/{}.json?snac=00AY'.format(slug)
    print(url)
    resp = requests.get(url)
    print(resp.status_code)
    if resp.status_code == 200:
        data = resp.json()
        print(data['format'])
        if data['format'] == 'local_transaction':
            with open(os.path.join(DIRECTORY, '{}.json'.format(slug)), 'w') as f:
                f.write(json.dumps(data))
    sleep(0.5)
