#!/usr/env/python3

from csv import DictReader, DictWriter
import os
import requests
import ssl


RESULTS_DIRECTORY = 'external_pages'
os.makedirs(RESULTS_DIRECTORY, exist_ok=True)

STATUS_CODES_FILE = os.path.join(RESULTS_DIRECTORY, 'status_codes')
STATUS_CODES_FIELDS = ['status', 'redirected', 'url']
EXCEPTIONS_FILE = os.path.join(RESULTS_DIRECTORY, 'exceptions')


with open('urls-used-for-local-transactions.csv', 'r', encoding='utf8') as f:
    all_results_csv = DictReader(f)
    all_results = [row for row in all_results_csv]

all_urls = list({row['interaction_url_used'] for row in all_results} - {''})


def get_html_filename(url):
    return (url.replace('/', '_') + '.html')


def handle_response(url, resp):
    print(resp.status_code)
    with open(STATUS_CODES_FILE, 'a') as f:
        writer = DictWriter(f, STATUS_CODES_FIELDS)
        row = {
            'status': resp.status_code,
            'redirected': (resp.history != []),
            'url': url
        }
        writer.writerow(row)

    html_filename = get_html_filename(url)
    if len(html_filename) >= 8:
        try:
            with open(os.path.join(RESULTS_DIRECTORY, html_filename), 'w') as f:
                f.write(resp.text)
        except OSError as e:
            handle_failure(url, e)


def handle_failure(url, exception):
    print(exception)
    with open(EXCEPTIONS_FILE, 'a') as f:
        f.write(url)
        f.write('\n')
        f.write(str(exception))
        f.write('\n\n')


def fetch_pages():
    print('{} unique URLs to fetch'.format(len(all_urls)))
    with open(STATUS_CODES_FILE, 'a') as f:
        writer = DictWriter(f, STATUS_CODES_FIELDS)
        writer.writeheader()

    for count, url in enumerate(all_urls):
        print('{}    {}'.format(count, url))
        if os.path.exists(os.path.join(RESULTS_DIRECTORY, get_html_filename(url))):
            print('Already fetched; skipping')
            continue

        try:
            resp = requests.get(url, timeout=5)
            handle_response(url, resp)
        except (requests.exceptions.RequestException, ssl.SSLError) as e:
            handle_failure(url, e)
        print('')


if __name__ == '__main__':
    fetch_pages()
