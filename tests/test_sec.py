import pytest
from requests import HTTPError

from sec_retrieval import SEC
from sec_retrieval.SEC import CIKNotFound, SECRequestError, ReportError, Filing10KNotFound


@pytest.fixture
def sec():
    return SEC()


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

        with pytest.raises(SECRequestError):
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
            assert sec.get_form_data(cik='invalid_cik', year=1950)

        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='123', year=1950)

        with pytest.raises(ReportError):
            assert sec.get_form_data(cik='', year=1950)

    def test_get_form_data_invalid_date_raises_Filing10KNotFound(self, sec):
        with pytest.raises(Filing10KNotFound):
            sec.get_form_data(cik='0000789019', year=1950)

    def test_get_form_data(self, sec):
        docs = sec.get_form_data(cik='0000789019', year=2016)

        assert docs['q3_gross_margin'] == pytest.approx(0.6157993436474449)
