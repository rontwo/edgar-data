# Running tests

`$ python setup.py test`

# Installing

`$ python setup.py install`

# Usage

```python
from sec_retrieval import SEC

sec = SEC()

cik = sec.get_cik(names=['microsoft'])
# or
cik = sec.get_cik(ticker='msft')

sec.get_form_data(cik, year=2010)
```
