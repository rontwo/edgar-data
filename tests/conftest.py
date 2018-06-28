import pytest
from edgar_data import EdgarData


@pytest.fixture
def sec():
    return EdgarData()


@pytest.fixture(params=[
    {
        'company': ['Royal Dutch Shell'],
        '2017_revenue': 305,
        'ticker': 'RDSA',
        'cik': '0001306965',
        'currency': 'usd'
    },
    # {
    #     'company': ['SINOPEC SHANGHAI'],
    #     '2017_revenue': 92,
    #     'ticker': 'SHI',
    #     'cik': '0000908732',
    #     'currency': 'cny'
    # },
    # {
    #     'company': ['Toyota'],
    #     '2017_revenue': 27597,
    #     'ticker': 'TM',
    #     'cik': '0001094517',
    #     'currency': 'jpy'
    # },
    # {
    #     'company': ['Walmart Inc'],
    #     '2017_revenue': 486,
    #     'cik': '0000104169',
    #     'currency': 'usd'
    # },
    # {
    #     'company': ['BERKSHIRE HATHAWAY INC'],
    #     '2017_revenue': 242,
    #     'ticker': 'BRKA',
    #     'cik': '0001067983',
    #     'currency': 'usd'
    # },
    # {
    #     'company': ['Apple inc'],
    #     '2017_revenue': 229,
    #     'cik': '0000320193',
    #     'currency': 'usd'
    # },
    # {
    #     'company': ['Exxon Mobil'],
    #     '2017_revenue': 237,
    #     'cik': '0000034088',
    #     'currency': 'usd'
    # }
])
def company(request):
    return request.param