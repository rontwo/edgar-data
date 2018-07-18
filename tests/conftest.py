import pytest
from edgar_data import EdgarData


@pytest.fixture
def sec():
    return EdgarData()


@pytest.fixture(params=[
    {
        'company': ['Tesla, Inc'],
        '2017_revenue': 12,
        'cik': '0001318605',
        'currency': 'USD'
    },
    {
        'company': ['Hudson Ltd'],
        '2017_revenue': 2,
        'ticker': 'HUD',
        'cik': '0001714368',
        'currency': 'USD'
    },
    {
        'company': ['INTERNATIONAL BUSINESS MACHINES'],
        '2017_revenue': 79,
        'ticker': 'IBM',
        'cik': '0000051143',
        'currency': 'USD'
    },
    {
        'company': ['Royal Dutch Shell'],
        '2017_revenue': 305,
        'ticker': 'RDSA',
        'cik': '0001306965',
        'currency': 'USD'
    },
    {
        'company': ['SINOPEC SHANGHAI'],
        '2017_revenue': 92,
        'ticker': 'SHI',
        'cik': '0000908732',
        'currency': 'CNY'
    },
    {
        'company': ['Toyota'],
        '2017_revenue': 27597,
        'ticker': 'TM',
        'cik': '0001094517',
        'currency': 'JPY'
    },
    {
        'company': ['Walmart Inc'],
        '2017_revenue': 486,
        'cik': '0000104169',
        'currency': 'USD'
    },
    {
        'company': ['BERKSHIRE HATHAWAY INC'],
        '2017_revenue': 242,
        'ticker': 'BRKA',
        'cik': '0001067983',
        'currency': 'USD'
    },
    {
        'company': ['Apple inc'],
        '2017_revenue': 229,
        'cik': '0000320193',
        'currency': 'USD'
    },
    {
        'company': ['Exxon Mobil'],
        '2017_revenue': 237,
        'cik': '0000034088',
        'currency': 'USD'
    },
    {
        'company': ['BOEING CO'],
        '2017_revenue': 93,
        'cik': '0000012927',
        'currency': 'USD'
    },
    {
        'company': ['BOSTON SCIENTIFIC'],
        '2017_revenue': 9,
        'cik': '0000885725',
        'currency': 'USD'
    }
])
def company(request):
    return request.param
