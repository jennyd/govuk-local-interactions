#!/usr/env/python3

from collections import defaultdict
from csv import DictReader, DictWriter
import json


# This is from http://local.direct.gov.uk/Data/local_authority_service_details.csv
# $ file local_authority_service_details.csv
# local_authority_service_details.csv: ISO-8859 text, with CRLF line terminators

with open('local_authority_service_details.csv', 'r', encoding='iso-8859-1') as f:
    ldg_csv = DictReader(f)
    ldg_data = [row for row in ldg_csv]
ldg_data_by_snac = defaultdict(list)
for row in ldg_data:
    if row['SNAC']:
        ldg_data_by_snac[row['SNAC']].append(row)


# This is from https://docs.google.com/spreadsheets/d/15khIbspxUl8gpOi0KVleu6Xohikz8MDCa9ANAywE5vs/edit#gid=0 but updated to include current LGIL overrides for the local transactions which had duplicate lgsl-lgil codes in the spreadsheet (the data there is from last summer, and we fixed them after finding this)
# $ file govuk-local-transactions.csv
# govuk-local-transactions.csv: ASCII text, with CRLF line terminators

with open('govuk-local-transactions.csv', 'r', encoding='ascii') as f:
    govuk_local_transactions_csv = DictReader(f)
    govuk_local_transactions_data = [row for row in govuk_local_transactions_csv]
transaction_slugs = [row['slug'] for row in govuk_local_transactions_data]


# authorities.json from frontend - this defines which LAs we support

with open('authorities.json') as f:
    authorities = json.load(f)
authorities_snac_to_slug = {details['ons']: slug for slug, details in authorities.items()}


def find_interaction_by_lgil(interactions, lgil_code):
    interactions_for_lgil = [row for row in interactions if row['LGIL'] == lgil_code]
    if interactions_for_lgil:
        return interactions_for_lgil[0]

def preferred_interaction(snac, lgsl_code, lgil_code=None):
    la_data = ldg_data_by_snac[snac]
    interactions = [row for row in la_data if row['LGSL'] == lgsl_code]
    chosen_interaction = None
    if lgil_code:
        chosen_interaction = find_interaction_by_lgil(interactions, lgil_code)
    else:
        interactions_excluding_8 = [row for row in interactions if row['LGIL'] != '8']
        if interactions_excluding_8:
            interactions_excluding_8.sort(key=lambda interaction: int(interaction['LGIL']))
            chosen_interaction = interactions_excluding_8[0]
        else:
            chosen_interaction = find_interaction_by_lgil(interactions, '8')
    return chosen_interaction

def build_govuk_url(transaction_slug, authority_slug):
    return 'https://www.gov.uk/{0}/{1}'.format(transaction_slug.strip(), authority_slug.strip())


fields = ['govuk_url', 'govuk_title', 'snac', 'lgsl', 'lgil_override', 'interaction_found', 'interaction_lgil_used', 'interaction_url_used']

def write_output():
    with open('urls-used-for-local-transactions.csv', 'w', encoding='utf8') as output:
        writer = DictWriter(output, fields)
        writer.writeheader()

        for local_transaction in govuk_local_transactions_data:
            for snac, authority_slug in authorities_snac_to_slug.items():
                interaction = preferred_interaction(snac, local_transaction['LGSL'], local_transaction['LGIL'])
                row = {
                    'govuk_url': build_govuk_url(local_transaction['slug'], authority_slug),
                    'govuk_title': local_transaction['title'],
                    'snac': snac,
                    'lgsl': local_transaction['LGSL'],
                    'lgil_override': local_transaction['LGIL'],
                    'interaction_found': bool(interaction),
                    'interaction_lgil_used': interaction['LGIL'] if interaction else '',
                    'interaction_url_used': interaction['Service URL'] if interaction else '',
                }
                writer.writerow(row)

if __name__ == '__main__':
    write_output()
