# What is this?

This is a collection of Python scripts to find all the URLs linked to from
local transactions, and how many of them are broken.

# How does it work?

The starting data files are:

- [`authorities.json`](https://github.com/jennyd/govuk-local-interactions/blob/master/authorities.json)
- [`local_authority_service_details.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/local_authority_service_details.csv)
- [`govuk-local-transactions.csv`](https://github.com/jennyd/govuk-local-interactions/blob/master/govuk-local-transactions.csv)

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


# What's left to do?

- check that the original list of local transactions includes all of the
now-published ones

- add pageview data to the list of all local transactions, so that we can see how
many people are presented with a URL that works

- detect from the saved responses whether or not the page is actually useful,
even if it was a 200.


I used Python 3.4.3 when working on this.
