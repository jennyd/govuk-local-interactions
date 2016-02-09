#!/usr/env/python3

from csv import DictReader, DictWriter
import os
import re

from fetch_results_pages import get_html_filename, RESULTS_DIRECTORY


# Add quality assessments into a CSV of URLs used for local transactions.


with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews.csv', 'r', encoding='utf8') as f:
    urls_used_csv = DictReader(f)
    urls_used = [row for row in urls_used_csv]


not_found_strings = (
    'cannot be found',
    'error 404',
    'not found',
    ' 404[< ] ',
    '<title>.*?homepage.*?<\/title>',
)

not_found_pattern = re.compile('|'.join(not_found_strings), re.IGNORECASE)

def looks_like_404(row):
    """Check for text in the page which looks like it's a "not found" page.

    If we get a 200 response for both the interaction URL and a jumbled version
    of it, we can't be confident that 200 really means 200 on that site. Looking
    for a few phrases in the text of the page which are commonly used on 404-type
    pages gives an indication of whether the interaction URL is really a content
    page or not.

    This technique and the patterns used here are taken from
    https://github.com/daibach/govuk-local-services/blob/fecd9da2c989fd962e0df73ec06afd29ca94405b/application/controllers/cli/url_checker.php#L157-L161
    """
    filename = os.path.join(RESULTS_DIRECTORY, get_html_filename(row['interaction_url_used']))
    with open(filename, 'r') as f:
        response_body = f.read()
    match = not_found_pattern.search(response_body)
    if match:
        print(row['interaction_url_used'], '    ', match.group())
    return match


def generate_row_with_quality(row):
    quality = 'unknown'
    if row['interaction_found'] == 'False':
        quality = 'no_interaction'
    elif row['exception']:
        quality = 'exception'
    elif row['status_code'] != '200':
        quality = 'bad'
    elif row['status_code'] == '200' and row['jumbled_url_status_code'] != '200':
        # We can be confident that 200 means 200 in this case:
        quality = 'good'
    elif looks_like_404(row):
        quality = 'looks_like_404'
    else:
        quality = 'doesnt_look_like_404'

    row['quality'] = quality
    return row

urls_used_with_quality = [generate_row_with_quality(row.copy()) for row in urls_used]


fields = urls_used_csv.fieldnames + ['quality']


def write_output():
    with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews-and-quality.csv', 'w', encoding='utf8') as output:
        writer = DictWriter(output, fields)
        writer.writeheader()
        writer.writerows(urls_used_with_quality)


if __name__ == '__main__':
    write_output()
