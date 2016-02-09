#!/usr/env/python3

from collections import defaultdict
from csv import DictReader, DictWriter


# Print a summary of the number of unique pageviews for each quality category.


with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews-and-quality.csv', 'r') as f:
    quality_csv = DictReader(f)
    quality_data = [row for row in quality_csv]


pageviews_by_quality = defaultdict(int)
for row in quality_data:
    if row['unique_pageviews']:
        pageviews_by_quality[row['quality']] += int(row['unique_pageviews'])

stats = list(pageviews_by_quality.items())
stats.sort(key=lambda t: t[1], reverse=True)
for quality, pageviews in stats:
    print('{} links: {} unique pageviews'.format(quality, pageviews))
