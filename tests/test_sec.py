import pytest

from sec_retrieval import SEC


@pytest.fixture
def sec():
    return SEC()


class TestSEC:

    def test_get_sik(self, sec):
        assert sec.get_cik() == '0000789019'

    def test_get_form_data(self, sec):
        assert sec.get_form_data(year=2010) == {
            'fillings': [],
            'xblr': None,
            'q3_gross_margin': None,
            'ticker': None
        }
