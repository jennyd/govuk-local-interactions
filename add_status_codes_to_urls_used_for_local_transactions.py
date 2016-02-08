#!/usr/env/python3

from collections import Counter
from csv import DictReader, DictWriter
import os

from fetch_results_pages import get_html_filename, RESULTS_DIRECTORY


# Collect status_codes and exceptions data back into a CSV of URLs used for
# local transactions.


with open(os.path.join(RESULTS_DIRECTORY, 'exceptions'), 'r') as f:
    exception_lines = f.read().splitlines()

with open(os.path.join(RESULTS_DIRECTORY, 'status_codes'), 'r') as f:
    status_codes_csv = DictReader(f)
    status_codes_data = [row for row in status_codes_csv]

status_codes_by_url = {
    row['url']: {'status': row['status'], 'redirected': row['redirected']}
    for row in status_codes_data
}


def groups(lines):
    """Yield successive groups of 3 items from lines.

    From http://stackoverflow.com/a/312464
    """
    for i in range(0, len(lines), 3):
        yield lines[i:i+3]

exceptions_by_url = {group[0]: group[1] for group in groups(exception_lines)}


with open('urls-used-for-local-transactions.csv', 'r', encoding='utf8') as f:
    urls_used_for_local_transactions_csv = DictReader(f)
    urls_used_for_local_transactions = [row for row in urls_used_for_local_transactions_csv]


fields = [
    'govuk_url',
    'govuk_title',
    'snac',
    'lgsl',
    'lgil_override',
    'interaction_found',
    'interaction_lgil_used',
    'interaction_url_used',
    'status_code',
    'redirected',
    'exception',
]


def generate_row_with_status_details(row):
    url = row['interaction_url_used']
    row_with_status = row.copy()
    status_details = status_codes_by_url.get(url)
    if status_details:
        row_with_status['status_code'] = status_details['status']
        row_with_status['redirected'] = status_details['redirected']
    else:
        row_with_status['status_code'] = row_with_status['redirected'] = None
    row_with_status['exception'] = exceptions_by_url.get(url)
    return row_with_status

urls_used_with_statuses = [generate_row_with_status_details(row) for row in urls_used_for_local_transactions]


def write_output():
    with open('urls-used-for-local-transactions-with-statuses.csv', 'w', encoding='utf8') as output:
        writer = DictWriter(output, fields)
        writer.writeheader()
        writer.writerows(urls_used_with_statuses)


if __name__ == '__main__':
    write_output()
