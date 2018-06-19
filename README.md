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

sec.get_form_data(cik, year=2010)
```
