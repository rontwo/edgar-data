# Installing

`$ python setup.py install`

# Running tests

`$ python setup.py test`

# Usage

```python
from edgar_data import EdgarData

sec = EdgarData()

cik = sec.get_cik(names=['microsoft'])
# or
cik = sec.get_cik(ticker='msft')

docs = sec.get_form_data(cik, year=2010)

# Accessing XBRL for 10-K and 20-F forms:
for doc in docs.all_filings():
    if doc.form_type in ('10-K', '20-F'):
        if not doc.xbrl:
            continue
        revenue = doc.fields['Revenues']
        currency = doc.fields.currency('Revenues')[0]
        year = doc.period_end_date.year
```
