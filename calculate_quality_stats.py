#!/usr/env/python3

from collections import defaultdict, Counter
from csv import DictReader, DictWriter


# Print a summary of the number of unique pageviews for each quality category.


with open('urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews-and-quality.csv', 'r') as f:
    quality_csv = DictReader(f)
    quality_data = [row for row in quality_csv]


def percentage(n, d):
    return (n * 100.0) / d


pageviews_by_quality = defaultdict(int)
for row in quality_data:
    if row['unique_pageviews']:
        pageviews_by_quality[row['quality']] += int(row['unique_pageviews'])

pageview_stats = list(pageviews_by_quality.items())
pageview_stats.sort(key=lambda t: t[1], reverse=True)

total_pageviews = sum(t[1] for t in pageview_stats)

print('Quality categories as a percentage of pageviews:')
for quality, pageviews in pageview_stats:
    print(
        '{} links: {} unique pageviews ({}%)'.format(
            quality,
            pageviews,
            round(percentage(pageviews, total_pageviews), 2)
        )
    )


print('\n\n')


quality_by_interaction_urls = {
    row['interaction_url_used']: row['quality']
    for row in quality_data
    if row['quality'] != 'no_interaction'
}

c = Counter(list(quality_by_interaction_urls.values()))
counts_of_urls = list(c.items())
counts_of_urls.sort(key=lambda t: t[1], reverse=True)

total_interaction_urls = sum(t[1] for t in counts_of_urls)

print('Quality categories with counts of interaction URLs:')
for quality, url_count in counts_of_urls:
    print(
        '{} links: {} ({}%)'.format(
            quality,
            url_count,
            round(percentage(url_count, total_interaction_urls), 2)
        )
    )


print('\n\n')


link_quality_by_govuk_urls = {row['govuk_url']: row['quality'] for row in quality_data}

counter = Counter(list(link_quality_by_govuk_urls.values()))
counts_of_govuk_urls = list(counter.items())
counts_of_govuk_urls.sort(key=lambda t: t[1], reverse=True)

total_govuk_urls = sum(t[1] for t in counts_of_govuk_urls)

print('Link quality categories with counts of GOV.UK pages:')
for quality, url_count in counts_of_govuk_urls:
    print(
        '{} links on pages: {} ({}%)'.format(
            quality,
            url_count,
            round(percentage(url_count, total_govuk_urls), 2)
        )
    )
