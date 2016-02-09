# What is this?

This is a collection of Python scripts to find all the URLs linked to from
GOV.UK local transactions, and how many of them are broken.

@daibach's [local services explorer](http://govuklocal.dafyddvaughan.co.uk/)
shows data about the full list of all URLs in the Local Directgov dataset, but
we only use some of these on GOV.UK. This repo matches data about the quality of
those links to the pages which display them on GOV.UK, and will also include
pageview data so that we can see the proportion of users who are presented with
a working link on a local transaction page.

# How does it work?

The starting data files are:

- [`authorities.json`](https://github.com/jennyd/govuk-local-interactions/blob/master/authorities.json)
- [`local_authority_service_details.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/local_authority_service_details.csv)
- [`govuk-local-transactions.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/govuk-local-transactions.csv)
- [`unique-pageviews-top-15000-local-transaction-pages.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/unique-pageviews-top-15000-local-transaction-pages.csv)

[`update_authorities_json.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/update_authorities_json.py)
generates [`authorities-with-tiers.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/authorities-with-tiers.json)
to add the LA tier field, by fetching a local transaction for every local authority.

[`fetch_artefacts.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/fetch_artefacts.py)
fetches the JSON representation of each local transaction in
[`govuk-local-transactions.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/govuk-local-transactions.csv)
and writes it to [`artefacts/`](https://github.com/jennyd/govuk-local-interactions/tree/master/artefacts).

[`update_local_transactions_csv.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/update_local_transactions_csv.py)
generates [`govuk-local-transactions-updated.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/govuk-local-transactions-updated.csv)
to add the tiers for each local transaction and update all other fields except
the slug, using the artefact data.

[`generate_urls_used_for_local_transactions.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/generate_urls_used_for_local_transactions.py)
finds the local interaction URL which will be used for each local transaction
authority results page and writes that data to
[`urls-used-for-local-transactions.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/urls-used-for-local-transactions.csv).

[`fetch_results_pages.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/fetch_results_pages.py)
visits each used local interaction URL (following redirects) and:

- creates [`external_pages/status_codes`](https://github.com/jennyd/govuk-local-interactions/blob/master/external_pages/status_codes)
for requests which received a response
- writes the response body to [`external_pages/*.html`](https://github.com/jennyd/govuk-local-interactions/tree/master/external_pages)
- writes details of any exceptions raised to [`external_pages/exceptions`](https://github.com/jennyd/govuk-local-interactions/blob/master/external_pages/exceptions)

[`add_status_codes_to_urls_used_for_local_transactions.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/add_status_codes_to_urls_used_for_local_transactions.py)
then adds the status codes and exceptions from those requests into the full
list of all URLs used for local transactions and writes that to
[`urls-used-for-local-transactions-with-statuses.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/urls-used-for-local-transactions-with-statuses.csv).

[`urls-used-for-local-transactions-with-statuses-and-jumbled-urls.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/urls-used-for-local-transactions-with-statuses-and-jumbled-urls.csv)
includes 4 extra fields with data exported from @daibach's local services explorer.
They're the results of getting a slightly jumbled version of the interaction URL
to see if that section of the site is capable of returning a 404 status code,
which indicates whether a 200 response is trustworthy.

[`clean_jumbled_urls_csv.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/clean_jumbled_urls_csv.py) cleans that file in place; it was exported from a
database and had some inconsistencies with the other CSVs which needed sorting out.

[`add-pageviews-to-urls-used.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/add-pageviews-to-urls-used.py)
adds unique pageview data to the list of all URLs used for local transactions
including the jumbled URL fields, sorts by pageview and writes the list to
[`urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews.csv).

[`add_quality_to_urls_used.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/add_quality_to_urls_used.py)
uses the accumulated data, including the saved HTML page content, to assess the
quality of each local transaction page's link and adds that field to the full list in
[`urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews-and-quality.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/urls-used-for-local-transactions-with-statuses-and-jumbled-urls-and-pageviews-and-quality.csv).
[`look-like-404-matches`](https://github.com/jennyd/govuk-local-interactions/blob/master/look-like-404-matches) contains the matched strings
for the pages which looked like 404s.

[`calculate_quality_stats.py`](https://github.com/jennyd/govuk-local-interactions/blob/master/calculate_quality_stats.py)
prints basic statistics about the quality of interaction links, as percentages
of pageviews and counts of interaction URLs.


I used Python 3.4.3 when working on this.
