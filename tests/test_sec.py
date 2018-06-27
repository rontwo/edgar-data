from datetime import datetime

import pytest
from requests import HTTPError

from edgar_data.EdgarData import CIKNotFound, EDGARRequestError, ReportError, Filing10KNotFound


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

    def test_get_form_data_invalid_company_raises_ReportError(self, sec):
        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='invalid_cik', calendar_year=1950)

        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='123', calendar_year=1950)

        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='', calendar_year=1950)

    def test_get_form_data_returns_within_range(self, sec):
        # Should return only year = 2016
        docs = sec.get_form_data(cik='0000789019', calendar_year=2016)

        for doc in docs.all_filings():
            assert doc.period_end_date.year == 2016

        min_date = datetime(2016, 1, 1)
        max_date = datetime(2016, 4, 15)

        docs = sec.get_form_data(cik='0000789019', date_start=min_date, date_end=max_date)

        for doc in docs.all_filings():
            assert min_date < doc.period_end_date < max_date

    def test_get_form_data(self, sec, company):
        try:
            cik = sec.get_cik(names=company['company'])
        except CIKNotFound:
            cik = sec.get_cik(ticker=company['ticker'])

        assert cik == company['cik']

        docs = sec.get_form_data(cik=cik, calendar_year=2017)

        for doc in docs.all_filings():
            if doc.period_end_date.year == 2017:
                if doc.form_type in ('10-K', '20-F'):
                    assert round(doc.fields['Revenues'] / 1e9) == company['2017_revenue']
                    assert doc.fields.currency('Revenues')[0] == company['currency']
