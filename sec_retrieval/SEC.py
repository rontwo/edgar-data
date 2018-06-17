import datetime
import re
from urllib.parse import urlencode, urlparse, urlunparse
import itertools

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from lxml import html


class SECRequestError(Exception):
    """A request-related error occurred."""


class CIKNotFound(Exception):
    """Could not find a CIK for the given names or ticker."""


class ReportError(Exception):
    """An error occurred when trying to fetch a report."""


class FilingNotFound(Exception):
    """Could not find a filing with the given constraints."""


class Filing10KNotFound(FilingNotFound):
    """Could not find a 10-K filing with the given constraints."""


class SEC:

    def __init__(self):
        self.edgar_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        self.current_date_str = datetime.datetime.now().strftime("%Y-%m-%d")

    def _default_edgar_query(self):
        return {
            'owner': 'exclude',
            'action': 'getcompany',
            'output': 'xml',
            'count': 1
        }

    def _generate_edgar_url(self, **kwargs):
        query = self._default_edgar_query()
        query.update(kwargs)

        url_parts = list(urlparse(self.edgar_url))
        url_parts[4] = urlencode(query)
        url = urlunparse(url_parts)

        return url

    def _request_edgar(self, **kwargs):
        url = self._generate_edgar_url(**kwargs)
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except RequestException:
            raise SECRequestError

        return resp

    def _request_cik(self, **kwargs):
        resp = self._request_edgar(**kwargs)

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
            cik = self._request_cik(CIK=ticker, dateb=self.current_date_str)
        elif names:
            cik = self._request_cik(company=names[0], dateb=self.current_date_str)

        if (not cik) and names:
            # try again with the remaining names
            cik = self.get_cik(names[1:])

        if not cik:
            # could not find a valid name
            raise CIKNotFound('Names list exhausted or bad ticker.')

        return cik

    def get_form_data(self, cik, year):
        """Retrieves information about a company's filings from the SEC.
        Based on: https://github.com/lukerosiak/pysec
        """

        forms_filenames = self._get_forms_filenames(cik, year)
        for form_filename in forms_filenames:
            retriever = FilingRetriever(form_filename)
            data = retriever.retrieve()

        return {
            'filings': [],
            'xbrl': None,
            'q3_gross_margin': None,
            'ticker': None
        }

    def _get_forms_filenames(self, cik, year):
        return itertools.chain(self._get_filename_10k(cik, year),
                               self._get_filenames_10q(cik, year),
                               self._get_filenames_8k(cik, year))

    def _get_filing_urls(self, cik, filing_type, datea, dateb):
        resp = self._request_edgar(CIK=cik, type=filing_type, datea=datea, dateb=dateb)
        soup = BeautifulSoup(resp.content, 'lxml-xml')

        if soup.findAll(text=re.compile("No matching", re.IGNORECASE)):
            # Can be either "No matching Ticker Symbol" or "No matching CIK"
            raise ReportError("No matching CIK.")

        if soup.findAll("div", {"class": "noCompanyMatch"}):
            raise ReportError("Invalid company selection.")

        if not soup.results:
            return

        filing_links = soup.results.find_all('filingHREF')

        for filing_link in filing_links:
            url = filing_link.string
            yield url

    def _get_filename_10k(self, cik, year):
        datea = '{}-01-01'.format(year)
        dateb = '{}-12-31'.format(year+1)

        for filing_url in self._get_filing_urls(cik, '10-K', datea, dateb):
            r = requests.get(filing_url)

            tree = html.fromstring(r.content)

            period_of_report = tree.xpath("//*[contains(text(),'Period of Report')]/following-sibling::div/text()")

            if not period_of_report:
                raise ReportError('Something wrong happened when fetching {} 10-K filing.'.format(cik))

            period_of_report = period_of_report[0]

            if period_of_report[:4] == str(year):
                # Period of report year == given end of fiscal year
                # https://www.investopedia.com/terms/f/fiscalyear.asp
                yield filing_url.replace('-index', '')
                return

        raise Filing10KNotFound('Could not find a 10-K filing for the '
                                'corresponding year ({0}) and CIK ({1}).'.format(year, cik))

    def _get_filenames_10q(self, cik, year):
        datea = '{}-01-01'.format(year)
        dateb = '{}-03-31'.format(year+1)

        for filing_url in self._get_filing_urls(cik, '10-Q', datea, dateb):
            yield filing_url.replace('-index', '')

    def _get_filenames_8k(self, cik, year):
        datea = '{}-01-01'.format(year)
        dateb = '{}-12-31'.format(year+1)

        for filing_url in self._get_filing_urls(cik, '8-K', datea, dateb):
            yield filing_url.replace('-index', '')


class FilingRetriever:

    def __init__(self, filename):
        self.filename = filename
        self.html = ''
        self.xbrl = None

    def retrieve(self):
        # Download html
        # Download xbrl
        pass

    def ticker(self):
        # get a company's stock ticker from an XML filing
        pass
