#!/usr/env/python3

from csv import DictReader, DictWriter


# Add unique pageview data into a CSV of URLs used for local transactions.


with open('unique-pageviews-top-15000-local-transaction-pages.csv', 'r') as f:
    pageviews_csv = DictReader(f)
    pageviews_by_url = {
        'https://www.gov.uk{}'.format(row['path']): row['unique_pageviews']
        for row in pageviews_csv
    }


with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls.csv', 'r', encoding='utf8') as f:
    urls_used_csv = DictReader(f)
    urls_used = [row for row in urls_used_csv]


fields = ['unique_pageviews'] + urls_used_csv.fieldnames

def generate_row_with_pageviews(row):
    govuk_url = row['govuk_url']
    row_with_pageviews = row.copy()
    # Use -1 for the URLs outside the top 15,000 so that we can sort by pageviews:
    row_with_pageviews['unique_pageviews'] = int(pageviews_by_url.get(govuk_url, -1))
    return row_with_pageviews

urls_used_with_pageviews = [generate_row_with_pageviews(row) for row in urls_used]
urls_used_with_pageviews.sort(key=lambda r:r['unique_pageviews'], reverse=True)
# Remove the -1 pageview values now that we've sorted:
for row in urls_used_with_pageviews:
    if row['unique_pageviews'] == -1:
        row['unique_pageviews'] = None


def write_output():
    with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews.csv', 'w', encoding='utf8') as output:
        writer = DictWriter(output, fields)
        writer.writeheader()
        writer.writerows(urls_used_with_pageviews)


if __name__ == '__main__':
    write_output()
