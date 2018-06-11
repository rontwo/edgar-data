import pytest

from sec_retrieval import SEC


@pytest.fixture
def sec():
    return SEC()


class TestSEC:

    def test_get_sik_raises_ValueError(self, sec):
        with pytest.raises(ValueError):
            sec.get_cik()

        with pytest.raises(ValueError):
            sec.get_cik(names=[], ticker='')

    def test_get_sik(self, sec):
        pass

    def test_get_form_data(self, sec):
        assert sec.get_form_data(cik='', year=2010) == {
            'fillings': [],
            'xblr': None,
            'q3_gross_margin': None,
            'ticker': None
        }
