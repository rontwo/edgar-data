import datetime
import re
from urllib.parse import urlencode, urlparse, urlunparse
import itertools

import requests
from bs4 import BeautifulSoup
from requests import RequestException
from lxml import html

from .xbrl import XBRL


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

        all_filings = {
            'filings': [],
            'xbrl': None,
            'q3_gross_margin': None,
            'ticker': None
        }

        for filing in self._get_all_filings(cik, year):
            retriever = FilingRetriever(url=filing['url'],
                                        form=filing['form'],
                                        tree=filing['tree'],
                                        cik=cik)

            filing_html, xbrl, gross_margin, ticker = retriever.retrieve()

            all_filings['filings'].append(filing_html)
            if filing['form'] == '10-K':
                all_filings['xbrl'] = xbrl
                all_filings['q3_gross_margin'] = gross_margin
                all_filings['ticker'] = ticker

        return all_filings

    def _get_all_filings(self, cik, year):
        return itertools.chain(self._get_filing_10k(cik, year),
                               self._get_filings_10q(cik, year),
                               self._get_filings_8k(cik, year))

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

    def _get_filing_page(self, cik, form, datea, dateb):

        for filing_url in self._get_filing_urls(cik, form, datea, dateb):
            r = requests.get(filing_url)

            tree = html.fromstring(r.content)

            period_of_report = tree.xpath("//*[contains(text(),'Period of Report')]/following-sibling::div/text()")

            if not period_of_report:
                raise ReportError('Something wrong happened when fetching {0} {1} filing.'.format(cik, form))

            yield {'form': form, 'url': filing_url, 'tree': tree, 'period_of_report': period_of_report[0]}

    def _get_filing_10k(self, cik, year):
        datea = '{}-01-01'.format(year)
        dateb = '{}-12-31'.format(year+1)

        for filing_page in self._get_filing_page(cik, '10-K', datea, dateb):
            period_of_report = filing_page['period_of_report']

            if period_of_report[:4] == str(year):
                # Period of report year == given end of fiscal year
                # https://www.investopedia.com/terms/f/fiscalyear.asp
                yield filing_page
                return

        raise Filing10KNotFound('Could not find a 10-K filing for the '
                                'corresponding year ({0}) and CIK ({1}).'.format(year, cik))

    def _get_filings_10q(self, cik, year):
        datea = '{}-01-01'.format(year)
        dateb = '{}-03-31'.format(year+1)

        for filing_page in self._get_filing_page(cik, '10-Q', datea, dateb):
            yield filing_page

    def _get_filings_8k(self, cik, year):
        datea = '{}-01-01'.format(year)
        dateb = '{}-12-31'.format(year)

        for filing_page in self._get_filing_page(cik, '8-K', datea, dateb):
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
            raise SECRequestError

        return resp.text

    def retrieve(self):
        full_filing_doc = self._retrieve_document(self._html_url())
        filing = self._clean_html(full_filing_doc)

        if self.form.startswith('10-K'):
            xbrl_doc = self._retrieve_document(self._xbrl_url())

            # If using the python-xbrl library:
            #xbrl_parser = XBRLParser(precision=0)
            #xbrl = xbrl_parser.parse(io.StringIO(xbrl_doc))
            #gaap = xbrl_parser.parseGAAP(xbrl, ...)

            xbrl = XBRL(xbrl_doc.encode())

            gross_margin = xbrl.fields['GrossProfit'] / xbrl.fields['Revenues']

            ticker = xbrl.fields['TradingSymbol']

            return filing, xbrl, gross_margin, ticker

        return filing, None, None, None

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
