import pytest
from edgar_data import EdgarData


@pytest.fixture
def sec():
    return EdgarData()


@pytest.fixture(params=[
    {
        'company': ['Walmart Inc'],
        '2017_revenue': 486,
        'cik': '0000104169'
    },
    {
        'company': ['BERKSHIRE HATHAWAY INC'],
        '2017_revenue': 242,
        'ticker': 'BRKA',
        'cik': '0001067983'
    },
    {
        'company': ['Apple inc'],
        '2017_revenue': 216,
        'cik': '0000320193'
    },
    {
        'company': ['Exxon Mobil'],
        '2017_revenue': 205,
        'cik': '0000034088'
    }
])
def company(request):
    return request.param