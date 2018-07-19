import pytest
from edgar_data import EdgarData


@pytest.fixture
def sec():
    return EdgarData()


@pytest.fixture(params=[
    {
        'company': ['ADVANTAGE OIL'],
        '2017_revenue': 225,
        'revenue_order': 1e6,
        'cik': '0001468079',
        'currency': 'CAD'
    },
    {
        'company': ['Tesla, Inc'],
        '2017_revenue': 12,
        'revenue_order': 1e9,
        'cik': '0001318605',
        'currency': 'USD'
    },
    {
        'company': ['Hudson Ltd'],
        '2017_revenue': 2,
        'revenue_order': 1e9,
        'ticker': 'HUD',
        'cik': '0001714368',
        'currency': 'USD'
    },
    {
        'company': ['INTERNATIONAL BUSINESS MACHINES'],
        '2017_revenue': 79,
        'revenue_order': 1e9,
        'ticker': 'IBM',
        'cik': '0000051143',
        'currency': 'USD'
    },
    {
        'company': ['Royal Dutch Shell'],
        '2017_revenue': 305,
        'revenue_order': 1e9,
        'ticker': 'RDSA',
        'cik': '0001306965',
        'currency': 'USD'
    },
    {
        'company': ['SINOPEC SHANGHAI'],
        '2017_revenue': 92,
        'revenue_order': 1e9,
        'ticker': 'SHI',
        'cik': '0000908732',
        'currency': 'CNY'
    },
    {
        'company': ['Toyota'],
        '2017_revenue': 27597,
        'revenue_order': 1e9,
        'ticker': 'TM',
        'cik': '0001094517',
        'currency': 'JPY'
    },
    {
        'company': ['Walmart Inc'],
        '2017_revenue': 486,
        'revenue_order': 1e9,
        'cik': '0000104169',
        'currency': 'USD'
    },
    {
        'company': ['BERKSHIRE HATHAWAY INC'],
        '2017_revenue': 242,
        'revenue_order': 1e9,
        'ticker': 'BRKA',
        'cik': '0001067983',
        'currency': 'USD'
    },
    {
        'company': ['Apple inc'],
        '2017_revenue': 229,
        'revenue_order': 1e9,
        'cik': '0000320193',
        'currency': 'USD'
    },
    {
        'company': ['Exxon Mobil'],
        '2017_revenue': 237,
        'revenue_order': 1e9,
        'cik': '0000034088',
        'currency': 'USD'
    },
    {
        'company': ['BOEING CO'],
        '2017_revenue': 93,
        'revenue_order': 1e9,
        'cik': '0000012927',
        'currency': 'USD'
    },
    {
        'company': ['BOSTON SCIENTIFIC'],
        '2017_revenue': 9,
        'revenue_order': 1e9,
        'cik': '0000885725',
        'currency': 'USD'
    }
])
def company(request):
    return request.param
