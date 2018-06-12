import datetime
from urllib.parse import urlencode, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup


class CIKNotFound(Exception):
    pass


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

    def _request_cik(self, **kwargs):
        url = self._generate_get_cik_url(**kwargs)
        resp = requests.get(url)

        resp.raise_for_status()

        if resp.headers['Content-Type'] != 'application/xml':
            return None

        soup = BeautifulSoup(resp.content, 'lxml-xml')
        if soup.CIK:
            return soup.CIK.string

    def get_cik(self, names=None, ticker=''):
        """Returns the company's CIK.
        Provide either a list of company names, or a ticker.
        """

        cik = None

        if (names is None and not ticker) or (names is not None and ticker):
            raise ValueError('Provide either a valid names array OR a ticker.')
        elif ticker:
            cik = self._request_cik(CIK=ticker)
        elif names:
            cik = self._request_cik(company=names[0])

        if (not cik) and names:
            # try again with the remaining names
            cik = self.get_cik(names[1:])

        if not cik:
            # could not find a valid name
            raise CIKNotFound('Names list exhausted.')

        return cik

    def get_form_data(self, cik, year):
        """Retrieves information about a company's filings from the SEC.
        Based on: https://github.com/lukerosiak/pysec
        """
        return {
            'filings': [],
            'xbrl': None,
            'q3_gross_margin': None,
            'ticker': None
        }
