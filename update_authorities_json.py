#!/usr/env/python3

from collections import OrderedDict
import json
import requests
from time import sleep

# Fetch a local transaction for all local authorities to get the tier for each
# one, and write authorities-with-tiers.json including the tiers.


with open('authorities.json') as f:
    # object_pairs_hook allows us to pass a function to use when loading the
    # data instead of a dict. OrderedDict preserves the load order, so that the
    # output is written in the same order as the input:
    authorities = json.load(f, object_pairs_hook=OrderedDict)

for authority_details in authorities.values():
    snac = authority_details['ons']
    # Use this local transaction because it has all 3 tiers so all LAs should
    # return results:
    url = 'https://www.gov.uk/api/after-school-holiday-club.json?snac={}'.format(snac)
    print(authority_details['name'])
    print(url)
    resp = requests.get(url)
    print(resp.status_code)
    data = resp.json()
    # Newry and Mourne District Council isn't working on local transactions for
    # some reason, so we need to allow for the LA being missing for this case:
    if 'local_authority' in data['details']:
        tier = data['details']['local_authority']['tier']
    else:
        tier = 'unknown'
    print(tier)
    authority_details['tier'] = tier
    sleep(0.5)

with open('authorities-with-tiers.json', 'w') as f:
    f.write(json.dumps(authorities))
