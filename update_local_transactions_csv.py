#!/usr/env/python3

from csv import DictReader, DictWriter
import json
import os

# Write govuk-local-transactions-updated.csv using data from the artefacts
# directory. The slug is taken from the file name and all other data is taken
# from the artefact itself. The three tier columns added here were not included
# in the original spreadsheet from which govuk-local-transactions.csv was
# exported.


ALL_TIERS = ['district', 'county', 'unitary']
ARTEFACT_DIRECTORY = 'artefacts'


def build_row(slug, data):
    row = {'slug': slug}

    row['title'] = data['title']
    row['LGSL'] = data['details']['lgsl_code']
    row['LGIL'] = data['details']['lgil_override']

    tiers = data['details']['local_service']['providing_tier']
    for tier in ALL_TIERS:
        row[tier] = bool(tier in tiers)

    return row


with open('govuk-local-transactions-updated.csv', 'w') as f:
    fields = ['slug', 'title', 'LGSL', 'LGIL'] + ALL_TIERS
    writer = DictWriter(f, fields)
    writer.writeheader()

    rows = []
    for artefact in os.listdir(ARTEFACT_DIRECTORY):
        slug = os.path.splitext(artefact)[0]
        with open(os.path.join(ARTEFACT_DIRECTORY, artefact), 'r') as artefact_file:
            data = json.load(artefact_file)
            rows.append(build_row(slug, data))

    rows.sort(key=lambda row: row['slug'])
    writer.writerows(rows)
