import pytest

from sec_retrieval import SEC


@pytest.fixture
def sec():
    return SEC()


class TestSEC:

    def test_get_cik_raises_ValueError_if_invalid_args(self, sec):
        with pytest.raises(ValueError):
            sec.get_cik()

        with pytest.raises(ValueError):
            sec.get_cik(names=[], ticker='')

    def test_get_cik_raises_ValueError_if_invalid_company(self, sec):
        with pytest.raises(ValueError):
            sec.get_cik(ticker='invalid')

        with pytest.raises(ValueError):
            sec.get_cik(names=['advanced', 'invalid name'])

    def test_get_cik(self, sec):
        cik = sec.get_cik(ticker='msft')
        assert cik == '0000789019'

        cik = sec.get_cik(names=['microsoft corp'])
        assert cik == '0000789019'

    def test_get_form_data(self, sec):
        assert sec.get_form_data(cik='', year=2010) == {
            'fillings': [],
            'xblr': None,
            'q3_gross_margin': None,
            'ticker': None
        }
