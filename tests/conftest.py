import pytest
from edgar_data import EdgarData


@pytest.fixture
def sec():
    return EdgarData()


@pytest.fixture(params=[
    {
        'company': ['DEUTSCHE BANK AKTIENGESELLSCHAFT'],
        'revenue': 480,
        'revenue_order': 1e6,
        'year': 2015,
        'ticker': '0001159508',
        'cik': '0001159508',
        'currency': 'USD'
    },
    {
        'company': ['EXICURE, INC.'],
        'revenue': 10,
        'revenue_order': 1e6,
        'year': 2017,
        'ticker': '0001698530',
        'cik': '0001698530',
        'currency': 'USD'
    },
    {
        'company': ['Evans Brewing'],
        'revenue': 2,
        'revenue_order': 1e6,
        'year': 2017,
        'cik': '0001580490',
        'currency': 'USD'
    },
    {
        'company': ['Intelsat'],
        'revenue': 2,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'I',
        'cik': '0001525773',
        'currency': 'USD'
    },
    {
        'company': ['ADVANTAGE OIL'],
        'revenue': 225,
        'revenue_order': 1e6,
        'year': 2017,
        'cik': '0001468079',
        'currency': 'CAD'
    },
    {
        'company': ['Tesla, Inc'],
        'revenue': 12,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0001318605',
        'currency': 'USD'
    },
    {
        'company': ['Hudson Ltd'],
        'revenue': 2,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'HUD',
        'cik': '0001714368',
        'currency': 'USD'
    },
    {
        'company': ['INTERNATIONAL BUSINESS MACHINES'],
        'revenue': 79,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'IBM',
        'cik': '0000051143',
        'currency': 'USD'
    },
    {
        'company': ['Royal Dutch Shell'],
        'revenue': 305,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'RDSA',
        'cik': '0001306965',
        'currency': 'USD'
    },
    {
        'company': ['SINOPEC SHANGHAI'],
        'revenue': 92,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'SHI',
        'cik': '0000908732',
        'currency': 'CNY'
    },
    {
        'company': ['Toyota'],
        'revenue': 27597,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'TM',
        'cik': '0001094517',
        'currency': 'JPY'
    },
    {
        'company': ['Walmart Inc'],
        'revenue': 486,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0000104169',
        'currency': 'USD'
    },
    {
        'company': ['BERKSHIRE HATHAWAY INC'],
        'revenue': 242,
        'revenue_order': 1e9,
        'year': 2017,
        'ticker': 'BRKA',
        'cik': '0001067983',
        'currency': 'USD'
    },
    {
        'company': ['Apple inc'],
        'revenue': 229,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0000320193',
        'currency': 'USD'
    },
    {
        'company': ['Exxon Mobil'],
        'revenue': 237,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0000034088',
        'currency': 'USD'
    },
    {
        'company': ['BOEING CO'],
        'revenue': 93,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0000012927',
        'currency': 'USD'
    },
    {
        'company': ['BOSTON SCIENTIFIC'],
        'revenue': 9,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0000885725',
        'currency': 'USD'
    },
    {
        'company': ['Medtronic plc'],
        'revenue': 30,
        'revenue_order': 1e9,
        'year': 2017,
        'cik': '0001613103',
        'currency': 'USD'
    }
])
def company(request):
    return request.param
