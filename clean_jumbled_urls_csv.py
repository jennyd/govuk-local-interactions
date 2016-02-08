#!/usr/env/python3

from csv import DictReader, DictWriter


with open('urls-used-for-local-transactions-with-statuses.csv', 'r', encoding='utf8') as f:
    urls_used_with_statuses_csv = DictReader(f)
    urls_used_with_statuses = [row for row in urls_used_with_statuses_csv]

with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls.csv', 'r') as f:
    jumbled_urls_csv = DictReader(f, escapechar='\\')
    jumbled_urls_by_govuk_url = {row['govuk_url']: row for row in jumbled_urls_csv}


jumbled_url_fields = ['jumbled_url', 'jumbled_url_status_code', 'jumbled_url_test_date']

def add_jumbled_fields(row, jumbled_url_row):
    for field in ['id'] + jumbled_url_fields:
        if jumbled_url_row[field] == 'NULL':
            row[field] = None
        else:
            row[field] = jumbled_url_row[field]
    return row

fields = ['id'] + urls_used_with_statuses_csv.fieldnames + jumbled_url_fields

with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls.csv', 'w', encoding='utf8') as output:
    writer = DictWriter(output, fields)
    writer.writeheader()
    writer.writerows([
        add_jumbled_fields(row.copy(), jumbled_urls_by_govuk_url[row['govuk_url']])
        for row in urls_used_with_statuses
    ])
