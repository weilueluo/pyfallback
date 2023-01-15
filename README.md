# pyfallback

Provide a simple Fallback class that wraps an object, any operations that fails will use/return specified fallback.

## Install

```bash
pip install pyfallback
```

## Usage

```python
from pyfallback import Fallback

json = Fallback({'exists': 'exists-value'}, fallback="fallback-value")

# fallback
json["exists"].get()  # "exists-value"
json["not-exists"].get()  # "fallback"

# chaining
json["exists"].split('-')[0].get()  # "exists"
json["not-exists"].split('-')[0].get()  # "fallback"

# see tests/test_fallback.py for more example 
```

## Contributing

Just submit a pull request :D <br />
Note: this project uses [poetry](https://github.com/python-poetry/poetry) and [pyenv](https://github.com/pyenv/pyenv).
