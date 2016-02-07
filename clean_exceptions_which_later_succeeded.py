#!/usr/env/python3

from collections import Counter
from csv import DictReader, DictWriter
import os

from fetch_results_pages import get_html_filename, RESULTS_DIRECTORY


with open(os.path.join(RESULTS_DIRECTORY, 'exceptions'), 'r') as f:
    exception_lines = f.read().splitlines()

with open(os.path.join(RESULTS_DIRECTORY, 'status_codes'), 'r') as f:
    status_codes_csv = DictReader(f)
    status_codes_data = [row for row in status_codes_csv]

    status_codes_by_url = {}
    overridden_count = 0
    for row in status_codes_data:
        url = row['url']
        details = {'status': row['status'], 'redirected': row['redirected']}

        if url in status_codes_by_url and status_codes_by_url[url] != details:
            print('Overriding earlier row for {}:'.format(url))
            print('    Old: {}'.format(status_codes_by_url[row['url']]))
            print('    New: {}'.format(details))
            overridden_count += 1
        status_codes_by_url[row['url']] = details

print('Overridden {} rows'.format(overridden_count))

print('All rows from status codes CSV: {}'.format(len(status_codes_data)))
print('All URLs from status codes CSV: {}'.format(len(status_codes_by_url)))


urls_from_dict = [url for url in status_codes_by_url.keys()]

print('URLs in status codes which have exceptions:')
urls_in_both = [url for url in urls_from_dict if url in exception_lines]

def truncate_long_url(url):
    if len(url) > 200:
        return url[:150] + url[-50:]
    else:
        return url

print('\n\n')
for url in urls_in_both:
    print(url)
    print(truncate_long_url(url))
    print('\n')
