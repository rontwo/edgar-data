
class SEC:

    def __init__(self):
        pass

    def get_cik(self, names=None, ticker=None):
        """Returns the company's CIK.
        Provide either a list of company names, or a ticker.
        """
        return '0000789019'

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
