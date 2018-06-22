import itertools
from datetime import datetime


class UnknownFilingType(Exception):
    """A filing of unknown type has been found."""


class Filing:

    def __init__(self, html, xbrl, cik, form_type, period_of_report):
        """Filing class. Access XBRL data through the `xbrl` attribute.
        See pysec XBRL class for more details on how to get DEI or GAAP data.

        :Example:

        >>> filing = Filing(...)
        >>> filing.fields['TradingSymbol']  # returns the ticker
        """
        self.html = html
        self.xbrl = xbrl
        if xbrl:
            self.fields = xbrl.fields
        else:
            self.fields = None
        self.cik = cik
        self.form_type = form_type
        self.period_end_date = datetime.strptime(period_of_report, "%Y-%m-%d")  # type: datetime

    def __repr__(self):
        return "{0} - {1} ({2})".format(self.cik, self.form_type, self.period_end_date)


class Filings:

    def __init__(self):
        """ Class for holding several Filing objects.
        """
        self._form_10k = None
        self._forms_10q = []
        self._forms_8k = []

    def all_filings(self):
        """
        :return: All found filings.
        :rtype: List[Filing]
        """
        return (filing
                for filing
                in itertools.chain([self._form_10k], self._forms_10q, self._forms_8k)
                if filing)

    def add_filing(self, filing):
        """ Gets a filing dict containing the full filing html and a XBRL object, turns
        that into a Filing object, and inserts it.

        :type filing: Filing obj
        """
        if filing.form_type == '10-K':
            self._form_10k = filing
        elif filing.form_type == '10-Q':
            self._forms_10q.append(filing)
        elif filing.form_type == '8-K':
            self._forms_8k.append(filing)
        else:
            raise UnknownFilingType(
                "Filing of unknown type ({0}) for CIK {1}".format(filing.form_type, filing.cik))
