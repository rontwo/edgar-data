from datetime import datetime
import re
from urllib.parse import urlencode, urlparse, urlunparse
import itertools

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from lxml import html

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
        self.current_date_str = datetime.now().strftime("%Y-%m-%d")

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

        return '0'*(10-len(cik))+cik

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
        :type date_start: datetime
        :type date_end: datetime
        :type calendar_year: int
        :return: All the found filings.
        :rtype: list(EdgarForm)
        """
        cik = '0'*(10-len(cik))+cik

        if calendar_year:
            date_start = None
            date_end = None

        all_filings = []

        for filing in self._get_all_filings_index_pages(cik, date_start, date_end, calendar_year):
            text_url, filing_html, xbrl = self.retrieve(
                index_url=filing['index_url'], form=filing['form'], tree=filing['tree'])

            all_filings.append(
                EdgarForm(filing_html, xbrl, cik, text_url, filing))

        return all_filings

    def _get_all_filings_index_pages(self, cik, datea, dateb, calendar_year=None):
        if datea:
            datea = datea.strftime("%Y-%m-%d")
        if dateb:
            dateb = dateb.strftime("%Y-%m-%d")

        return itertools.chain(self._get_filing_index_annual(cik, datea, dateb, calendar_year),
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
            form_type = filing_link.parent.type.string
            yield url, form_type

    def _get_filing_index_page(self, cik, form, datea, dateb):

        for filing_url, filing_type in self._get_filings_index_urls(cik, form, datea, dateb):
            if filing_type != form:
                continue

            r = requests.get(filing_url)

            tree = html.fromstring(r.content)

            period_of_report = tree.xpath("//*[contains(text(),'Period of Report')]/following-sibling::div/text()")
            filing_date = tree.xpath("//*[contains(text(),'Filing Date')]/following-sibling::div[1]/text()")

            if not period_of_report or not filing_date:
                raise ReportError('Something wrong happened when fetching {0} {1} filing.'.format(cik, form))

            yield {'form': form, 'index_url': filing_url, 'tree': tree,
                   'period_of_report': period_of_report[0], 'filing_date': filing_date[0]}

    def _get_filing_index_annual(self, cik, datea, dateb, calendar_year=None):
        # NOTE: if calendar_year is passed, we will only return filings within that calendar year
        if calendar_year:
            datea = '{}-01-01'.format(calendar_year)
            dateb = '{}-12-31'.format(calendar_year+1)

        for filing_page in self._get_filing_index_page(cik, '10-K', datea, dateb):
            period_of_report = filing_page['period_of_report']

            # Only proceed if:
            # (1) calendar_year was not provided (i.e. don't run a check)
            # (2) calendar_year check passes (i.e. period of report is within calendar year)
            if not calendar_year or period_of_report[:4] == str(calendar_year):
                # Period of report year == given end of fiscal year
                # https://www.investopedia.com/terms/f/fiscalyear.asp
                yield filing_page

        for filing_page in self._get_filing_index_page(cik, '20-F', datea, dateb):
            yield filing_page

    def _get_filings_index_10q(self, cik, datea, dateb, calendar_year=None):
        # NOTE: if calendar_year is passed, we will only return filings within that calendar year
        if calendar_year:
            datea = '{}-01-01'.format(calendar_year)
            dateb = '{}-03-31'.format(calendar_year+1)

        for filing_page in self._get_filing_index_page(cik, '10-Q', datea, dateb):
            period_of_report = filing_page['period_of_report']

            # Only proceed if:
            # (1) calendar_year was not provided (i.e. don't run a check)
            # (2) calendar_year check passes (i.e. period of report is within calendar year)
            if not calendar_year or period_of_report[:4] == str(calendar_year):
                yield filing_page

    def _get_filings_index_8k(self, cik, datea, dateb, calendar_year=None):
        if calendar_year:
            datea = '{}-01-01'.format(calendar_year)
            dateb = '{}-12-31'.format(calendar_year)

        for filing_page in self._get_filing_index_page(cik, '8-K', datea, dateb):
            yield filing_page

    # def __init__(self, url, form, tree, cik):
    #     self.cik = cik
    #     self.tree = tree
    #     self.form = form
    #     self.url = url
    #     self.html = ''
    #     self.xbrl = None

    def _retrieve_document(self, url):
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except RequestException:
            raise EDGARRequestError

        return resp.text

    def retrieve(self, index_url, form, tree):
        text_url = self._html_url(form, tree, index_url)
        full_filing_doc = self._retrieve_document(text_url)
        filing = self._clean_html(full_filing_doc)
        xbrl = None

        if form in ('10-K', '10-Q', '20-F'):
            try:
                xbrl_doc = self._retrieve_document(self._xbrl_url(tree, index_url))

                # If using the python-xbrl library (this actually doesn't work, as every info is filled as 0.0):
                #xbrl_parser = XBRLParser(precision=0)
                #xbrl = xbrl_parser.parse(io.StringIO(xbrl_doc))
                #gaap = xbrl_parser.parseGAAP(xbrl, ...)

                xbrl = XBRL(xbrl_doc.encode())
            except FilingNotFound:
                xbrl = None

        return text_url, filing, xbrl

    def _document_url(self, table_summary, file_description, tree, index_url):
        # link is relative (i.e. /Archives/edgar/data/... )
        link = tree.xpath('//*[@id="formDiv"]//table[@summary="{0}"]'
                               '//*[contains(text(),"{1}")]/..//a/@href'.format(table_summary, file_description))
        if not link:
            raise FilingNotFound('Could not find the file (type: {0}) at {1}'.format(file_description, index_url))

        # Safely insert https://www.sec.gov in the link
        url_parts = list(urlparse(link[0]))
        url_parts[0] = 'https'
        url_parts[1] = 'www.sec.gov'
        url = urlunparse(url_parts)

        return url

    def _html_url(self, form, tree, index_url):
        return self._document_url(table_summary="Document Format Files",
                                  file_description=form,
                                  tree=tree,
                                  index_url=index_url)

    def _xbrl_url(self, tree, index_url):
        return self._document_url(table_summary="Data Files",
                                  file_description="EX-101.INS",
                                  tree=tree,
                                  index_url=index_url)

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


class UnknownFilingType(Exception):
    """A filing of unknown type has been found."""


class EdgarForm:

    def __init__(self, html, xbrl, cik, text_url, filing):
        """Filing class. Access XBRL data through the `xbrl` attribute.
        See pysec XBRL class for more details on how to get DEI or GAAP data.

        :Example:

        >>> filing = EdgarForm(...)
        >>> filing.fields['TradingSymbol']  # returns the ticker
        """
        self.html = html
        self.xbrl = xbrl
        if xbrl:
            self.fields = xbrl.fields
            self.ticker = self.fields['TradingSymbol']
        else:
            self.fields = None
            self.ticker = None

        self.cik = cik
        self.form_type = filing['form']
        self.period_end_date = datetime.strptime(filing['period_of_report'],
                                                 "%Y-%m-%d")  # type: datetime.datetime
        self.filing_date = datetime.strptime(filing['filing_date'],
                                             "%Y-%m-%d")  # type: datetime.datetime
        self.index_url = filing['index_url']
        self.text_url = text_url

    def __repr__(self):
        return "{0} - {1} ({2})".format(self.cik, self.form_type, self.period_end_date)
