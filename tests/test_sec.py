from datetime import datetime

import pytest
from requests import HTTPError

from edgar_data.EdgarData import CIKNotFound, EDGARRequestError, ReportError, Filing10KNotFound


@pytest.fixture
def full_2017_date():
    return datetime(2016, 1, 1), datetime(2017, 12, 31)


class TestSEC:

    def test_get_cik_raises_ValueError_if_invalid_args(self, sec):
        with pytest.raises(ValueError):
            sec.get_cik()

        with pytest.raises(ValueError):
            sec.get_cik(names=['a'], ticker='a')

    def test_get_cik_raises_ValueError_if_invalid_company(self, sec):
        with pytest.raises(CIKNotFound):
            sec.get_cik(ticker='invalid')

        with pytest.raises(CIKNotFound):
            sec.get_cik(names=['advanced', 'invalid name'])

    def test_get_cik_raises_RequestError_if_response_error(self, mocker, sec):
        mock_get = mocker.patch('requests.get')

        mock_resp = mocker.Mock()
        mock_get.return_value = mock_resp

        mock_resp.raise_for_status.side_effect = HTTPError("SEC is down")
        mock_resp.status_code = 500

        with pytest.raises(EDGARRequestError):
            sec.get_cik(ticker='msft')

    def test_get_cik(self, sec):
        cik = sec.get_cik(ticker='msft')
        assert cik == '0000789019'

        cik = sec.get_cik(names=['microsoft corp'])
        assert cik == '0000789019'

        cik = sec.get_cik(names=['Microsoft', 'Microsoft Corp'])
        assert cik == '0000789019'

        cik = sec.get_cik(names=['advanced', 'AMD', 'Advanced Micro Devices'])
        assert cik == '0000002488'

    def test_get_form_data_invalid_company_raises_ReportError(self, sec, full_2017_date):
        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='invalid_cik', date_start=datetime(1950, 1, 1))

        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='123', date_start=datetime(1950, 1, 1))

        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='', date_start=datetime(1950, 1, 1))

    def test_get_form_data_returns_within_range(self, sec):
        min_date = datetime(2016, 1, 1)
        max_date = datetime(2016, 4, 15)

        docs = sec.get_form_data(cik='0000789019', date_start=min_date, date_end=max_date)

        assert docs
        for doc in docs:
            assert min_date < doc.filing_date < max_date

    def test_invalid_field_currency(self, sec, full_2017_date):
        docs = sec.get_form_data(cik='0000789019', date_start=full_2017_date[0], date_end=full_2017_date[1])

        assert docs
        for doc in docs:
            if doc.fields:
                assert doc.fields.currency('InvalidField') is None

    def test_get_form_data_specific_forms(self, sec, full_2017_date):
        docs = sec.get_form_data(cik='0000789019', date_start=full_2017_date[0], date_end=full_2017_date[1],
                                 form_types=['10-Q'])

        assert docs
        for doc in docs:
            assert doc.form_type == '10-Q'

    def test_get_form_data_html_or_xbrl(self, sec, full_2017_date):
        docs_xbrl_only = sec.get_form_data(cik='0000789019', date_start=full_2017_date[0], date_end=full_2017_date[1],
                                           form_types=['10-K'], fetch_html=False)

        assert docs_xbrl_only
        for doc in docs_xbrl_only:
            assert doc.xbrl is not None
            assert doc.html is None

        docs_html_only = sec.get_form_data(cik='0000789019', date_start=full_2017_date[0], date_end=full_2017_date[1],
                                           form_types=['10-K'], fetch_xbrl=False)

        assert docs_html_only
        for doc in docs_html_only:
            assert doc.html is not None
            assert doc.xbrl is None

    def test_get_form_data_6k(self, sec, full_2017_date):
        docs = sec.get_form_data(cik='0000908732', date_start=full_2017_date[0], date_end=full_2017_date[1],
                                 form_types=['6-K'])

        assert docs
        for doc in docs:
            assert doc.form_type == '6-K'

    def test_get_form_data_s1(self, sec, full_2017_date):
        docs = sec.get_form_data(cik='0001564408', date_start=full_2017_date[0], date_end=full_2017_date[1],
                                 form_types=['S-1'])

        assert docs
        for doc in docs:
            assert doc.form_type == 'S-1'

    def test_supplemental_links(self, sec):
        url = 'https://www.sec.gov/Archives/edgar/data/1318605/000156459018002956/tsla-10k_20171231.htm'
        links = sec.get_supplemental_links_from_html_url(url)
        assert len(links) == 13

    def test_qtd_vs_ytd(self, sec, full_2017_date):
        docs = sec.get_form_data(cik='0000789019', date_start=full_2017_date[0], date_end=full_2017_date[1],
                                 form_types=['10-K', '10-Q'])

        assert docs
        for doc in docs:
            #print()
            # print('Fiscal Period:', doc.fiscal_period_focus)
            # print('End Date:', doc.period_end_date)
            # print('Start date (YTD):', doc.fields['IncomeStatementPeriodYTD'])
            # print('YTD:', doc.fields['Revenues'])
            rev_ytd = doc.fields['Revenues']
            doc.set_period(this_quarter=True)
            rev_qtd = doc.fields['Revenues']
            # print('Start date (QTD):', doc.fields['IncomeStatementPeriodYTD'])
            # print('QTD:', doc.fields['Revenues'])
            # print()

            assert rev_qtd.value <= rev_ytd.value

    def test_get_form_data(self, sec, company):
        try:
            cik = sec.get_cik(names=company['company'])
        except CIKNotFound:
            cik = sec.get_cik(ticker=company['ticker'])

        assert cik == company['cik']

        docs = sec.get_form_data(cik=cik, date_start=datetime(2017, 1, 1), date_end=datetime(2018, 12, 31))

        assert docs
        for doc in docs:
            if doc.period_end_date.year == 2017:
                if doc.xbrl and doc.form_type in ('10-K', '20-F', '40-F'):
                    print('==========')
                    print(company['company'], doc.ticker, doc.filing_date)
                    print(doc.index_url)
                    print(doc.text_url)
                    print('Revenues:', doc.fields['Revenues'], doc.fields.currency('Revenues'))
                    print('Revenues segments:', doc.fields['Revenues'].segment_values)
                    print('Assets:', doc.fields['Assets'], doc.fields.currency('Assets'))
                    print('Cost of Revenues:', doc.fields['CostOfRevenue'], doc.fields.currency('CostOfRevenue'))
                    print('GrossProfit:', doc.fields['GrossProfit'], doc.fields.currency('GrossProfit'))
                    print('OperatingIncomeLoss (EBIT):', doc.fields['OperatingIncomeLoss'], doc.fields.currency('OperatingIncomeLoss'))
                    print('IncomeFromContinuingOperationsBeforeTax (EBIT?):', doc.fields['IncomeFromContinuingOperationsBeforeTax'], doc.fields.currency('IncomeFromContinuingOperationsBeforeTax'))
                    print('ProfitLoss (Net Income):', doc.fields['NetIncomeLoss'], doc.fields.currency('NetIncomeLoss'))
                    #print('NetIncomeLoss segments:', doc.fields['NetIncomeLoss'].segment_values)
                    print('Net Income attributable:', doc.fields['NetIncomeAttributableToParent'], doc.fields.currency('NetIncomeAttributableToParent'))
                    if doc.fields['NetIncomeAttributableToParent'] is not None:
                        print('NetIncomeAttributableToParent segments:', doc.fields['NetIncomeAttributableToParent'].segment_values)
                    print(doc.fields['ContextForDurations'])
                    print('==========')

                    assert round(doc.fields['Revenues'].value / company['revenue_order']) == company['2017_revenue']
                    assert doc.fields['Revenues'].currency.code == company['currency']

