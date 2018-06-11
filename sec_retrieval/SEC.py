import datetime
from urllib.parse import urlencode, urlparse, urlunparse

import requests


class SEC:

    def __init__(self):
        self.edgar_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        self.current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    def _default_edgar_query(self):
        return {
            'owner': 'exclude',
            'action': 'getcompany',
            'output': 'xml',
            'datea': '2015-01-01',
            'dateb': self.current_date_str,
            'count': 1
        }

    def _generate_get_cik_url(self, **kwargs):
        query = self._default_edgar_query()
        query.update(kwargs)

        url_parts = list(urlparse(self.edgar_url))
        url_parts[4] = urlencode(query)
        url = urlunparse(url_parts)

        return url

    def get_cik(self, names=None, ticker=''):
        """Returns the company's CIK.
        Provide either a list of company names, or a ticker.
        """
        if not names:
            names = []

        if (not names and not ticker) or (names and ticker):
            raise ValueError('Provide either a valid names array OR a ticker.')
        elif ticker:
            url = self._generate_get_cik_url(CIK=ticker)
        else:
            url = self._generate_get_cik_url(company=names[0])

        # Send request

        wrong_result = False  # Check request
        if wrong_result:
            self.get_cik(names[1:])

        return None

    def get_form_data(self, cik, year):
        """Retrieves information about a company's filings from the SEC.
        Based on: https://github.com/lukerosiak/pysec
        """
        return {
            'fillings': [],
            'xblr': None,
            'q3_gross_margin': None,
            'ticker': None
        }
