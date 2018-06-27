import datetime
import re
from urllib.parse import urlencode, urlparse, urlunparse
import itertools

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from lxml import html

from edgar_data.FilingsDataset import FilingsDataset, Filing
from .xbrl import XBRL


class EDGARRequestError(Exception):
    """A request-related error occurred."""


class CIKNotFound(Exception):
    """Could not find a CIK for the given names or ticker."""


class ReportError(Exception):
    """An error occurred when trying to fetch a report."""


class FilingNotFound(Exception):
    """Could not find a filing with the given constraints."""


class Filing10KNotFound(FilingNotFound):
    """Could not find a 10-K filing with the given constraints."""


class EdgarData:

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
        kwargs_without_Nones = {k: v for k, v in kwargs.items() if v is not None}
        url = self._generate_edgar_url(**kwargs_without_Nones)
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except RequestException:
            raise EDGARRequestError

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

        :param names: List of possible company names.
        :param ticker: Company's trading symbol.
        :type names: List[str]
        :type ticker: str
        :return: Company's Central Index Key (CIK)
        :rtype: str
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

    def get_form_data(self, cik, date_start=None, date_end=None, calendar_year=None):
        """Retrieves information about a company's filings from the SEC.
        Based on: https://github.com/lukerosiak/pysec

        :Example:

        >>> from datetime import datetime
        >>> edgar = EdgarData()
        >>> # Retrieves all filings between 2015-01-01 to 2015-03-15:
        >>> filings = edgar.get_form_data('0000002488', datetime(2015, 1, 1), datetime(2015, 3, 15))
        >>> # Retrieves all filings for the calendar year 2015:
        >>> filings_year = edgar.get_form_data('0000002488', calendar_year=2015)

        :param cik: Company's CIK.
        :param date_start: Optional. Date from.
        :param date_end: Optional. Date to.
        :param calendar_year: Optional. If provided, parameters `date_start` and `date_end` will be ignored,
            and the algorithm will try to retrieve filings for the given year (i.e. period end date within given year).
        :type cik: str
        :type date_start: datetime object
        :type date_end: datetime object
        :type calendar_year: int
        :return: All the found filings.
        :rtype: FilingsDataset
        """

        if calendar_year:
            date_start = None
            date_end = None

        all_filings = FilingsDataset()

        for filing in self._get_all_filings_index_pages(cik, date_start, date_end, calendar_year):
            retriever = FilingRetriever(url=filing['url'],
                                        form=filing['form'],
                                        tree=filing['tree'],
                                        cik=cik)
            filing_html, xbrl = retriever.retrieve()

            all_filings.add_filing(
                Filing(filing_html, xbrl, cik, filing['form'], filing['period_of_report']))

        return all_filings

    def _get_all_filings_index_pages(self, cik, datea, dateb, calendar_year):
        if datea:
            datea = datea.strftime("%Y-%m-%d")
        if dateb:
            dateb = dateb.strftime("%Y-%m-%d")

        return itertools.chain(self._get_filing_index_10k(cik, datea, dateb, calendar_year),
                               self._get_filings_index_10q(cik, datea, dateb, calendar_year),
                               self._get_filings_index_8k(cik, datea, dateb, calendar_year))

    def _get_filings_index_urls(self, cik, filing_type, datea, dateb):
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

    def _get_filing_index_page(self, cik, form, datea, dateb):

        for filing_url in self._get_filings_index_urls(cik, form, datea, dateb):
            r = requests.get(filing_url)

            tree = html.fromstring(r.content)

            period_of_report = tree.xpath("//*[contains(text(),'Period of Report')]/following-sibling::div/text()")

            if not period_of_report:
                raise ReportError('Something wrong happened when fetching {0} {1} filing.'.format(cik, form))

            yield {'form': form, 'url': filing_url, 'tree': tree, 'period_of_report': period_of_report[0]}

    def _get_filing_index_10k(self, cik, datea, dateb, calendar_year):
        if calendar_year:
            datea = '{}-01-01'.format(calendar_year)
            dateb = '{}-12-31'.format(calendar_year+1)

        for filing_page in self._get_filing_index_page(cik, '10-K', datea, dateb):
            period_of_report = filing_page['period_of_report']

            if period_of_report[:4] == str(calendar_year):
                # Period of report year == given end of fiscal year
                # https://www.investopedia.com/terms/f/fiscalyear.asp
                yield filing_page
                return

        if calendar_year:
            raise Filing10KNotFound('Could not find a 10-K filing for the '
                                    'corresponding date range ({0} / {1}) and CIK ({2}).'.format(datea, dateb, cik))

    def _get_filings_index_10q(self, cik, datea, dateb, calendar_year):
        if calendar_year:
            datea = '{}-01-01'.format(calendar_year)
            dateb = '{}-03-31'.format(calendar_year+1)

        for filing_page in self._get_filing_index_page(cik, '10-Q', datea, dateb):
            period_of_report = filing_page['period_of_report']

            if period_of_report[:4] == str(calendar_year):
                yield filing_page

    def _get_filings_index_8k(self, cik, datea, dateb, calendar_year):
        if calendar_year:
            datea = '{}-01-01'.format(calendar_year)
            dateb = '{}-12-31'.format(calendar_year)

        for filing_page in self._get_filing_index_page(cik, '8-K', datea, dateb):
            yield filing_page


class FilingRetriever:

    def __init__(self, url, form, tree, cik):
        self.cik = cik
        self.tree = tree
        self.form = form
        self.url = url
        self.html = ''
        self.xbrl = None

    def _retrieve_document(self, url):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except RequestException:
            raise EDGARRequestError

        return resp.text

    def retrieve(self):
        full_filing_doc = self._retrieve_document(self._html_url())
        filing = self._clean_html(full_filing_doc)

        if self.form == '10-K' or self.form == '10-Q':
            xbrl_doc = self._retrieve_document(self._xbrl_url())

            # If using the python-xbrl library (this actually doesn't work, as every info is filled as 0.0):
            #xbrl_parser = XBRLParser(precision=0)
            #xbrl = xbrl_parser.parse(io.StringIO(xbrl_doc))
            #gaap = xbrl_parser.parseGAAP(xbrl, ...)

            xbrl = XBRL(xbrl_doc.encode())

            return filing, xbrl

        return filing, None

    def _document_url(self, table_summary, file_description):
        # link is relative (i.e. /Archives/edgar/data/... )
        link = self.tree.xpath('//*[@id="formDiv"]//table[@summary="{0}"]'
                               '//*[contains(text(),"{1}")]/..//a/@href'.format(table_summary, file_description))

        if not link:
            raise FilingNotFound('Could not find the filing htm file at {}'.format(self.url))

        # Safely insert https://www.sec.gov in the link
        url_parts = list(urlparse(link[0]))
        url_parts[0] = 'https'
        url_parts[1] = 'www.sec.gov'
        url = urlunparse(url_parts)

        return url

    def _html_url(self):
        return self._document_url(table_summary="Document Format Files",
                                  file_description=self.form)

    def _xbrl_url(self):
        return self._document_url(table_summary="Data Files",
                                  file_description="XBRL INSTANCE DOCUMENT")

    def _clean_html(self, content):
        font_tags = re.compile(r'(<(font|FONT).*?>|</(font|FONT)>)')
        style_attrs = re.compile(r'('
                                 r'((style|STYLE)=\".*?\")|'
                                 r'((valign|VALIGN)=\".*?\")|'
                                 r'((align|ALIGN)=\".*?\")|'
                                 r'((width|WIDTH)=\".*?\")|'
                                 r'((height|HEIGHT)=\".*?\")|'
                                 r'((border|BORDER)=\".*?\")|'
                                 r'((cellpadding|CELLPADDING)=\".*?\")|'
                                 r'((cellspacing|CELLSPACING)=\".*?\")|'
                                 r'((size|SIZE)=\".*?\")|'
                                 r'((colspan|COLSPAN)=\".*?\")'
                                 r')')
        no_font = re.sub(font_tags, '', content)
        no_style = re.sub(style_attrs, '', no_font)

        return no_style
